#!/usr/bin/env python3
"""H7248 — freeze a deterministic DCS CoNLL-U evaluation sample.

Downloads one chapter file per selected DCS text from the pinned release commit
(OliverHellwig/sanskrit @ 8aeed5a1, CC BY 4.0), parses CoNLL-U, filters usable
sentences, and freezes a stratified sample plus a manifest carrying every sha256
needed to re-derive the numbers in the H7248 report offline.

Determinism: candidate and sample order are both derived from sha256(seed|text|
file|sentence-index). Re-running the script against the same pinned commit with
the same seed reproduces byte-identical outputs.

Usage:
    python scripts/h7248_freeze_dcs_sample.py            # build/refresh sample
    python scripts/h7248_freeze_dcs_sample.py --check     # verify committed bytes
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

DCS_REPO = "OliverHellwig/sanskrit"
DCS_PIN = "8aeed5a1343d0e48b64eb32af8c00e8c6eb29359"  # master HEAD, 2026-08-24
DCS_PIN_DATE = "2026-08-24T18:22:25Z"
DCS_ROUTE = "dcs/data/conllu/files"
RAW = "https://raw.githubusercontent.com/{repo}/{sha}/{route}/{text}/{name}"

SEED = "h7248-dcs-freeze-2026-10-24"
MAX_SENTENCES = 1000
MAX_TOKENS = 20000
MIN_TOKENS = 4
MIN_FEATS_SHARE = 0.5

STRATA = {
    "vedic": ["\u1e5agveda", "Atharvaveda (\u015aaunaka)", "\u015aatapathabr\u0101hma\u1e47a"],
    "epic": ["Mah\u0101bh\u0101rata", "R\u0101m\u0101ya\u1e47a", "Hariva\u1e43\u015ba"],
    "classical": ["Kum\u0101rasa\u1e43bhava", "Meghad\u016bta", "Hitopade\u015ba"],
    "shastra": [
        "A\u1e63\u1e6d\u0101\u1e45gah\u1e5bdayasa\u1e43hit\u0101",
        "Ny\u0101yabh\u0101\u1e63ya",
        "Artha\u015b\u0101stra",
    ],
}

OUT_DIR = Path(__file__).resolve().parent.parent / "data" / "h7248"
MANIFEST = OUT_DIR / "manifest.json"
GOLD = OUT_DIR / "gold_sample.jsonl"


def _get(url: str, timeout: int = 60) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "h7248-freeze"})
    return urllib.request.urlopen(req, timeout=timeout).read()


_TREE_CACHE: dict[str, list[tuple[int, str]]] = {}


def dcs_tree() -> dict[str, list[str]]:
    """text folder -> sorted chapter files, from one recursive git-tree call."""
    if not _TREE_CACHE:
        url = (
            f"https://api.github.com/repos/{DCS_REPO}/git/trees/{DCS_PIN}?recursive=1"
        )
        tree = json.loads(_get(url, timeout=120))["tree"]
        prefix = DCS_ROUTE + "/"
        for node in tree:
            path = node["path"]
            if not path.startswith(prefix) or node["type"] != "blob":
                continue
            rest = path[len(prefix):].split("/")
            if len(rest) != 2:
                continue
            _TREE_CACHE.setdefault(rest[0], []).append((node.get("size", 0), rest[1]))
        for key in _TREE_CACHE:
            # largest chapter first: small chapters starve a stratum's pool
            _TREE_CACHE[key].sort(key=lambda t: (-t[0], t[1]))
    return _TREE_CACHE


def list_chapters(text: str) -> list[tuple[int, str]]:
    names = dcs_tree().get(text) or []
    if not names:
        raise SystemExit(f"no chapter files for {text!r}")
    return names


def parse_conllu(payload: bytes) -> list[dict]:
    """CoNLL-U -> list of sentences with {form, lemma, upos, xpos, feats}."""
    sent: list[dict] = []
    out: list[dict] = []
    for raw in payload.decode("utf-8").splitlines():
        line = raw.rstrip("\n")
        if not line.strip():
            if sent:
                out.append({"tokens": sent})
                sent = []
            continue
        if line.startswith("#"):
            continue
        cols = line.split("\t")
        if len(cols) < 6:
            continue
        tid = cols[0]
        if "-" in tid or "." in tid:  # multiword tokens / empty nodes
            continue
        sent.append(
            {
                "form": cols[1],
                "lemma": cols[2],
                "upos": cols[3],
                "xpos": cols[4],
                "feats": cols[5],
            }
        )
    if sent:
        out.append({"tokens": sent})
    return out


def usable(tokens: list[dict]) -> bool:
    if len(tokens) < MIN_TOKENS:
        return False
    with_feats = sum(1 for t in tokens if t["feats"] not in ("_", ""))
    return with_feats / len(tokens) >= MIN_FEATS_SHARE


def h(*parts) -> str:
    return hashlib.sha256("|".join(str(p) for p in parts).encode("utf-8")).hexdigest()


def build() -> tuple[dict, str]:
    provenance = {
        "corpus": "Digital Corpus of Sanskrit (DCS), CoNLL-U dump",
        "repo": f"https://github.com/{DCS_REPO}",
        "route": DCS_ROUTE,
        "commit": DCS_PIN,
        "commit_date": DCS_PIN_DATE,
        "license": "CC BY 4.0",
        "citation": "Hellwig, Oliver (2010-2024). The Digital Corpus of Sanskrit (DCS).",
    }

    per_stratum: dict[str, list[dict]] = {}
    texts_meta: list[dict] = []

    for stratum, texts in STRATA.items():
        pool: list[dict] = []
        for text in texts:
            names = list_chapters(text)
            chapter = names[0][1]  # largest chapter file, deterministic
            url = RAW.format(
                repo=DCS_REPO, sha=DCS_PIN, route=DCS_ROUTE,
                text=urllib.parse.quote(text), name=urllib.parse.quote(chapter),
            )
            payload = _get(url)
            sents = parse_conllu(payload)
            kept = 0
            for idx, s in enumerate(sents):
                toks = s["tokens"]
                if not usable(toks):
                    continue
                kept += 1
                pool.append(
                    {
                        "id": h(SEED, text, chapter, idx)[:20],
                        "text": text,
                        "chapter": chapter,
                        "sent_index": idx,
                        "tokens": toks,
                    }
                )
            texts_meta.append(
                {
                    "text": text,
                    "stratum": stratum,
                    "chapter_file": chapter,
                    "chapter_url": url,
                    "chapter_sha256": hashlib.sha256(payload).hexdigest(),
                    "sentences_in_file": len(sents),
                    "sentences_usable": kept,
                    "chapter_bytes": len(payload),
                }
            )
            print(f"  {stratum:9s} {text}: {len(sents)} sents, {kept} usable", file=sys.stderr)
        if not pool:
            raise SystemExit(f"empty pool for stratum {stratum}")
        pool.sort(key=lambda s: s["id"])
        per_stratum[stratum] = pool

    # Per-stratum quota, filled from each pool's hash order, then leftover
    # redistributed to strata that still have candidates.
    order = list(STRATA.keys())
    quota = MAX_SENTENCES // len(order)
    picked: list[dict] = []
    for stratum in order:
        for cand in per_stratum[stratum][:quota]:
            picked.append({"stratum": stratum, **cand})
    used = {s: min(quota, len(per_stratum[s])) for s in order}
    short = sum(quota - used[s] for s in order)
    if short:
        for stratum in order:
            take = per_stratum[stratum][used[stratum]:]
            for cand in take:
                if short <= 0:
                    break
                picked.append({"stratum": stratum, **cand})
                short -= 1
    picked.sort(key=lambda x: x["id"])

    bound_by = "tokens"
    capped: list[dict] = []
    total_tokens = 0
    for s in picked:
        n = len(s["tokens"])
        if total_tokens + n > MAX_TOKENS:
            bound_by = "tokens"
            continue
        capped.append(s)
        total_tokens += n
    picked = capped
    if len(picked) >= MAX_SENTENCES:
        bound_by = "sentences"
        total_tokens = sum(len(s["tokens"]) for s in picked[:MAX_SENTENCES])
        picked = picked[:MAX_SENTENCES]

    counts: dict[str, int] = {}
    tokens_by: dict[str, int] = {}
    for s in picked:
        counts[s["stratum"]] = counts.get(s["stratum"], 0) + 1
        tokens_by[s["stratum"]] = tokens_by.get(s["stratum"], 0) + len(s["tokens"])

    gold_lines = []
    for s in picked:
        for i, t in enumerate(s["tokens"]):
            gold_lines.append(
                json.dumps(
                    {
                        "sent": s["id"],
                        "i": i,
                        "form": t["form"],
                        "lemma": t["lemma"],
                        "upos": t["upos"],
                        "xpos": t["xpos"],
                        "feats": t["feats"],
                    },
                    ensure_ascii=False,
                )
            )

    gold_text = "\n".join(gold_lines) + "\n"
    gold_sha = hashlib.sha256(gold_text.encode("utf-8")).hexdigest()

    manifest = {
        "handoff": "H7248",
        "seed": SEED,
        "sampling_rule": (
            "per stratum: candidate sentences hashed as sha256(seed|text|chapter|sent_index); "
            "pool sorted by that digest; round-robin across strata in STRATA declaration order; "
            "stop at MAX_SENTENCES or MAX_TOKENS, whichever binds first"
        ),
        "filters": {"min_tokens": MIN_TOKENS, "min_feats_share": MIN_FEATS_SHARE},
        "caps": {"max_sentences": MAX_SENTENCES, "max_tokens": MAX_TOKENS, "bound_by": bound_by},
        "strata": list(STRATA.keys()),
        "texts": texts_meta,
        "counts": {
            "sentences": len(picked),
            "tokens": total_tokens,
            "by_stratum": {
                s: {"sentences": counts.get(s, 0), "tokens": tokens_by.get(s, 0)} for s in order
            },
        },
        "sentences": [
            {
                "id": s["id"],
                "stratum": s["stratum"],
                "text": s["text"],
                "chapter_file": s["chapter"],
                "sent_index": s["sent_index"],
                "tokens": len(s["tokens"]),
            }
            for s in picked
        ],
        "gold_sample": {
            "path": "data/h7248/gold_sample.jsonl",
            "sha256": gold_sha,
            "rows": len(gold_lines),
        },
    }
    body = json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    manifest_sha = hashlib.sha256(body.encode("utf-8")).hexdigest()
    manifest["provenance"] = provenance
    # hash covers the content without itself
    out = body.rstrip("\n")
    out = out[:-1] + ',\n  "manifest_sha256": "%s"\n}\n' % manifest_sha
    return json.loads(out), gold_text


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    if args.check:
        if not MANIFEST.exists() or not GOLD.exists():
            print("FAIL: sample artifacts missing", file=sys.stderr)
            return 1
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        actual = hashlib.sha256(GOLD.read_bytes()).hexdigest()
        ok = actual == manifest["gold_sample"]["sha256"]
        print(f"gold_sample sha256 {'MATCH' if ok else 'MISMATCH'} {actual}")
        return 0 if ok else 1

    manifest, gold_text = build()
    GOLD.write_text(gold_text, encoding="utf-8", newline="\n")
    MANIFEST.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        json.dumps(
            {
                "sentences": manifest["counts"]["sentences"],
                "tokens": manifest["counts"]["tokens"],
                "bound_by": manifest["caps"]["bound_by"],
                "gold_sha256": manifest["gold_sample"]["sha256"],
                "manifest_sha256": manifest["manifest_sha256"],
                "by_stratum": manifest["counts"]["by_stratum"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
