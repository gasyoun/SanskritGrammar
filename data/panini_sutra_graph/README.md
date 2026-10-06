# Pāṇini sūtra dependency graph (H6056)

Uttara-pūrva dependency graph of the Aṣṭādhyāyī built from the canonical [ashtadhyayi-com/data](https://github.com/ashtadhyayi-com/data) dataset (`sutraani/data.txt`, sha256 `4d46f436d77574f3…`), the same source that powers `/panini-sutra-lookup`. Regenerate with `python tools/panini_sutra_graph.py build`.

## Method

The dataset encodes, per sūtra, the anuvṛtti continuations (`an`: word + source sūtra id) and the governing adhikāras (`ad`). These listings are partially **flattened** — a sūtra names remote continuations that also reach it through intermediate sūtras. Two graphs are therefore exported:

- **raw** — every encoded dependency edge, typed `adhikara` / `anuvritti` (21147 typed edges, 20890 untyped);
- **reduced** — the transitive reduction of the raw graph (3923 edges): the **immediate** uttara-pūrva chains, i.e. the reconstructed reading structure (each edge = one direct continuation/governance).

The raw graph is a forward DAG (every edge points from an earlier sūtra to a later one; 0 back-edges, 0 dangling references), which validates the uttara-pūrva reading against the encoded data.

## Metrics

- nodes (sūtras): **3983**
- diameter (raw / reduced): **9 / 21**
- deepest study layer: **22**

Top depended-on sūtras (raw in-degree — the great adhikāra/anuvṛtti hubs):

| ref | sūtra | in-degree |
|---|---|---|
| 4.1.109 | लुक् स्त्रियाम् | 12 |
| 5.1.87 | रात्र्यहस्संवत्सराच्च | 12 |
| 5.1.88 | वर्षाल्लुक् च | 12 |
| 5.1.89 | चित्तवति नित्यम् | 12 |
| 5.3.17 | अधुना | 12 |
| 5.3.18 | दानीं च | 12 |
| 5.3.19 | तदो दा च | 12 |
| 3.3.53 | रश्मौ च | 11 |
| 3.3.65 | क्वणो वीणायां च | 11 |
| 4.1.108 | वतण्डाच्च | 11 |

Top immediate hubs (reduced in-degree):

| ref | sūtra | in-degree |
|---|---|---|
| 1.1.3 | इको गुणवृद्धी | 2 |
| 2.3.32 | पृथग्विनानानाभिस्तृतीयाऽन्यतरस्याम् | 2 |
| 2.3.44 | प्रसितोत्सुकाभ्यां तृतीया च | 2 |
| 4.3.23 | सायंचिरम्प्राह्णेप्रगेऽव्ययेभ्यष्ट्युट्युलौ तुट् च | 2 |
| 6.2.144 | थाथघञ्क्ताजबित्रकाणाम् | 2 |
| 6.2.145 | सूपमानात् क्तः | 2 |
| 6.2.152 | सप्तम्याः पुण्यम् | 2 |
| 6.2.153 | ऊनार्थकलहं तृतीयायाः | 2 |
| 6.2.155 | नञो गुणप्रतिषेधे सम्पाद्यर्हहितालमर्थास्तद्धिताः | 2 |
| 6.2.162 | बहुव्रीहाविदमेतत्तद्भ्यः प्रथमपूरणयोः क्रियागणने | 2 |

## Pedagogy — study order

`study_order.tsv` is the **study-order predictor**: sūtras are stratified into topological layers over the reduced graph — every sūtra appears strictly after all of its immediate prerequisites, and within a layer in book order. Layer 1 is the prerequisite-free foundation; a learner can take layers in sequence. The layer invariant is machine-checked by `panini_sutra_graph.py check` (and by `tests/test_panini_sutra_graph.py`) on the committed artifacts.

Layer-1 foundations begin with: 1.1.1 _वृद्धिरादैच्_, 1.1.2 _अदेङ् गुणः_, 1.1.7 _हलोऽनन्तराः संयोगः_, 1.1.8 _मुखनासिकावचनोऽनुनासिकः_, 1.1.9 _तुल्यास्यप्रयत्नं सवर्णम्_, 1.1.11 _ईदूदेद्द्विवचनं प्रगृह्यम्_, 1.1.20 _दाधा घ्वदाप्_, 1.1.21 _आद्यन्तवदेकस्मिन्_, 1.1.22 _तरप्तमपौ घः_, 1.1.23 _बहुगणवतुडति संख्या_, 1.1.26 _क्तक्तवतू निष्ठा_, 1.1.27 _सर्वादीनि सर्वनामानि_ …

## Files

- `graph.json` — machine format: meta, metrics, nodes, reduced edges.
- `edges.tsv` — reduced (immediate) edges with relation type.
- `edges_full.tsv` — raw typed edges as encoded.
- `study_order.tsv` — the pedagogy predictor (layer order).

