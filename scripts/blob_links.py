"""Rewrite relative Markdown link targets to full GitHub blob URLs.

Uprava H5423 (E016 wave 5). Committed repo Markdown carries full blob URLs (estate
clickable-links rule); the H4092 wave-3 sweep (05-09-2026) upgraded the generated
CLAIMS_VERIFIED.md / ERRATA.md files by hand-run pass, while their generators kept
emitting relative links. Any regeneration then reverted the sweep, so a live
regen trigger would fight it forever. The generators now call absolutize() on the
.md files they write. ERRATA.mdx stays relative on purpose: the Docusaurus site
resolves those links itself.
"""

import posixpath
import re

BLOB_BASE = "https://github.com/gasyoun/SanskritGrammar/blob/main/"
_LINK = re.compile(r"\]\((?!https?://|mailto:|#)([^)\s]+)\)")


def absolutize(md: str, rel_dir: str = "") -> str:
    """Rewrite every relative `](target)` in md, resolved against rel_dir (repo-relative)."""
    def repl(m):
        target = posixpath.normpath(posixpath.join(rel_dir, m.group(1)))
        return f"]({BLOB_BASE}{target})"
    return _LINK.sub(repl, md)
