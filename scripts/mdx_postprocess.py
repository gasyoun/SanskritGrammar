"""Make Pandoc-produced .mdx MDX-v3-safe so a Docusaurus book site builds.

Run after docx_to_mdx.py. Pandoc's `markdown` output is NOT valid MDX; MDX v3
parses `{` as JS expressions, `<` as JSX, and this repo's grammar content has
~750 `[x]{.underline}` spans, image/heading attribute blocks, stray raw block-HTML
tables, degenerate single-border rst-tables, and escaped-bracket edge cases that
each break `npm run build`. Passes (in order), all OUTSIDE ``` fenced blocks:

  1. frontmatter   — prepend YAML title/sidebar_label (else gray-matter misreads
                     a leading setext heading as a frontmatter delimiter).
  2. spans         — [x]{.underline|mark|smallcaps} -> <u>/<mark>/<span>.
  3. attr-blocks   — remove {#id .class}, {width=".." height=".."}, {dir=".."}.
  4. braces        — escape remaining literal { } as \\{ \\} (real content, e.g.
                     "{guṇa или vṛddhi}").
  5. block-html    — strip Pandoc's raw <p>/<blockquote>/<td>/<colgroup>/... tags.
  6. degen-tables  — drop ```rst-table``` blocks with < 2 border lines (the
                     remarkRstTable plugin throws on them).
  7. unescape-tags — strip a stray leading backslash before <u>/<mark>/<span>
                     (from "\\[[x]{.underline}" -> "\\<u>..</u>" -> orphan </u>).

Idempotent enough for re-runs: spans won't re-match once converted, frontmatter is
skipped if already present, and brace-escaping guards on a preceding backslash.

Every file also gets an explicit `slug:` in frontmatter, ASCII-slugified from the
title. Without this, Docusaurus derives the route from the raw filename — and a
filename with spaces/parens/periods (e.g. "A. Zalizniak Morphophonological
Classification (English).mdx") produces a URL that Docusaurus's static-site
generator fails to route at build time: the page silently renders as the site's
404 content at the correct path, with a [SUCCESS] build and no error message.
Found the hard way on ZalizniakMorphology_1975 (06-07-2026) — 0 <table> tags
rendered though the build reported success. A clean ASCII slug sidesteps the
bug entirely.
"""
import re, sys, glob, os, unicodedata
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

BS = chr(92)

# Per-book frontmatter (title, sidebar_label) keyed by path suffix. Anything not
# listed here falls back to the first ATX H1, then the humanized filename stem —
# see title_for().
TITLES = {
    "ApteSyntax_1885/Apte-unicode.mdx": ("Apte — Sanskrit Syntax (1885)", "Apte 1885"),
    "BuhlerLeitfaden_1923/Buhler_Unicode.mdx": ("Bühler — Leitfaden (1923)", "Bühler 1923"),
    "KnauerFrazy_1908/Frazy-Knauer-03.05.2023.mdx": ("Knauer — Phrases (1908)", "Knauer 1908"),
    "KocherginaUchebnik_1998/Kochergina_unicode.mdx": ("Kochergina — Uchebnik (1998)", "Kochergina 1998"),
    "ZalizniakKonspekt_2004/zaliznyak-konspekt-2015-11-X_bd_t.mdx": ("Zaliznyak — Konspekt (2004)", "Zaliznyak Konspekt"),
    "ZalizniakOcherk_1978/Zaliznyak-Ocherk_29-11-20-aligned.mdx": ("Zaliznyak — Ocherk (1978)", "Zaliznyak Ocherk"),
}


def slugify(text):
    ascii_text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"[^a-zA-Z0-9]+", "-", ascii_text).strip("-").lower()
    return s or "page"


def title_for(path, text):
    key = path.replace(os.sep, "/")
    for suffix, (title, label) in TITLES.items():
        if key.endswith(suffix):
            return title, label
    m = re.search(r"^#\s+(.+)$", text, re.M)
    if m:
        title = m.group(1).strip()
        return title, title
    stem = os.path.splitext(os.path.basename(path))[0]
    title = re.sub(r"[_\-]+", " ", stem).strip()
    return title, title

BORDER = re.compile(r"^\+[-=+]+\+\s*$")
SPAN = re.compile(r"\[([^\]]*)\]\{\.(underline|mark|smallcaps)\}")
ATTR = re.compile(r'\{(?:[#.][^}]*|[^}]*\b(?:width|height|dir|style)="[^}]*)\}')
BLOCK = re.compile(
    r"</?(?:p|blockquote|div|table|thead|tbody|tfoot|tr|td|th|col|colgroup|caption)\b[^>]*/?>",
    re.I,
)
INTENDED = ["<u>", "</u>", "<mark>", "</mark>", "<span", "</span>"]


def repl_span(m):
    txt, cls = m.group(1), m.group(2)
    return {"underline": f"<u>{txt}</u>", "mark": f"<mark>{txt}</mark>"}.get(
        cls, f'<span className="smallcaps">{txt}</span>'
    )


def esc_braces(s):
    s = re.sub(r"(?<!" + re.escape(BS) + r")\{", BS + "{", s)
    s = re.sub(r"(?<!" + re.escape(BS) + r")\}", BS + "}", s)
    return s


def split_fences(text):
    lines, out, buf, in_f = text.split("\n"), [], [], False
    for ln in lines:
        if ln.startswith("```"):
            if not in_f:
                if buf:
                    out.append((False, "\n".join(buf))); buf = []
                buf.append(ln); in_f = True
            else:
                buf.append(ln); out.append((True, "\n".join(buf))); buf = []; in_f = False
        else:
            buf.append(ln)
    if buf:
        out.append((in_f, "\n".join(buf)))
    return out


def drop_degenerate_tables(text):
    lines, out, i = text.split("\n"), [], 0
    while i < len(lines):
        if lines[i].strip() == "```rst-table":
            j = i + 1
            while j < len(lines) and lines[j].strip() != "```":
                j += 1
            body = lines[i + 1:j]
            if sum(1 for l in body if BORDER.match(l)) < 2:
                i = j + 1; continue
            out.extend(lines[i:j + 1]); i = j + 1
        else:
            out.append(lines[i]); i += 1
    return "\n".join(out)


def process(path):
    text = open(path, encoding="utf-8").read()
    # 6. degenerate rst-tables (whole-text, fence-aware by construction)
    text = drop_degenerate_tables(text)
    # 2-5. prose-only transforms
    out = []
    for is_f, chunk in split_fences(text):
        if is_f:
            out.append(chunk); continue
        c = SPAN.sub(repl_span, chunk)
        c = ATTR.sub("", c)
        c = esc_braces(c)
        c = BLOCK.sub("", c)
        out.append(c)
    text = "\n".join(out)
    # 7. unescape intended inline tags
    for tag in INTENDED:
        text = text.replace(BS + tag, tag)
    # 1. frontmatter (prepend if absent) — always includes an ASCII-safe slug
    if not text.startswith("---\n"):
        title, label = title_for(path, text)
        book_dir = os.path.basename(os.path.dirname(os.path.abspath(path)))
        slug = f"/{book_dir}/{slugify(title)}"
        title_esc = title.replace('"', '\\"')
        label_esc = label.replace('"', '\\"')
        text = f'---\ntitle: "{title_esc}"\nsidebar_label: "{label_esc}"\nslug: {slug}\n---\n\n' + text
    open(path, "w", encoding="utf-8", newline="").write(text)


if __name__ == "__main__":
    files = sys.argv[1:] or sorted(glob.glob("*/*.mdx"))
    for f in files:
        process(f)
        print(f"[mdx-safe] {f}")
