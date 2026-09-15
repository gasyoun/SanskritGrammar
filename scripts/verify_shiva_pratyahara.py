#!/usr/bin/env python3
"""H4716 — verify the vendored Shiva Sutra pratyāhāra reference table (data/shiva_sutras/).

Deterministic, offline, stdlib-only. Exit 0 = all checks PASS, 1 = FAIL list non-empty.

Conventions (kosha shiva-sutras-machine, H4471): the master sequence carries each sūtra's
anubandha/it-marker as consonant+virāma (so the string is 71 code points = 57 tokens:
43 phonemes + 14 markers); `letters_only` strips markers; two sūtras legitimately share
the it-marker ण् (nos. 1 and 6), which is why the table names aN1/aN2.

Checks:
  C1  14 sūtras numbered 1..14, each devanagari ends with its terminal it-marker.
  C2  Master sequence round-trip: concatenating the 14 sūtra strings (markers included)
      == JSON master_sequence == TSV concatenation; token census 43 phonemes + 14 markers.
  C3  All 42 named pratyāhāra spans round-trip against the master sequence:
      span is a contiguous substring of master; it-marker (if any) terminates the span;
      stripping all 14 marker substrings from the span reproduces letters_only;
      first char of span == first char of letters_only; length == token census of the span
      (a consonant+virāma anubandha counts as ONE token, i.e. len(span) - virāma count).
  C4  All 14 it-markers are consumed by >= 1 named pratyāhāra (every sūtra round-trips
      through the pratyāhāra table).
  C5  Classic-semantics canaries (own-data control, hardcoded): aC = the 9 vowels;
      haL = 34 consonants, vowel-free; iK = इ उ ऋ ऌ; eC = ए ओ ऐ औ;
      aC ⊎ haL == the 43-phoneme multiset.
"""
from __future__ import annotations

import csv
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent / "data" / "shiva_sutras"

VOWELS = set("अइउऋऌएओऐऔ")

EXPECTED_CANARY = {
    "aC": "अइउऋऌएओऐऔ",
    "iK": "इउऋऌ",
    "uK": "उऋऌ",
    "eC": "एओऐऔ",
    "aiC": "ऐऔ",
    "haL": "हयवरलञमङणनझभघढधजबगडदखफछठथचटतकपशषसह",
}


def load_tsv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def main() -> int:
    fails: list[str] = []

    sutras = load_tsv(HERE / "sutras.tsv")
    pras = load_tsv(HERE / "pratyaharas.tsv")
    blob = json.loads((HERE / "shiva_sutras.json").read_text(encoding="utf-8"))
    master: str = blob["master_sequence"]
    markers = [r["it_marker"] for r in sutras]

    def strip_markers(s: str) -> str:
        for m in markers:
            s = s.replace(m, "")
        return s

    # C1
    if [int(r["sutra_number"]) for r in sutras] != list(range(1, 15)):
        fails.append(f"C1 sūtra numbering broken: {[r['sutra_number'] for r in sutras]}")
    for r in sutras:
        if not r["it_marker"] or not r["devanagari"].endswith(r["it_marker"]):
            fails.append(f"C1 sūtra {r['sutra_number']}: it_marker not terminal "
                         f"({r['it_marker']!r} vs {r['devanagari']!r})")

    # C2 — 14-sūtra round-trip of the master sequence
    for label, concat in (
        ("TSV", "".join(r["devanagari"] for r in sutras)),
        ("JSON", "".join(r["devanagari"] for r in blob["sutras"])),
    ):
        if concat != master:
            fails.append(f"C2 {label} sūtra concatenation != master_sequence")
    phonemes = sum(len(r["letters_only"]) for r in sutras)
    if (len(master), phonemes, len(markers)) != (71, 43, 14):
        fails.append(f"C2 census wrong: {len(master)} code points / {phonemes} phonemes / "
                     f"{len(markers)} markers (expected 71 / 43 / 14 = 57 tokens)")
    stripped = strip_markers(master)
    if stripped != "".join(r["letters_only"] for r in sutras):
        fails.append("C2 marker-stripped master != concatenated letters_only")
    if not stripped or strip_markers(master) != stripped:
        fails.append("C2 strip_markers not idempotent")

    # C3 — every named pratyāhāra round-trips against the master sequence
    for r in pras:
        name, letters, marker, span, length = (
            r["name"], r["letters_only"], r["it_marker"], r["devanagari_span"], int(r["length"]),
        )
        if span not in master:
            fails.append(f"C3 {name}: span {span!r} not contiguous in master sequence")
            continue
        if marker:
            if not span.endswith(marker):
                fails.append(f"C3 {name}: span does not end with it-marker {marker!r}")
            if master.rfind(marker) < master.index(span):
                fails.append(f"C3 {name}: it-marker {marker!r} does not occur at/after span start")
        if strip_markers(span) != letters:
            fails.append(f"C3 {name}: marker-stripped span {strip_markers(span)!r} != "
                         f"stored letters_only {letters!r}")
        if not letters or span[0] != letters[0]:
            fails.append(f"C3 {name}: first letter mismatch")
        tokens = len(span) - span.count("\u094d")  # consonant+virāma marker folds into 1 token
        if tokens != length:
            fails.append(f"C3 {name}: length {length} != token census {tokens}")

    # C4 — every sūtra's it-marker consumed by >= 1 pratyāhāra
    used = {r["it_marker"] for r in pras}
    for r in sutras:
        if r["it_marker"] not in used:
            fails.append(f"C4 it-marker {r['it_marker']!r} (sūtra {r['sutra_number']}) "
                         f"consumed by no pratyāhāra")

    # C5 — classic canaries
    by_name = {r["name"]: r["letters_only"] for r in pras}
    for nm, expected in EXPECTED_CANARY.items():
        got = by_name.get(nm)
        if got != expected:
            fails.append(f"C5 canary {nm}: {got!r} != expected {expected!r}")
    if set(by_name.get("aC", "")) != VOWELS:
        fails.append("C5 aC is not exactly the vowel set")
    if VOWELS & set(by_name.get("haL", "")):
        fails.append("C5 haL contains vowels")
    if Counter(by_name.get("aC", "")) + Counter(by_name.get("haL", "")) != Counter(stripped):
        fails.append("C5 aC ⊎ haL != 43-phoneme multiset")

    print(f"shiva_sutras: {len(sutras)} sutras, {len(pras)} pratyaharas, "
          f"master={len(master)} code points (57 tokens)")
    if fails:
        print("FAIL:")
        for f_ in fails:
            print(f"  - {f_}")
        return 1
    print("PASS: C1 sūtras well-formed · C2 14-sūtra master round-trip (43+14=57 tokens) · "
          "C3 42/42 pratyāhāra round-trip · C4 all 14 it-markers consumed · C5 classic canaries")
    return 0


if __name__ == "__main__":
    sys.exit(main())
