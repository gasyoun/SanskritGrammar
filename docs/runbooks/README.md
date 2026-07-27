# Runbooks — SanskritGrammar operator index

_Created: 27-07-2026 · Last updated: 28-07-2026_

## Purpose

One index of every standing **operator runbook** in this repo — a durable how-to for a
repeatable ops cycle, distinct from a one-shot handoff. Runbooks are authored once (by the
owning handoff) and then consumed by humans and agents every time the cycle repeats; they are
not re-authored per run.

## Audience

- Humans running the RQ4 pilot, methodichka visa-apply pass, monthly errata/claims
  maintenance, or a Sangram freeze-exit.
- Agents executing the pedagogy export → Systema hop, or picking up a suite sibling
  handoff (H1672–H1677) that is still queued.

## Suite provenance

This suite was minted as H1672–H1677 (26-07-2026) off the wave-1 last-mile plan
([`docs/PLAN_SANSKRITGRAMMAR_PEDAGOGY_LAST_MILE_2026H2.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/PLAN_SANSKRITGRAMMAR_PEDAGOGY_LAST_MILE_2026H2.md)).
H1677 (this index) is the hub + hygiene handoff — it does not author runbook bodies owned by
siblings.

## Index

| Runbook | Status | Owning handoff | What it covers |
|---|---|---|---|
| [`RQ4_GO_LIVE_HUMAN.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/runbooks/RQ4_GO_LIVE_HUMAN.md) | ✅ merged | [H1672](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1672-Sonnet_SanskritGrammar_runbook-rq4-go-live-human_26.07.26.md) | Human-operator checklist for the RQ4 pilot (n≈5) go-live: preflight, flag-flip sequencing, retention path, stop rules. |
| [`PEDAGOGY_EXPORT_HOP.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/runbooks/PEDAGOGY_EXPORT_HOP.md) | ✅ merged | [H1673](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1673-Sonnet_SanskritGrammar_runbook-pedagogy-export-hop_26.07.26.md) | Pedagogy export → Systema vendor → smoke cycle (build → `--check` → sync → RQ4 smoke test), flag-OFF/rights fences, failure table. |
| [`METHODICHKA_VISA_APPLY.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/runbooks/METHODICHKA_VISA_APPLY.md) | ✅ merged | [H1674](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1674-Sonnet_SanskritGrammar_runbook-methodichka-visa-apply_26.07.26.md) | Methodichka residual visa-apply checklist runbook (procedure; apply itself remains H1454/H1615). |
| (monthly errata + claims maintenance one-pager) | 🟡 pending handoff | [H1675](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1675-Sonnet_SanskritGrammar_runbook-monthly-errata-claims_26.07.26.md) | Monthly `npm run errata` / `npm run claims` maintenance cycle. |
| (Sangram freeze-exit operator runbook) | 🟡 pending handoff | [H1676](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1676-Sonnet_SanskritGrammar_runbook-sangram-freeze-exit_26.07.26.md) | Sangram freeze-exit procedure (zero-survivors = no review sheet, per H1614). |

Rows for H1675–H1676 will get their filename + a full-blob-URL link and flip to ✅ merged as
each sibling PR lands — update this table in the same pass as that merge, do not re-author the
runbook body here.

## Related

- [`docs/ROADMAP_SANSKRITGRAMMAR_PEDAGOGY_LAST_MILE_2026H2.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/ROADMAP_SANSKRITGRAMMAR_PEDAGOGY_LAST_MILE_2026H2.md) + its [metadoc](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/ROADMAP_SANSKRITGRAMMAR_PEDAGOGY_LAST_MILE_2026H2.meta.md)
- [`docs/PLAN_SANSKRITGRAMMAR_PEDAGOGY_LAST_MILE_2026H2.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/PLAN_SANSKRITGRAMMAR_PEDAGOGY_LAST_MILE_2026H2.md)

---

_Dr. Mārcis Gasūns_
