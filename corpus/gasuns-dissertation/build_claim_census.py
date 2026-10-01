#!/usr/bin/env python3
"""H4479 — dhātu-claim census over the extracted dissertation text.

Deterministic pattern census (scholars, root counts, novelty claims,
concordance hooks) with printed-page references. Feeds claim_census.md,
which maps each claim to the GasunsDhatu_2014 revision-2026 lane.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

HERE = Path(__file__).parent
TEXT = HERE / "text"

PATTERNS: dict[str, str] = {
    # scholar mentions (RU + Latin spellings)
    "palsule": r"Пальсуле|Palsule",
    "whitney": r"Уитни|Whitney",
    "panini": r"Панини|Pāṇini|Пан\.",
    "boehtlingk": r"Бётлингк|Бетлингк|Böhtlingk|Böhtl",
    "mayrhofer": r"Майрхофер|Mayrhofer|KEWA|EWA",
    "werba": r"Верба|Werba|VIA",
    "huet": r"Юэт|Huet",
    "bucknell": r"Бакнелл|Bucknell",
    "liebich": r"Либих|Liebich",
    "zaliznyak": r"Зализняк",
    "krylov": r"Крылов",
    # root-count claims ("N корней", numbers near 'корн-')
    "root_counts": r"\d[\d\u00a0 ]{1,5}\s+корн",
    "dhatu_term": r"dhātu|дхату|дхāту",
    "dhatupatha": r"dhātupāṭha|дхатупатха|Dhātupāṭha",
    # concordance / appendix hooks (PALSULE_AUDIT lane)
    "concordance": r"конкорданс|Конкорданс",
    "appendix3": r"Приложени[еия]\s*3",
    # novelty claims
    "novelty": r"впервые|новизн|не разработан|не был[ao] изучен",
    "morphophonemic": r"морфонологическ",
}


def load(stem: str) -> list[dict]:
    return [json.loads(l) for l in (TEXT / f"{stem}.jsonl").open(encoding="utf-8")]


def snippet(text: str, m: re.Match, width: int = 110) -> str:
    a, b = max(0, m.start() - width // 2), min(len(text), m.end() + width // 2)
    s = re.sub(r"\s+", " ", text[a:b]).strip()
    return ("…" if a else "") + s + ("…" if b < len(text) else "")


def census(stem: str, role: str) -> dict:
    pages = load(stem)
    out: dict = {"volume": stem, "role": role, "patterns": {}}
    for name, pat in PATTERNS.items():
        rx = re.compile(pat)
        hits, snippets = [], []
        for p in pages:
            for m in rx.finditer(p["text"]):
                hits.append(p["page"])
                if len(snippets) < 3:
                    snippets.append({"page": p["page"], "text": snippet(p["text"], m)})
        if hits:
            out["patterns"][name] = {
                "total": len(hits),
                "pages": sorted(set(hits)),
                "page_span": [min(hits), max(hits)],
                "samples": snippets,
            }
    return out


def main() -> None:
    vols = [
        ("02_gasuns-dhatu-PhD-text", "основной текст"),
        ("01_gasuns-dhatu-PhD-ref", "автореферат"),
        ("05_03-gasuns-dhatu-suppl", "Приложение 3 — конкорданс"),
        ("04_02-gasuns-dhatu-suppl", "Приложение 2 — корни по префиксам"),
        ("03_01-gasuns-dhatu-suppl", "Приложение 1 — Уитни/Бакнелл"),
        ("06_04-gasuns-dhatu-suppl", "Приложение 4 — Юэт"),
        ("07_05-gasuns-dhatu-suppl", "Приложение 5 — бинарное сопоставление"),
    ]
    result = {"handoff": "H4479", "volumes": [census(s, r) for s, r in vols]}
    out = HERE / "claim_census.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for v in result["volumes"]:
        tops = sorted(v["patterns"].items(), key=lambda kv: -kv[1]["total"])[:5]
        tops_s = ", ".join(f"{k}={n['total']}" for k, n in tops)
        print(f"{v['volume']}: {tops_s}")


if __name__ == "__main__":
    main()
