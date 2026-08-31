# Metodichka artifact shape — the five documents a textbook line owes

_Created: 30-08-2026 · Last updated: 31-08-2026_

Each digitised textbook line in this repo carries a Russian-language *metodichka* —
a teaching apparatus wrapped around the source book. The apparatus is not one file
but **five**, each answering a different question for a different reader. This page
is the convention and the live coverage matrix; it exists so the shape survives the
handoffs that build it ([FINDINGS §619](https://github.com/gasyoun/Uprava/blob/main/FINDINGS.md) class — a taxonomy
stranded inside a handoff disappears when that handoff is archived).

## The five artifacts

| Artifact | Filename pattern | Answers | Reader |
|---|---|---|---|
| **COMPANION** | `METODICHKA_<LINE>_COMPANION_2026.md` | How is this book taught — sequence, pacing, what to skip | the teacher, before the course |
| **CORPUS_LAYER** | `METODICHKA_<LINE>_CORPUS_LAYER_2026.md` | Where does the book's material sit in the attested corpus | the compiler wiring the book to DCS / dictionary data |
| **KOMMENTARII** | `METODICHKA_<LINE>_[V1_]KOMMENTARII_2026.md` | What does this passage actually say, and where is the book wrong or dated | the teacher, mid-lesson |
| **OTSYLKI** | `METODICHKA_<LINE>_V1_OTSYLKI_2026.md` | Where do I look this up — dictionary and corpus cross-references | the student following a thread outward |
| **UPRAZHNENIIA** | `METODICHKA_<LINE>_V1_UPRAZHNENIIA_2026.md` | What does the student *do* | the student, practising |

Two rules that are not obvious from the filenames:

1. **Exercises are drawn, never invented.** UPRAZHNENIIA items come from the source
   book's own material, each citing the paragraph it came from. A metodichka that
   invents drills stops being an apparatus for *that* book.
2. **Every `s.v.` is a live link.** OTSYLKI (and any dictionary reference elsewhere)
   resolves to a Cologne getword URL on the SLP1 key — a standing house rule across
   this org, not a nicety local to one line.

A long-lived COMPANION also carries a sibling `<name>.meta.md`.

## Coverage — measured 31-08-2026 (Apte row closed by H3739, Bühler row by H3804)

| Line | COMPANION | CORPUS_LAYER | KOMMENTARII | OTSYLKI | UPRAZHNENIIA |
|---|---|---|---|---|---|
| Kochergina — [`KocherginaUchebnik_1998/`](https://github.com/gasyoun/SanskritGrammar/tree/main/KocherginaUchebnik_1998) | yes | yes | yes (V1) | yes (V1) | yes (V1) |
| Apte — [`ApteSyntax_1885/`](https://github.com/gasyoun/SanskritGrammar/tree/main/ApteSyntax_1885) | yes (+meta) | yes | yes | yes (V1) | yes (V1) |
| Bühler — [`BuhlerLeitfaden_1923/`](https://github.com/gasyoun/SanskritGrammar/tree/main/BuhlerLeitfaden_1923) | yes (+meta) | yes | yes (V1) | yes (V1) | yes (V1) |

**Kochergina is the reference implementation.** When building a missing artifact for
another line, read the Kochergina file of that kind first and mirror its section order
and register rather than inventing a layout — the value of the shape is that a teacher
moving between lines finds the same thing in the same place.

## In flight

- **H3739 — EXECUTED 31-08-2026** (Fable 5, `claude-fable-5`): the Apte row is complete —
  [COMPANION](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/METODICHKA_APTE_COMPANION_2026.md)
  (+ [metadoc](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/METODICHKA_APTE_COMPANION_2026.meta.md)),
  [OTSYLKI](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/METODICHKA_APTE_V1_OTSYLKI_2026.md),
  [UPRAZHNENIIA](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/METODICHKA_APTE_V1_UPRAZHNENIIA_2026.md).
  **The shape transferred cleanly** — the one friction point was раздел numbering (the
  Apte corpus layer had already claimed «раздел II», so отсылки/упражнения are III/IV
  against Kochergina's II/III; recorded as Decision D in the Apte companion).
- **H3804 — EXECUTED 31-08-2026** (Fable 5, `claude-fable-5`): the Bühler row is complete
  on the Apte numbering (II corpus layer · III отсылки · IV упражнения) —
  [CORPUS_LAYER](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/METODICHKA_BUHLER_CORPUS_LAYER_2026.md)
  (31 lemmas incl. the causative-as-lemma note, `corpus_layer/` data + the shared
  build/test harness extended to a third book),
  [OTSYLKI](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/METODICHKA_BUHLER_V1_OTSYLKI_2026.md)
  (MW s.v. links — keys verified offline against csl-orig during a portal per-IP
  throttle window — plus Scherzl pages from the line's own government lexicon),
  [UPRAZHNENIIA](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/METODICHKA_BUHLER_V1_UPRAZHNENIIA_2026.md)
  (exercises drawn from Bühler's own lessons, Decision D of the Bühler companion now
  delivered).
- **H3386** (Fable 5, 🟢1 trivial) — a separate job on the same line: *applying* the
  voted `review/sanskritgrammar-metodichka-apte-v1_17.07.26_decisions.json` verdicts.
  H3739 consumed those verdicts as constraints (8 approvals, 1 null — nothing rejected);
  it did not do H3386's work.

Update the coverage table in the same pass as any artifact that lands.

_Dr. Mārcis Gasūns_
