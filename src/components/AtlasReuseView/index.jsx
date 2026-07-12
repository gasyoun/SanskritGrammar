// Interactive reuse view of the Sangram public atlas (slot B3, H630).
// Reads ONLY the sanitised bundle prop (contract B1, H623) — no other data
// source. Renders owner → asset → consumer chains for the 18 canonical asset
// families with type/rights/owner/programme filters, do-not-rebuild
// prohibitions, rights warnings and per-element provenance.
import React, { useMemo, useState } from 'react';

const TYPE_LABELS = {
  code: 'код',
  data: 'данные',
  schema: 'схема',
  workflow: 'workflow',
};

const RIGHTS_META = {
  open: {
    label: 'открытый',
    marker: '',
    note: 'Публичный воспроизводимый актив.',
    border: 'var(--ifm-color-success-dark)',
  },
  'rights-gated': {
    label: '⚖️ ограничен правами',
    marker: '⚖️',
    note: 'Актив или его источник ограничен правами: лицензия, закрытый ярус данных или обязательная проверка перед публикацией.',
    border: 'var(--ifm-color-warning-dark)',
  },
  quarantine: {
    label: '🧪 карантин данных',
    marker: '🧪',
    note: 'Кандидатный или неоднозначный слой: потреблять только с явной меткой кандидата, без продвижения в проверенные данные.',
    border: 'var(--ifm-color-danger-dark)',
  },
};

const tableWrap = { overflowX: 'auto' };
const cardStyle = {
  border: '1px solid var(--ifm-color-emphasis-300)',
  borderRadius: 'var(--ifm-card-border-radius, 8px)',
  padding: '0.75rem 1rem',
  marginBottom: '1rem',
};
const badgeStyle = {
  display: 'inline-block',
  border: '1px solid var(--ifm-color-emphasis-400)',
  borderRadius: '999px',
  padding: '0 0.6rem',
  marginRight: '0.35rem',
  fontSize: '0.8rem',
  whiteSpace: 'nowrap',
};
const prohibitionStyle = {
  borderLeft: '4px solid var(--ifm-color-warning-dark)',
  background: 'var(--ifm-color-emphasis-100)',
  padding: '0.4rem 0.75rem',
  margin: '0.5rem 0',
  borderRadius: '0 6px 6px 0',
};
const controlStyle = {
  display: 'inline-flex',
  flexDirection: 'column',
  gap: '0.15rem',
  marginRight: '1rem',
  marginBottom: '0.75rem',
  fontSize: '0.85rem',
};
const mutedStyle = { color: 'var(--ifm-color-emphasis-700)' };

function pluralRu(n, [one, few, many]) {
  const mod10 = n % 10;
  const mod100 = n % 100;
  if (mod10 === 1 && mod100 !== 11) return one;
  if (mod10 >= 2 && mod10 <= 4 && (mod100 < 12 || mod100 > 14)) return few;
  return many;
}

function nodeLink(node) {
  if (!node) return null;
  if (node.url) {
    return (
      <a href={node.url} target="_blank" rel="noopener noreferrer">
        {node.label_ru}
      </a>
    );
  }
  return <span>{node.label_ru}</span>;
}

export default function AtlasReuseView({ bundle }) {
  const { provenance, nodes, edges } = bundle;

  const model = useMemo(() => {
    const byId = new Map(nodes.map((n) => [n.id, n]));
    const assets = nodes.filter((n) => n.kind === 'asset');
    const anchorsByRepo = new Map();
    for (const e of edges) {
      if (e.kind !== 'anchors') continue;
      if (!anchorsByRepo.has(e.target)) anchorsByRepo.set(e.target, []);
      anchorsByRepo.get(e.target).push(byId.get(e.source));
    }
    const rows = assets
      .map((a) => {
        const owner = byId.get(a.owner);
        const consumers = edges
          .filter((e) => e.kind === 'feeds' && e.source === a.id)
          .map((e) => ({ node: byId.get(e.target), edge: e }))
          .filter((c) => c.node);
        const programmes = (anchorsByRepo.get(a.owner) || [])
          .filter(Boolean)
          .map((t) => ({ section: t.section, label: t.label_ru }));
        return { asset: a, owner, consumers, programmes };
      })
      .sort((x, y) => x.asset.label_ru.localeCompare(y.asset.label_ru, 'ru'));

    // repo-level consumption of canonical owners (e.g. the CDSL source spine)
    const consumesByTarget = new Map();
    for (const e of edges) {
      if (e.kind !== 'consumes') continue;
      if (!consumesByTarget.has(e.target)) consumesByTarget.set(e.target, []);
      consumesByTarget.get(e.target).push({ node: byId.get(e.source), edge: e });
    }
    const consumesGroups = [...consumesByTarget.entries()]
      .map(([target, items]) => ({ target: byId.get(target), items }))
      .sort((a, b) => b.items.length - a.items.length);

    const vendorEdges = edges
      .filter((e) => e.kind === 'vendors')
      .map((e) => ({ edge: e, source: byId.get(e.source), target: byId.get(e.target) }));
    const produceEdges = edges
      .filter((e) => e.kind === 'produces')
      .map((e) => ({ edge: e, source: byId.get(e.source), target: byId.get(e.target) }));
    const citeEdges = edges
      .filter((e) => e.kind === 'cites')
      .map((e) => ({ edge: e, source: byId.get(e.source), target: byId.get(e.target) }));
    const externals = nodes
      .filter((n) => n.kind === 'external-stack')
      .sort((a, b) => a.label_ru.localeCompare(b.label_ru, 'ru'));

    const owners = [...new Set(rows.map((r) => r.owner && r.owner.id))]
      .map((id) => byId.get(id))
      .filter(Boolean)
      .sort((a, b) => a.label_ru.localeCompare(b.label_ru, 'ru'));
    const programmes = [
      ...new Map(
        rows.flatMap((r) => r.programmes).map((p) => [p.section, p]),
      ).values(),
    ].sort((a, b) => a.section.localeCompare(b.section));

    return {
      rows,
      consumesGroups,
      vendorEdges,
      produceEdges,
      citeEdges,
      externals,
      owners,
      programmes,
    };
  }, [nodes, edges]);

  const [typeFilter, setTypeFilter] = useState('all');
  const [rightsFilter, setRightsFilter] = useState('all');
  const [ownerFilter, setOwnerFilter] = useState('all');
  const [programmeFilter, setProgrammeFilter] = useState('all');
  const [query, setQuery] = useState('');

  const visible = model.rows.filter(({ asset, owner, consumers, programmes }) => {
    if (typeFilter !== 'all' && !asset.asset_types.includes(typeFilter)) return false;
    if (rightsFilter !== 'all' && asset.rights !== rightsFilter) return false;
    if (ownerFilter !== 'all' && (!owner || owner.id !== ownerFilter)) return false;
    if (
      programmeFilter !== 'all' &&
      !programmes.some((p) => p.section === programmeFilter)
    )
      return false;
    if (query.trim()) {
      const q = query.trim().toLowerCase();
      const hay = [
        asset.label_ru,
        asset.prohibition_ru,
        owner ? owner.label_ru : '',
        ...consumers.map((c) => c.node.label_ru),
      ]
        .join(' ')
        .toLowerCase();
      if (!hay.includes(q)) return false;
    }
    return true;
  });

  return (
    <div>
      <section aria-labelledby="reuse-provenance">
        <h2 id="reuse-provenance">Источник данных представления</h2>
        <p>
          Снимок bundle от <strong>{provenance.generated}</strong> (
          {provenance.generated_by}, слот {provenance.series_slot} серии):{' '}
          {model.rows.length} семейств активов, {model.externals.length} внешних
          стеков. Санитизация denylist {provenance.sanitisation.denylist_version}:
          отброшено {provenance.sanitisation.dropped_nodes} узлов и{' '}
          {provenance.sanitisation.dropped_edges} ребер приватного яруса — карта
          показывает только публичный срез.
        </p>
      </section>

      <section aria-labelledby="reuse-families">
        <h2 id="reuse-families">Семейства активов: владелец → актив → потребители</h2>
        <div role="group" aria-label="Фильтры семейств активов">
          <label style={controlStyle}>
            Тип актива
            <select value={typeFilter} onChange={(e) => setTypeFilter(e.target.value)}>
              <option value="all">все типы</option>
              {Object.entries(TYPE_LABELS).map(([k, v]) => (
                <option key={k} value={k}>
                  {v}
                </option>
              ))}
            </select>
          </label>
          <label style={controlStyle}>
            Права
            <select value={rightsFilter} onChange={(e) => setRightsFilter(e.target.value)}>
              <option value="all">все ярусы</option>
              {Object.entries(RIGHTS_META).map(([k, v]) => (
                <option key={k} value={k}>
                  {v.label}
                </option>
              ))}
            </select>
          </label>
          <label style={controlStyle}>
            Владелец
            <select value={ownerFilter} onChange={(e) => setOwnerFilter(e.target.value)}>
              <option value="all">все владельцы</option>
              {model.owners.map((o) => (
                <option key={o.id} value={o.id}>
                  {o.label_ru}
                </option>
              ))}
            </select>
          </label>
          <label style={controlStyle}>
            Программа (тезис владельца)
            <select
              value={programmeFilter}
              onChange={(e) => setProgrammeFilter(e.target.value)}
            >
              <option value="all">все программы</option>
              {model.programmes.map((p) => (
                <option key={p.section} value={p.section}>
                  {p.section} · {p.label}
                </option>
              ))}
            </select>
          </label>
          <label style={controlStyle}>
            Поиск
            <input
              type="search"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="актив, владелец, потребитель…"
              aria-label="Поиск по семействам активов"
            />
          </label>
        </div>
        <p aria-live="polite" style={mutedStyle}>
          Показано {visible.length} из {model.rows.length} семейств.
        </p>

        {visible.map(({ asset, owner, consumers, programmes }) => {
          const rights = RIGHTS_META[asset.rights] || RIGHTS_META.open;
          return (
            <article
              key={asset.id}
              style={{ ...cardStyle, borderLeft: `4px solid ${rights.border}` }}
              aria-label={asset.label_ru}
            >
              <h3 style={{ marginBottom: '0.35rem', fontSize: '1.05rem' }}>
                {asset.label_ru}
              </h3>
              <p style={{ marginBottom: '0.35rem' }}>
                {asset.asset_types.map((t) => (
                  <span key={t} style={badgeStyle}>
                    {TYPE_LABELS[t] || t}
                  </span>
                ))}
                <span
                  style={badgeStyle}
                  title={rights.note}
                  aria-label={`Ярус прав: ${rights.label}. ${rights.note}`}
                >
                  {rights.label}
                </span>
              </p>
              <p style={{ marginBottom: '0.35rem' }}>
                <strong>Владелец:</strong> {nodeLink(owner)}
                {programmes.length > 0 && (
                  <>
                    {' '}
                    · <strong>программа:</strong>{' '}
                    {programmes.map((p) => `${p.section} ${p.label}`).join('; ')}
                  </>
                )}
                {asset.url && (
                  <>
                    {' '}
                    ·{' '}
                    <a href={asset.url} target="_blank" rel="noopener noreferrer">
                      публичный дом актива
                    </a>
                  </>
                )}
              </p>
              <div style={prohibitionStyle} role="note" aria-label="Запрет пересоздания">
                <strong>Не пересоздавать:</strong> {asset.prohibition_ru}
                {rights.marker && (
                  <>
                    {' '}
                    <em>
                      {rights.marker} {rights.note}
                    </em>
                  </>
                )}
              </div>
              <p style={{ marginBottom: '0.35rem' }}>
                <strong>Потребители ({consumers.length}):</strong>{' '}
                {consumers.map((c, i) => (
                  <React.Fragment key={c.node.id}>
                    {i > 0 && ' · '}
                    {nodeLink(c.node)}
                  </React.Fragment>
                ))}
              </p>
              <p style={{ ...mutedStyle, marginBottom: 0, fontSize: '0.85rem' }}>
                Свидетельство:{' '}
                {asset.evidence && asset.evidence.visibility === 'public' ? (
                  <a
                    href={asset.evidence.url}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    {asset.evidence.label_ru}
                  </a>
                ) : (
                  <>
                    {asset.evidence ? asset.evidence.label_ru : '—'} — внутренний
                    источник, без публичной ссылки
                  </>
                )}
                {asset.rule_refs && asset.rule_refs.length > 0 && (
                  <> · правила {asset.rule_refs.join(', ')}</>
                )}
                {asset.as_of && <> · оценка от {asset.as_of}</>}
              </p>
            </article>
          );
        })}
      </section>

      <section aria-labelledby="reuse-spine">
        <h2 id="reuse-spine">Потребление на уровне владельцев</h2>
        <p>
          Часть переиспользования течет не из отдельного актива, а из
          репозитория-владельца целиком: ребра <code>consumes</code> фиксируют,
          кто читает канонический источник напрямую.
        </p>
        {model.consumesGroups.map(({ target, items }) => (
          <details key={target.id} style={{ marginBottom: '0.5rem' }}>
            <summary>
              {target.label_ru}: {items.length}{' '}
              {pluralRu(items.length, ['потребитель', 'потребителя', 'потребителей'])}
            </summary>
            <div style={tableWrap}>
              <table>
                <thead>
                  <tr>
                    <th scope="col">Потребитель</th>
                    <th scope="col">Что течет</th>
                    <th scope="col">Статус · дата</th>
                  </tr>
                </thead>
                <tbody>
                  {items.map(({ node, edge }) => (
                    <tr key={edge.id}>
                      <td>{nodeLink(node)}</td>
                      <td>{edge.asset_ru || '—'}</td>
                      <td>
                        {edge.status || '—'}
                        {edge.as_of ? ` · ${edge.as_of}` : ''}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </details>
        ))}
      </section>

      <section aria-labelledby="reuse-external">
        <h2 id="reuse-external">Внешние стеки: вызывать, не клонировать</h2>
        <div style={tableWrap}>
          <table>
            <thead>
              <tr>
                <th scope="col">Стек</th>
                <th scope="col">Как потреблять</th>
                <th scope="col">Запрет</th>
                <th scope="col">Лицензия</th>
              </tr>
            </thead>
            <tbody>
              {model.externals.map((x) => (
                <tr key={x.id}>
                  <td>{nodeLink(x)}</td>
                  <td>{x.consume_rule_ru}</td>
                  <td>{x.prohibition_ru}</td>
                  <td>{x.license || '—'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      <section aria-labelledby="reuse-vendored">
        <h2 id="reuse-vendored">Вендоренные копии и канонические производители</h2>
        <p>
          Ребра <code>vendors</code> — уже существующие вендоренные копии чужого
          кода или данных (копию синхронизируют, а не переписывают); ребра{' '}
          <code>produces</code> — канонические производители, чей выход потребляет
          вся организация.
        </p>
        <div style={tableWrap}>
          <table>
            <thead>
              <tr>
                <th scope="col">Ребро</th>
                <th scope="col">Связь (source → target)</th>
                <th scope="col">Что именно</th>
                <th scope="col">Статус</th>
              </tr>
            </thead>
            <tbody>
              {model.vendorEdges.map(({ edge, source, target }) => (
                <tr key={edge.id}>
                  <td>
                    <code>vendors</code>
                  </td>
                  <td>
                    {nodeLink(source)} → {nodeLink(target)}
                  </td>
                  <td>{edge.asset_ru || '—'}</td>
                  <td>{edge.status || '—'}</td>
                </tr>
              ))}
              {model.produceEdges.map(({ edge, source, target }) => (
                <tr key={edge.id}>
                  <td>
                    <code>produces</code>
                  </td>
                  <td>
                    {nodeLink(source)} → {nodeLink(target)}
                  </td>
                  <td>{edge.asset_ru || '—'}</td>
                  <td>{edge.status || '—'}</td>
                </tr>
              ))}
              {model.citeEdges.map(({ edge, source, target }) => (
                <tr key={edge.id}>
                  <td>
                    <code>cites</code>
                  </td>
                  <td>
                    {nodeLink(source)} → {nodeLink(target)}
                  </td>
                  <td>{edge.asset_ru || '—'}</td>
                  <td>{edge.status || '—'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}
