"""Batch convert .doc/.docx -> .mdx (LibreOffice for .doc, Pandoc for .docx).

.mdx + ```rst-table```-wrapped grid tables is universal (every target), because Pandoc's
default table-style auto-pick can emit "simple tables" (bare dashes) that are not
valid GFM/MDX and render as inert text on any target.
"""
import sys, subprocess, pathlib, shutil, re
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

DEFAULT_ROOT = r"C:\Users\user\Documents\GitHub\SanskritGrammar"

args = sys.argv[1:]
force = "--force" in args
positional = [a for a in args if not a.startswith("--")]
root = pathlib.Path(positional[0]) if positional else pathlib.Path(DEFAULT_ROOT)

if not root.is_dir():
    print(f"[FATAL] target dir not found: {root}")
    sys.exit(1)

print(f"[target] {root}  ->  .mdx, ```rst-table```-wrapped grid tables")


def find_soffice():
    for c in (shutil.which("soffice"),
              r"C:\Program Files\LibreOffice\program\soffice.exe",
              r"C:\Program Files (x86)\LibreOffice\program\soffice.exe"):
        if c and pathlib.Path(c).exists():
            return c
    return None


def newer_ok(out, src):
    return out.exists() and out.stat().st_mtime >= src.stat().st_mtime


SOFFICE = find_soffice()

# ---------- Pass 1: .doc -> .docx (LibreOffice) ----------
doc_done, doc_skip, doc_fail = [], [], []
doc_files = sorted(p for p in root.rglob("*.doc") if not p.name.startswith("~$"))

for src in doc_files:
    out = src.with_suffix(".docx")
    if out.exists():
        doc_skip.append(out)
        print(f"[doc  skip] {out}  (.docx already exists - authoritative, not overwritten)")
        continue
    if not SOFFICE:
        doc_fail.append((src, "LibreOffice (soffice) not found"))
        print(f"[doc  FAIL] {src}  (no soffice)")
        continue
    cmd = [SOFFICE, "--headless", "--convert-to", "docx",
           "--outdir", str(src.parent), src.name]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                         errors="replace", cwd=str(src.parent))
    if out.exists():
        doc_done.append(out)
        print(f"[doc  ok  ] {out}")
    else:
        doc_fail.append((src, (res.stderr or res.stdout).strip()))
        print(f"[doc  FAIL] {src}\n            {(res.stderr or res.stdout).strip()[:200]}")

# ---------- Pass 2: .docx -> .mdx (Pandoc) ----------
PANDOC_TO = "markdown-simple_tables-multiline_tables"
BASE_FLAGS = ["--from", "docx", "--to", PANDOC_TO,
              "--wrap=none", "--markdown-headings=atx"]
GRID_BORDER = re.compile(r"^\+[-=+]+\+\s*$")


def wrap_grid_tables(md_text):
    lines = md_text.splitlines()
    out, i, wrapped = [], 0, 0
    while i < len(lines):
        if GRID_BORDER.match(lines[i]):
            start = i
            i += 1
            while i < len(lines) and (GRID_BORDER.match(lines[i]) or lines[i].startswith("|")):
                i += 1
            block = "\n".join(lines[start:i])
            out.append("```rst-table")
            out.append(block)
            out.append("```")
            wrapped += 1
        else:
            out.append(lines[i])
            i += 1
    return "\n".join(out) + "\n", wrapped


md_done, md_skip, md_fail = [], [], []
docx_files = sorted(p for p in root.rglob("*.docx") if not p.name.startswith("~$"))

for src in docx_files:
    out = src.with_suffix(".mdx")
    if newer_ok(out, src) and not force:
        md_skip.append(out)
        print(f"[docx skip] {out}")
        continue
    rel_media = src.stem + "_media"
    cmd = ["pandoc", src.name, *BASE_FLAGS,
           "--extract-media", rel_media, "-o", out.name]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                         errors="replace", cwd=str(src.parent))
    if res.returncode == 0:
        text = out.read_text(encoding="utf-8")
        wrapped_text, n_wrapped = wrap_grid_tables(text)
        if n_wrapped:
            out.write_text(wrapped_text, encoding="utf-8")
        md_done.append(out)
        print(f"[docx ok  ] {out}" + (f"  ({n_wrapped} grid table(s) wrapped)" if n_wrapped else ""))
    else:
        md_fail.append((src, (res.stderr or "").strip()))
        print(f"[docx FAIL] {src}\n            {(res.stderr or '').strip()[:200]}")

print("\n===== SUMMARY =====")
print(f".doc -> .docx :  converted {len(doc_done)}   skipped {len(doc_skip)}   failed {len(doc_fail)}")
print(f".docx -> .mdx :  converted {len(md_done)}   skipped {len(md_skip)}   failed {len(md_fail)}")
for s, err in doc_fail + md_fail:
    print(f"  FAILED {s}: {(err.splitlines()[0] if err else '(no output)')}")
