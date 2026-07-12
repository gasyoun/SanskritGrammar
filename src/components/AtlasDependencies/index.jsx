// Repo-dependency view of the Sangram public atlas (slot B5, H620).
// Reads ONLY the sanitised bundle (B1 contract): the assessed interlinks
// edges (feeds / consumes / vendors / produces / cites) between public
// repos, external stacks and surfaces, grouped by census programme
// (programme_ru, MEGABOOK §9.x subsection titles). Census coverage is
// explicit: every public repo renders, including edge-isolated ones.
// Controlled mode ({selectedId, onSelect}) plugs into the unified route
// (slot B6); standalone the component keeps selection in local state.
import React, { useMemo, useState } from 'react';
import styles from './styles.module.css';

const KIND_META = {
  feeds: {
    badge: 'feeds',
    className: styles.kindFeeds,
    legend_ru: 'данные источника втекают в приемник (канон — источник ребра)',
    out_ru: 'питает',
    in_ru: 'получает от',
  },
  consumes: {
    badge: 'consumes',
    className: styles.kindConsumes,
    legend_ru: 'потребитель читает/выводит из чужого актива (канон — владелец, приемник ребра)',
    out_ru: 'потребляет у',
    in_ru: 'его потребляет',
  },
  vendors: {
    badge: 'vendors',
    className: styles.kindVendors,
    legend_ru: 'вендоренная копия чужого кода/данных (канон — приемник ребра; копия требует синхронизации)',
    out_ru: 'вендорит копию у',
    in_ru: 'его копию вендорит',
  },
  produces: {
    badge: 'produces',
    className: styles.kindProduces,
    legend_ru: 'канонический производитель актива для всей организации',
    out_ru: 'производит для',
    in_ru: 'получает продукцию',
  },
  cites: {
    badge: 'cites',
    className: styles.kindCites,
    legend_ru: 'ссылка уровня документации/стандартов, без потока данных',
    out_ru: 'ссылается на',
    in_ru: 'цитируется в',
  },
};

// Which endpoint holds the CANONICAL asset of the relation (see legend).
const CANONICAL_END = { feeds: 'source', consumes: 'target', vendors: 'target', produces: 'source', cites: null };

const STATUS_META = {
  live: { label: 'live', className: styles.statusLive },
  queued: { label: 'queued', className: styles.statusQueued },
  proposed: { label: 'proposed', className: '' },
  unverified: { label: 'unverified', className: '' },
};

const PROGRAMME_ORDER = [
  'Управление и общие движки',
  'Исследования и данные',
  'Dictionary tooling, pipelines и interfaces',
  'CDSL dictionaries',
  'DH, corpora и инфраструктура',
  'Образование и выручка',
];
const NO_PROGRAMME = 'Вне групп census (§9)';

function KindBadge({ kind }) {
  const meta = KIND_META[kind];
  return <span className={`${styles.kindBadge} ${meta.className}`}>{meta.badge}</span>;
}

function StatusChip({ status }) {
  if (!status) return null;
  const meta = STATUS_META[status] || { label: status, className: '' };
  return <span className={`${styles.statusChip} ${meta.className}`}>{meta.label}</span>;
}

function CounterpartLabel({ node }) {
  if (!node) return null;
  const marker =
    node.kind === 'external-stack' ? ' (внешний стек)' : node.kind === 'surface' ? ' (поверхность)' : '';
  const text = node.kind === 'repo' ? node.name : node.label_ru;
  return node.url ? (
    <a href={node.url}>{text}</a>
  ) : (
    <span>{text}</span>
  );
  // marker is appended by the caller so links stay short
}

export default function AtlasDependencies({ bundle, selectedId, onSelect }) {
  const [localSelected, setLocalSelected] = useState(null);
  const controlled = typeof onSelect === 'function';
  const selected = controlled ? selectedId : localSelected;
  const select = (id) => (controlled ? onSelect(id) : setLocalSelected(id));

  const [query, setQuery] = useState('');
  const [kindsOff, setKindsOff] = useState(() => new Set());
  const [programmesOff, setProgrammesOff] = useState(() => new Set());

  const model = useMemo(() => {
    const view = bundle.views.find((v) => v.id === 'dependencies');
    const byId = Object.fromEntries(bundle.nodes.map((n) => [n.id, n]));
    const nodeKinds = new Set(view.node_kinds);
    const edges = bundle.edges.filter(
      (e) =>
        view.edge_kinds.includes(e.kind) &&
        nodeKinds.has(byId[e.source]?.kind) &&
        nodeKinds.has(byId[e.target]?.kind)
    );
    const adjacency = {};
    for (const e of edges) {
      (adjacency[e.source] = adjacency[e.source] || []).push({ edge: e, dir: 'out' });
      (adjacency[e.target] = adjacency[e.target] || []).push({ edge: e, dir: 'in' });
    }
    const repos = bundle.nodes.filter((n) => n.kind === 'repo');
    const groups = new Map();
    for (const r of repos) {
      const g = r.programme_ru || NO_PROGRAMME;
      if (!groups.has(g)) groups.set(g, []);
      groups.get(g).push(r);
    }
    for (const list of groups.values()) list.sort((a, b) => a.name.localeCompare(b.name));
    const groupNames = [...groups.keys()].sort((a, b) => {
      const ia = PROGRAMME_ORDER.indexOf(a);
      const ib = PROGRAMME_ORDER.indexOf(b);
      return (ia < 0 ? PROGRAMME_ORDER.length : ia) - (ib < 0 ? PROGRAMME_ORDER.length : ib) || a.localeCompare(b);
    });
    const kindCounts = {};
    for (const e of edges) kindCounts[e.kind] = (kindCounts[e.kind] || 0) + 1;
    const covered = repos.filter((r) => adjacency[r.id]?.length).length;
    const vendorRows = edges
      .filter((e) => e.kind === 'vendors')
      .map((e) => ({ edge: e, holder: byId[e.source], canonical: byId[e.target] }));
    return { view, byId, edges, adjacency, repos, groups, groupNames, kindCounts, covered, vendorRows };
  }, [bundle]);

  const q = query.trim().toLowerCase();
  const cardMatches = (repo) => {
    if (!q) return true;
    if (repo.name.toLowerCase().includes(q) || repo.label_ru.toLowerCase().includes(q)) return true;
    return (model.adjacency[repo.id] || []).some(({ edge, dir }) => {
      const other = model.byId[dir === 'out' ? edge.target : edge.source];
      return (
        (edge.asset_ru || '').toLowerCase().includes(q) ||
        (other?.name || other?.label_ru || '').toLowerCase().includes(q)
      );
    });
  };

  const toggle = (set, value, apply) => {
    const next = new Set(set);
    if (next.has(value)) next.delete(value);
    else next.add(value);
    apply(next);
  };

  const isolatedTotal = model.repos.length - model.covered;

  return (
    <div>
      <div className={styles.stats} role="group" aria-label="Покрытие публичного census">
        <span className={styles.statItem}>
          <strong>{model.repos.length}</strong> публичных репозиториев в census
        </span>
        <span className={styles.statItem}>
          <strong>{model.covered}</strong> с типизированными ребрами
        </span>
        <span className={styles.statItem}>
          <strong>{isolatedTotal}</strong> пока без ребер (показаны пунктиром)
        </span>
        <span className={styles.statItem}>
          <strong>{model.edges.length}</strong> ребер зависимостей
        </span>
      </div>

      <div className={styles.controls}>
        <div>
          <label htmlFor="atlas-dep-search" style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600 }}>
            Поиск по репозиториям, активам и контрагентам
          </label>
          <input
            id="atlas-dep-search"
            type="search"
            className={styles.searchInput}
            placeholder="например: kosha, transcoder, crosswalk…"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
        </div>

        <fieldset className={styles.chipRow}>
          <legend>Виды ребер</legend>
          {Object.keys(KIND_META).map((kind) => (
            <button
              key={kind}
              type="button"
              className={styles.chip}
              aria-pressed={!kindsOff.has(kind)}
              onClick={() => toggle(kindsOff, kind, setKindsOff)}
            >
              <KindBadge kind={kind} /> {model.kindCounts[kind] || 0}
            </button>
          ))}
        </fieldset>

        <fieldset className={styles.chipRow}>
          <legend>Программные группы census</legend>
          {model.groupNames.map((g) => (
            <button
              key={g}
              type="button"
              className={styles.chip}
              aria-pressed={!programmesOff.has(g)}
              onClick={() => toggle(programmesOff, g, setProgrammesOff)}
            >
              {g} · {model.groups.get(g).length}
            </button>
          ))}
        </fieldset>
      </div>

      <section aria-labelledby="atlas-dep-legend">
        <h3 id="atlas-dep-legend">Легенда: направление и канон</h3>
        <ul className={styles.edgeList}>
          {Object.entries(KIND_META).map(([kind, meta]) => (
            <li key={kind}>
              <KindBadge kind={kind} /> <span className={styles.edgeAsset}>{meta.legend_ru}</span>
            </li>
          ))}
        </ul>
      </section>

      {!kindsOff.has('vendors') && model.vendorRows.length > 0 && (
        <section aria-labelledby="atlas-dep-vendored">
          <h3 id="atlas-dep-vendored">Канон против копии: все вендоренные копии</h3>
          <div className={styles.tableWrap}>
            <table>
              <thead>
                <tr>
                  <th scope="col">Копия живет в</th>
                  <th scope="col">Канонический источник</th>
                  <th scope="col">Актив</th>
                  <th scope="col">Статус</th>
                </tr>
              </thead>
              <tbody>
                {model.vendorRows.map(({ edge, holder, canonical }) => (
                  <tr key={edge.id}>
                    <td>
                      <CounterpartLabel node={holder} />
                    </td>
                    <td>
                      <CounterpartLabel node={canonical} />{' '}
                      <span className={styles.canonicalMark}>★ канон</span>
                    </td>
                    <td>{edge.asset_ru}</td>
                    <td>
                      <StatusChip status={edge.status} />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      )}

      {model.groupNames.map((g) => {
        if (programmesOff.has(g)) return null;
        const visible = model.groups.get(g).filter(cardMatches);
        if (!visible.length) return null;
        return (
          <section key={g} className={styles.group} aria-label={g}>
            <h3 className={styles.groupTitle}>
              {g} · {visible.length}
              {visible.length !== model.groups.get(g).length && ` из ${model.groups.get(g).length}`}
            </h3>
            <ul className={styles.cards}>
              {visible.map((repo) => {
                const entries = (model.adjacency[repo.id] || []).filter(
                  ({ edge }) => !kindsOff.has(edge.kind)
                );
                const isolated = !(model.adjacency[repo.id] || []).length;
                const isSelected = selected === repo.id;
                return (
                  <li key={repo.id}>
                    <article
                      className={`${styles.card} ${isolated ? styles.cardIsolated : ''}`}
                      style={isSelected ? { borderColor: 'var(--ifm-color-primary)', borderWidth: 2 } : undefined}
                      aria-label={repo.name}
                    >
                      <div className={styles.cardHead}>
                        <h4>
                          <button
                            type="button"
                            className={styles.chip}
                            aria-pressed={isSelected}
                            onClick={() => select(isSelected ? null : repo.id)}
                            title="Выбрать узел (выбор сохраняется между представлениями на едином маршруте)"
                          >
                            {repo.name}
                          </button>
                        </h4>
                        <span className={styles.orgBadge}>
                          <a href={repo.url}>{repo.org}/{repo.name}</a>
                        </span>
                      </div>
                      {isolated ? (
                        <p className={styles.isolatedNote}>
                          Нет типизированных ребер в публичном экспорте interlinks — репозиторий
                          показан ради полноты census.
                        </p>
                      ) : entries.length ? (
                        <ul className={styles.edgeList}>
                          {entries.map(({ edge, dir }) => {
                            const other = model.byId[dir === 'out' ? edge.target : edge.source];
                            const meta = KIND_META[edge.kind];
                            const canonicalHere =
                              CANONICAL_END[edge.kind] &&
                              ((dir === 'out' && CANONICAL_END[edge.kind] === 'source') ||
                                (dir === 'in' && CANONICAL_END[edge.kind] === 'target'));
                            const canonicalThere =
                              CANONICAL_END[edge.kind] &&
                              ((dir === 'out' && CANONICAL_END[edge.kind] === 'target') ||
                                (dir === 'in' && CANONICAL_END[edge.kind] === 'source'));
                            return (
                              <li key={`${edge.id}-${dir}`}>
                                <KindBadge kind={edge.kind} />{' '}
                                <span aria-hidden="true">{dir === 'out' ? '→' : '←'}</span>{' '}
                                {dir === 'out' ? meta.out_ru : meta.in_ru}{' '}
                                <CounterpartLabel node={other} />
                                {other?.kind === 'external-stack' && ' (внешний стек)'}
                                {other?.kind === 'surface' && ' (поверхность)'}
                                {canonicalThere && (
                                  <>
                                    {' '}
                                    <span className={styles.canonicalMark}>★ канон там</span>
                                  </>
                                )}
                                {canonicalHere && (
                                  <>
                                    {' '}
                                    <span className={styles.canonicalMark}>★ канон здесь</span>
                                  </>
                                )}{' '}
                                <StatusChip status={edge.status} />
                                {edge.asset_ru && (
                                  <div className={styles.edgeAsset}>{edge.asset_ru}</div>
                                )}
                              </li>
                            );
                          })}
                        </ul>
                      ) : (
                        <p className={styles.isolatedNote}>
                          Все ребра этого репозитория скрыты текущим фильтром видов.
                        </p>
                      )}
                    </article>
                  </li>
                );
              })}
            </ul>
          </section>
        );
      })}

      {q &&
        model.groupNames.every(
          (g) => programmesOff.has(g) || !model.groups.get(g).filter(cardMatches).length
        ) && (
          <p className={styles.noMatch} role="status">
            Ничего не найдено по запросу «{query}» — попробуйте имя репозитория (например,
            «kosha») или фрагмент названия актива («crosswalk», «frequency»).
          </p>
        )}
    </div>
  );
}
