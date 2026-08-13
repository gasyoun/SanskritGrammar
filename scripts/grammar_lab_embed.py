#!/usr/bin/env python3
"""Pinned offline topic vectors for Grammar Lab (H2492).

Preferred backend: sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
(384-d). CI and developer machines without the model use a documented
deterministic character-ngram hash projection of the same dimensionality.
G2 must keep features.grammar_lab_semantic OFF until a real-model rebuild
sets semantic_ready true and Recall@5 passes.

Usage:
    python scripts/grammar_lab_embed.py
    python scripts/grammar_lab_embed.py --check
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

REPO = Path(__file__).resolve().parents[1]
EXPORT = REPO / "data" / "grammar_lab" / "export"
BUNDLE = EXPORT / "grammar_lab.json"
VECTORS = EXPORT / "topic_vectors.json"

INTENDED_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
INTENDED_REV = "e3a3b314ca4b9b401dd9253288192138aa43db59"
DIM = 384
ALGO = "charngram-hash-v1"


def _source_text(topic: dict) -> str:
    aliases = topic.get("aliases") or {}
    parts = [
        topic.get("title_ru") or "",
        topic.get("summary_ru") or "",
        " ".join(aliases.get("ru") or []),
        " ".join(aliases.get("deva") or []),
        " ".join(aliases.get("iast") or []),
        " ".join(aliases.get("slp1") or []),
    ]
    return " ".join(p for p in parts if p)


def _ngrams(text: str, n: int = 3) -> list[str]:
    folded = re.sub(r"\s+", " ", text.casefold()).strip()
    padded = f"  {folded}  "
    return [padded[i : i + n] for i in range(len(padded) - n + 1)]


def hash_project(text: str, dim: int = DIM) -> list[float]:
    vec = [0.0] * dim
    grams = _ngrams(text)
    if not grams:
        return vec
    for g in grams:
        digest = hashlib.sha256(f"{ALGO}:{g}".encode("utf-8")).digest()
        idx = int.from_bytes(digest[:2], "little") % dim
        sign = 1.0 if digest[2] % 2 == 0 else -1.0
        vec[idx] += sign
    norm = math.sqrt(sum(x * x for x in vec)) or 1.0
    return [round(x / norm, 8) for x in vec]


def try_st_encode(texts: list[str]) -> tuple[list[list[float]] | None, str]:
    """Opt-in only. Importing sentence-transformers can trigger a multi-hundred-MB
    download; CI and default G1 builds stay on the hash projection."""
    import os

    if os.environ.get("GRAMMAR_LAB_ST_MODEL") != "1":
        return None, "hash projection (set GRAMMAR_LAB_ST_MODEL=1 to use MiniLM)"
    try:
        from sentence_transformers import SentenceTransformer  # type: ignore
    except Exception as exc:  # pragma: no cover - optional extra
        return None, f"sentence-transformers unavailable: {exc}"
    try:
        model = SentenceTransformer(INTENDED_MODEL)
        raw = model.encode(texts, normalize_embeddings=True)
        out = [[round(float(x), 8) for x in row] for row in raw]
        return out, "ok"
    except Exception as exc:  # pragma: no cover
        return None, f"encode failed: {exc}"


def build_vectors(bundle: dict | None = None) -> dict:
    data = bundle or json.loads(BUNDLE.read_text(encoding="utf-8"))
    topics = data["topics"]
    texts = [_source_text(t) for t in topics]
    encoded, note = try_st_encode(texts)
    if encoded is None:
        encoded = [hash_project(t) for t in texts]
        backend = ALGO
        semantic_ready = False
        model_name = ALGO
        revision = "algorithmic"
    else:
        backend = "sentence-transformers"
        semantic_ready = True
        model_name = INTENDED_MODEL
        revision = INTENDED_REV
    payload = {
        "schema_version": "1.0.0",
        "model_name": model_name,
        "intended_sidecar_model": INTENDED_MODEL,
        "revision": revision,
        "dimensionality": DIM,
        "backend": backend,
        "semantic_ready": semantic_ready,
        "backend_note": note,
        "source_text_sha256": hashlib.sha256(
            "\n".join(texts).encode("utf-8")
        ).hexdigest(),
        "vectors": [
            {"id": topic["id"], "vector": vec}
            for topic, vec in zip(topics, encoded, strict=True)
        ],
    }
    return payload


def write_vectors(payload: dict) -> None:
    EXPORT.mkdir(parents=True, exist_ok=True)
    VECTORS.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def check_vectors() -> int:
    if not VECTORS.is_file():
        print("topic_vectors.json missing", file=sys.stderr)
        return 1
    data = json.loads(VECTORS.read_text(encoding="utf-8"))
    if data.get("dimensionality") != DIM:
        print("vector dimensionality mismatch", file=sys.stderr)
        return 1
    if not data.get("vectors"):
        print("no vectors", file=sys.stderr)
        return 1
    for item in data["vectors"]:
        if len(item["vector"]) != DIM:
            print(f"bad dim for {item['id']}", file=sys.stderr)
            return 1
    print(f"vectors ok: {len(data['vectors'])} x {DIM}; backend={data.get('backend')}")
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--check", action="store_true")
    args = p.parse_args(argv)
    if args.check:
        return check_vectors()
    if not BUNDLE.is_file():
        print("run build_grammar_lab.py first", file=sys.stderr)
        return 1
    payload = build_vectors()
    write_vectors(payload)
    print(
        f"wrote {VECTORS.relative_to(REPO)} "
        f"backend={payload['backend']} semantic_ready={payload['semantic_ready']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
