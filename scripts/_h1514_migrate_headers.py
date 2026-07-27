"""One-shot H1514 migration: update errata.yml header comments for the new
tier/id/checksum schema. Run once, then delete."""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent

STANDARD_TIER_DOC = (
    "#\n"
    "# tier:    (optional) erratum (default) | revision | retraction — the ACL\n"
    "#          three-tier corrections model (https://aclanthology.org/info/corrections/).\n"
    "# revises: (revision only) the `id` of the entry this one replaces — its own\n"
    "#          id becomes `<that-id>.v2` (or `.v3`, ... for a chain).\n"
    "# reason:  (retraction only) why this entry is withdrawn.\n"
    "# id / date / checksum are never hand-authored — build_errata.py computes them.\n"
)

for yml in sorted(ROOT.glob("*/errata.yml")):
    text = yml.read_text(encoding="utf-8")
    text = text.replace("ERRATA.md", "ERRATA.mdx")
    if "Entry shape: {" in text and "tier:" not in text:
        lines = text.splitlines(keepends=True)
        out = []
        for ln in lines:
            out.append(ln)
            if ln.startswith("# Entry shape: {"):
                out.append(STANDARD_TIER_DOC)
        text = "".join(out)
    yml.write_text(text, encoding="utf-8")
    print(f"  {yml.parent.name}: header updated")
