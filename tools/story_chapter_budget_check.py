"""Natural-method story — per-chapter budget + verse-ID check (H3493 acceptance gate).

For every CHAPTER_*.md under docs/NATURAL_METHOD_STORY_START_CHTENIYA/:
  * count rows of the «New vocabulary» table by band (L1/L2/L3/glue/функц./имя)
  * check total <= cap and glue share of content <= 30 % (caps from the budget doc)
  * resolve every `subh_NNNN` / `bhg_C_V` id the chapter cites against
      - kosha data/subhashita/subhashita_beginner_pack.json  (sayings[].num)
      - SanskritKaraoke verses/data/<id>.json
  * count † sandhi events (informational)

Exit 1 on any FAIL. Run from anywhere; sibling repos are resolved next to this clone
(falls back to ../<repo> and to the canonical GitHub/ dir).
"""
import io
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve()
REPO = HERE.parents[1]
DOCS = REPO / "docs" / "NATURAL_METHOD_STORY_START_CHTENIYA"
CAP_TOTAL = {1: 40, 2: 20, 3: 20, 4: 15, 5: 15}
GLUE_MAX_PCT = 30.0
BANDS = ("L1", "L2", "L3", "glue", "функц.", "имя")


def sibling(name):
    for base in (REPO.parent, Path("C:/Users/user/Documents/GitHub")):
        p = base / name
        if p.is_dir():
            return p
    return None


def load_pack_nums():
    k = sibling("kosha")
    if not k:
        return None
    p = k / "data" / "subhashita" / "subhashita_beginner_pack.json"
    if not p.is_file():
        return None
    d = json.loads(io.open(p, encoding="utf-8").read())
    return {int(s["num"]) for s in d["sayings"]}


def karaoke_dir():
    k = sibling("SanskritKaraoke")
    return (k / "verses" / "data") if k else None


def vocab_rows(text):
    m = re.search(r"## New vocabulary.*?\n(\|.*?)\n\n", text, re.S)
    if not m:
        return []
    rows = []
    for line in m.group(1).splitlines()[2:]:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 3:
            rows.append(cells)
    return rows


def main():
    pack = load_pack_nums()
    kdir = karaoke_dir()
    fails = 0
    print("| Ch. | total | L1 | L2 | L3 | glue | функц. | имя | glue % | cap | verse ids | † |")
    print("|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---:|")
    for f in sorted(DOCS.glob("CHAPTER_*.md")):
        ch = int(re.match(r"CHAPTER_(\d+)_", f.name).group(1))
        text = io.open(f, encoding="utf-8").read()
        rows = vocab_rows(text)
        counts = {b: 0 for b in BANDS}
        for cells in rows:
            band = cells[2]
            band = "имя" if band.startswith("имя") else band
            if band not in counts:
                counts.setdefault(band, 0)
            counts[band] += 1
        total = len(rows)
        content = counts["L1"] + counts["L2"] + counts["L3"] + counts["glue"]
        glue_pct = 100.0 * counts["glue"] / content if content else 0.0
        cap = CAP_TOTAL.get(ch, 99)
        ok = total <= cap and (ch < 4 or glue_pct <= GLUE_MAX_PCT)
        ids = sorted(set(re.findall(r"`(subh_\d+|bhg_\d+_\d+)`", text)))
        id_status = []
        for vid in ids:
            resolved = False
            if kdir and (kdir / f"{vid}.json").is_file():
                resolved = True
            if vid.startswith("subh_") and pack is not None and int(vid[5:]) in pack:
                resolved = True
            id_status.append(("✓" if resolved else "✗") + vid)
            if not resolved:
                ok = False
        dagger = text.count("**†**")
        if not ok:
            fails += 1
        print(f"| {ch} | {total} | {counts['L1']} | {counts['L2']} | {counts['L3']} | {counts['glue']} | "
              f"{counts['функц.']} | {counts['имя']} | {glue_pct:.0f} % | {'✅' if ok else '❌'} ≤ {cap} | "
              f"{' '.join(id_status) or '—'} | {dagger} |")
    if pack is None:
        print("WARN: kosha pack not found — subh_ ids resolved via Karaoke only")
    if kdir is None:
        print("WARN: SanskritKaraoke not found — bhg_ ids cannot resolve")
    print("RESULT:", "PASS" if fails == 0 else f"FAIL ({fails} chapter(s))")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
