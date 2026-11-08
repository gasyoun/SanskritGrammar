# data/ud_sanskrit — UD_Sanskrit-UFAL external gold layer (H6842)

DATA-ONLY mirror of the UD_Sanskrit-UFAL CoNLL-U treebank, used as an external
gold layer for dependency/lemma probes against the claim registers
(`claims.yml` in this directory, probed by [`tools/verify_claims_ud.py`](../../tools/verify_claims_ud.py)).

## Provenance

- Upstream: [UniversalDependencies/UD_Sanskrit-UFAL](https://github.com/UniversalDependencies/UD_Sanskrit-UFAL) (mirror-only; upstream untouched, no PRs back).
- File: `sa_ufal-ud-test.conllu`, mirrored byte-exact from upstream `master`
  at commit `80f88c8bb3c933deb272bb7a0b7683352134f57e`, fetched 22-10-2026.
- Release state: the treebank's last substantive annotation change is v2.2
  (2018-07-01, per upstream README changelog); the official LINDAT release
  bundle was unreachable at fetch time (3 retries across endpoints), so the
  GitHub master snapshot is the mirror source. Verifier: re-fetch the upstream
  blob and diff — it must be byte-identical.
- Content: Pañcatantra (preface + start of Mitrabheda), 230 sentences.
- Annotation: UD v2 guidelines; lemmas/UPOS/Features/Relations = manual native.

## Licence facts (recorded, H6842 acceptance)

- Upstream repo licence metadata: NOASSERTION (per GitHub licence API);
  the treebank data itself is **CC BY-SA 4.0** per the upstream README
  machine-readable block and `LICENSE.txt`
  (<http://creativecommons.org/licenses/by-sa/4.0/legalcode>).
- No GPL vendoring; the file is mirrored verbatim with this provenance note as
  the required attribution + share-alike pointer.

## Schema label (mandatory for cross-schema comparison)

Every measurement taken on this gold carries the **UD** label: dependency
relations are **UD v2** `DEPREL` values (root, nsubj, obj, conj, …), lemmas are
**UD lemma** column values (Devanagari), UPOS is the **UD v2** 17-tag set. Our
claim registers speak Paninian/karaka-DCST terms — see the mapping statement in
[`claims.yml`](claims.yml) and the dated report
[`docs/REPORT_UD_SANSKRIT_GOLD_PROBES_22-10-2026.md`](../../docs/REPORT_UD_SANSKRIT_GOLD_PROBES_22-10-2026.md);
cross-schema numbers without the UD label are invalid (wheel dossier rule).
