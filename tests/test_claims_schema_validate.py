"""Wires scripts/claims_schema_validate.py into CI (H1842).

Structural twin of tests/test_article_validate.py for the six book claim
registers. Ensures the schema + validator reject invented fields/enums and
that every committed */claims.yml validates clean without content edits.
"""
import copy

import claims_schema_validate as csv_


def test_self_test():
    assert csv_.self_test() == 0


def test_all_real_claims_yml_pass():
    targets = csv_.discover_claims_files()
    assert targets, "no */claims.yml files found — the glob would be a silent no-op"
    assert len(targets) >= 6, f"expected the six book registers, found {len(targets)}: {targets}"
    failures = []
    for p in targets:
        import yaml
        raw = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        errors = csv_.validate(raw)
        if errors:
            failures.append((str(p), errors))
    assert not failures, "\n".join(f"{p}: {e}" for p, e in failures)


def test_bad_verdict_fact_rejected():
    m = csv_.minimal_fixture()
    m["entries"][0]["verdict_fact"] = "MAYBE"
    errors = csv_.validate(m)
    assert errors, "invented verdict_fact must fail"


def test_unknown_entry_key_rejected():
    m = csv_.minimal_fixture()
    m["entries"][0]["invented_category"] = "nope"
    errors = csv_.validate(m)
    assert errors, "unknown entry key must fail (no invented fields)"


def test_duplicate_id_rejected():
    m = csv_.minimal_fixture()
    m["entries"].append(copy.deepcopy(m["entries"][0]))
    errors = csv_.validate(m)
    assert any("duplicate" in e.lower() for e in errors), errors


def test_yaml_boolean_true_false_coerce():
    m = csv_.minimal_fixture()
    m["entries"][0]["verdict_fact"] = True
    assert not csv_.validate(m)
    m["entries"][0]["verdict_fact"] = False
    assert not csv_.validate(m)
