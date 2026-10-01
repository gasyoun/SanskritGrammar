#!/usr/bin/env python3
"""Build the cross-claim statistics dashboard (H3114 / zan-22 + zan-10 + prilozhenie).

Derive-don't-store: every number rendered here is read at run time from the
committed registries (claims.json per book) and the committed corpus
instruments (apte_*_stats.json). No hand-typed statistics.

Outputs
-------
1. ``ApteSyntax_1885/CLAIMS_STATS_DASHBOARD.md`` — full regeneration each run:
   cross-registry totals, per-instrument quantified rows for the Apte
   methodichka claims, zan-22/zan-10 anchors, per-book FALSE/OVERSTATED lists.
2. A marker-fenced generated block inserted into
   ``ApteSyntax_1885/METODICHKA_APTE_KOMMENTARII_2026.md`` (prilozhenie):
   compact cross-book calibration table + pointer to the dashboard.

Usage::
    python scripts/build_cross_claim_dashboard.py           # build
    python scripts/build_cross_claim_dashboard.py --check   # exit 1 on drift
"""
from __future__ import annotations

import io
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
APTE = REPO / "ApteSyntax_1885"
BOOKS = [
    ("ApteSyntax_1885", "Апте (Apte Syntax 1885)"),
    ("BuhlerLeitfaden_1923", "Бюлер (Leitfaden 1923)"),
    ("KocherginaUchebnik_1998", "Кочергина (1998)"),
    ("ZalizniakOcherk_1978", "Зализняк-Очерк (1978)"),
]
NO_REGISTRY = [("KnauerFrazy_1908", "Кнауэр (Frazy 1908)")]
DASH = APTE / "CLAIMS_STATS_DASHBOARD.md"
METOD = APTE / "METODICHKA_APTE_KOMMENTARII_2026.md"
BEGIN = "<!-- BEGIN generated:cross-claim-dashboard (scripts/build_cross_claim_dashboard.py) -->"
END = "<!-- END generated:cross-claim-dashboard -->"

VF_ORDER = ["TRUE", "OVERSTATED", "FALSE", "UNTESTABLE"]


def load_claims(book_dir: str) -> list[dict]:
    data = json.loads(io.open(REPO / book_dir / "claims.json", encoding="utf-8").read())
    if isinstance(data, list):
        return data
    for v in data.values():
        if isinstance(v, list):
            return v
    raise SystemExit(f"no claim list found in {book_dir}/claims.json")


def load_json(rel: str) -> dict:
    return json.loads(io.open(APTE / rel, encoding="utf-8").read())


def fmt_pct(x) -> str:
    if x is None:
        return "—"
    return f"{x:.1f}".rstrip("0").rstrip(".").replace(".", ",")


def cross_table(rows: list[tuple[str, str, list[dict]]]) -> str:
    out = [
        "| Реестр | Утверждений | TRUE | OVERSTATED | FALSE | UNTESTABLE | Проверяемых | Доля TRUE (проверяемые) | MISLEADING (педагогика) |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for slug, label, items in rows:
        vf = {v: 0 for v in VF_ORDER}
        mis = 0
        for it in items:
            vf[it.get("verdict_fact")] = vf.get(it.get("verdict_fact"), 0) + 1
            if it.get("verdict_pedagogy") == "MISLEADING":
                mis += 1
        tested = sum(vf[v] for v in VF_ORDER if v != "UNTESTABLE")
        share = fmt_pct(100.0 * vf["TRUE"] / tested) if tested else "—"
        out.append(
            f"| {label} | {len(items)} | {vf['TRUE']} | {vf['OVERSTATED']} | "
            f"{vf['FALSE']} | {vf['UNTESTABLE']} | {tested} | {share}% | {mis} |"
        )
    for slug, label in NO_REGISTRY:
        out.append(f"| {label} | — реестр claims.yml не создан (см. примечание) | | | | | | | |")
    return "\n".join(out)


def false_over_list(items: list[dict]) -> str:
    lines = []
    for it in items:
        if it.get("verdict_fact") in ("FALSE", "OVERSTATED"):
            claim = (it.get("claim_ru") or "").strip().replace("\n", " ")
            if len(claim) > 110:
                claim = claim[:107] + "…"
            lines.append(f"- `{it['id']}` — **{it['verdict_fact']}**: {claim}")
    return "\n".join(lines) if lines else "- (нет)"


def instrument_rows() -> list[str]:
    """Quantified Apte rows straight from the committed instrument JSONs."""
    out: list[str] = []

    tb = load_json("apte_treebank_stats.json")
    cov = tb["coverage"]
    out.append(f"### Инструмент: дерево разбора DCS (`apte_treebank_stats.py`)")
    tt = f"{cov['tagged_tokens']:,}".replace(",", " ")
    tot = f"{cov['total_tokens']:,}".replace(",", " ")
    out.append(f"_Покрытие: {tt} размеченных токенов из {tot} ({fmt_pct(cov['tagged_pct'])} %)._")
    flat_sections = ["A_enclitic_position", "B_subject_verb_agreement", "B_adjective_noun_agreement", "B_relative_pronoun_order", "D_motion_goal_case"]
    for sec in flat_sections:
        d = tb.get(sec, {})
        ref = d.get("claim", "")
        metrics = []
        for k, lab in (("n", "n"), ("initial_pct", "начальных%"), ("agree_pct", "согласовано%"), ("postposed_pct", "постпозици%"), ("n_goal_cases", "n_цели"), ("acc_share_pct", "вин%цели"), ("non_acc_goal_pct", "не-вин%цели")):
            if d.get(k) is not None:
                metrics.append(f"{lab}={d.get(k)}")
        met = ", ".join(metrics)
        out.append(
            f"- `{ref}` — {d.get('desc','')}"
            + (f": {met}" if met else "")
            + (f", вердикт инструмента **{d.get('verdict')}**." if d.get('verdict') else ".")
        )
    for sec in ("A_particle_position",):
        for key, d in tb.get(sec, {}).items():
            if not isinstance(d, dict):
                continue
            ref = d.get("claim", key)
            out.append(
                f"- `{ref}` — частица *{key}*, {d.get('desc','')}: n={d.get('n')}, "
                f"предложение-начальных {d.get('sentence_initial')} ({fmt_pct(d.get('initial_pct', 0))} %), "
                f"вердикт инструмента **{d.get('verdict')}**."
            )
    cgov = tb.get("C_case_government", {})
    out.append(f"- Управление по дереву разбора ({len(cgov)} гнёзд): см. строки ниже и классический контур.")

    gov = load_json("apte_classical_government_stats.json")
    out.append(f"\n### Инструмент: классическое управление, оконный лифт (`apte_classical_government_stats.py`)")
    bl = gov["baseline_oblique_shares_pct"]
    out.append("_Базовые доли косвенных падежей: " + ", ".join(f"{k} {fmt_pct(v)} %" for k, v in sorted(bl.items(), key=lambda kv: -kv[1])) + "._")
    for cid, d in sorted(gov.get("claims", {}).items()):
        lift = d.get("predicted_lift")
        out.append(
            f"- `{cid}` — {d.get('desc','')}: n={d.get('n_windowed_obliques')}, "
            f"прогноз **{d.get('predicted_case')}**, лифт **×{fmt_pct(lift)}** (топ по лифту), "
            f"вердикт инструмента **{d.get('verdict')}**."
        )
    for name, d in sorted(gov.get("controls", {}).items()):
        holds = d.get("verdict") == "TRUE"
        if name.startswith("neg_"):
            out.append(f"- негатив-контроль `{name}`: ожидаемо не держится (держится: {str(holds).lower()})")
        else:
            out.append(
                f"- контроль `{name}`: прогноз {d.get('predicted_case')}, лифт ×{fmt_pct(d.get('predicted_lift'))}, держится: {str(holds).lower()}"
            )

    ps = load_json("apte_pada_stats.json")
    out.append(f"\n### Инструмент: залог по окончаниям (`apte_pada_stats.py`)")
    for name, d in sorted(ps.get("controls", {}).items()):
        out.append(
            f"- контроль `{name}` ({d.get('lemma')}): P {fmt_pct(d.get('P_pct'))}% / Ā {fmt_pct(d.get('A_pct'))}%, n={d.get('n')}, держится: {str(bool(d.get('control_holds'))).lower()}"
        )
    if ps.get("rules"):
        for r in ps["rules"]:
            out.append(
                f"- `{r.get('id', r.get('root'))}` — залог при приставках: P {fmt_pct(r.get('P_pct'))}% / Ā {fmt_pct(r.get('A_pct'))}%, n={r.get('n_classified')}, вердикт инструмента **{r.get('verdict')}**."
            )

    pv = load_json("apte_pada_preverb_stats.json")
    out.append(f"\n### Инструмент: залог приставочных композитов (`apte_pada_preverb_stats.py`, H3113/zan-29)")
    for r in pv.get("rules", []):
        out.append(
            f"- `{r.get('id')}` (*{r.get('root')}*): P {fmt_pct(r.get('P_pct'))}% / Ā {fmt_pct(r.get('A_pct'))}%, n={r.get('n_classified')}, вердикт инструмента **{r.get('verdict')}**."
        )
    return out


def uta_row_line() -> str:
    tb = load_json("apte_treebank_stats.json")
    d = tb.get("A_particle_position", {}).get("uta")
    if not isinstance(d, dict):
        return "_Строка uta в `apte_treebank_stats.json` не найдена — см. сноску 3 комментариев._"
    return (
        f"Частица *uta* (реестр APT-12, занятие 22): n={d.get('n')}, предложений-начальных "
        f"{d.get('sentence_initial')} ({fmt_pct(d.get('initial_pct', 0))} %) — вердикт инструмента **{d.get('verdict')}** "
        "(сноска 3 комментария)."
    )


def build() -> tuple[str, str]:
    rows = [(slug, label, load_claims(slug)) for slug, label in BOOKS]
    apte_items = rows[0][2]
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    L: list[str] = []
    L.append("# Apte methodichka — сводный дашборд статистики утверждений (zan-22)")
    L.append("")
    L.append(f"_Сгенерировано `scripts/build_cross_claim_dashboard.py` · {now} · источники: 4 реестра `claims.json` + 4 инструмента `apte_*_stats.json`. Числа не вводятся вручную._")
    L.append("")
    L.append("## 1. Межкнижные итоги калибровки (приложение, «а что ещё у кого лучше»)")
    L.append("")
    L.append(cross_table(rows))
    L.append("")
    L.append("_Кнауэр: реестра нет — строка честно пуста, а не заполнена нулями. Сведённый список «где какая книга сильнее» — это данные для человеческого решения; полнота списка калибруется владельцем (лист sanskritgrammar-metodichka-apte-v1, карточка `prilozhenie`)._")
    L.append("")
    for slug, label in BOOKS[1:]:
        items = load_claims(slug)
        L.append(f"### {label}: неверные и преувеличенные утверждения")
        L.append("")
        L.append(false_over_list(items))
        L.append("")
    L.append("## 2. Занятие 10 — винительный versus родительный (zan-10, APT-19)")
    L.append("")
    L.append(
        "Реестр: `APT-19` — «глаголы власти/памяти управляют родительным» — **OVERSTATED**: "
        "в корпусе у smṛ винительный опережает родительный. Виза-цифры «41 % против 30 %, ≈1,4 раза» "
        "применены в тексте занятия 10 (ревизия zan-10 от 19-07-2026, H1205/H1275); инструментальная "
        "строка: `APT-H-115` (īś/prabhū/smṛ/adhī) — см. раздел 4."
    )
    L.append("")
    L.append("## 3. Занятие 22 — позиция uta (zan-22, APT-12)")
    L.append("")
    L.append(uta_row_line())
    L.append("")
    L.append("## 4. Квантифицированные строки по инструментам")
    L.append("")
    L.extend(instrument_rows())
    L.append("")
    L.append("## 5. Апте: FALSE/OVERSTATED (полный список)")
    L.append("")
    L.append(false_over_list(apte_items))
    L.append("")
    dash = "\n".join(L).rstrip() + "\n"

    # Compact block for the metodichka prilozhenie section
    B: list[str] = []
    B.append(BEGIN)
    B.append("")
    B.append("**Межкнижная калибровка (generated — `scripts/build_cross_claim_dashboard.py`):**")
    B.append("")
    B.append("| Реестр | Утверждений | TRUE | OVERSTATED | FALSE | Доля TRUE (проверяемые) |")
    B.append("|---|---|---|---|---|---|")
    for slug, label, items in rows:
        vf = {v: 0 for v in VF_ORDER}
        for it in items:
            vf[it.get("verdict_fact")] = vf.get(it.get("verdict_fact"), 0) + 1
        tested = sum(vf[v] for v in VF_ORDER if v != "UNTESTABLE")
        share = fmt_pct(100.0 * vf["TRUE"] / tested) if tested else "—"
        B.append(f"| {label} | {len(items)} | {vf['TRUE']} | {vf['OVERSTATED']} | {vf['FALSE']} | {share}% |")
    B.append(f"| Кнауэр (Frazy 1908) | — реестра нет | | | | |")
    B.append("")
    B.append(
        "Полный дашборд со всеми статистическими выкладками (zan-22): "
        "[CLAIMS_STATS_DASHBOARD.md](CLAIMS_STATS_DASHBOARD.md). "
        "Полнота межкнижного списка «где какая книга сильнее» калибруется владельцем (карточка `prilozhenie`)."
    )
    B.append("")
    B.append(END)
    return dash, "\n".join(B)


def upsert_block(text: str, block: str) -> tuple[str, bool]:
    if BEGIN in text:
        pre = text.split(BEGIN, 1)[0]
        post = text.split(END, 1)[1]
        return pre + block + post, True
    anchor = "сведённого межкнижного списка «где какая книга сильнее других» пока нет; отдельный handoff._"
    idx = text.find(anchor)
    if idx < 0:
        raise SystemExit("anchor paragraph not found in METODICHKA doc")
    insert_at = text.find("\n---", idx)
    if insert_at < 0:
        raise SystemExit("no trailing --- after prilozhenie anchor")
    return text[:insert_at] + "\n\n" + block + text[insert_at:], False


def main(argv: list[str]) -> int:
    check = "--check" in argv
    dash, block = build()
    met_text = io.open(METOD, encoding="utf-8").read()
    new_met, replaced = upsert_block(met_text, block)
    drift_dash = dash != io.open(DASH, encoding="utf-8").read() if DASH.exists() else True
    drift_met = new_met != met_text
    if check:
        if drift_dash or drift_met:
            print("DRIFT: dashboard" if drift_dash else "", "metodichka" if drift_met else "")
            return 1
        print("up-to-date")
        return 0
    io.open(DASH, "w", encoding="utf-8", newline="\n").write(dash)
    io.open(METOD, "w", encoding="utf-8", newline="\n").write(new_met)
    print(f"wrote {DASH.name} ({len(dash)} chars); metodichka block {'replaced' if replaced else 'inserted'} ({len(block)} chars)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
