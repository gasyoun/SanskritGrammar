#!/usr/bin/env python3
"""Validate Sangram article manifests against the C4 editorial contract (H633).

Checks, in order:
  1. JSON Schema conformance (sangram/editorial/data/article.schema.json) when
     the `jsonschema` package is importable; otherwise a built-in structural
     subset (required keys, closed enums, id/date patterns, locale rules).
  2. Editorial semantics —
     * example IDs are unique, and their <slug> segment equals the article's;
     * canonical script: text_slp1/segmentation_slp1 are ASCII SLP1 only, and
       no hand-written IAST/Devanagari sibling copy sneaks in under any key
       (single-canonical-copy rule; renders derive via sanskrit-util);
     * scientific-layer examples carry a real corpus locus ('constructed' is
       pedagogical-only);
     * evidence: internal carries no URL, public carries an https URL;
     * EN locale never leads RU: locales.en.translated_from names the date of
       an existing revisions[] entry (when revisions are non-empty);
     * revisions dates are non-decreasing (append-only history).
  3. Private-data leakage — the serialized manifest contains no private hub
     URL, no local filesystem path, no volatile-registry pattern. Leakage
     must be exactly 0 to pass (same rule as atlas_validate_bundle.py).

Usage:
  python scripts/article_validate.py sangram/editorial/data/article.fixture.json
  python scripts/article_validate.py --all      # every article.manifest.json under sangram/
  python scripts/article_validate.py --self-test

Exit 0 = valid; exit 1 = one or more violations (all printed).
"""

import argparse
import copy
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
SCHEMA_PATH = HERE.parent / "sangram" / "editorial" / "data" / "article.schema.json"
FIXTURE_PATH = HERE.parent / "sangram" / "editorial" / "data" / "article.fixture.json"

ART_ID_RE = re.compile(r"^art:[a-z0-9][a-z0-9-]*$")
EX_ID_RE = re.compile(r"^ex:([a-z0-9][a-z0-9-]*):([1-9]\d*)$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SLP1_RE = re.compile(r"^[a-zA-Z'/\\^|~. +-]+$")
CORPUS_RE = re.compile(r"^[a-z][a-z0-9-]*$")
LAYERS = {"scientific", "pedagogical"}
REVISION_KINDS = {"published", "erratum", "revision", "retraction"}

# Keys that would smuggle a second, hand-written copy of a Sanskrit text in a
# non-canonical script. Renders are derived by sanskrit-util, never stored.
BANNED_SCRIPT_KEY_RE = re.compile(r"^(text|segmentation)_(iast|deva(nagari)?|hk|itrans|velthuis)$")

# C3 interface point: the closed corpus registry with quality/rights/liveness
# gates is owned by the C3 evidence method. Until it lands, unknown corpus
# slugs WARN rather than fail; 'constructed' is the no-witness marker.
KNOWN_CORPORA = {"dcs", "vedaweb", "gretil", "samudramanthanam", "wisdomlib",
                 "dharmamitra", "constructed"}

LEAKAGE_PATTERNS = [
    "github.com/gasyoun/Uprava",
    "github.com/gasyoun/github-spine",
    "RuWritingStyles-corpus",
    "telegram-sanskrit-corpus",
    "C:/Users", "C:\\Users", "/home/", "Documents/GitHub",
    "GTD_NEXT_ACTIONS", "BOTTLENECKS.md", "NEXT_TASK_QUEUE",
    "@DECIDE", "@WAITING", ".claim",
    "\U0001f512",  # 🔒 — claims/volatile state never enter a manifest
]


def _builtin_schema_subset(manifest, err):
    """Structural subset used when `jsonschema` is unavailable."""
    if manifest.get("canonical_script") != "slp1":
        err("canonical_script must be the constant 'slp1'")
    if not re.match(r"^\d+\.\d+\.\d+$", str(manifest.get("contract_version", ""))):
        err("contract_version must be semver")
    art = manifest.get("article")
    if not isinstance(art, dict):
        err("article object missing")
        return
    for key in ("id", "as_of", "layers", "locales", "examples", "revisions"):
        if key not in art:
            err(f"article.{key} missing")
    if not ART_ID_RE.match(str(art.get("id", ""))):
        err(f"article.id {art.get('id')!r} does not match art:<slug>")
    if not DATE_RE.match(str(art.get("as_of", ""))):
        err("article.as_of is not YYYY-MM-DD")
    layers = art.get("layers", [])
    if not layers or not set(layers) <= LAYERS or len(set(layers)) != len(layers):
        err(f"article.layers {layers!r} must be a non-empty unique subset of {sorted(LAYERS)}")
    locales = art.get("locales", {})
    if "ru" not in locales:
        err("locales.ru is mandatory (Russian is the default locale)")
    for loc, entry in locales.items():
        if loc not in ("ru", "en"):
            err(f"unknown locale {loc!r} (contract 1.x fixes the set to ru+en)")
        elif not isinstance(entry, dict) or not entry.get("title"):
            err(f"locales.{loc}.title missing")
    if "en" in locales and isinstance(locales["en"], dict) and "translated_from" not in locales["en"]:
        err("locales.en.translated_from missing (EN never leads RU)")
    for rev in art.get("revisions", []):
        if rev.get("kind") not in REVISION_KINDS:
            err(f"revision kind {rev.get('kind')!r} not in {sorted(REVISION_KINDS)}")
        if not DATE_RE.match(str(rev.get("date", ""))):
            err(f"revision date {rev.get('date')!r} is not YYYY-MM-DD")
        if not rev.get("note_ru"):
            err("revision note_ru missing")
    for ex in art.get("examples", []):
        for key in ("id", "layer", "text_slp1", "locus", "translations", "evidence", "as_of"):
            if key not in ex:
                err(f"example {ex.get('id', '?')}: {key} missing")
        if ex.get("layer") not in LAYERS:
            err(f"example {ex.get('id', '?')}: layer {ex.get('layer')!r} invalid")
        tr = ex.get("translations", {})
        if not isinstance(tr, dict) or not tr.get("ru"):
            err(f"example {ex.get('id', '?')}: translations.ru is mandatory")
        if not DATE_RE.match(str(ex.get("as_of", ""))):
            err(f"example {ex.get('id', '?')}: as_of is not YYYY-MM-DD")


def _walk_keys(obj, path=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield f"{path}.{k}" if path else k, k
            yield from _walk_keys(v, f"{path}.{k}" if path else k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from _walk_keys(v, f"{path}[{i}]")


def validate(manifest, serialized):
    errors, warnings = [], []
    err, warn = errors.append, warnings.append

    # -- 1. schema ----------------------------------------------------------
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    try:
        import jsonschema
        validator = jsonschema.Draft202012Validator(schema)
        for v in validator.iter_errors(manifest):
            path = "/".join(str(p) for p in v.absolute_path)
            err(f"schema: {path or '<root>'}: {v.message}")
    except ImportError:
        _builtin_schema_subset(manifest, err)

    art = manifest.get("article") or {}
    art_id = str(art.get("id", ""))
    art_slug = art_id.split(":", 1)[1] if ":" in art_id else ""

    # -- 2. editorial semantics ---------------------------------------------
    seen_ex = set()
    for ex in art.get("examples", []):
        ex_id = str(ex.get("id", ""))
        m = EX_ID_RE.match(ex_id)
        if not m:
            err(f"example id {ex_id!r} does not match ex:<slug>:<n>")
        else:
            if m.group(1) != art_slug:
                err(f"example {ex_id}: slug segment {m.group(1)!r} != article slug {art_slug!r}")
            if ex_id in seen_ex:
                err(f"example id {ex_id} duplicated (stable IDs are never reused)")
            seen_ex.add(ex_id)
        for field in ("text_slp1", "segmentation_slp1"):
            text = ex.get(field)
            if text is not None and not SLP1_RE.match(str(text)):
                bad = sorted({c for c in str(text) if not SLP1_RE.match(c)})
                err(f"example {ex_id}: {field} is not canonical SLP1 (offending: {bad!r}); "
                    f"IAST/Devanagari are derived by sanskrit-util, never stored")
        locus = ex.get("locus") or {}
        corpus = str(locus.get("corpus", ""))
        if corpus and not CORPUS_RE.match(corpus):
            err(f"example {ex_id}: corpus slug {corpus!r} invalid")
        elif corpus and corpus not in KNOWN_CORPORA:
            warn(f"example {ex_id}: corpus {corpus!r} not in the interim registry "
                 f"{sorted(KNOWN_CORPORA)} — must be registered in the C3 corpus registry")
        if ex.get("layer") == "scientific" and corpus == "constructed":
            err(f"example {ex_id}: scientific-layer examples require a corpus witness "
                f"('constructed' is pedagogical-only)")
        ev = ex.get("evidence") or {}
        if ev.get("visibility") == "internal" and ev.get("url"):
            err(f"example {ex_id}: internal evidence must not carry a URL")
        if ev.get("visibility") == "public" and not str(ev.get("url", "")).startswith("https://"):
            err(f"example {ex_id}: public evidence requires an https URL")

    for path, key in _walk_keys(manifest):
        if BANNED_SCRIPT_KEY_RE.match(key):
            err(f"{path}: banned non-canonical script copy (single-source rule: "
                f"store SLP1 once, derive IAST/Devanagari via sanskrit-util)")

    revisions = art.get("revisions", [])
    dates = [r.get("date", "") for r in revisions]
    if dates != sorted(dates):
        err(f"revisions dates {dates!r} are not non-decreasing (history is append-only)")
    en = (art.get("locales") or {}).get("en")
    if isinstance(en, dict) and revisions:
        if en.get("translated_from") not in dates:
            err(f"locales.en.translated_from {en.get('translated_from')!r} names no "
                f"revisions[] entry (EN must mirror a settled RU revision)")

    # -- 3. leakage -----------------------------------------------------------
    for pattern in LEAKAGE_PATTERNS:
        if pattern in serialized:
            err(f"leakage: forbidden pattern {pattern!r} present in serialized manifest")

    return errors, warnings


def run_file(path: Path) -> int:
    serialized = path.read_text(encoding="utf-8")
    manifest = json.loads(serialized)
    errors, warnings = validate(manifest, serialized)
    for w in warnings:
        print(f"WARN  {path.name}: {w}")
    for e in errors:
        print(f"ERROR {path.name}: {e}")
    print(f"{'PASS' if not errors else 'FAIL'}  {path.name}: "
          f"{len(errors)} error(s), {len(warnings)} warning(s)")
    return 0 if not errors else 1


def self_test() -> int:
    """Fixture must pass; characteristic mutations must each fail."""
    serialized = FIXTURE_PATH.read_text(encoding="utf-8")
    fixture = json.loads(serialized)
    failures = []

    errors, _ = validate(fixture, serialized)
    if errors:
        failures.append(f"fixture should pass but got: {errors}")

    def mutated(mutate):
        m = copy.deepcopy(fixture)
        mutate(m)
        s = json.dumps(m, ensure_ascii=False)
        errs, _ = validate(m, s)
        return errs

    cases = {
        "devanagari in text_slp1": lambda m: m["article"]["examples"][0].__setitem__(
            "text_slp1", "विद्या"),
        "iast diacritic in text_slp1": lambda m: m["article"]["examples"][0].__setitem__(
            "text_slp1", "vidyā dadāti"),
        "hand-written iast sibling copy": lambda m: m["article"]["examples"][0].__setitem__(
            "text_iast", "vidya dadati"),
        "internal evidence with URL": lambda m: m["article"]["examples"][1]["evidence"].__setitem__(
            "url", "https://example.org/"),
        "public evidence without URL": lambda m: m["article"]["examples"][0]["evidence"].pop("url"),
        "en locale without translated_from": lambda m: m["article"]["locales"]["en"].pop("translated_from"),
        "translated_from names no revision": lambda m: m["article"]["locales"]["en"].__setitem__(
            "translated_from", "2001-01-01"),
        "scientific example on constructed locus": lambda m: m["article"]["examples"][0]["locus"].__setitem__(
            "corpus", "constructed"),
        "duplicate example id": lambda m: m["article"]["examples"][1].__setitem__(
            "id", m["article"]["examples"][0]["id"]),
        "foreign slug in example id": lambda m: m["article"]["examples"][0].__setitem__(
            "id", "ex:other-article:1"),
        "missing ru translation": lambda m: m["article"]["examples"][0]["translations"].pop("ru"),
        "leakage pattern in manifest": lambda m: m["article"]["examples"][0]["gloss_ru"].__class__ and
            m["article"]["examples"][0].__setitem__("gloss_ru", "see GTD_NEXT_ACTIONS row"),
    }
    for name, mutate in cases.items():
        if not mutated(mutate):
            failures.append(f"mutation {name!r} should fail but passed")

    for f in failures:
        print(f"SELF-TEST FAIL: {f}")
    print(f"{'PASS' if not failures else 'FAIL'}  self-test: "
          f"{len(cases) + 1 - len(failures)}/{len(cases) + 1} checks green")
    return 0 if not failures else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("manifest", nargs="?", help="path to an article manifest JSON")
    ap.add_argument("--all", action="store_true",
                    help="validate every article.manifest.json under sangram/ plus the fixture")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()

    if args.self_test:
        return self_test()
    if args.all:
        targets = sorted((HERE.parent / "sangram").rglob("article.manifest.json"))
        targets.append(FIXTURE_PATH)
        return max((run_file(p) for p in targets), default=0)
    if not args.manifest:
        ap.error("give a manifest path, --all, or --self-test")
    return run_file(Path(args.manifest))


if __name__ == "__main__":
    sys.exit(main())
