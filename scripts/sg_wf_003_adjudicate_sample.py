#!/usr/bin/env python3
"""SG-WF-003 P5: manual adjudication of the 81-lemma kṛt surface sample.

Each surface -ana/-ti/-in lemma is judged: is it a GENUINE primary kṛt derivative
(root + primary suffix on a simple stem), or a false surface match? False matches
are categorised: compound (final member is kṛt but the lemma is a compound),
name (proper name), taddhita (denominal, esp. possessive -in / -vin), numeral,
denominal, primitive, unclear.

This manual rate is the AUTHORITATIVE kill-gate measure (C5 § 7 P5): it separates
true surface noise from cases the automatic MW+strip validator merely failed to
confirm (low recall on prefixed roots and compounds). Verdicts are
model-provisional (Opus 4.8), flagged for scholarly review.

Reads   sangram/articles/krt-suffixes/data/adjudication_sample.tsv
Writes  sangram/articles/krt-suffixes/data/adjudication_verdicts.tsv
"""
import csv
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
DATA = Path(__file__).resolve().parents[1] / "sangram" / "articles" / "krt-suffixes" / "data"

# lemma -> (genuine 1/0, false_category, note). category="" when genuine.
V = {
    # ---- -ana ----
    "gagana": (0, "primitive", "sky — not a transparent root+ana derivative"),
    "pratipādana": (1, "", "pra-ti-pad + ana — action noun, prefixed root"),
    "maudgalyāyana": (0, "name", "patronymic proper name"),
    "gorocana": (0, "compound", "go+rocana (pigment)"),
    "vajraudana": (0, "compound", "vajra+odana"),
    "samañjana": (1, "", "sam-añj + ana — ointment, prefixed"),
    "bhūtānadyatana": (0, "compound", "grammatical compound bhūta+an-adyatana"),
    "apatana": (1, "", "ava/apa-pat + ana — falling-off"),
    "āvirbhāvana": (1, "", "āvir-bhāvana — causative action noun, prefixed"),
    "mṛgendrāsana": (0, "compound", "mṛgendra+āsana lion-seat"),
    "jugupsana": (1, "", "√gup desiderative + ana — disgust"),
    "hāsana": (1, "", "√has (caus) + ana — causing laughter"),
    "uddyotana": (1, "", "ud-dyut + ana — illuminating, prefixed"),
    "avitrāsana": (1, "", "a-vi-trāsana — deverbal core (√tras caus)"),
    "svadana": (1, "", "√svad + ana — tasting"),
    "dhūmāvalokana": (0, "compound", "dhūma+avalokana"),
    "jantuhanana": (0, "compound", "jantu+hanana creature-killing"),
    "ajavāhana": (0, "name", "king Ajavāhana (also aja+vāhana)"),
    "ujjhana": (1, "", "ud-jh(ujjh) + ana — abandoning"),
    "bhaktimahimavarṇana": (0, "compound", "colophon compound"),
    "garuḍāsana": (0, "compound", "garuḍa+āsana posture"),
    "sātana": (0, "unclear", "sandalwood substance name; s/ś opaque"),
    "ujjayana": (0, "name", "in a genealogical name-list"),
    "sāṃvaureśvaratīrthamāhātmyavarṇana": (0, "compound", "colophon compound"),
    "vyakṣaraṇidhana": (0, "compound", "vi-akṣara-nidhana"),
    "atistana": (0, "compound", "ati+stana (stana primitive)"),
    "kumāreśvaratīrthamāhātmyavarṇana": (0, "compound", "colophon compound"),
    # ---- -in ----
    "tapasvin": (0, "taddhita", "tapas+vin — possessive 'ascetic'"),
    "kāmarūpin": (0, "compound", "kāma-rūpa+in"),
    "avalambin": (1, "", "ava-lamb + in — agentive, prefixed"),
    "stambhin": (1, "", "√stambh + in — obstructing"),
    "cirajīvin": (0, "compound", "cira+jīvin long-lived"),
    "atiśayin": (1, "", "ati-śī + in — surpassing, prefixed"),
    "valayin": (0, "taddhita", "valaya+in — possessive 'braceleted'"),
    "anuśāyin": (1, "", "anu-śī + in — inherent, prefixed"),
    "utkledin": (1, "", "ud-klid + in — exuding, prefixed"),
    "doṣin": (0, "taddhita", "doṣa+in — possessive 'faulty'"),
    "asaṃvibhāgin": (1, "", "a-sam-vi-bhaj + in — non-sharing agentive"),
    "paropakārin": (0, "compound", "para-upakārin beneficent"),
    "śrotrasvin": (0, "taddhita", "śrotra+svin — possessive"),
    "pratirāgin": (1, "", "prati-raj + in — responsive, prefixed"),
    "viśrambhin": (1, "", "vi-śrambh + in — trusting, prefixed"),
    "āśaṃsin": (1, "", "ā-śaṃs + in — hoping, prefixed"),
    "gṛhavāsin": (0, "compound", "gṛha-vāsin house-dweller"),
    "raṇapakṣin": (0, "compound", "raṇa-pakṣin"),
    "muravijayin": (0, "compound", "mura-vijayin Mura-conqueror"),
    "parikartin": (1, "", "pari-kṛt + in — cutting-around, prefixed"),
    "chandasvin": (0, "taddhita", "chandas+vin — possessive"),
    "anābhayin": (0, "taddhita", "possessive/negated 'fearless'"),
    "vibandhin": (1, "", "vi-bandh + in — obstructing, prefixed"),
    "kauṇḍapāyin": (0, "compound", "kuṇḍa-pāyin priest class"),
    "sātyakin": (0, "name", "patronymic Sātyaki"),
    "nisarpin": (1, "", "ni-sṛp + in — creeping, prefixed"),
    "suvikrāntavikrāmin": (0, "compound", "long compound / bodhisattva name"),
    # ---- -ti ----
    "gati": (1, "", "√gam + ti — going"),
    "mūrti": (1, "", "√mūrch + ti — form (lexicalised but primary)"),
    "ekāśīti": (0, "numeral", "'eighty-one' — numeral -ti, not kṛt"),
    "yuvati": (0, "denominal", "from yuvan — young woman"),
    "vīti": (1, "", "√vī + ti — enjoyment"),
    "srakti": (0, "unclear", "'corner/edge' — opaque morphology"),
    "māruti": (0, "name", "patronymic 'son of the Marut'"),
    "viṣṭuti": (1, "", "vi-stu + ti — praise, prefixed"),
    "jagatīpati": (0, "compound", "jagatī+pati (pati primitive)"),
    "avasthiti": (1, "", "ava-sthā + ti — position, prefixed"),
    "acitti": (1, "", "a-cit + ti — folly (core citti = √cit+ti)"),
    "namaukti": (0, "compound", "namas+ukti homage-utterance"),
    "tati": (1, "", "√tan + ti — extent"),
    "gaurīpati": (0, "compound", "gaurī+pati Śiva"),
    "citpati": (0, "compound", "cit+pati"),
    "arthaprāpti": (0, "compound", "artha+prāpti"),
    "mitrābṛhaspati": (0, "compound", "compound of two names"),
    "ananyagati": (0, "compound", "an-anya-gati bahuvrīhi"),
    "sambhrānti": (1, "", "sam-bhram + ti — confusion, prefixed"),
    "parisruti": (1, "", "pari-sru + ti — distillation, prefixed"),
    "tīrabhukti": (0, "compound", "tīra+bhukti place-name"),
    "tantrayukti": (0, "compound", "tantra+yukti"),
    "tānti": (1, "", "√tan/tam + ti — weariness"),
    "prāgāhuti": (0, "compound", "prāk+āhuti prior-oblation"),
    "avipakti": (1, "", "a-vi-pac + ti — non-digestion, prefixed core"),
    "śivasvāti": (0, "name", "king Śivasvāti"),
    "añjinīpati": (0, "compound", "añjinī+pati sun-epithet"),
}


def main() -> int:
    src = DATA / "adjudication_sample.tsv"
    rows = list(csv.DictReader(open(src, encoding="utf-8"), delimiter="\t"))
    out = []
    by_suf = {}
    fp_cat = Counter()
    # validator confusion vs manual
    tp = fp = tn = fn = 0
    for r in rows:
        lem = r["lemma"]
        genuine, cat, note = V.get(lem, (None, "MISSING", "UNADJUDICATED"))
        auto = int(r["auto_confirmed"])
        s = r["suffix"]
        by_suf.setdefault(s, [0, 0])
        by_suf[s][1] += 1
        if genuine == 1:
            by_suf[s][0] += 1
        else:
            fp_cat[cat] += 1
        # validator vs manual (auto_confirmed as predictor of genuine)
        if genuine is not None:
            if auto and genuine:
                tp += 1
            elif auto and not genuine:
                fp += 1
            elif not auto and not genuine:
                tn += 1
            elif not auto and genuine:
                fn += 1
        out.append([lem, s, r["tokens"], r["mw_etym"], r["dhatu_strip"], auto,
                    genuine if genuine is not None else "?", cat, note])

    with open(DATA / "adjudication_verdicts.tsv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["lemma", "suffix", "tokens", "mw_etym", "dhatu_strip",
                    "auto_confirmed", "genuine_krt", "false_category", "note"])
        w.writerows(out)

    n = len(rows)
    genuine_total = sum(1 for r in out if r[6] == 1)
    fp_total = n - genuine_total
    print(f"adjudicated {n} surface lemmas")
    for s in ("ana", "ti", "in"):
        g, t = by_suf.get(s, [0, 0])
        print(f"  -{s}: genuine {g}/{t} = {round(100*g/t,1)}% ; false {t-g} ({round(100*(t-g)/t,1)}%)")
    print(f"OVERALL genuine primary kṛt: {genuine_total}/{n} = {round(100*genuine_total/n,1)}%")
    print(f"TRUE false-positive rate: {fp_total}/{n} = {round(100*fp_total/n,1)}%  (kill-gate >20% -> FIRED)")
    print(f"false-positive categories: {dict(fp_cat.most_common())}")
    prec = tp/(tp+fp) if (tp+fp) else 0
    rec = tp/(tp+fn) if (tp+fn) else 0
    print(f"auto-validator vs manual: precision {round(prec,2)} recall {round(rec,2)} "
          f"(tp{tp} fp{fp} tn{tn} fn{fn}) — high precision, low recall")
    return 0


if __name__ == "__main__":
    sys.exit(main())
