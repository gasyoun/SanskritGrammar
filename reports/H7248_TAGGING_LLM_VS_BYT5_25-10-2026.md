# H7248 — Sanskrit morphological tagging: Qwen3.5-9B against ByT5-Sanskrit on DCS gold

_Created: 24-10-2026 · Executed: 25-10-2026 · Executor: DeepSeek v4.1 Flash (`deepseek/deepseek-flash`)_

**Status: PARTIAL.** The frozen, reproducible measurement harness and Arm A's pinned
published figures are done. Arm B (Qwen3.5-9B) is **not measured**: no Qwen3.5-9B weights
were reachable from the executing box. The comparison this handoff exists to make therefore
remains open, and this report does not claim it.

## 1. The handoff's premise is wrong, and that changes the comparison

H7248 opens with "its DCS table reports 90.11 / 93.83 / 94.29 on three tagging metrics".
Read from the full text ([arXiv 2409.13920v1](https://arxiv.org/html/2409.13920v1),
ACL Anthology 2024.findings-emnlp.805), those three numbers are **Table 3, sentence-level
perfect matches on three word-*segmentation* datasets**:

> Table 3: Sentence level perfect matches on previous Sanskrit word segmentation tasks.
> — rcNN-SS 85.2 / 87.08 / 77.62; TransLIST – / 93.97 / 85.47; **ByT5-Sanskrit 90.11 / 93.83 / 94.29**
> (DCS 2018, 509k samples · SIGHUM, 99k · Hackathon, 89k)

The paper publishes **no token-level morphological-tagging metric at all** — no UPOS
accuracy, no FEATS F1, no lemma accuracy. Its only morphosyntax-bearing figures are
**sentence-level perfect matches of joint tasks** (Table 7, DCS April-2024 snapshot,
601,403 sentences, dev 8,190 / test 8,398):

| task | mT5 sen | ByT5 sen | ByT5 par | ByT5-Sanskrit sen | ByT5-Sanskrit par |
|---|---|---|---|---|---|
| S | 76.09 | 83.71 | 87.21 | 84.61 | 88.21 |
| L | 68.27 | 77.99 | 82.05 | 79.88 | 83.96 |
| S+M | 49.94 | 60.93 | 71.5 | 63.86 | 74.38 |
| L+M | 49.23 | 59.28 | 69.4 | 62.0 | 72.33 |
| S+L+M | 49.1 | 58.75 | 71.92 | 61.27 | 74.31 |

Generated table: [`reports/h7248_tables.md`](h7248_tables.md); pinned source with verbatim
captions: [`data/h7248/byt5_paper_numbers.json`](../data/h7248/byt5_paper_numbers.json).

Consequences, stated before any number is compared:

1. **No published baseline exists for the metric H7248 specifies.** A token-level
   UPOS/FEATS/lemma comparison against this paper is not possible from the publication —
   it needs the model re-run, not the table.
2. **The Table-7 M figures are not "tagging accuracy".** Each `+M` row scores a whole
   sentence reproduced exactly across *joint* tasks; a single segmentation slip zeroes the
   sentence without any tagging error. They are a strict lower bound on tagging quality,
   not a measure of it.
3. **Split mismatch on top of metric mismatch**: the paper holds back its own
   April-2024 dev/test split, which is not published as a file, and its test split is
   explicitly "strongly biased towards Vedic texts" (paper §5.5) because reconstructed
   forms are excluded from test/validation. Our sample is stratified by layer by design.
4. The prior expectation quoted in the handoff (arXiv 2511.08145, "Still Not There") is
   cited as expectation only; it is about poetry-to-prose conversion and is not evidence
   for or against a tagging result.

## 2. Frozen sample (delivered)

[`data/h7248/manifest.json`](../data/h7248/manifest.json) + [`data/h7248/gold_sample.jsonl`](../data/h7248/gold_sample.jsonl),
built by [`scripts/h7248_freeze_dcs_sample.py`](../scripts/h7248_freeze_dcs_sample.py).

- **Corpus**: DCS CoNLL-U dump, `OliverHellwig/sanskrit` @ `8aeed5a1` (commit date
  2026-08-24), route `dcs/data/conllu/files`, **CC BY 4.0**. Citation: Hellwig, Oliver
  (2010–2024), *The Digital Corpus of Sanskrit (DCS)*.
- **Texts** (one chapter file each, the largest chapter of the text, deterministic):
  vedic — Ṛgveda, Atharvaveda (Śaunaka), Śatapathabrāhmaṇa; epic — Mahābhārata, Rāmāyaṇa,
  Harivaṃśa; classical — Kumārasaṃbhava, Meghadūta, Hitopadeśa; śāstra —
  Aṣṭāṅgahṛdayasaṃhitā, Nyāyabhāṣya, Arthaśāstra. Every chapter file's sha256, byte size,
  sentence count and usable-sentence count is in the manifest.
- **Deterministic rule**: candidate score = `sha256(seed|text|chapter|sentence_index)`;
  each stratum's pool sorted by that digest; a per-stratum quota of 250 filled from the
  pool (leftover redistribution if a stratum runs short), then a global cap.
- **Size**: **1,000 sentences / 7,973 tokens — sentences bound first** (cap 1,000
  sentences *or* 20,000 tokens). 250 sentences per stratum.
- **Filters**: ≥4 tokens per sentence; ≥50 % of tokens carry a non-`_` FEATS string
  (morphological content, not bare punctuation runs).
- **Manifest hash**: `29fe570b896edf3addccfee020282dcbf64089d96b5e2d847681229cdf8c0ec4`
  (content hash, `manifest_sha256` field). Gold-sample sha256:
  `70c59f6da3692eed43fcc8840e019f1abed20177e5a26a1b86d5d7e4d128a156`.

This is a **fresh sample, not the paper's test split** — deliberately, and the comparability
section says what that costs.

## 3. Arms

### Arm A — ByT5-Sanskrit: quoted, split- and metric-adjusted

Not re-run: the paper's April-2024 split is not published as a file, and no ByT5-Sanskrit
checkpoint was available on this box. Figures above are quoted from the publication and are
labelled **not comparable at token level** in the results JSON
(`arm_a.comparable_to_arm_b_at_token_level: false`).

### Arm B — Qwen3.5-9B: NOT MEASURED

Blocker, recorded verbatim in [`reports/h7248_results.json`](h7248_results.json):
no Qwen3.5-9B weights reachable — no local Ollama endpoint (`127.0.0.1:11434` refused
connection) and no sanctioned API lane for this model on this executor. Zero-shot and
3-shot arms are therefore both unmeasured, and **no inference-cost figure exists**.

The runner contract is in place: any system that emits
`{"sent": <manifest sentence id>, "i": <token index>, "lemma", "upos", "feats"}` rows to
`data/h7248/predictions/<arm>.jsonl` is scored by one command —

```
python scripts/h7248_tagging_bench.py --predictions data/h7248/predictions/armB-zeroshot.jsonl
```

which adds per-stratum UPOS accuracy, FEATS exact match, FEATS micro-F1 and lemma accuracy
with token denominators, plus a missing-prediction count so a partial run cannot silently
inflate a denominator.

### Arm C — majority floor (measured here, zero cost)

Per stratum, every token gets the single most frequent lemma/UPOS/FEATS string observed in
the **other three strata** (leave-one-stratum-out, so no target-stratum leakage). Not a
tagger: it is the floor any real system must clear, and it fixes the scale of the metrics
on this sample.

| stratum | tokens | UPOS acc | FEATS exact | FEATS micro-F1 | lemma acc |
|---|---|---|---|---|---|
| classical | 2313 | 0.4436 | 0.1457 | 0.0 | 0.0372 |
| epic | 1638 | 0.4792 | 0.1197 | 0.075 | 0.0317 |
| śāstra | 2116 | 0.4976 | 0.1248 | 0.0 | 0.0284 |
| vedic | 1906 | 0.352 | 0.0262 | 0.0153 | 0.0383 |

Denominator under every figure: **tokens**, per stratum. Two things the floor already shows
and any Arm B run must be read against: (a) UPOS majority sits at 0.35–0.50, so a tagger
scoring 0.60 is barely above a constant; (b) FEATS micro-F1 collapses to ~0 because DCS
feature bundles are near-unique per token — FEATS exact match is the informative metric,
and the paper's byte-level tag serialisation (46 chars/tag average, compressed 0.14) exists
precisely because of this.

## 4. Comparability statement

| | Arm A (ByT5-Sanskrit) | Arm B (Qwen3.5-9B) | Arm C (floor) |
|---|---|---|---|
| metric | sentence-level perfect match, joint S/L/M | token-level UPOS / FEATS / lemma | token-level UPOS / FEATS / lemma |
| population | paper's own dev/test split, 8,398 test sentences, Vedic-biased | this frozen 1,000-sentence stratified sample | same sample |
| split | April-2024 DCS snapshot, unpublished | DCS @ `8aeed5a1`, published manifest | same |
| status | quoted, **split+metric adjusted** | **not measured** | measured |

**No cross-arm claim is made in this report.** Arm A cannot be placed beside Arm B in one
table without inventing an equivalence between sentence-perfect-match on a joint task and
token-level accuracy on a different split; that equivalence is not established here and is
not assumed. A real comparison needs the ByT5 model re-run **on this manifest** (then both
arms sit on one population and one metric), which is the named residual.

## 5. Refutation condition (stated before the result exists)

The LLM arm is **competitive** if, on this frozen manifest, Qwen3.5-9B (zero-shot or 3-shot,
temperature 0, reasoning disabled, full tag inventory + one worked example in the prompt,
output constrained to CoNLL-U columns) reaches **UPOS accuracy within 2 points** of
ByT5-Sanskrit **measured on the same manifest**, and **FEATS exact match within 5 points**
of it. It is **not competitive** if either gap exceeds those margins. If the ByT5 model
cannot be re-run on the manifest, the comparison is **inconclusive by construction** — the
paper's numbers cannot adjudicate it — and no "LLM wins/loses" sentence may be written.
The handoff's personal-communication expectation (LLM "behind by quite some margin") is a
hypothesis to test, not a prior to confirm.

## 6. Inference cost

Not measured (Arm B not run). Cost fields are absent rather than zero in the results JSON,
so a future run cannot be read as free. The scoring harness reports no wall time by design —
cost belongs to the runner, and a runner that does not report it fails the handoff's step 5.

## 7. Verifier recipe

```
python scripts/h7248_freeze_dcs_sample.py --check   # gold sha256 vs manifest: PASS
python scripts/h7248_tagging_bench.py --check       # frozen-sample integrity: PASS
python scripts/h7248_tagging_bench.py               # rewrites reports/h7248_results.json + reports/h7248_tables.md
git diff --exit-code reports/h7248_results.json reports/h7248_tables.md   # identical bytes
```

No network, no sampling, no clock in the payload: re-derivation is byte-identical.
