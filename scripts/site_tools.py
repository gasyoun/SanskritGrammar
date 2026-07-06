"""Book-site tooling for the docx->mdx pipeline: fidelity report, image
optimization, and an idempotent Docusaurus site scaffold + build-verify.

Usage:
  python scripts/site_tools.py fidelity [ROOT]     # QA report over the .mdx
  python scripts/site_tools.py images   [ROOT]     # downscale + WebP media
  python scripts/site_tools.py site     [ROOT]     # scaffold if absent + npm build
All are safe to re-run; `site` only writes files that don't already exist.
"""
import sys, os, re, glob, json, subprocess, shutil, pathlib
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
PLUGIN_SRCS = [
    r"C:\Users\user\Documents\GitHub\csl-guides\src\remark",
    r"C:\Users\user\Documents\GitHub\buhler-sanskrit-book\src\remark",
]
PLUGIN_FILES = ["rstTable.mjs", "rstTableAst.mjs", "rstTableParser.mjs"]


def _write_if_absent(path, content):
    if os.path.exists(path):
        print(f"[site] keep {os.path.basename(path)} (exists)"); return False
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8", newline="").write(content)
    print(f"[site] wrote {os.path.relpath(path)}"); return True


def vendor_plugin(root):
    dst = os.path.join(root, "src", "remark")
    os.makedirs(dst, exist_ok=True)
    have = all(os.path.exists(os.path.join(dst, f)) for f in PLUGIN_FILES)
    if have:
        print("[site] rstTable plugin already vendored"); return
    src = next((s for s in PLUGIN_SRCS if all(os.path.exists(os.path.join(s, f)) for f in PLUGIN_FILES)), None)
    if not src:
        print("[site] WARNING: no sibling rstTable source found (csl-guides/buhler) - vendor by hand"); return
    for f in PLUGIN_FILES:
        shutil.copy(os.path.join(src, f), os.path.join(dst, f))
    print(f"[site] vendored rstTable plugin from {src}")


def scaffold(root, project="SanskritGrammar", org="gasyoun"):
    book_dirs = sorted(d for d in os.listdir(root)
                       if os.path.isdir(os.path.join(root, d)) and glob.glob(os.path.join(root, d, "*.mdx")))
    includes = ",\n            ".join(f"'{d}/**.mdx'" for d in book_dirs)
    vendor_plugin(root)
    _write_if_absent(os.path.join(root, "package.json"), json.dumps({
        "name": f"{project.lower()}-book-site", "version": "0.1.0", "private": True,
        "scripts": {"docusaurus": "docusaurus", "start": "docusaurus start",
                    "build": "docusaurus build", "serve": "docusaurus serve", "clear": "docusaurus clear"},
        "dependencies": {"@docusaurus/core": "3.6.3", "@docusaurus/preset-classic": "3.6.3",
                         "clsx": "^2.1.1", "prism-react-renderer": "^2.4.0",
                         "react": "^18.3.1", "react-dom": "^18.3.1", "unist-util-visit": "^5.0.0"},
        "devDependencies": {"@docusaurus/module-type-aliases": "3.6.3", "@docusaurus/types": "3.6.3"},
        "overrides": {"webpack": "5.97.1"},
        "engines": {"node": ">=18.0"},
    }, indent=2, ensure_ascii=False) + "\n")
    _write_if_absent(os.path.join(root, "docusaurus.config.mjs"),
        "import remarkRstTable from './src/remark/rstTable.mjs';\n\n"
        "const config = {\n"
        f"  title: '{project}', url: 'https://{org}.github.io', baseUrl: '/{project}/',\n"
        f"  organizationName: '{org}', projectName: '{project}',\n"
        "  onBrokenLinks: 'warn', onBrokenMarkdownLinks: 'warn', onBrokenAnchors: 'ignore',\n"
        "  presets: [['classic', {\n"
        "    docs: { path: '.', routeBasePath: 'grammars', sidebarPath: './sidebars.mjs',\n"
        f"            include: [\n            {includes},\n          ],\n"
        "            exclude: ['**/node_modules/**','**/build/**','**/.docusaurus/**','**/src/**'],\n"
        "            remarkPlugins: [remarkRstTable] },\n"
        "    blog: false, theme: {} }]],\n"
        "  themeConfig: { navbar: { title: '" + project + "', items: [\n"
        "    { type: 'docSidebar', sidebarId: 'grammarsSidebar', position: 'left', label: 'Grammars' } ] } },\n"
        "};\nexport default config;\n")
    _write_if_absent(os.path.join(root, "sidebars.mjs"),
        "const sidebars = { grammarsSidebar: [{ type: 'autogenerated', dirName: '.' }] };\n"
        "export default sidebars;\n")
    _write_if_absent(os.path.join(root, ".gitignore"),
        "/node_modules\n/build\n/.docusaurus\n~$*\n")


def site(root):
    scaffold(root)
    if not os.path.isdir(os.path.join(root, "node_modules")):
        print("[site] npm install ...")
        subprocess.run(["npm", "install"], cwd=root, shell=True)
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
