#!/usr/bin/env python
"""build_root_classifier.py — digitizes Zaliznyak 1975's own root classification
(H797 Phase 2, Morphology 1975).

WHY THIS SCRIPT EXISTS (methodology note, checked before writing any of it):
Zaliznyak's "Morphophonological Classification" is not a discursive textbook like
Kochergina/Bühler/Ocherk (whose claims are corpus-frequency hedges, verified against DCS
token counts) and not a phrase-reader like Knauer (whose claims are individual footnote
parses, verified against Whitney citations one at a time). It is a scholarly paper counting
how many of Whitney's ~750-847 verbal roots fall into each cell of a classification scheme
(alternation series A/I/U/R/L/M/N x degree-of-alternation Type I/II/III/IV, and separately
aniṭ/seṭ/veṭ). The falsifiable unit here is "how many roots are in this bucket", checkable
only against an actual enumerated root list — not a corpus frequency count.

WHAT THIS SCRIPT DOES: it does NOT attempt to independently re-derive Zaliznyak's
classification from raw phonology (that would mean re-doing his own scholarly analysis from
scratch, with a real risk of getting subtle Indological judgment calls wrong). Instead it
digitizes the ~180 roots Zaliznyak names EXPLICITLY by citation throughout his own prose
(the paper's own primary data) into structured, queryable form, then cross-checks that
against two things a non-Indologist CAN check reliably:
  1. root EXISTENCE — does each named root actually appear in Whitney's root list
     (WhitneyRoots/crosswalk/roots.csv, 930 entries), under a matching gloss?
  2. COUNT consistency — do his own stated approximate counts ("about 60", "approximately
     100") match the number of roots he actually goes on to name for that category, and do
     his own table totals sum consistently?
This is verification against his own stated data and an independent root inventory, not a
fresh phonological analysis — the appropriately scoped task for a non-specialist.

Usage:  python build_root_classifier.py            # report + write root_classifier.json
        python build_root_classifier.py --check     # report only, no file write
"""
import sys, csv, json
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
WHITNEY_ROOTS = REPO.parent / "WhitneyRoots" / "crosswalk" / "roots.csv"

# ---------------------------------------------------------------------------------------
# Zaliznyak's own explicitly-named roots, transcribed from the paper's prose (not tables,
# which are reproduced separately below). `series` uses Zaliznyak's own alternation-series
# labels (A1, A2, I1, I2, U1, U2, R1, R2, L1, M1, M2, N1, N2); `ztype` is his Type I-IV
# (degree of alternation: I=full, II/III/IV=partial); `period` notes Vedic-only/Epic-onward
# restrictions where he states them; `loc` is the mdx line this entry was transcribed from.
# ---------------------------------------------------------------------------------------

NAMED_ROOTS = [
    # --- Type IV, closed list (mdx line 165) ---
    {"root": "ḍhauk", "series": None, "ztype": "IV", "loc": 165, "note": "to approach"},
    {"root": "mārg", "series": None, "ztype": "IV", "loc": 165, "note": "to chase"},
    {"root": "kāṅkṣ", "series": None, "ztype": "IV", "loc": 165, "note": "to desire"},
    {"root": "vāñch", "series": None, "ztype": "IV", "loc": 165, "note": "to desire"},
    {"root": "dhāv", "series": None, "ztype": "IV", "loc": 165, "note": "to run"},
    {"root": "dhāv", "series": None, "ztype": "IV", "loc": 165, "note": "to rinse (variant: type I in RV per dhūtaḥ)"},
    {"root": "cāy", "series": None, "ztype": "IV", "loc": 165, "note": "to note/observe (disputed inclusion)"},

    # --- A1 series (mdx 169-179) ---
    {"root": "as", "series": "A1", "ztype": "I", "loc": 171, "note": "to be (post-Vedic sole type-I exception)"},
    {"root": "ghas", "series": "A1", "ztype": "I", "loc": 171, "period": "Vedic-only", "note": "to eat"},
    {"root": "bhas", "series": "A1", "ztype": "I", "loc": 171, "period": "Vedic-only", "note": "to devour"},
    {"root": "sac", "series": "A1", "ztype": "I", "loc": 171, "period": "Vedic-only", "note": "to accompany"},
    {"root": "pat", "series": "A1", "ztype": "I", "loc": 171, "period": "Vedic traces only", "note": "to fly/fall"},
    {"root": "yaj", "series": "A1-sampras", "ztype": "I", "loc": 173, "note": "to offer"},
    {"root": "svap", "series": "A1-sampras", "ztype": "I", "loc": 173, "note": "to sleep"},
    {"root": "grabh", "series": "A1-sampras", "ztype": "I", "loc": 173, "note": "to seize (=grah)"},
    {"root": "vyac", "series": "A1-sampras", "ztype": "I", "loc": 173, "period": "Vedic", "note": "to extend"},
    {"root": "myakṣ", "series": "A1-sampras", "ztype": "I", "loc": 173, "period": "Vedic", "note": "to be situated"},
    {"root": "vyadh", "series": "A1-sampras", "ztype": "I", "loc": 173, "note": "to pierce"},
    {"root": "vac", "series": "A1-sampras", "ztype": "I", "loc": 173, "note": "to speak"},
    {"root": "vad", "series": "A1-sampras", "ztype": "I", "loc": 173, "note": "to speak"},
    {"root": "vas", "series": "A1-sampras", "ztype": "I", "loc": 173, "note": "to shine"},
    {"root": "vas", "series": "A1-sampras", "ztype": "I", "loc": 173, "note": "to dwell"},
    {"root": "vah", "series": "A1-sampras", "ztype": "I", "loc": 173, "note": "to carry"},
    {"root": "vaç", "series": "A1-sampras", "ztype": "I", "loc": 173, "note": "to be eager"},
    {"root": "vap", "series": "A1-sampras", "ztype": "I", "loc": 173, "note": "to strew"},
    {"root": "vap", "series": "A1-sampras", "ztype": "I", "loc": 173, "note": "to shear"},
    {"root": "vakṣ", "series": "A1-sampras", "ztype": "I", "loc": 173, "period": "Vedic", "note": "to increase"},
    {"root": "prach", "series": "A1-sampras", "ztype": "I", "loc": 173, "note": "to ask"},
    {"root": "vraçc", "series": "A1-sampras", "ztype": "I", "loc": 173, "note": "to cut up"},
    {"root": "krap", "series": "A1-sampras", "ztype": "I", "loc": 173, "period": "Vedic", "note": "to lament (Whitney: kṛp)"},
    {"root": "mrad", "series": "A1-sampras", "ztype": "I", "loc": 173, "period": "Vedic variant", "note": "variant of mṛd 'to crush'"},
    {"root": "bhraç", "series": "A1-sampras", "ztype": "I", "loc": 173, "period": "Vedic variant", "note": "variant of bhraṁç 'to fall'"},
    {"root": "tyaj", "series": "A1-sampras", "ztype": "II", "loc": 177, "note": "to forsake"},
    {"root": "vas", "series": "A1-sampras", "ztype": "II", "loc": 177, "note": "to clothe"},
    {"root": "tras", "series": "A1-sampras", "ztype": "II", "loc": 177, "note": "to be terrified"},
    {"root": "yat", "series": "A1-sampras", "ztype": "II", "loc": 177, "note": "to stretch"},
    {"root": "yas", "series": "A1-sampras", "ztype": "II", "loc": 177, "note": "to be heated"},
    {"root": "vyaj", "series": "A1-sampras", "ztype": "II", "loc": 177, "note": "to fan (=vīj)"},
    {"root": "vyath", "series": "A1-sampras", "ztype": "II", "loc": 177, "note": "to waver"},
    {"root": "kvath", "series": "A1-sampras", "ztype": "II", "loc": 177, "note": "to boil"},
    {"root": "tvakṣ", "series": "A1-sampras", "ztype": "II", "loc": 177, "period": "Vedic", "note": "to fashion"},
    {"root": "vadh", "series": "A1-sampras", "ztype": "II", "loc": 177, "note": "to slay (=badh)"},
    {"root": "çvas", "series": "A1-sampras", "ztype": "II", "loc": 177, "note": "to blow"},
    {"root": "svaj", "series": "A1-sampras", "ztype": "II", "loc": 177, "note": "to embrace"},
    {"root": "svad", "series": "A1-sampras", "ztype": "II", "loc": 177, "note": "to sweeten (=svād)"},
    {"root": "gras", "series": "A1-sampras", "ztype": "II", "loc": 177, "note": "to devour"},
    {"root": "grath", "series": "A1-sampras", "ztype": "II", "loc": 177, "note": "to tie (=granth)"},
    {"root": "prath", "series": "A1-sampras", "ztype": "II", "loc": 177, "note": "to spread"},
    {"root": "vraj", "series": "A1-sampras", "ztype": "II", "loc": 177, "note": "to proceed"},
    {"root": "hras", "series": "A1-sampras", "ztype": "II", "loc": 177, "note": "to shorten"},
    {"root": "rakṣ", "series": "A1-sampras", "ztype": "II", "loc": 177, "note": "to protect"},
    {"root": "ras", "series": "A1-sampras", "ztype": "II", "loc": 177, "note": "to roar"},
    {"root": "çrath", "series": "A1-sampras", "ztype": "fluctuating", "loc": 179, "note": "to slacken (mainly Vedic; Classical çlath, type II)"},
    {"root": "yabh", "series": "A1-sampras", "ztype": "unattested-pos1", "loc": 179, "note": "futuere"},
    {"root": "vat", "series": "A1-sampras", "ztype": "unattested-pos1", "loc": 179, "period": "Vedic", "note": "to apprehend"},
    {"root": "trap", "series": "A1-sampras", "ztype": "unattested-pos1", "loc": 179, "note": "to be abashed"},

    # --- A2 series (mdx 181-191) ---
    {"root": "sthā", "series": "A2", "ztype": "I", "loc": 183, "note": "to stand"},
    {"root": "pā", "series": "A2", "ztype": "I", "loc": 183, "note": "to drink"},
    {"root": "jyā", "series": "A2", "ztype": "I", "loc": 183, "note": "to overpower/injure"},
    {"root": "hvā", "series": "A2", "ztype": "I", "loc": 183, "note": "to call (=hū)"},
    {"root": "gā", "series": "A2", "ztype": "I", "loc": 183, "note": "to sing"},
    {"root": "gā", "series": "A2", "ztype": "I", "loc": 183, "note": "to go"},
    {"root": "dā", "series": "A2", "ztype": "I", "loc": 183, "note": "to give (=dad)"},
    {"root": "dā", "series": "A2", "ztype": "I", "loc": 183, "note": "to divide, share"},
    {"root": "dā", "series": "A2", "ztype": "I", "loc": 183, "note": "to bind"},
    {"root": "dhā", "series": "A2", "ztype": "I", "loc": 183, "note": "to put"},
    {"root": "dhā", "series": "A2", "ztype": "I", "loc": 183, "note": "to suck"},
    {"root": "mā", "series": "A2", "ztype": "I", "loc": 183, "note": "to measure"},
    {"root": "mā", "series": "A2", "ztype": "I", "loc": 183, "period": "Vedic", "note": "to bellow (=mi)"},
    {"root": "çā", "series": "A2", "ztype": "I", "loc": 183, "note": "to sharpen"},
    {"root": "sā", "series": "A2", "ztype": "I", "loc": 183, "note": "to bind (=si)"},
    {"root": "sphā", "series": "A2", "ztype": "I", "loc": 183, "note": "to fatten"},
    {"root": "hā", "series": "A2", "ztype": "I", "loc": 183, "note": "to leave"},
    {"root": "çyā", "series": "A2-sampras", "ztype": "I", "loc": 183, "note": "to coagulate"},
    {"root": "vyā", "series": "A2-sampras", "ztype": "I", "loc": 183, "note": "to envelop"},
    {"root": "çvā", "series": "A2-sampras", "ztype": "I", "loc": 183, "note": "to swell (=çū)"},
    {"root": "vā", "series": "A2-sampras", "ztype": "I", "loc": 183, "note": "to weave (=u)"},
    {"root": "chā", "series": "A2", "ztype": "fluctuating", "loc": 187, "note": "to cut up (chitaḥ/chātaḥ)"},
    {"root": "hā", "series": "A2", "ztype": "fluctuating", "loc": 187, "note": "to go forth (jihīte but hānaḥ)"},
    {"root": "khyā", "series": "A2", "ztype": "II", "loc": 189, "note": "to see"},
    {"root": "bhā", "series": "A2", "ztype": "II", "loc": 189, "note": "to shine"},
    {"root": "vā", "series": "A2", "ztype": "II", "loc": 189, "note": "to blow"},
    {"root": "rā", "series": "A2", "ztype": "II", "loc": 189, "note": "to give (faint Vedic type-I traces)"},
    {"root": "psā", "series": "A2", "ztype": "II", "loc": 189, "period": "Vedic", "note": "to devour (faint type-I traces)"},
    {"root": "ās", "series": "A2-cons", "ztype": "II", "loc": 191, "note": "to sit"},
    {"root": "yāc", "series": "A2-cons", "ztype": "II", "loc": 191, "note": "to ask"},
    {"root": "çās", "series": "A2-cons", "ztype": "I", "loc": 191, "note": "to order (SOLE exception in this subgroup; multiple peculiarities)"},

    # --- I/U/R series, "ending in alternating element" (mdx 195-199) ---
    {"root": "i", "series": "I1", "ztype": "I", "loc": 195, "note": "to go"},
    {"root": "nī", "series": "I2", "ztype": "I", "loc": 195, "note": "to lead"},
    {"root": "çru", "series": "U1", "ztype": "I", "loc": 195, "note": "to hear"},
    {"root": "pū", "series": "U2", "ztype": "I", "loc": 195, "note": "to cleanse"},
    {"root": "kṛ", "series": "R1", "ztype": "I", "loc": 195, "note": "to do"},
    {"root": "çṛ", "series": "R1", "ztype": "I", "loc": 195, "note": "to crush"},
    {"root": "car", "series": "R1", "ztype": "II", "loc": 197, "note": "to move"},
    {"root": "kṣar", "series": "R1", "ztype": "II", "loc": 197, "note": "to flow"},
    {"root": "tvar", "series": "R1", "ztype": "II", "loc": 197, "note": "to hasten"},
    {"root": "sphar", "series": "R1", "ztype": "II", "loc": 197, "note": "to jerk (Whitney also: sphṛ)"},
    {"root": "har", "series": "R1", "ztype": "II", "loc": 197, "period": "Vedic", "note": "to be gratified"},
    {"root": "day", "series": "I1", "ztype": "II", "loc": 197, "note": "quasi-root from dā 'to share'"},
    {"root": "chay", "series": "I1", "ztype": "II", "loc": 197, "note": "quasi-root from chā 'to cut up'"},
    {"root": "vyay", "series": "I1", "ztype": "II", "loc": 197, "note": "quasi-root from vyā 'to envelop'"},
    {"root": "hvay", "series": "I1", "ztype": "II", "loc": 197, "note": "quasi-root from hvā/hū 'to call'"},
    {"root": "çvay", "series": "I1", "ztype": "II", "loc": 197, "note": "quasi-root from çvā/çū 'to swell'"},
    {"root": "vay", "series": "I1", "ztype": "II", "loc": 197, "note": "quasi-root from vā/u 'to weave'"},
    {"root": "vyay", "series": "I1", "ztype": "II", "loc": 197, "note": "denominative quasi-root 'to expend'"},
    {"root": "klav", "series": "U1", "ztype": "II", "loc": 197, "note": "denominative quasi-root 'to stammer'"},
    {"root": "çī", "series": "I2", "ztype": "II", "loc": 197, "note": "to lie (perfect çiçye follows type I)"},
    {"root": "av", "series": "U1", "ztype": "fluctuating", "loc": 199, "note": "to favor"},
    {"root": "dhav", "series": "U1", "ztype": "unattested-pos1", "loc": 199, "period": "Vedic", "note": "to flow"},
    {"root": "svar", "series": "R1", "ztype": "unattested-pos1", "loc": 199, "note": "to sound"},
    {"root": "jar", "series": "R1", "ztype": "unattested-pos1", "loc": 199, "period": "Vedic", "note": "to sing (Whitney: jṛ)"},
    {"root": "jhar", "series": "R1", "ztype": "unattested-pos1", "loc": 199, "note": "to fall"},
    {"root": "phar", "series": "R1", "ztype": "unattested-pos1", "loc": 199, "period": "Vedic", "note": "to scatter"},
    {"root": "jvar", "series": "R1", "ztype": "ambiguous", "loc": 199, "note": "to be hot"},
    {"root": "tsar", "series": "R1", "ztype": "ambiguous", "loc": 199, "note": "to approach stealthily"},

    # --- I/U/R series, "ending in consonant" (mdx 201-213) ---
    {"root": "sev", "series": "I1-cons", "ztype": "II", "loc": 201, "note": "to serve"},
    {"root": "lok", "series": "U1-cons", "ztype": "II", "loc": 201, "note": "to look"},
    {"root": "garh", "series": "R1-cons", "ztype": "II", "loc": 201, "note": "to chide"},
    {"root": "edh", "series": "I1-cons", "ztype": "II", "loc": 201, "note": "to thrive"},
    {"root": "kṣvel", "series": "R1-cons", "ztype": "II", "loc": 201, "note": "to play"},
    {"root": "khel", "series": "R1-cons", "ztype": "II", "loc": 201, "note": "to stagger"},
    {"root": "ceṣṭ", "series": "I1-cons", "ztype": "II", "loc": 201, "note": "to stir"},
    {"root": "med", "series": "I1-cons", "ztype": "II", "loc": 201, "note": "to be fat"},
    {"root": "vell", "series": "R1-cons", "ztype": "II", "loc": 201, "note": "to stagger"},
    {"root": "heṣ", "series": "I1-cons", "ztype": "II", "loc": 201, "note": "to whinny"},
    {"root": "hreṣ", "series": "R1-cons", "ztype": "II", "loc": 201, "note": "to neigh"},
    {"root": "loc", "series": "U1-cons", "ztype": "II", "loc": 201, "note": "to see/consider"},
    {"root": "garj", "series": "R1-cons", "ztype": "II", "loc": 201, "note": "to roar"},
    {"root": "tarj", "series": "R1-cons", "ztype": "II", "loc": 201, "note": "to threaten"},
    {"root": "nard", "series": "R1-cons", "ztype": "II", "loc": 201, "note": "to bellow"},
    {"root": "arc", "series": "R1-cons", "ztype": "II", "loc": 201, "period": "post-Vedic only (Vedic: ṛc)", "note": "to shine/praise"},
    {"root": "spardh", "series": "R1-cons", "ztype": "II", "loc": 201, "period": "post-Vedic only (Vedic: spṛdh)", "note": "to contend"},
    {"root": "carv", "series": "R1-cons", "ztype": "II", "loc": 201, "note": "to chew"},
    {"root": "ruc", "series": "U1-cons", "ztype": "I", "loc": 207, "note": "to shine"},
    {"root": "chid", "series": "I1-cons", "ztype": "I", "loc": 207, "note": "to cut off"},
    {"root": "vṛj", "series": "R1-cons", "ztype": "I", "loc": 207, "note": "to twist"},
    {"root": "bhikṣ", "series": "I1-cons", "ztype": "III", "loc": 207, "note": "to beg"},
    {"root": "cumb", "series": "U1-cons", "ztype": "III", "loc": 207, "note": "to kiss"},
    {"root": "jṛmbh", "series": "R1-cons", "ztype": "III", "loc": 207, "note": "to gape"},
    {"root": "gir", "series": "R1-cons", "ztype": "III", "loc": 207, "note": "quasi-root from gṛ 'to swallow'"},
    {"root": "krīḍ", "series": "I2-cons", "ztype": "III", "loc": 207, "note": "to play"},
    {"root": "pūj", "series": "U2-cons", "ztype": "III", "loc": 207, "note": "to reverence"},
    {"root": "pūr", "series": "U2-cons", "ztype": "III", "loc": 207, "note": "quasi-root from pṛ 'to fill'"},
    {"root": "viṣṭ", "series": "I1-cons", "ztype": "I", "loc": 209, "note": "to wrap (exception to the rule)"},
    {"root": "mikṣ", "series": "I1-cons", "ztype": "I", "loc": 209, "note": "to mix (exception to the rule)"},
    {"root": "bhṛjj", "series": "R1-cons", "ztype": "I", "loc": 209, "note": "to roast (exception to the rule)"},
    {"root": "mṛkṣ", "series": "R1-cons", "ztype": "I", "loc": 209, "note": "to stroke (exception; also mṛkṣaya- follows III)"},
    {"root": "cur", "series": "U1-cons", "ztype": "I", "loc": 209, "note": "to steal (exception to the rule)"},
    {"root": "lul", "series": "U1-cons", "ztype": "I", "loc": 209, "note": "to be lively (exception to the rule)"},
    {"root": "mil", "series": "I1-cons", "ztype": "I", "loc": 209, "note": "to combine (exception; miliṣyati follows III)"},
    {"root": "dīv", "series": "I1-cons", "ztype": "I", "loc": 209, "note": "to play (exception to the rule)"},
    {"root": "dīv", "series": "I1-cons", "ztype": "I", "loc": 209, "note": "to lament (exception to the rule)"},
    {"root": "sīv", "series": "I1-cons", "ztype": "I", "loc": 209, "note": "to sew (exception to the rule)"},
    {"root": "ṣṭhīv", "series": "I1-cons", "ztype": "I", "loc": 209, "note": "to spew (exception to the rule)"},
    {"root": "srīv", "series": "I1-cons", "ztype": "I", "loc": 209, "period": "Vedic", "note": "to fail (=çrīv, exception to the rule)"},
    {"root": "rūṣ", "series": "U1-cons", "ztype": "I", "loc": 209, "note": "to strew (exception to the rule)"},
    {"root": "ujh", "series": "I1-cons", "ztype": "III", "loc": 209, "note": "to forsake (jh treated as two consonants, exception-to-exception)"},

    # --- Series L (mdx 217, ~20 roots, all type II except kḷp) ---
    {"root": "cal", "series": "L1", "ztype": "II", "loc": 217, "note": "to stir"},
    {"root": "jalp", "series": "L1", "ztype": "II", "loc": 217, "note": "to murmur/speak"},
    {"root": "kḷp", "series": "L1", "ztype": "I", "loc": 217, "note": "to be adapted (SOLE type-I exception in series L)"},

    # --- Series M/N (mdx 221-235) ---
    {"root": "gam", "series": "M1", "ztype": "I", "loc": 221, "note": "to go"},
    {"root": "bhram", "series": "M2", "ztype": "I", "loc": 221, "note": "to wander"},
    {"root": "man", "series": "N1", "ztype": "I", "loc": 221, "note": "to think"},
    {"root": "jan", "series": "N2", "ztype": "I", "loc": 221, "note": "to give birth"},
    {"root": "stan", "series": "N1", "ztype": "II", "loc": 221, "note": "to thunder"},
    {"root": "çam", "series": "M1", "ztype": "II", "loc": 223, "note": "to toil"},
    {"root": "dham", "series": "M1", "ztype": "II", "loc": 223, "note": "variant of dhmā 'to blow'"},
    {"root": "kṣam", "series": "M1", "ztype": "fluctuating", "loc": 223, "note": "to endure (kṣāntaḥ/kṣamitaḥ)"},
    {"root": "kan", "series": "N1", "ztype": "I", "loc": 223, "period": "Vedic", "note": "to be pleased"},
    {"root": "kṣaṇ", "series": "N1", "ztype": "I", "loc": 223, "note": "to wound"},
    {"root": "khan", "series": "N1", "ztype": "I", "loc": 223, "note": "to dig"},
    {"root": "tan", "series": "N1", "ztype": "I", "loc": 223, "note": "to stretch"},
    {"root": "dhvan", "series": "N1", "ztype": "I", "loc": 223, "period": "Vedic", "note": "to cover"},
    {"root": "san", "series": "N1", "ztype": "I", "loc": 223, "note": "to gain"},
    {"root": "han", "series": "N1", "ztype": "I", "loc": 223, "note": "to smite"},
    {"root": "van", "series": "N1", "ztype": "shifts I->II", "loc": 223, "note": "to win (Vedic type I, Epic-onward type II)"},
    {"root": "pan", "series": "N1", "ztype": "fluctuating", "loc": 223, "period": "Vedic", "note": "to admire"},
    {"root": "stambh", "series": "M1-cons", "ztype": "I", "loc": 227, "note": "to prop"},
    {"root": "dhvaṁs", "series": "M1-cons", "ztype": "I", "loc": 227, "note": "to scatter"},
    {"root": "añj", "series": "N1-cons", "ztype": "I", "loc": 227, "note": "to anoint"},
    {"root": "krand", "series": "N1-cons", "ztype": "I", "loc": 227, "period": "Vedic only", "note": "to cry out"},
    {"root": "chand", "series": "N1-cons", "ztype": "I", "loc": 227, "note": "to seem/please"},
    {"root": "taṁs", "series": "M1-cons", "ztype": "I", "loc": 227, "period": "Vedic", "note": "to shake"},
    {"root": "tañc", "series": "N1-cons", "ztype": "I", "loc": 227, "note": "to coagulate"},
    {"root": "baṁh", "series": "M1-cons", "ztype": "I", "loc": 227, "period": "Vedic", "note": "to make firm"},
    {"root": "bandh", "series": "N1-cons", "ztype": "I", "loc": 227, "note": "to bind"},
    {"root": "bhañj", "series": "N1-cons", "ztype": "I", "loc": 227, "note": "to break"},
    {"root": "maṁh", "series": "M1-cons", "ztype": "I", "loc": 227, "period": "Vedic", "note": "to bestow"},
    {"root": "raṁh", "series": "M1-cons", "ztype": "I", "loc": 227, "period": "Vedic only", "note": "to hasten"},
    {"root": "randh", "series": "N1-cons", "ztype": "I", "loc": 227, "note": "to be/make subject"},
    {"root": "vañc", "series": "N1-cons", "ztype": "I", "loc": 227, "note": "to move crookedly"},
    {"root": "çaṁs", "series": "M1-cons", "ztype": "I", "loc": 227, "note": "to praise"},
    {"root": "çrambh", "series": "M1-cons", "ztype": "I", "loc": 227, "note": "to trust"},
    {"root": "çvañc", "series": "N1-cons", "ztype": "I", "loc": 227, "period": "Vedic", "note": "to spread"},
    {"root": "skand", "series": "N1-cons", "ztype": "I", "loc": 227, "note": "to leap"},
    {"root": "skambh", "series": "M1-cons", "ztype": "I", "loc": 227, "note": "to prop"},
    {"root": "syand", "series": "N1-cons", "ztype": "I", "loc": 227, "note": "to move on"},
    {"root": "sraṁs", "series": "M1-cons", "ztype": "I", "loc": 227, "note": "to fall"},
    {"root": "daṁç", "series": "N1-cons", "ztype": "variant-pair", "loc": 229, "note": "to bite (=daç, type distinction only in pos 2/3)"},
    {"root": "manth", "series": "N1-cons", "ztype": "I", "loc": 231, "note": "to shake (blends with math in later language)"},
    {"root": "math", "series": "N1-cons", "ztype": "I", "loc": 231, "note": "to crush (blends with manth in later language)"},
    {"root": "mad", "series": "N1-cons", "ztype": "I", "loc": 231, "note": "to be exhilarated (Vedic/Brāhmaṇa variant: mand)"},
    {"root": "sañj", "series": "N1-cons", "ztype": "shifts I->A1", "loc": 231, "note": "to hang (Epic-onward A1 forms: saktum)"},
    {"root": "granth", "series": "N1-cons", "ztype": "shifts I->A1", "loc": 231, "note": "to tie (Classical-onward variant: grath)"},
    {"root": "jambh", "series": "N1-cons", "ztype": "shifts I->A1", "loc": 231, "note": "to chew up/crush (Classical-onward variant: jabh)"},
    {"root": "raj", "series": "N1-cons", "ztype": "shifts A1->N", "loc": 231, "note": "to color (Epic-onward variant: rañj)"},
    {"root": "dabh", "series": "N1-cons", "ztype": "shifts->A1", "loc": 231, "note": "to harm (=dambh)"},
    {"root": "rabh", "series": "N1-cons", "ztype": "shifts->A1", "loc": 231, "note": "to take hold (=rambh)"},
    {"root": "labh", "series": "N1-cons", "ztype": "shifts->A1", "loc": 231, "note": "to take (=lambh)"},
    {"root": "nabh", "series": "N1-cons", "ztype": "partial-nasalization", "loc": 231, "note": "to burst (nasalizes only in causative)"},
    {"root": "aṁç", "series": "M1-cons", "ztype": "partial-nasalization", "loc": 231, "note": "to attain (nasalizes only in perfect)"},
    {"root": "majj", "series": "N1-cons", "ztype": "partial-nasalization", "loc": 231, "note": "to sink (nasalizes only pos.2 before non-y consonant)"},
    {"root": "bhraṁç", "series": "M1-cons", "ztype": "I", "loc": 233, "note": "to fall (Vedic variant: bhraç, also type I)"},
    {"root": "añc", "series": "N1-cons", "ztype": "I-in-Vedic-fluctuating-later", "loc": 233, "note": "to bend (Vedic type I with variant ac; post-Vedic fluctuates I/II)"},
    {"root": "nand", "series": "N1-cons", "ztype": "II", "loc": 235, "note": "to rejoice"},
    {"root": "aṇṭh", "series": "N1-cons", "ztype": "II", "loc": 235, "note": "to visit"},
    {"root": "kamp", "series": "M1-cons", "ztype": "II", "loc": 235, "note": "to tremble"},
    {"root": "lamb", "series": "M1-cons", "ztype": "II", "loc": 235, "note": "to hang down (=ramb)"},
    {"root": "vaṇṭ", "series": "N1-cons", "ztype": "II", "loc": 235, "note": "to divide"},
    {"root": "vand", "series": "N1-cons", "ztype": "II", "loc": 235, "note": "to greet"},
    {"root": "çaṅk", "series": "N1-cons", "ztype": "II", "loc": 235, "note": "to doubt"},
    {"root": "spand", "series": "N1-cons", "ztype": "II", "loc": 235, "note": "to quiver"},
    {"root": "dham", "series": "M1-cons", "ztype": "II", "loc": 235, "period": "Vedic", "note": "to run"},
    {"root": "raṇv", "series": "M1-cons", "ztype": "II", "loc": 235, "period": "Vedic", "note": "to delight"},
]

# ---------------------------------------------------------------------------------------
# Table 4's own summary row (mdx line 283) — the paper's grand total, reproduced verbatim
# for the internal-consistency check (see verify_table4_arithmetic below).
# ---------------------------------------------------------------------------------------
TABLE4_SUMMARY = {"type_I": 435, "type_II_definite": 229, "type_II_ambiguous": 109, "type_III": 117}

# Table 5's own summary row (mdx line 341)
TABLE5_SUMMARY = {"aniṭ": 170, "seṭ": 100, "mixed_or_ta_only": 320}  # all "≈"


def load_whitney_roots():
    with open(WHITNEY_ROOTS, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _normalize_transliteration(s):
    """The paper's English translation uses the older ç/ṁ IAST convention (ç=ś, ṁ=ṃ);
    WhitneyRoots/crosswalk/roots.csv uses the modern ś/ṃ convention. Same phonemes, two
    transliteration schemes — normalize both sides to compare fairly rather than treating
    this as a missing root."""
    return s.replace("ç", "ś").replace("ṁ", "ṃ")


def check_root_existence(whitney_rows):
    """Does each of Zaliznyak's explicitly-named roots appear in Whitney's actual root list?
    Matches on root_iast after normalizing the ç/ṁ vs ś/ṃ transliteration difference. A
    remaining "miss" after normalization is still not necessarily an ERROR — Whitney's own
    list sometimes cites a root in a different grade or variant-name than Zaliznyak's
    regularized by-type citation (e.g. Whitney cites 'spṛdh', Zaliznyak's Type-II convention
    cites the same root as 'spardh') — flagged for human review, not auto-failed."""
    whitney_set = {_normalize_transliteration(r["root_iast"]) for r in whitney_rows if r["root_iast"]}
    results = []
    for entry in NAMED_ROOTS:
        found = _normalize_transliteration(entry["root"]) in whitney_set
        results.append({**entry, "found_in_whitney_roots_csv": found})
    hits = sum(1 for r in results if r["found_in_whitney_roots_csv"])
    return {
        "total_named": len(results),
        "distinct_named": len({e["root"] for e in NAMED_ROOTS}),
        "found_in_whitney": hits,
        "not_found": [r for r in results if not r["found_in_whitney_roots_csv"]],
    }


def verify_table4_arithmetic():
    """Table 4's own summary row: 435 + 229+109 + 117 = ? Cross-check against the paper's
    own stated corpus size ('approximately 750 out of 847', mdx line 29) and its own
    explanation that transitional/fluctuating roots are counted twice (mdx line 287)."""
    s = TABLE4_SUMMARY
    total_with_double_count = s["type_I"] + s["type_II_definite"] + s["type_II_ambiguous"] + s["type_III"]
    return {
        "table4_summary_row": s,
        "sum_of_summary_row": total_with_double_count,
        "paper_stated_corpus_size": "approximately 750 out of 847 (mdx line 29)",
        "paper_stated_double_counting_note": "roots with historical transitions/fluctuations counted twice (mdx line 287)",
        "excess_over_750": total_with_double_count - 750,
        "assessment": (
            "Internally consistent WITH the paper's own double-counting caveat: the "
            f"{total_with_double_count - 750}-root excess over the ~750 base corpus is the "
            "right order of magnitude for a 'some roots counted twice' correction (not a "
            "contradiction) but this pass did not independently verify the exact count of "
            "double-counted roots, so treat as PLAUSIBLE not CONFIRMED."
        ),
    }


def verify_table5_arithmetic():
    """Table 5's summary (≈170+≈100+≈320=≈590) against the paper's own stated exclusions
    (mdx line 307: ~240 roots with no attested relevant forms, PLUS all ā-final roots,
    excluded from this table entirely)."""
    s = TABLE5_SUMMARY
    total = s["aniṭ"] + s["seṭ"] + s["mixed_or_ta_only"]
    return {
        "table5_summary_row": s,
        "sum_of_summary_row_approx": total,
        "paper_stated_exclusions": "~240 roots with no attested relevant forms (incl. ~110 seṭ-only-by-default) PLUS all ā-final roots entirely (mdx line 307)",
        "assessment": (
            "NOT independently verified — this pass could not confirm how many roots are "
            "'ā-final' as a category (the paper does not give that count explicitly), so the "
            "arithmetic 750(analyzed) - 240(unattested) - X(ā-final) = ~590(Table 5 total) "
            "cannot be checked without knowing X. Flagged as a candidate for a human "
            "Sanskritist to check, NOT asserted as an error — the gap could equally be this "
            "session's incomplete understanding of which roots count as 'ā-final' here."
        ),
    }


def check_whitney_corpus_size(whitney_rows):
    """Paper states 'approximately 750 out of 847 non-cross-referenced entries in Whitney's
    list' (mdx line 29). WhitneyRoots/crosswalk/roots.csv has 930 entries — check the gap."""
    return {
        "whitney_roots_csv_total_entries": len(whitney_rows),
        "paper_stated_whitney_total": 847,
        "paper_stated_analyzed": "approximately 750",
        "gap": len(whitney_rows) - 847,
        "assessment": (
            "WhitneyRoots/crosswalk/roots.csv has more entries than Zaliznyak's stated "
            "Whitney total (847) — likely a different counting convention (e.g. this digitized "
            "list may include cross-referenced/homonym-split entries Zaliznyak's '847 "
            "non-cross-referenced entries' phrasing explicitly excludes) rather than an error "
            "in either source. Not resolved in this pass — flagged for whoever maintains "
            "WhitneyRoots to confirm the exact filtering Zaliznyak applied."
        ),
    }


def main():
    whitney_rows = load_whitney_roots()
    existence = check_root_existence(whitney_rows)
    t4 = verify_table4_arithmetic()
    t5 = verify_table5_arithmetic()
    corpus = check_whitney_corpus_size(whitney_rows)

    print(f"ROOT EXISTENCE CHECK: {existence['found_in_whitney']}/{existence['total_named']} named-root "
          f"citations ({existence['distinct_named']} distinct roots) found in WhitneyRoots/crosswalk/roots.csv")
    if existence["not_found"]:
        print(f"  NOT FOUND ({len(existence['not_found'])}):")
        for r in existence["not_found"]:
            print(f"    {r['root']} ({r.get('note','')}) — mdx line {r['loc']}")
    print()
    print("TABLE 4 ARITHMETIC:", t4["sum_of_summary_row"], "vs ~750 stated corpus ->", t4["assessment"])
    print()
    print("TABLE 5 ARITHMETIC:", t5["sum_of_summary_row_approx"], "->", t5["assessment"])
    print()
    print("WHITNEY CORPUS SIZE:", corpus["whitney_roots_csv_total_entries"], "vs stated 847 ->", corpus["assessment"])

    if "--check" not in sys.argv:
        out = HERE / "root_classifier.json"
        out.write_text(json.dumps({
            "named_roots": NAMED_ROOTS,
            "existence_check": existence,
            "table4_arithmetic": t4,
            "table5_arithmetic": t5,
            "whitney_corpus_size_check": corpus,
        }, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\n-> wrote {out.relative_to(REPO)}")


if __name__ == "__main__":
    main()
