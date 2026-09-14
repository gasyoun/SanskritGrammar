#!/usr/bin/env python3
"""idml_coverage_check.py — lexical coverage gate for an extracted .mdx edition vs its .idml source.

H4628 acceptance: "coverage-check зелёный". The check re-extracts the source text
INDEPENDENTLY of tools/idml_to_mdx.py (every Content/Br element of every
Stories/Story_*.xml, no spread ordering, nothing skipped) and measures how much of
that lexical mass the committed .mdx carries back.

Coverage metrics (token = whitespace-delimited, punctuation kept):
  token_coverage = |multiset(src) ∩ multiset(mdx)| / |multiset(src)|
  char_coverage  = (src_chars - lost_chars) / src_chars  over the token alignment

Green verdict: token_coverage >= 0.90 AND char_coverage >= 0.90 AND mdx has a
YAML front matter with source_package == the checked idml file name.
(The H4484 pilot scored 92.9% against an EXTERNAL control versta; this check is
the same-source mechanical floor — anything below 90% means the extractor
dropped stories, not that a control disagrees.)

Usage: python3 tools/idml_coverage_check.py <file.idml> <edition.mdx>
Exit 0 = GREEN, 1 = RED, 2 = usage error.
"""
import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from collections import Counter

try:
    import pymupdf
except ImportError:
    pymupdf = None

GREEN_FLOOR = 0.90


def local(el):
    return el.tag.rsplit("}", 1)[-1]


def source_tokens(idml_path, kind="idml"):
    """All text mass in the package, read independently of the extractor's ordering."""
    if kind == "pdf":
        if pymupdf is None:
            raise SystemExit("pymupdf is required for --source-kind pdf")
        doc = pymupdf.open(idml_path)
        texts = []
        for i in range(doc.page_count):
            for w in doc[i].get_text("words"):
                texts.append(w[4])
                texts.append(" ")
        doc.close()
        return "".join(texts)
    zf = zipfile.ZipFile(idml_path)
    texts = []
    for name in zf.namelist():
        if not (name.startswith("Stories/Story_") and name.endswith(".xml")):
            continue
        root = ET.fromstring(zf.read(name))
        for el in root.iter():
            if local(el) == "Content" and el.text:
                texts.append(el.text)
            elif local(el) == "Br":
                texts.append("\n")
    return "".join(texts)


def mdx_body(mdx_path):
    raw = open(mdx_path, encoding="utf-8").read()
    if raw.startswith("---\n"):
        end = raw.find("\n---\n", 4)
        if end != -1:
            fm = raw[4:end]
            raw = raw[end + 5:]
            m = re.search(r"^source_package:\s*(.+)$", fm, re.M)
            pkg = m.group(1).strip() if m else None
            return raw, pkg
    return raw, None


def tokens(text):
    return Counter(t for t in text.split() if t)


def main():
    argv = sys.argv[1:]
    kind = "idml"
    if "--source-kind" in argv:
        idx = argv.index("--source-kind")
        kind = argv[idx + 1] if idx + 1 < len(argv) else "idml"
        argv = argv[:idx] + argv[idx + 2:]
    if len(argv) != 2:
        print(__doc__)
        return 2
    idml_path, mdx_path = argv[0], argv[1]
    src = source_tokens(idml_path, kind)
    body, pkg = mdx_body(mdx_path)

    ok_pkg = pkg == idml_path.rsplit("/", 1)[-1]
    sc, mc = tokens(src), tokens(body)
    common = sum((sc & mc).values())
    src_total = sum(sc.values())
    token_cov = common / src_total if src_total else 0.0
    src_chars = len(re.sub(r"\s", "", src))
    kept_chars = sum(len(re.sub(r"\s", "", t)) * n for t, n in (sc & mc).items())
    char_cov = kept_chars / src_chars if src_chars else 0.0

    missing = sc - mc
    missing_top = sorted(missing.items(), key=lambda kv: -kv[1])[:10]

    green = token_cov >= GREEN_FLOOR and char_cov >= GREEN_FLOOR and ok_pkg
    print(f"source_package_match: {'OK' if ok_pkg else f'MISMATCH (mdx={pkg})'}")
    print(f"source tokens: {src_total} unique={len(sc)} chars: {src_chars}")
    print(f"token_coverage: {token_cov:.1%}  char_coverage: {char_cov:.1%}")
    print(f"missing token instances: {sum(missing.values())} "
          f"(unique {len(missing)}); top: "
          + ", ".join(f"{t!r}x{n}" for t, n in missing_top))
    print(f"VERDICT: {'GREEN' if green else 'RED'} (floor {GREEN_FLOOR:.0%}) — "
          f"{idml_path} vs {mdx_path}")
    return 0 if green else 1


if __name__ == "__main__":
    sys.exit(main())
