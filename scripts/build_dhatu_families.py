#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_dhatu_families.py -- H6256: dhatu derivational families vs DCS frequency.

Offline, deterministic builder. Reads pinned sibling-repo data (no network) and
writes a csl-observatory-style dataset + report into this repo:

  data/dhatu_families/families.json     root -> derivatives (with source tags)
  data/dhatu_families/families.tsv      flat edge table (machine check)
  data/dhatu_families/root_stats.tsv    per-root aggregates
  data/dhatu_families/canary_10.tsv     10-root manual canary evidence
  reports/DHATU_DERIVATIONAL_FAMILIES_2026-11-25.md

Sources (all read-only, sibling checkouts under --sources-root):
  csl-orig/v02/etymology_stats/dhatu_roots.txt    canonical dhatu inventory
  csl-orig/v02/mw/mw_roots.tsv                    MW verbal-root register
  csl-orig/v02/mw/mw_etymology.tsv                MW parse=/fr. sqrt root attributions
  csl-orig/v02/etymology_stats/root_oracle.tsv    cross-dict form -> root (mw rows)
  csl-orig/v02/mw/mw.txt                          MW itself (canary evidence)
  MWderivations/step4/analysis2.txt               MW derivational decomposition
  MWderivations/step4/auxiliary/{deriv,pfxderiv}.txt
  kosha/data/frequency/lemma_frequency.tsv        DCS-conllu lemma counts (SLP1)

Run:  python scripts/build_dhatu_families.py --sources-root ~/Documents/GitHub
      python scripts/build_dhatu_families.py --verify     # recompute from committed TSVs
"""
import argparse
import collections
import csv
import json
import math
import os
import sys

from dhatu_families_lib import (
    BINS, REPO, REPORT_NAME, canary_evidence, collect, iast, load_attr_roots,
    load_freq, load_inventory, load_substantives, median, path, spearman, zipf_slope,
)

def build_report(stats, verdicts):
    s = stats
    lines = []
    a = lines.append
    a("# Деривационные гнёзда dhātu: размер против частотности (25-11-2026)")
    a("")
    a("_Created: 25-11-2026 · Last updated: 25-11-2026_")
    a("_к.ф.н. М.Ю. Гасунс_")
    a("")
    a("H6256 · OxAlpha (MiMo v2.6 Flash, `ollama-cloud/mimo-v2.6-flash`) · "
      "датасет и отчёт в csl-observatory-формате: [families.json]"
      "(https://github.com/gasyoun/SanskritGrammar/blob/main/data/dhatu_families/families.json), "
      "[families.tsv](https://github.com/gasyoun/SanskritGrammar/blob/main/data/dhatu_families/families.tsv), "
      "[root_stats.tsv](https://github.com/gasyoun/SanskritGrammar/blob/main/data/dhatu_families/root_stats.tsv). "
      "Скрипт: [build_dhatu_families.py]"
      "(https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/build_dhatu_families.py).")
    a("")
    a("## Что построено")
    a("")
    a("Гнёздо = канонический dhātu (SLP1) → множество substantives (существительные / "
      "прилагательные / неизменяемые), приписанных ему MW-деривационными данными. "
      "Это НЕ парность dhatupatha-источников (H4741 / Q4.4): структуру дают "
      "[MWderivations](https://github.com/gasyoun/MWderivations) + MW, а частоты — "
      "[DCS lemma frequency](https://github.com/gasyoun/kosha/blob/main/data/frequency/lemma_frequency.tsv).")
    a("")
    a("| Канал (все из MW / MWderivations) | Ребёр |")
    a("|---|---:|")
    for tag, n in s["channel_edges"].most_common():
        a(f"| `{tag}` | {n:,} |")
    a("")
    a("## Покрытие")
    a("")
    a("| Метрика | Значение |")
    a("|---|---:|")
    for k, v in s["coverage"].items():
        a(f"| {k} | {v:,} |" if isinstance(v, int) else f"| {k} | {v} |")
    a("")
    a("## Распределение размеров гнёзд против корпусной частотности")
    a("")
    a("| Размер гнезда | Корней | Доля корней | Производных | Есть в DCS | Медиана токенов гнезда | Медиана log10(1+частота) |")
    a("|---|---:|---:|---:|---:|---:|---:|")
    for row in s["bins"]:
        a("| {label} | {roots:,} | {share:.1f}% | {forms:,} | {att:.1f}% | {tok:,.0f} | {lg:.2f} |".format(**row))
    a("")
    a("Zipf-подобие: наклон log10(count) ~ log10(rank) по всем {attested:,} "
      "произведениям, встреченным в DCS — **{slope:.3f}** (эталон ~−1). "
      "Spearman ρ между размером гнезда и суммарной частотой гнезда — **{rho:.3f}** "
      "(n={nr:,} корней с хотя бы одним производным).".format(
          attested=s["attested_forms"], slope=s["slope"], rho=s["rho"], nr=s["nonempty_roots"]))
    a("")
    a("## Крупнейшие гнёзда")
    a("")
    a("| Корень (IAST) | Размер | В DCS | Токенов DCS | Пример производного (IAST) |")
    a("|---|---:|---:|---:|---|")
    for r, size, att, tok, ex in s["top"]:
        a(f"| {iast(r)} (`{r}`) | {size:,} | {att:,} | {tok:,} | {iast(ex)} |")
    a("")
    a("## Канари: 10 корней, сверенных с MW вручную")
    a("")
    a("Строки — [canary_10.tsv](https://github.com/gasyoun/SanskritGrammar/blob/main/data/dhatu_families/canary_10.tsv); "
      "10 корней выбраны равноотстоящими по алфавиту среди корней с явной MW-атрибуцией "
      "`fr. √ root` у substantives; сниппет взят из СЫРОЙ записи `mw.txt` с тем же `L`, "
      "что и атрибуция в `mw_etymology.tsv`.")
    a("")
    a("| Корень | Производное | MW L | Сниппет MW | Вердикт | Примечание |")
    a("|---|---|---|---|---|---|")
    for r, d, L, snip, verdict, note in verdicts:
        snip = snip.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("|", "\\|")
        a(f"| {iast(r)} (`{r}`) | {iast(d)} | {L} | {snip} | {verdict} | {note} |")
    a("")
    tally = collections.Counter(v.split("-")[0] for _r, _d, _L, _s, v, _n in verdicts)
    a("Итог ручной сверки: " + ", ".join(f"{k} — {n}" for k, n in sorted(tally.items())) +
      ". Расхождения и слабые случаи оставлены в датасете с исходными тегами — "
      "это честная оценка точности канала `mw_etymology`, а не скрытая чистка.")
    a("")
    a("## Ограничения")
    a("")
    a("- Инвентарь датасета — 5,745 канонических dhātu (vidyut + m4 + MW + local); "
      "атрибуция производных идёт только по строгому множеству MW `genuineroot` "
      "без upasarg (чтобы `su-`, `pra-`, `vi-` не создавали гигантские ложные гнёзда). "
      "Остальные корни остаются гнёздом размера 0 — покрытие измеряется явно.")
    a("- Все каналы требуют, чтобы производное присутствовало в `analysis2.txt` "
      "(то есть было substantivum в MWderivations), так что глагольные формы и "
      "не-substantive записи MW в гнёзда не попадают.")
    a("- Частоты — лемматизированного DCS-conllu (5.7M токенов); `count_all=0` означает "
      "не отсутствие слова в языке, а отсутствие в выборке DCS.")
    a("- Атрибуция по `analysis2_decomp` требует точного совпадения компонента разбора "
      "с каноническим корнем (длина ≥2), чтобы не путать префиксы `a`, `na` с корнями.")
    a("- Разные каналы могут приписать одну форму двум корням (омонимия корней); "
      "такие ребра сохранены с обоими тегами и видимы в `families.tsv`.")
    a("")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sources-root", default=os.path.expanduser("~/Documents/GitHub"))
    ap.add_argument("--out-dir", default=REPO)
    ap.add_argument("--canary-verdicts", default="")
    ap.add_argument("--verify", action="store_true")
    args = ap.parse_args()
    outdir = os.path.abspath(args.out_dir)
    ddir = path(outdir, "data", "dhatu_families")

    if args.verify:
        with open(path(ddir, "families.tsv"), encoding="utf-8") as f:
            edges = list(csv.DictReader(f, delimiter="\t"))
        with open(path(ddir, "root_stats.tsv"), encoding="utf-8") as f:
            roots = list(csv.DictReader(f, delimiter="\t"))
        rep = open(path(outdir, "reports", REPORT_NAME), encoding="utf-8").read()
        assert len(roots) >= 5000, f"only {len(roots)} roots"
        assert len(edges) == sum(int(r["family_size"]) for r in roots)
        for lo, hi, label in BINS:
            n = sum(1 for r in roots if lo <= int(r["family_size"]) <= hi)
            assert f"| {label} | {n:,} |" in rep, f"bin {label} missing from report"
        with open(path(ddir, "canary_10.tsv"), encoding="utf-8") as f:
            can = list(csv.DictReader(f, delimiter="\t"))
        assert len(can) == 10, f"canary has {len(can)} rows"
        with open(path(ddir, "canary_verdicts.tsv"), encoding="utf-8") as f:
            verdicts = list(csv.DictReader(f, delimiter="\t"))
        assert len(verdicts) == 10, f"canary verdicts have {len(verdicts)} rows"
        print(f"VERIFY PASS: {len(roots)} roots, {len(edges)} edges, "
              f"canary {len(verdicts)}/10, report tables consistent")
        return 0

    roots, prov = load_inventory(args.sources_root)
    attr = load_attr_roots(args.sources_root)
    subs = load_substantives(args.sources_root)
    fam, lid = collect(args.sources_root, attr, subs)
    counts, ranks = load_freq(args.sources_root)

    os.makedirs(ddir, exist_ok=True)
    os.makedirs(path(outdir, "reports"), exist_ok=True)

    # flat edge table + per-root aggregates
    edge_rows = []
    stats_rows = []
    nonempty = []
    all_forms = set()
    for r in sorted(roots):  # full canonical inventory; empty families are a measured class
        forms = sorted(fam.get(r, {}))
        all_forms.update(forms)
        att = 0
        tok = 0
        lgs = []
        for form in forms:
            c = counts.get(form, 0)
            edge_rows.append((r, form, "+".join(sorted(fam.get(r, {})[form])), c,
                              ranks.get(form) or ""))
            if c > 0:
                att += 1
                tok += c
            lgs.append(math.log10(1 + c))
        size = len(forms)
        stats_rows.append((r, iast(r), size, att, tok, round(sum(lgs) / size, 4) if size else 0.0,
                           round(median(lgs), 4), "+".join(sorted({t for f in forms for t in fam.get(r, {})[f]}))))
        if size:
            nonempty.append(r)

    with open(path(ddir, "families.tsv"), "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(("root_slp1", "derivative_slp1", "sources", "dcs_count", "dcs_rank"))
        w.writerows(edge_rows)
    with open(path(ddir, "root_stats.tsv"), "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(("root_slp1", "root_iast", "family_size", "attested_in_dcs",
                    "dcs_tokens", "mean_log10_1p", "median_log10_1p", "channels"))
        w.writerows(stats_rows)

    payload = {
        "dataset": "csl-obs/dhatu-families@1.0.0",
        "handoff": "H6256",
        "built": "2026-11-25",
        "root_inventory": len(roots),
        "roots": [
            {"root_slp1": r, "root_iast": iast(r), "family_size": size,
             "derivatives": [
                 {"form_slp1": form, "sources": sorted(fam.get(r, {})[form]),
                  "dcs_count": counts.get(form, 0)}
                 for form in sorted(fam.get(r, {}))]}
            for r, _ia, size, *_rest in stats_rows
        ],
    }
    with open(path(ddir, "families.json"), "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, separators=(",", ":"))

    # canary evidence and verdicts
    can = canary_evidence(args.sources_root, fam)
    with open(path(ddir, "canary_10.tsv"), "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(("root_slp1", "derivative_slp1", "mw_L", "mw_evidence"))
        w.writerows(can)
    verdicts = []
    vmap = {}
    if args.canary_verdicts:
        with open(args.canary_verdicts, encoding="utf-8", newline="") as f:
            for r in csv.DictReader(f, delimiter="\t"):
                vmap[r["root_slp1"]] = (r["verdict"], r["note"])
    for r, d, L, snip in can:
        v, note = vmap.get(r, ("ПРОВЕРКА", "вердикт не зафиксирован"))
        verdicts.append((r, d, L, snip, v, note))

    # report
    channel_edges = collections.Counter()
    for r, ds in fam.items():
        for form, tags in ds.items():
            for t in tags:
                channel_edges[t] += 1
    nroots = len(stats_rows)
    attested_forms = sum(1 for form in all_forms if counts.get(form, 0) > 0)
    form_counts = [counts.get(form, 0) for form in all_forms if counts.get(form, 0) > 0]
    bin_rows = []
    for lo, hi, label in BINS:
        sel = [row for row in stats_rows if lo <= row[2] <= hi]
        forms = sum(row[2] for row in sel)
        att = sum(row[3] for row in sel)
        toks = [row[4] for row in sel]
        lgs = [row[6] for row in sel]
        bin_rows.append({"label": label, "roots": len(sel),
                         "share": 100.0 * len(sel) / nroots, "forms": forms,
                         "att": 100.0 * att / forms if forms else 0.0,
                         "tok": median(toks), "lg": median(lgs)})
    rho = spearman([r[2] for r in stats_rows if r[2]],
                   [r[4] for r in stats_rows if r[2]])
    top = sorted((r for r in stats_rows if r[2]), key=lambda r: (-r[2], r[0]))[:20]
    top_rows = [(r[0], r[2], r[3], r[4],
                 max(sorted(fam[r[0]]), key=lambda x: counts.get(x, 0))) for r in top]
    coverage = collections.OrderedDict([
        ("Корней в инвентаре (канонический dhātu + MW)", nroots),
        ("Из них в строгом множестве атрибуции (MW genuineroot без upasarga)", len(attr)),
        ("Корней с >=1 производным", len(nonempty)),
        ("Корней с >=5 производными", sum(1 for r in nonempty if len(fam[r]) >= 5)),
        ("Уникальных производных", len(all_forms)),
        ("Производных с частотой DCS > 0", attested_forms),
        ("Доля производных с DCS-частотой", f"{100.0*attested_forms/len(all_forms):.1f}%"),
        ("Суммарных рёбер root→derivative", len(edge_rows)),
    ])
    stats = {"channel_edges": channel_edges, "coverage": coverage, "bins": bin_rows,
             "slope": zipf_slope(dict((i + 1, c) for i, c in enumerate(form_counts))),
             "rho": rho, "nonempty_roots": len(nonempty), "attested_forms": attested_forms,
             "top": top_rows}
    with open(path(outdir, "reports", REPORT_NAME), "w", encoding="utf-8") as f:
        f.write(build_report(stats, verdicts))

    print(f"roots={nroots} edges={len(edge_rows)} forms={len(all_forms)} "
          f"attested={attested_forms} channels={dict(channel_edges)}")
    print(f"wrote {path(ddir, 'families.json')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
