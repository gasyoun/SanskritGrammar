// Attention view of the Sangram public atlas (slot B2, H629).
// Reads ONLY the sanitised bundle prop (contract B1/H623) — no other data
// source. Renders the 21 programme theses grouped by verdict with dated
// E/Z/P/K scores, gate types, evidence and anchored public repositories.
// Interaction: verdict/gate filters + sort (toolbar with arrow-key roving
// focus), native <details> cards (keyboard- and touch-operable by default).
import React, { useId, useMemo, useState } from 'react';
import styles from './styles.module.css';

const VERDICTS = [
  { id: 'amplify', label: 'Усилить', hint: 'K ≥ 3' },
  { id: 'sustain', label: 'Поддерживать', hint: '1,5 ≤ K < 3' },
  { id: 'pause', label: 'Пауза новых ветвей', hint: 'K < 1,5' },
];

const GATE_FILTERS = [
  { id: 'all', label: 'Все ворота' },
  { id: 'human', label: '👤 автор' },
  { id: 'external', label: '🌐 внешняя сторона' },
  { id: 'none', label: 'Без ворот — агентные' },
];

const SORTS = [
  { id: 'k', label: 'По K (убыв.)' },
  { id: 'section', label: 'По § тезиса' },
];

const IMPORTANCE_RU = {
  key: { dot: '🔴', label: 'ключевая' },
  mid: { dot: '🟠', label: 'средняя' },
  aux: { dot: '🟡', label: 'вспомогательная' },
};

const STATE_RU = {
  stable: 'устойчивый фундамент',
  partial: 'частично / с оговорками',
  blocked: 'заблокировано / не решено',
};

const GATE_TYPE_RU = {
  human: { icon: '👤', label: 'узкое место автора' },
  external: { icon: '🌐', label: 'внешняя сторона' },
};

const SCORE_RU = [
  { key: 'e', letter: 'E', label: 'эффект' },
  { key: 'z', letter: 'Z', label: 'затраты' },
  { key: 'p', letter: 'P', label: 'переиспользование' },
];

// '2026-07-11' -> '11-07-2026' (house date convention).
function fmtDate(iso) {
  const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(iso || '');
  return m ? `${m[3]}-${m[2]}-${m[1]}` : iso || '';
}

// 3.33 -> '3,33' without relying on SSR ICU locales.
function fmtK(k) {
  return typeof k === 'number' ? k.toFixed(2).replace('.', ',') : String(k);
}

function sectionSortKey(section) {
  const [a, b] = String(section).split('.');
  return Number(a) * 100 + Number(b);
}

function gateSet(thesis) {
  return new Set((thesis.gates || []).map((g) => g.type));
}

function matchesGateFilter(thesis, filter) {
  if (filter === 'all') return true;
  const set = gateSet(thesis);
  if (filter === 'none') return set.size === 0;
  return set.has(filter);
}

// Roving-focus toolbar (ARIA toolbar pattern): ArrowLeft/Right/Home/End move
// focus between the buttons of one control group.
function toolbarKeyDown(event) {
  const keys = ['ArrowLeft', 'ArrowRight', 'Home', 'End'];
  if (!keys.includes(event.key)) return;
  const buttons = Array.from(event.currentTarget.querySelectorAll('button'));
  const i = buttons.indexOf(document.activeElement);
  if (i === -1) return;
  event.preventDefault();
  let next = i;
  if (event.key === 'ArrowLeft') next = (i - 1 + buttons.length) % buttons.length;
  if (event.key === 'ArrowRight') next = (i + 1) % buttons.length;
  if (event.key === 'Home') next = 0;
  if (event.key === 'End') next = buttons.length - 1;
  buttons[next].focus();
}

function FilterGroup({ label, options, value, onChange, counts }) {
  return (
    <div
      className={styles.filterGroup}
      role="toolbar"
      aria-label={label}
      onKeyDown={toolbarKeyDown}
    >
      <span className={styles.filterLabel}>{label}:</span>
      {options.map((opt) => (
        <button
          key={opt.id}
          type="button"
          className={styles.filterBtn}
          aria-pressed={value === opt.id}
          onClick={() => onChange(opt.id)}
        >
          {opt.label}
          {counts && counts[opt.id] != null ? ` (${counts[opt.id]})` : ''}
          {opt.hint ? <span className={styles.hint}> · {opt.hint}</span> : null}
        </button>
      ))}
    </div>
  );
}

function ScoreMeters({ thesis }) {
  return (
    <div
      className={styles.scores}
      role="group"
      aria-label={`Оценки автора от ${fmtDate(thesis.as_of)}: эффект ${thesis.scores.e}, затраты ${thesis.scores.z}, переиспользование ${thesis.scores.p} из 5; коэффициент K ${fmtK(thesis.scores.k)}`}
    >
      {SCORE_RU.map(({ key, letter, label }) => (
        <div key={key} className={styles.score}>
          <span className={styles.scoreLabel}>
            <abbr title={label}>{letter}</abbr> {thesis.scores[key]}/5
          </span>
          <span className={styles.meter} aria-hidden="true">
            <span
              className={styles.meterFill}
              style={{ width: `${(thesis.scores[key] / 5) * 100}%` }}
            />
          </span>
        </div>
      ))}
      <div className={styles.kFormula}>
        K = (E + P) / Z = <strong>{fmtK(thesis.scores.k)}</strong>
        <span className={styles.asOf}> · оценка от {fmtDate(thesis.as_of)}</span>
      </div>
    </div>
  );
}

function ThesisCard({ thesis, repos, verdict }) {
  const imp = IMPORTANCE_RU[thesis.importance] || { dot: '', label: thesis.importance };
  const gates = thesis.gates || [];
  return (
    <details className={styles.card}>
      <summary className={styles.cardSummary}>
        <span className={`${styles.kBadge} ${styles[`k_${verdict.id}`]}`}>
          K {fmtK(thesis.scores.k)}
        </span>
        <span className={styles.cardTitle}>
          §{thesis.section} · {thesis.label_ru}
        </span>
        <span className={styles.cardMarks}>
          <span title={`важность: ${imp.label}`} aria-label={`важность: ${imp.label}`}>
            {imp.dot}
          </span>
          {gates.map((g, i) => {
            const t = GATE_TYPE_RU[g.type] || { icon: '', label: g.type };
            return (
              <span key={i} title={`ворота: ${t.label}`} aria-label={`ворота: ${t.label}`}>
                {t.icon}
              </span>
            );
          })}
        </span>
      </summary>
      <div className={styles.cardBody}>
        <ScoreMeters thesis={thesis} />
        <dl className={styles.facts}>
          <dt>Вердикт</dt>
          <dd>
            {verdict.label} ({verdict.hint})
          </dd>
          <dt>Важность · состояние</dt>
          <dd>
            {imp.dot} {imp.label} · {STATE_RU[thesis.state] || thesis.state}
          </dd>
          <dt>Ворота</dt>
          <dd>
            {gates.length === 0 ? (
              <>
                устойчивых человеческих ворот нет — пропускную способность
                определяют агенты
              </>
            ) : (
              <>
                {gates
                  .map((g) => {
                    const t = GATE_TYPE_RU[g.type] || { icon: '', label: g.type };
                    return `${t.icon} ${t.label}`;
                  })
                  .join(' · ')}
                {thesis.gates_summary_ru ? ` — ${thesis.gates_summary_ru}` : ''}
              </>
            )}
          </dd>
          <dt>Свидетельство</dt>
          <dd>
            {thesis.evidence?.visibility === 'public' && thesis.evidence?.url ? (
              <a href={thesis.evidence.url}>{thesis.evidence.label_ru}</a>
            ) : (
              <>
                {thesis.evidence?.label_ru}{' '}
                <span className={styles.internalNote}>
                  — внутренний источник, публичная ссылка исключена правилами
                  санитизации
                </span>
              </>
            )}
          </dd>
          <dt>Смысловые дома ({repos.length})</dt>
          <dd>
            {repos.length === 0 ? (
              <span className={styles.internalNote}>
                якорных публичных репозиториев в bundle нет
              </span>
            ) : (
              <span className={styles.chips}>
                {repos.map((r) => (
                  <a key={r.id} className={styles.chip} href={r.url}>
                    {r.label_ru}
                  </a>
                ))}
              </span>
            )}
          </dd>
        </dl>
      </div>
    </details>
  );
}

export default function AtlasAttentionView({ bundle }) {
  const [verdictFilter, setVerdictFilter] = useState('all');
  const [gateFilter, setGateFilter] = useState('all');
  const [sort, setSort] = useState('k');
  const headingId = useId();

  const { theses, reposByThesis, asOfDates, verdictCounts, gateCounts } = useMemo(() => {
    const nodes = bundle.nodes || [];
    const edges = bundle.edges || [];
    const thesesAll = nodes.filter((n) => n.kind === 'thesis');
    const repoById = new Map(nodes.filter((n) => n.kind === 'repo').map((n) => [n.id, n]));
    const byThesis = new Map();
    for (const e of edges) {
      if (e.kind !== 'anchors') continue;
      const repo = repoById.get(e.target);
      if (!repo) continue;
      if (!byThesis.has(e.source)) byThesis.set(e.source, []);
      byThesis.get(e.source).push(repo);
    }
    for (const list of byThesis.values()) {
      list.sort((a, b) => a.label_ru.localeCompare(b.label_ru, 'ru'));
    }
    const vCounts = { all: thesesAll.length };
    for (const v of VERDICTS) {
      vCounts[v.id] = thesesAll.filter((t) => t.verdict === v.id).length;
    }
    const gCounts = { all: thesesAll.length };
    for (const g of GATE_FILTERS.slice(1)) {
      gCounts[g.id] = thesesAll.filter((t) => matchesGateFilter(t, g.id)).length;
    }
    return {
      theses: thesesAll,
      reposByThesis: byThesis,
      asOfDates: [...new Set(thesesAll.map((t) => t.as_of))].sort(),
      verdictCounts: vCounts,
      gateCounts: gCounts,
    };
  }, [bundle]);

  const visibleGroups = VERDICTS.filter(
    (v) => verdictFilter === 'all' || verdictFilter === v.id
  ).map((v) => {
    const items = theses
      .filter((t) => t.verdict === v.id && matchesGateFilter(t, gateFilter))
      .sort((a, b) =>
        sort === 'k'
          ? b.scores.k - a.scores.k || sectionSortKey(a.section) - sectionSortKey(b.section)
          : sectionSortKey(a.section) - sectionSortKey(b.section)
      );
    return { verdict: v, items };
  });

  const shownCount = visibleGroups.reduce((n, g) => n + g.items.length, 0);

  return (
    <section aria-labelledby={headingId} className={styles.view}>
      <h2 id={headingId} className={styles.srOnly}>
        Интерактивное представление: распределение внимания по тезисам
      </h2>

      <p className={styles.provenanceLine}>
        Данные: {theses.length} тезисов из снимка bundle от{' '}
        {fmtDate(bundle.provenance?.generated)} · оценки автора от{' '}
        {asOfDates.map(fmtDate).join(', ')} · источник посева — карта внимания
        MEGABOOK §11 (внутренний Uprava, слот A2 серии).
      </p>

      <div className={styles.summaryStrip} role="group" aria-label="Сводка по вердиктам и воротам">
        {VERDICTS.map((v) => (
          <div key={v.id} className={`${styles.summaryCard} ${styles[`k_${v.id}`]}`}>
            <span className={styles.summaryNum}>{verdictCounts[v.id]}</span>
            <span>
              {v.label} <span className={styles.hint}>({v.hint})</span>
            </span>
          </div>
        ))}
        <div className={styles.summaryCard}>
          <span className={styles.summaryNum}>{gateCounts.none}</span>
          <span>
            без человеческих ворот <span className={styles.hint}>(агентный резерв)</span>
          </span>
        </div>
      </div>

      <div className={styles.controls}>
        <FilterGroup
          label="Вердикт"
          options={[{ id: 'all', label: 'Все' }, ...VERDICTS]}
          value={verdictFilter}
          onChange={setVerdictFilter}
          counts={verdictCounts}
        />
        <FilterGroup
          label="Ворота"
          options={GATE_FILTERS}
          value={gateFilter}
          onChange={setGateFilter}
          counts={gateCounts}
        />
        <FilterGroup label="Сортировка" options={SORTS} value={sort} onChange={setSort} />
      </div>

      <p aria-live="polite" className={styles.resultLine}>
        Показано {shownCount} из {theses.length} тезисов.
      </p>

      {visibleGroups.map(({ verdict, items }) =>
        items.length === 0 ? null : (
          <div key={verdict.id} className={styles.group}>
            <h3 className={styles.groupHeading}>
              {verdict.label}{' '}
              <span className={styles.hint}>
                {verdict.hint} · {items.length}{' '}
                {verdictFilter === 'all' && gateFilter === 'all'
                  ? 'тезисов'
                  : `из ${verdictCounts[verdict.id]}`}
              </span>
            </h3>
            {items.map((t) => (
              <ThesisCard
                key={t.id}
                thesis={t}
                verdict={verdict}
                repos={reposByThesis.get(t.id) || []}
              />
            ))}
          </div>
        )
      )}
    </section>
  );
}
