"""Book-site tooling for the docx->mdx pipeline: fidelity report, image
optimization, and build verification against the canonical configuration.

Usage:
  python scripts/site_tools.py fidelity [ROOT]     # QA report over the .mdx
  python scripts/site_tools.py images   [ROOT]     # downscale + WebP media
  python scripts/site_tools.py site     [ROOT]     # npm build; never scaffolds
All commands are safe to re-run.
"""
import sys, os, re, glob, subprocess, pathlib
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

DEFAULT_ROOT = r"C:\Users\user\Documents\GitHub\SanskritGrammar"
GRID = re.compile(r"^\+[-=+]+\+\s*$", re.M)
PIPE_SEP = re.compile(r"^\|[\s:|-]+\|\s*$", re.M)
# Pandoc simple-table underline = 2+ dash-groups separated by spaces ("----- -----"),
# NOT a lone "---" (frontmatter delimiter / thematic break).
SIMPLE = re.compile(r"^-+( +-+)+\s*$", re.M)


# ---------------------------------------------------------------- fidelity ---
def fidelity(root):
    files = sorted(glob.glob(os.path.join(root, "*", "*.mdx")))
    print("FIDELITY REPORT")
    print(f"{'file':44} {'repl':>4} {'grid':>5} {'pipe':>5} {'simple':>6} {'rel-img':>7}")
    ok = True
    for f in files:
        t = open(f, encoding="utf-8").read()
        # count grid tables = number of ```rst-table fences
        grid = len(re.findall(r"^```rst-table\s*$", t, re.M))
        pipe = len(PIPE_SEP.findall(t))
        # simple-table leftovers only OUTSIDE fenced blocks
        prose = re.sub(r"```.*?```", "", t, flags=re.S)
        simple = len(SIMPLE.findall(prose))
        repl = t.count("�")
        imgs = re.findall(r"!\[[^\]]*\]\(([^)]+)\)", t)
        rel = all(not (u.startswith("/") or u.startswith("http") or ":" in u[:5]) for u in imgs) if imgs else True
        flag = ""
        if repl or simple or not rel:
            ok = False; flag = "  <-- FLAG"
        name = os.path.relpath(f, root).replace("\\", "/")
        print(f"{name:44} {repl:>4} {grid:>5} {pipe:>5} {simple:>6} {'yes' if rel else 'NO':>7}{flag}")
    print("RESULT:", "all clean" if ok else "flags above need a look")
    return ok


# ------------------------------------------------------------------ images ---
def optimize_images(root, max_w=1400, quality=80):
    try:
        from PIL import Image
    except ImportError:
        print("[images] Pillow not installed (pip install Pillow) - skipped")
        return
    media = glob.glob(os.path.join(root, "*", "*_media", "**", "*.*"), recursive=True)
    imgs = [p for p in media if p.lower().endswith((".png", ".jpg", ".jpeg"))]
    if not imgs:
        print("[images] no raster media found"); return
    saved = 0
    for p in imgs:
        webp = os.path.splitext(p)[0] + ".webp"
        try:
            im = Image.open(p)
            if im.width > max_w:
                im = im.resize((max_w, round(im.height * max_w / im.width)))
            im.save(webp, "WEBP", quality=quality, method=6)
            before, after = os.path.getsize(p), os.path.getsize(webp)
            if after < before:
                saved += before - after
                # Rewrite links ONLY in the .mdx that OWNS this image (same book folder),
                # matching the full media-relative path — NOT the bare basename, which is
                # shared across books ("image1.png" exists in several) and would cross-
                # contaminate other books' links into non-existent files.
                pp = pathlib.Path(p)
                media_anc = next(a for a in pp.parents if a.name.endswith("_media"))
                book_dir = media_anc.parent
                oldrel = os.path.relpath(p, book_dir).replace(os.sep, "/")
                newrel = os.path.relpath(webp, book_dir).replace(os.sep, "/")
                for mdx in glob.glob(os.path.join(str(book_dir), "*.mdx")):
                    tx = open(mdx, encoding="utf-8").read()
                    if oldrel in tx:
                        open(mdx, "w", encoding="utf-8", newline="").write(tx.replace(oldrel, newrel))
                os.remove(p)
                print(f"[images] {os.path.relpath(webp, root)}  {before//1024}KB -> {after//1024}KB")
            else:
                os.remove(webp)
        except Exception as e:
            print(f"[images] skip {os.path.basename(p)}: {e}")
    print(f"[images] saved ~{saved//1024} KB total")


# ------------------------------------------------------------------- site ---
def site(root):
    """Build the one canonical site; dependency installation is explicit."""
    if not os.path.isfile(os.path.join(root, "docusaurus.config.mjs")):
        print("[site] canonical docusaurus.config.mjs is missing")
        return False
    if not os.path.isdir(os.path.join(root, "node_modules")):
        print("[site] node_modules missing; run `npm ci` first")
        return False
    print("[site] npm run build ...")
    r = subprocess.run(["npm", "run", "build"], cwd=root, shell=True,
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    ok = "[SUCCESS] Generated static files" in (r.stdout + r.stderr)
    print("[site] build:", "GREEN" if ok else "FAILED")
    # per-book rendered-table counts
    for p in sorted(glob.glob(os.path.join(root, "build", "grammars", "*", "*", "index.html"))):
        n = open(p, encoding="utf-8", errors="replace").read().count("<table")
        book = os.path.relpath(p, os.path.join(root, "build", "grammars")).replace("\\", "/").rsplit("/", 1)[0]
        print(f"[site] {n:>4} <table>  {book}")
    if not ok:
        tail = "\n".join((r.stdout + r.stderr).splitlines()[-15:])
        print("---- build tail ----\n" + tail)
    return ok


# ------------------------------------------------------------------ links ---
def _cfg(text, key, default):
    m = re.search(key + r"\s*:\s*'([^']*)'", text)
    return m.group(1) if m else default


def links(root, fmt="md"):
    """Print each .mdx as its Docusaurus route (deployed URL), read from
    docusaurus.config.mjs (url + baseUrl + docs routeBasePath). `fmt`: md|url."""
    cfg = ""
    cfgp = os.path.join(root, "docusaurus.config.mjs")
    if os.path.exists(cfgp):
        cfg = open(cfgp, encoding="utf-8").read()
    url = _cfg(cfg, "url", "https://example.github.io").rstrip("/")
    base = _cfg(cfg, "baseUrl", "/").strip("/")
    rbp = _cfg(cfg, "routeBasePath", "docs").strip("/")
    prefix = "/".join(x for x in (base, rbp) if x)
    mdx = sorted(glob.glob(os.path.join(root, "*", "*.mdx")))
    for m in mdx:
        route = os.path.splitext(os.path.relpath(m, root).replace(os.sep, "/"))[0]
        full = f"{url}/{prefix}/{route}"
        label = os.path.basename(route)
        print(f"- [{label}]({full})" if fmt == "md" else full)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "fidelity"
    root = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_ROOT
    {"fidelity": fidelity, "images": optimize_images, "site": site, "links": links}[cmd](root)
