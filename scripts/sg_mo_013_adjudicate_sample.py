#!/usr/bin/env python3
"""SG-MO-013 P2 kill-gate: manual adjudication of the seeded validation sample.

For each CHECK token (tier MULTI or UNJOINED — the inventory join did not yield a
single gaṇa) the adjudicator asks: does the SURFACE FORM (athematic stem-marker,
guṇa grade, or -ya-) resolve the present class? This separates
  - inventory-only recoverability (SINGLE + AYA tiers, no analysis), from
  - morphological recoverability (adds the form-resolved tokens), from
  - the irreducible residue (plain-thematic I/VI with no grade cue; -ya- masked
    by the passive; corrupt/Vedic forms).

Adjudicator: Opus 4.8 (claude-opus-4-8[1m]), 15-07-2026; each verdict cites the
resolving marker. Scholarly responsibility for the final calls rests with the
author (candidate article, pre-visa)."""
import csv
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
DATA = Path(__file__).resolve().parents[1] / "sangram" / "articles" / "thematic-present" / "data"

# token_id -> (verdict, resolved_gana, resolving_marker)
# verdict: form-resolved | secondary | ambiguous
CHECK = {
    "5272006": ("form-resolved", "IX", "utpunāmy: -nā- (punā-) class-IX infix"),
    "1488200": ("form-resolved", "VII", "niyunakti: nasal infix yu-na-k class VII"),
    "1778777": ("form-resolved", "IV", "trāyasva: -ya- (trāya-) class IV"),
    "3148319": ("form-resolved", "V", "prāpnotu: -no- (āp-no-) class V (unjoined preverb pra+āp)"),
    "206666": ("form-resolved", "II", "vidyāma: athematic optative of vid (vetti) class II"),
    "4734048": ("ambiguous", "?", "pṛcchyatām: voice=Pass — -ya- masked by the passive (IV/passive collision)"),
    "1168685": ("form-resolved", "IX", "gṛhāṇa: -āṇa (gṛh-ṇā-) class-IX imperative (unjoined)"),
    "1701120": ("form-resolved", "II", "syāt: athematic optative s-yāt of as class II"),
    "5303780": ("form-resolved", "I", "anupraharati: guṇa har-a class I (hṛ)"),
    "5516182": ("ambiguous", "?", "niraṇyatho: corrupt/Vedic, suspect lemma 'niran'; I/IV residual"),
    "5317658": ("form-resolved", "VIII", "karoti: -o- (kar-o-) class VIII kṛ"),
    "2021198": ("form-resolved", "VI", "saṃspṛśet: weak-grade thematic spṛś-a class VI (unjoined preverb)"),
    "2436228": ("form-resolved", "II", "bravīmi: athematic bravī-mi of brū class II"),
    "3049958": ("form-resolved", "I", "yajase: thematic yaj-a (a-root default) class I"),
    "3747620": ("form-resolved", "II", "vinyaset: optative of (vi-ni-)as class II (unjoined)"),
    "5593217": ("form-resolved", "I", "tiradhvam: thematic tir-a of tṛ class I"),
    "2557235": ("form-resolved", "VIII", "kuru: -u- (kur-u) class VIII kṛ imperative"),
    "1375447": ("form-resolved", "IX", "jāne: -nā- (jā-nā-) class IX jñā"),
    "395551": ("form-resolved", "II", "'si: asi, athematic class II as"),
    "5681637": ("form-resolved", "V", "śṛṇoti: -ṇo- (śṛ-ṇo-) class V śru"),
    "1759726": ("form-resolved", "I", "yaja: thematic yaj-a class I"),
    "5071806": ("form-resolved", "I", "vahet: thematic vah-a (a-root) class I"),
    "3706550": ("form-resolved", "IV", "śudhyati: -ya- (śudh-ya-) class IV"),
    "635053": ("form-resolved", "I", "vivartante: guṇa vart-a class I vṛt"),
    "4074666": ("form-resolved", "II", "hanyāṃ: athematic optative of han (hanti) class II"),
    "3328938": ("form-resolved", "I", "nirvaped: thematic vap-a class I (unjoined preverb nir+vap)"),
    "1203405": ("form-resolved", "IV", "anuprajāyante: -jā-ya- class IV jan (jāyate)"),
    "2426004": ("form-resolved", "VIII", "kuru: -u- class VIII kṛ"),
    "4664609": ("form-resolved", "II", "asi: athematic class II as"),
    "5186918": ("form-resolved", "III", "juhoti: reduplicated ju-ho class III hu"),
    "4813063": ("form-resolved", "IV", "prajāyata: -jā-ya- class IV jan"),
    "2093564": ("secondary", "desid", "bubhūṣate: reduplication + -ṣa- desiderative (secondary conjugation)"),
    "729042": ("form-resolved", "II", "asti: athematic class II as"),
    "3328900": ("form-resolved", "IV", "jāyate: -jā-ya- class IV jan"),
    "3188570": ("form-resolved", "VI", "icchāmi: weak-grade ich-a (no guṇa) class VI iṣ"),
    "4701601": ("form-resolved", "IX", "gṛhṇāti: -ṇā- class IX grah (unjoined)"),
    "4779710": ("form-resolved", "VIII", "kuryāt: -u- (kur-yāt) class VIII kṛ optative"),
    "3306758": ("form-resolved", "IX", "pratigṛhṇāti: -ṇā- class IX grah (unjoined preverb prati)"),
    "5262895": ("form-resolved", "IV", "utpadyate: -pad-ya- class IV pad (unjoined preverb ut)"),
    "4600384": ("form-resolved", "II", "nireti: guṇa e-ti of i class II (unjoined preverb nis)"),
    "592997": ("form-resolved", "II", "'si: asi, athematic class II as"),
}


def main() -> int:
    rows = list(csv.DictReader(open(DATA / "validation_sample.tsv", encoding="utf-8"),
                               delimiter="\t"))
    out = []
    inv_clean = form_res = secondary = ambiguous = 0
    for r in rows:
        tid = r["token_id"]
        if r["auto_verdict"] == "clean":
            verdict, rg, ev = "inventory-clean", r["whitney_gana"] or r["tier"], r["tier"]
            inv_clean += 1
        else:
            verdict, rg, ev = CHECK.get(tid, ("ambiguous", "?", "unadjudicated"))
            if verdict == "form-resolved":
                form_res += 1
            elif verdict == "secondary":
                secondary += 1
            else:
                ambiguous += 1
        out.append({
            "token_id": tid, "form": r["form"], "lemma": r["lemma"], "tier": r["tier"],
            "whitney_gana": r["whitney_gana"], "verdict": verdict,
            "resolved_gana": rg, "evidence": ev,
        })
    with open(DATA / "validation_verdicts.tsv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys()), delimiter="\t")
        w.writeheader()
        w.writerows(out)
    n = len(out)
    morph = inv_clean + form_res + secondary
    print(f"n={n}")
    print(f"inventory-clean (SINGLE+AYA):     {inv_clean}/{n} = {100*inv_clean/n:.1f}%")
    print(f"+ form-resolved / secondary:      {form_res}+{secondary}")
    print(f"morphologically recoverable:      {morph}/{n} = {100*morph/n:.1f}%")
    print(f"irreducibly ambiguous:            {ambiguous}/{n} = {100*ambiguous/n:.1f}%")
    print("ambiguous:", ", ".join(o['form'] for o in out if o['verdict'] == 'ambiguous'))
    return 0


if __name__ == "__main__":
    sys.exit(main())
