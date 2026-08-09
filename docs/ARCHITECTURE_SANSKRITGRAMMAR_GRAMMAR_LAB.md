# Architecture — SanskritGrammar Grammar Lab

_Created: 09-08-2026 · Last updated: 09-08-2026_

Architecture for the
[Grammar Lab plan](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/PLAN_SANSKRITGRAMMAR_GRAMMAR_LAB_2026H2.md).

## 1. Ownership boundary

| Concern | Owner | Contract |
|---|---|---|
| Scholarly topics, source anchors, evidence, public exercises | SanskritGrammar | Versioned static bundle |
| Canonical normalization/transcoding | `sanskrit-util` and existing shared utilities | Imported/reused functions, never rewritten |
| Dictionary/root crosswalks | Existing dictionary, WhitneyRoots and kosha assets | Stable IDs and pinned derived files |
| Corpus counts/examples | VisualDCS/DCS-derived registered assets | Pinned snapshot + provenance |
| Learner identity, bookmarks, attempts, mastery, recommendations | Systema-Sanscriticum | Database rows scoped to user and topic ID |
| Entitlement, tariff/subscription consequences | Systema-Sanscriticum | Provider-independent `grammar_lab` capability |
| Payment processing | Existing Systema billing services | Payment events grant/revoke capability; product never reads gateway state directly |

Core pages render from vendored/imported data. No live dictionary/corpus service is required.

## 2. Neutral topic graph and Type-D links

The topic locus is `subject:grammar-lab:<slug>`. It is stable, host-independent, and fits the
existing [Type-D target-locus grammar](https://github.com/gasyoun/Uprava/blob/main/TYPED_LINK_ID_GRAMMAR.md).
Whitney, Zalizniak, roots, dictionary entries, and corpus loci retain their own identifiers.
The graph joins them; it does not renumber them.

Minimum topic record:

```yaml
id: subject:grammar-lab:samprasarana
schema_version: 1.0.0
status: published
title_ru: Сампрасарана
aliases:
  ru: [сампрасарана, вокализация сонанта]
  deva: [सम्प्रसारण]
  iast: [samprasāraṇa]
  slp1: [samprasAraRa]
summary_ru: "..."
prerequisites: [subject:grammar-lab:ablaut-grades]
difficulty: intermediate
sources: []
dictionary_evidence: []
corpus_evidence: []
exercise_ids: []
provenance: {}
```

Every source edge normalizes to the Type-D record fields: `anchor_type`, `anchor_id`,
`anchor_key_slp1`, `target_locus`, `link_type`, `source_dataset`, `match_method`, `confidence`,
`evidence_count`, and `date`. A Zalizniak anchor must copy a stable section/record identifier
from its owning work; if an owning work lacks one, G1 creates and validates a deterministic
section-locus registry before publishing that edge.

## 3. SanskritGrammar source and export layout

| Path | Purpose |
|---|---|
| `data/grammar_lab/topics/*.yml` | Curated topic source records |
| `data/grammar_lab/exercises/*.yml` | Curated and approved/generated exercise records |
| `data/grammar_lab/schemas/*.json` | JSON Schemas for topics, links, evidence and exercises |
| `data/grammar_lab/review/*.json` | Deterministic sample manifests and decisions; no private student data |
| `data/grammar_lab/export/grammar_lab.json` | Compiled consumer bundle |
| `data/grammar_lab/export/typed_links.tsv` | Interoperable Type-D edge table |
| `data/grammar_lab/export/topic_vectors.json` | Pinned-model topic vectors and model metadata |
| `data/grammar_lab/export/manifest.json` | Semver, hashes, generator and source snapshot provenance |
| `scripts/build_grammar_lab.py` | Build and `--check` entry point |
| `scripts/grammar_lab_embed.py` | Pinned offline vector build/query parity tool |

The bundle includes concise public-safe summaries and evidence, not bulk source texts. Removing
or renaming a required field is a major schema bump. All builds are deterministic except an
explicit manifest timestamp excluded from content-hash comparison.

## 4. Evidence contract

A `published` topic requires:

1. at least one Whitney anchor and one Zalizniak anchor;
2. at least one dictionary/root evidence link;
3. at least one corpus attestation or a structured `not_attested` result naming corpus snapshot,
   query and limitation;
4. provenance for every quotation, paraphrase, number and derived join;
5. at least one publishable exercise;
6. aliases in every supported search script where a legitimate form exists.

If any scholarly requirement is ambiguous, status becomes `needs_review`; the topic is omitted
from the publishable bundle but retained in the authoring tree with its reason.

## 5. Systema import and learner model

Systema imports the bundle idempotently into tables conceptually equivalent to:

- `grammar_topics` and `grammar_topic_sources`;
- `grammar_exercises` and `grammar_exercise_versions`;
- `grammar_bookmarks` and `grammar_topic_views`;
- `grammar_attempts` and `grammar_mastery`;
- `grammar_entitlements` (or the existing general capability mechanism if audit proves it fits).

The source bundle is authoritative for topic content. Systema owns only consumer/cache state and
learner state. Re-import updates by stable ID and content hash, never deletes learner history,
and retires removed content through an explicit tombstone/status transition.

## 6. Offline hybrid search

Search combines:

1. normalized exact/prefix/token retrieval across Russian, Devanagari, IAST and SLP1 aliases;
2. BM25, reusing the house pure-PHP retrieval pattern;
3. cosine similarity over a pinned multilingual embedding model;
4. a deterministic fusion score whose weights are frozen by the evaluation set.

SanskritGrammar precomputes topic vectors. Systema runs a local, network-independent embedding
sidecar using the same pinned model for query vectors; the 25–40-topic corpus needs no external
vector database. The semantic route is feature-gated until model parity and Recall@5 pass. If
the sidecar cannot be deployed, BM25 remains available and the semantic flag stays OFF—no paid
API is silently substituted.

Search results expose title, snippet, source labels and topic ID only after entitlement. Public
landing pages may expose marketing metadata, never protected records or vectors.

## 7. Exercises, FSRS and recommendation

Exercise records carry `risk_class`:

- `deterministic`: normalization, classification, matching or selection with a mechanically
  checkable answer;
- `interpretive`: explanation, scholarly choice, disputed classification or free composition.

Deterministic candidates may publish after schema/domain validators, reproducible 20% sampling,
and a stored rollback version. Interpretive candidates require prior expert approval. Published
items are projected into the existing Systema SRS/FSRS machinery; no scheduler is rebuilt.

The Wave-1 recommender is transparent and rule-based: prerequisites not mastered → weakest
eligible topic → overdue SRS evidence → next difficulty band. It records the reason displayed
to the learner. No opaque adaptive model is introduced in the pilot.

## 8. Entitlement boundary

Application code asks one question: `canUse('grammar_lab')`. The resolver may be satisfied by:

- ownership of a selected course/tariff;
- an active standalone Grammar Lab subscription;
- a time-bounded admin/pilot grant.

Payment providers create lifecycle events, but UI/controllers never infer access directly from
gateway-specific rows. Revocation and expiry are explicit and tested. All product routes,
search endpoints, imported protected payloads, SRS decks and recommendation endpoints use the
same resolver.

## 9. Build-versus-reuse verdicts

| Piece | Verdict |
|---|---|
| Stable concordance IDs | Reuse Type-D; add only Grammar Lab subject loci and missing deterministic Zalizniak section loci |
| Sanskrit normalization | Reuse shared utilities |
| Root/dictionary joins | Reuse WhitneyRoots/MWS/kosha assets |
| Corpus evidence | Consume pinned DCS/VisualDCS assets |
| Export | Extend the versioned static-export precedent |
| Search | Reuse BM25 pattern; add only the local multilingual vector layer |
| SRS | Reuse Systema FSRS and deck/card models |
| Recommendations | Add a thin explainable policy over existing attempts/mastery |
| Payments/access | Reuse billing/tariff/access infrastructure behind a new provider-independent capability |

---

_Dr. Mārcis Gasūns_
