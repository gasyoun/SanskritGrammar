#!/usr/bin/env python3
"""Build / check the Grammar Lab Wave-1 bundle (H2492).

Usage:
    python scripts/build_grammar_lab.py
    python scripts/build_grammar_lab.py --check
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

REPO = Path(__file__).resolve().parents[1]
LAB = REPO / "data" / "grammar_lab"
SCHEMAS = LAB / "schemas"
TOPICS_DIR = LAB / "topics"
EX_DIR = LAB / "exercises"
EXPORT = LAB / "export"
LOCI = LAB / "loci" / "zalizniak_section_loci.yml"
PIN = LAB / "pins" / "whitneyroots_roots_slice.csv"
QUERIES = LAB / "queries" / "frozen_queries.json"
REPORT = LAB / "export" / "evidence_contract_report.json"

BUNDLE_NAME = "grammar_lab.json"
LINKS_NAME = "typed_links.tsv"
MANIFEST_NAME = "manifest.json"
VECTORS_NAME = "topic_vectors.json"
SCHEMA_VERSION = "1.0.0"
BUNDLE_VERSION = "1.0.0"
GENERATOR = "scripts/build_grammar_lab.py"
DATE = "13-08-2026"

TYPE_D_FIELDS = [
    "anchor_type",
    "anchor_id",
    "anchor_key_slp1",
    "target_locus",
    "link_type",
    "source_dataset",
    "match_method",
    "confidence",
    "evidence_count",
    "date",
]
WHITNEY_SEC_RE = re.compile(r"^whitney-sec:(\d+)(?:-(\d+))?$")
Z1978_RE = re.compile(r"^zalizniak-1978-sec:(\d+)$")
TOPIC_RE = re.compile(r"^subject:grammar-lab:[a-z0-9]+(?:-[a-z0-9]+)*$")
DATE_RE = re.compile(r"^[0-3][0-9]-[0-1][0-9]-[0-9]{4}$")
ALLOWED_MATCH = {"id-link", "curated", "xref", "exact"}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def load_json_schema(name: str) -> dict:
    return json.loads((SCHEMAS / name).read_text(encoding="utf-8"))


def validate_schema(instance: dict, schema_name: str) -> list[str]:
    schema = load_json_schema(schema_name)
    try:
        import jsonschema
    except ImportError:
        return _lite_required(instance, schema)
    validator = jsonschema.Draft202012Validator(schema)
    return [f"{schema_name}: {e.message}" for e in validator.iter_errors(instance)]


def _lite_required(instance: dict, schema: dict) -> list[str]:
    errs = []
    for key in schema.get("required", []):
        if key not in instance:
            errs.append(f"missing {key}")
    return errs


def load_loci() -> dict:
    return yaml.safe_load(LOCI.read_text(encoding="utf-8"))


def known_zalizniak(loci: dict) -> set[str]:
    known: set[str] = set()
    z1975 = loci["works"]["zalizniak-1975"]
    for row in z1975["loci"]:
        known.add(row["id"])
    z2004 = loci["works"]["zalizniak-2004"]
    for row in z2004["loci"]:
        known.add(row["id"])
    for n in loci["works"]["zalizniak-1978"]["used_sections"]:
        known.add(f"zalizniak-1978-sec:{n}")
    # Native 1978 §§ exist even if unused; accept 1–242.
    for n in range(1, 243):
        known.add(f"zalizniak-1978-sec:{n}")
    return known


def load_pin() -> dict[int, dict]:
    out: dict[int, dict] = {}
    with PIN.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            out[int(row["whitney_no"])] = row
    return out


def lint_edge(edge: dict, topic_id: str, known_z: set[str]) -> list[str]:
    errs: list[str] = []
    for field in (
        "anchor_type",
        "anchor_id",
        "target_locus",
        "link_type",
        "source_dataset",
        "match_method",
        "confidence",
        "date",
    ):
        if field not in edge:
            errs.append(f"{topic_id}: edge missing {field}")
    if edge.get("target_locus") != topic_id:
        errs.append(f"{topic_id}: target_locus {edge.get('target_locus')}")
    if edge.get("link_type") != "thematic":
        errs.append(f"{topic_id}: link_type {edge.get('link_type')}")
    if edge.get("match_method") not in ALLOWED_MATCH:
        errs.append(f"{topic_id}: match_method {edge.get('match_method')}")
    if not DATE_RE.match(str(edge.get("date") or "")):
        errs.append(f"{topic_id}: bad date {edge.get('date')}")
    aid = str(edge.get("anchor_id") or "")
    at = edge.get("anchor_type")
    if at == "whitney-sec":
        m = WHITNEY_SEC_RE.match(aid)
        if not m:
            errs.append(f"{topic_id}: bad whitney-sec {aid}")
        else:
            lo = int(m.group(1))
            hi = int(m.group(2) or lo)
            if not (1 <= lo <= hi <= 1316):
                errs.append(f"{topic_id}: whitney-sec out of range {aid}")
    elif at == "whitney-root":
        if not re.match(r"^whitney-root:\d+$", aid):
            errs.append(f"{topic_id}: bad whitney-root {aid}")
    elif at == "zalizniak-1975":
        if aid not in known_z:
            errs.append(f"{topic_id}: unknown 1975 locus {aid}")
    elif at == "zalizniak-1978-sec":
        if not Z1978_RE.match(aid) or aid not in known_z:
            errs.append(f"{topic_id}: unknown 1978 locus {aid}")
    elif at == "zalizniak-2004":
        if aid not in known_z:
            errs.append(f"{topic_id}: unknown 2004 locus {aid}")
        if aid.endswith(":sandhi"):
            errs.append(f"{topic_id}: Sandhi locus is fenced")
    return errs


def evidence_row(topic: dict, exercises: dict[str, dict]) -> dict:
    omissions: list[str] = []
    whitney = any(
        e["anchor_type"] in {"whitney-sec", "whitney-root"} for e in topic["sources"]
    )
    zal = any(str(e["anchor_type"]).startswith("zalizniak") for e in topic["sources"])
    dictionary = bool(topic.get("dictionary_evidence"))
    corpus = bool(topic.get("corpus_evidence"))
    aliases = topic.get("aliases") or {}
    four = all(aliases.get(k) for k in ("ru", "deva", "iast", "slp1"))
    pub_ex = False
    for eid in topic.get("exercise_ids") or []:
        ex = exercises.get(eid)
        if ex and ex.get("status") == "published" and ex.get("risk_class") == "deterministic":
            pub_ex = True
    if not whitney:
        omissions.append("missing Whitney anchor")
    if not zal:
        omissions.append("missing Zalizniak anchor")
    if not dictionary:
        omissions.append("missing dictionary evidence")
    if not corpus:
        omissions.append("missing corpus evidence")
    if not pub_ex:
        omissions.append("missing publishable exercise")
    if not four:
        omissions.append("missing four-script aliases")
    publishable = topic.get("status") == "published" and not omissions
    return {
        "topic_id": topic["id"],
        "has_whitney": whitney,
        "has_zalizniak": zal,
        "has_dictionary": dictionary,
        "has_corpus": corpus,
        "has_exercise": pub_ex,
        "has_four_script_aliases": four,
        "publishable": publishable,
        "omissions": omissions,
    }


def load_topics() -> list[dict]:
    paths = sorted(TOPICS_DIR.glob("*.yml"))
    return [load_yaml(p) for p in paths]


def load_exercises() -> dict[str, dict]:
    out: dict[str, dict] = {}
    for path in sorted(EX_DIR.glob("*.yml")):
        rec = load_yaml(path)
        out[rec["id"]] = rec
    return out


def build_queries(topics: list[dict]) -> dict:
    queries = []
    qid = 0
    intents = (
        ("exact", "ru"),
        ("transliteration", "iast"),
        ("transliteration", "slp1"),
        ("transliteration", "deva"),
        ("russian", "ru"),
    )
    for topic in topics:
        if topic["status"] != "published":
            continue
        aliases = topic["aliases"]
        for intent, script in intents:
            values = aliases.get(script) or []
            if not values:
                continue
            qid += 1
            queries.append(
                {
                    "id": f"q{qid:03d}",
                    "query": values[0],
                    "script": script,
                    "intent": intent,
                    "acceptable_topic_ids": [topic["id"]],
                }
            )
        # form-to-concept / root-to-topic extras from title
        qid += 1
        queries.append(
            {
                "id": f"q{qid:03d}",
                "query": topic["title_ru"],
                "script": "ru",
                "intent": "form-to-concept",
                "acceptable_topic_ids": [topic["id"]],
            }
        )
    # Pad to ≥100 with second aliases where present.
    for topic in topics:
        if qid >= 100:
            break
        if topic["status"] != "published":
            continue
        for script, intent in (("ru", "russian"), ("iast", "transliteration")):
            vals = (topic["aliases"].get(script) or [])[1:]
            for val in vals:
                if qid >= 120:
                    break
                qid += 1
                queries.append(
                    {
                        "id": f"q{qid:03d}",
                        "query": val,
                        "script": script,
                        "intent": intent,
                        "acceptable_topic_ids": [topic["id"]],
                    }
                )
    return {
        "schema_version": SCHEMA_VERSION,
        "split": "frozen-test",
        "note": "G2 may tune fusion only on a designated development subset; this file is the frozen test set.",
        "queries": queries,
    }


def stable_json(obj: object) -> bytes:
    return (json.dumps(obj, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def content_view(manifest: dict) -> dict:
    view = dict(manifest)
    view.pop("generated_at", None)
    return view


def build() -> dict:
    if not TOPICS_DIR.is_dir() or not any(TOPICS_DIR.glob("*.yml")):
        # Local authoring helper; CI consumes committed YAML.
        sys.path.insert(0, str(REPO / "scripts"))
        import grammar_lab_inventory as inv  # noqa: WPS433

        inv.emit()

    topics = load_topics()
    exercises = load_exercises()
    loci = load_loci()
    known_z = known_zalizniak(loci)
    pin = load_pin()
    errors: list[str] = []

    for topic in topics:
        errors.extend(validate_schema(topic, "topic.schema.json"))
        if not TOPIC_RE.match(topic.get("id") or ""):
            errors.append(f"bad topic id {topic.get('id')}")
        for edge in topic.get("sources") or []:
            errors.extend(lint_edge(edge, topic["id"], known_z))
        for card in topic.get("dictionary_evidence") or []:
            n = int(card["whitney_no"])
            if n not in pin:
                errors.append(f"{topic['id']}: whitney_no {n} not in pin slice")
        for card in topic.get("corpus_evidence") or []:
            if card.get("status") == "not_attested" and "impossib" in (card.get("limitation") or "").lower():
                errors.append(f"{topic['id']}: non-attestation overclaims")

    for ex in exercises.values():
        errors.extend(validate_schema(ex, "exercise.schema.json"))
        if ex["risk_class"] == "interpretive" and ex.get("status") == "published":
            if not ex.get("approval_record"):
                errors.append(f"{ex['id']}: interpretive published without approval")
        if ex["risk_class"] == "deterministic":
            distractors = ex.get("distractors") or []
            if ex.get("answer") in distractors:
                errors.append(f"{ex['id']}: answer listed as distractor")
            if len(set(distractors)) != len(distractors):
                errors.append(f"{ex['id']}: duplicate distractors")

    reports = [evidence_row(t, exercises) for t in topics]
    published = [t for t in topics if t["status"] == "published"]
    review = [t for t in topics if t["status"] == "needs_review"]
    invalid_pub = [r for r in reports if r["topic_id"] in {t["id"] for t in published} and not r["publishable"]]
    if invalid_pub:
        errors.append(f"invalid published topics: {[r['topic_id'] for r in invalid_pub]}")
    if not (25 <= len(published) <= 40):
        errors.append(f"published count {len(published)} not in 25–40")

    if errors:
        for err in errors:
            print(err, file=sys.stderr)
        raise SystemExit(1)

    published_ex = [
        exercises[eid]
        for t in published
        for eid in t.get("exercise_ids") or []
        if eid in exercises and exercises[eid]["status"] == "published"
    ]
    bundle_topics = []
    for topic in published:
        bundle_topics.append(
            {
                "id": topic["id"],
                "schema_version": topic["schema_version"],
                "status": topic["status"],
                "title_ru": topic["title_ru"],
                "cluster": topic.get("cluster"),
                "aliases": topic["aliases"],
                "summary_ru": topic["summary_ru"],
                "alignment_note": topic.get("alignment_note"),
                "prerequisites": topic["prerequisites"],
                "difficulty": topic["difficulty"],
                "sources": topic["sources"],
                "dictionary_evidence": topic["dictionary_evidence"],
                "corpus_evidence": topic["corpus_evidence"],
                "exercise_ids": topic["exercise_ids"],
                "provenance": topic["provenance"],
            }
        )

    bundle = {
        "schema_version": SCHEMA_VERSION,
        "bundle_version": BUNDLE_VERSION,
        "topics": sorted(bundle_topics, key=lambda t: t["id"]),
        "exercises": sorted(published_ex, key=lambda e: e["id"]),
        "omissions": [t["id"] for t in review],
    }

    links: list[dict] = []
    for topic in published:
        for edge in topic["sources"]:
            row = {k: edge.get(k, "") if edge.get(k) is not None else "" for k in TYPE_D_FIELDS}
            links.append(row)
    links.sort(key=lambda r: (r["target_locus"], r["anchor_id"], r["anchor_type"]))

    queries = build_queries(published)
    EXPORT.mkdir(parents=True, exist_ok=True)
    QUERIES.parent.mkdir(parents=True, exist_ok=True)
    (EXPORT / BUNDLE_NAME).write_bytes(stable_json(bundle))
    with (EXPORT / LINKS_NAME).open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=TYPE_D_FIELDS, delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(links)
    QUERIES.write_bytes(stable_json(queries))
    REPORT.write_bytes(
        stable_json(
            {
                "schema_version": SCHEMA_VERSION,
                "published": len(published),
                "needs_review": len(review),
                "invalid_published": 0,
                "typed_links": len(links),
                "frozen_queries": len(queries["queries"]),
                "rows": reports,
            }
        )
    )

    # Vectors depend on the just-written bundle.
    sys.path.insert(0, str(REPO / "scripts"))
    import grammar_lab_embed as embed  # noqa: WPS433

    vec = embed.build_vectors(bundle)
    embed.write_vectors(vec)

    feeds = []
    for fid, rel, rights in (
        ("grammar_lab_bundle", f"data/grammar_lab/export/{BUNDLE_NAME}", "aggregate-public-safe"),
        ("typed_links", f"data/grammar_lab/export/{LINKS_NAME}", "aggregate-public-safe"),
        ("topic_vectors", f"data/grammar_lab/export/{VECTORS_NAME}", "aggregate-public-safe"),
        ("frozen_queries", "data/grammar_lab/queries/frozen_queries.json", "aggregate-public-safe"),
        ("evidence_contract", f"data/grammar_lab/export/{REPORT.name}", "aggregate-public-safe"),
        (
            "zalizniak_loci",
            "data/grammar_lab/loci/zalizniak_section_loci.yml",
            "pointer-only-no-bulk-gloss",
        ),
    ):
        path = REPO / rel
        feeds.append(
            {
                "id": fid,
                "path": rel.replace("\\", "/"),
                "sha256": sha256_file(path),
                "rights": rights,
            }
        )
    manifest = {
        "schema_version": SCHEMA_VERSION,
        "bundle_version": BUNDLE_VERSION,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "generator": GENERATOR,
        "published_topic_count": len(published),
        "needs_review_count": len(review),
        "feeds": feeds,
        "source_snapshot": {
            "whitneyroots_revision": "b453ce0e739c761aa0e32a1df6200d9875b148a5",
            "pin": "data/grammar_lab/pins/whitneyroots_roots_slice.csv",
            "loci": "data/grammar_lab/loci/zalizniak_section_loci.yml",
        },
        "embedding": {
            "model_name": vec["model_name"],
            "intended_sidecar_model": vec["intended_sidecar_model"],
            "revision": vec["revision"],
            "dimensionality": vec["dimensionality"],
            "backend": vec["backend"],
            "semantic_ready": vec["semantic_ready"],
            "source_text_sha256": vec["source_text_sha256"],
        },
        "omissions": [t["id"] for t in review],
    }
    errors = validate_schema(manifest, "manifest.schema.json")
    if errors:
        for err in errors:
            print(err, file=sys.stderr)
        raise SystemExit(1)
    (EXPORT / MANIFEST_NAME).write_bytes(stable_json(manifest))
    print(
        f"published={len(published)} needs_review={len(review)} "
        f"links={len(links)} queries={len(queries['queries'])} "
        f"vectors={len(vec['vectors'])} backend={vec['backend']}"
    )
    return manifest


def check() -> int:
    man_path = EXPORT / MANIFEST_NAME
    if not man_path.is_file():
        print("manifest missing; run build first", file=sys.stderr)
        return 1
    manifest = json.loads(man_path.read_text(encoding="utf-8"))
    errs = validate_schema(manifest, "manifest.schema.json")
    for feed in manifest.get("feeds") or []:
        path = REPO / feed["path"]
        if not path.is_file():
            errs.append(f"missing feed {feed['path']}")
            continue
        digest = sha256_file(path)
        if digest != feed["sha256"]:
            errs.append(f"hash mismatch {feed['id']}: {digest} != {feed['sha256']}")
    count = manifest.get("published_topic_count", 0)
    if not (25 <= count <= 40):
        errs.append(f"published_topic_count {count}")
    report = json.loads(REPORT.read_text(encoding="utf-8")) if REPORT.is_file() else {}
    if report.get("invalid_published", 1) != 0:
        errs.append("evidence contract reports invalid published topics")
    if errs:
        for err in errs:
            print(err, file=sys.stderr)
        return 1
    print("check ok")
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--check", action="store_true")
    args = p.parse_args(argv)
    if args.check:
        return check()
    build()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
