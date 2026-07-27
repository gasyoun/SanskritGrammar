# Monthly errata maintenance — runbook

_Created: 27-07-2026 · Last updated: 27-07-2026_

> **Fence, read first:** `<Book>/ERRATA.mdx`, the root `ERRATA.md` index, and
> `<Book>/ERRATA_PRINT_SHEET.html` are **generated** — never hand-edit them. The only
> hand-edited source is `<Book>/errata.yml`. For the full mechanics (entry shape, tier
> model, id/checksum computation) run [`/errata`](https://github.com/gasyoun/claude-config/blob/main/commands/errata.md)
> instead of re-deriving them here — this page is the monthly-cadence checklist, not the
> skill's full depth.

This is the recurring maintenance pass referenced by `.ai_state.md` Phase 3. Run it
roughly monthly, or whenever a book's `errata.yml` gains entries, a printed
errata/opechatki sheet surfaces, or a `CHANGELOG.md` entry fixes a cataloged erratum.

## Phase 1A — printed errata sheet intake

When a new printed errata/opechatki sheet is transcribed for a book (see
[`KnauerFrazy_1908/errata.yml`](https://github.com/gasyoun/SanskritGrammar/blob/main/KnauerFrazy_1908/errata.yml)
for the canonical entry shape):

1. Add entries to that book's `errata.yml` under `entries:` — `{ page, line, read,
   instead, found_by, date_added, fixed_in?, note? }`. `id` / `date` / `checksum` are
   never hand-authored.
2. Regenerate:
   ```
   npm run errata
   ```
   (wraps `python scripts/build_errata.py` — regenerates every book's `ERRATA.mdx` +
   the root `ERRATA.md` index; pass one book directory as an argument to regenerate
   only that book).
3. If the sheet should also ship as a printable insert:
   ```
   npm run errata:print
   ```
   (wraps `python scripts/build_errata_print_sheet.py` — only books with a non-empty
   `errata.yml` get a sheet; a stale sheet whose register has since emptied is removed
   automatically).

## Phase 1B — edition diff (books with no printed sheet)

For a book whose `errata.yml` has no printed source (currently: `ApteSyntax_1885`,
`KocherginaUchebnik_1998`, `ZalizniakKonspekt_2004` — see the live table below), errata
accrue by diffing the book's own text across git revisions:

```
python scripts/build_errata.py diff <Book> <old-git-ref> [<new-git-ref>]
```

This writes `<Book>/errata.candidates.yml` (read = new text, instead = old text, tagged
with the diff source + today's date) for a **human** to review. Fold reviewed
candidates into `entries:` in `errata.yml` by hand, then run `npm run errata` as above.
Never fold `errata.candidates.yml` straight into `errata.yml` unreviewed.

## Phase 3 — CHANGELOG `fixed_in` cross-check

`build_errata.py` cross-references each book's `CHANGELOG.md` against `errata.yml`:

- An entry carrying `fixed_in: vX.Y.Z` is rendered as fixed in `ERRATA.mdx`, and the
  version is confirmed to actually exist in that book's changelog.
- A changelog line that mentions the book plus a correction keyword (fix/correct/typo/
  etc.) without a matching `fixed_in` on any errata entry prints a reminder in the
  build output — that is the signal to go back and set `fixed_in` on the entry the
  changelog line actually resolved.

Run `npm run errata` and read the console output for these reminders as part of every
monthly pass — don't just check that the command exits 0.

## Book inventory (verify live — do not trust this table blindly)

Re-derive with:

```
python -c "
import re
from pathlib import Path
for p in sorted(Path('.').glob('*/errata.yml')):
    text = p.read_text(encoding='utf-8')
    n = len(re.findall(r'- \{ page:', text))
    print(f'{p.parent.name}: {n} entries')
"
```

As of 27-07-2026 (H1675):

| Book | `errata.yml` | Entries | Source |
|---|---|---|---|
| ApteSyntax_1885 | yes | 0 | edition-diff (no printed sheet catalogued) |
| BuhlerLeitfaden_1923 | yes | 8 | H797 claim-verification fallout |
| GasunsDhatu_2014 | yes | 93 | mixed (dissertation text + review passes) |
| KnauerFrazy_1908 | yes | 30 | 1908 print + later electronic-edition sheets |
| KocherginaUchebnik_1998 | yes | 0 | edition-diff (no printed sheet catalogued) |
| TolchelnikovTalmud_2026 | yes | 3 | H1514 schema demonstration — not real corrections |
| ZalizniakKonspekt_2004 | yes | 0 | edition-diff (no printed sheet catalogued) |
| ZalizniakOcherk_1978 | yes | 2 | H978 1978-crosswalk encoding pass |
| WhitneyGrammar_1889 | **no** | — | generated from [WhitneyRoots](https://github.com/gasyoun/WhitneyRoots) — fix the generator/source, not here |
| ZalizniakMorphology_1975 | **no** | — | not yet wired into the errata pipeline |
| Concordance / SubjectConcordance | **no** | — | research layer, not book text — out of scope for this runbook |

Filling the empty `errata.yml`s from new printed sheets and wiring in
`ZalizniakMorphology_1975` are explicitly **out of scope** for this runbook (see
Non-goals) — this table exists so the monthly pass knows current state without
re-deriving it, not as a task list.

## Generated-file fence (repeat)

`ERRATA.mdx` (per book), the root `ERRATA.md`, and `ERRATA_PRINT_SHEET.html` are all
**generated**. If a correction is wrong, fix `errata.yml` and regenerate — never patch
the `.mdx`/`.md`/`.html` output directly; the next `npm run errata` silently overwrites
any hand edit there.

## Full skill depth

For anything beyond this monthly checklist (entry-shape edge cases, the three-tier
ACL erratum/revision/retraction model, id/checksum mechanics), use
[`/errata`](https://github.com/gasyoun/claude-config/blob/main/commands/errata.md)
rather than re-deriving it from the script source.

---

_Dr. Mārcis Gasūns_
