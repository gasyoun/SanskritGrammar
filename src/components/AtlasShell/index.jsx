// Route shell for the Sangram public atlas (slot B1, H623).
// Renders the sanitised bundle's provenance, composition counts, and the five
// view declarations. View slots B2-B6 replace the placeholder sections with
// interactive views that read the SAME bundle prop — no other data source.
import React from 'react';

const NODE_KIND_LABELS = {
  thesis: 'Тезисы',
  'source-class': 'Классы источников',
  repo: 'Репозитории',
  asset: 'Канонические активы',
  'external-stack': 'Внешние стеки',
  stage: 'Ступени цепочек',
  surface: 'Поверхности',
};

const tableWrap = { overflowX: 'auto' };
const cardStyle = {
  border: '1px solid var(--ifm-color-emphasis-300)',
  borderRadius: 'var(--ifm-card-border-radius, 8px)',
  padding: '0.75rem 1rem',
  marginBottom: '1rem',
};

function counts(items, key) {
  const acc = {};
  for (const it of items) acc[it[key]] = (acc[it[key]] || 0) + 1;
  return acc;
}

export default function AtlasShell({ bundle }) {
  const { provenance, nodes, edges, views } = bundle;
  const nodeCounts = counts(nodes, 'kind');

  return (
    <div>
      <section aria-labelledby="atlas-provenance">
        <h2 id="atlas-provenance">Провенанс снимка</h2>
        <div style={tableWrap}>
          <table>
            <tbody>
              <tr>
                <th scope="row">Снимок данных</th>
                <td>{provenance.generated}</td>
              </tr>
              <tr>
                <th scope="row">Исполнитель</th>
                <td>{provenance.generated_by}</td>
              </tr>
              <tr>
                <th scope="row">Слот серии</th>
                <td>{provenance.series_slot}</td>
              </tr>
              <tr>
                <th scope="row">Источники</th>
                <td>
                  {provenance.sources
                    .map((s) => s.name + (s.commit ? ` @ ${s.commit}` : ''))
                    .join(' · ')}
                </td>
              </tr>
              <tr>
                <th scope="row">Санитизация</th>
                <td>
                  denylist {provenance.sanitisation.denylist_version}: отброшено{' '}
                  {provenance.sanitisation.dropped_nodes} узлов и{' '}
                  {provenance.sanitisation.dropped_edges} ребер приватного/неразрешимого яруса
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <section aria-labelledby="atlas-composition">
        <h2 id="atlas-composition">Состав bundle</h2>
        <p>
          {nodes.length} узлов и {edges.length} типизированных ребер, контракт v
          {bundle.contract_version}.
        </p>
        <div style={tableWrap}>
          <table>
            <thead>
              <tr>
                <th scope="col">Тип узла</th>
                <th scope="col">Узлов</th>
              </tr>
            </thead>
            <tbody>
              {Object.entries(nodeCounts).map(([kind, n]) => (
                <tr key={kind}>
                  <td>{NODE_KIND_LABELS[kind] || kind}</td>
                  <td>{n}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      <section aria-labelledby="atlas-views">
        <h2 id="atlas-views">Пять представлений</h2>
        {views.map((v) => {
          const nodeCount = nodes.filter((n) => v.node_kinds.includes(n.kind)).length;
          const edgeCount = edges.filter((e) => v.edge_kinds.includes(e.kind)).length;
          return (
            <article key={v.id} style={cardStyle} aria-label={v.title_ru}>
              <h3 style={{ marginBottom: '0.25rem' }}>{v.title_ru}</h3>
              <p style={{ marginBottom: '0.25rem' }}>{v.question_ru}</p>
              <p style={{ marginBottom: 0, color: 'var(--ifm-color-emphasis-700)' }}>
                Данные готовы: {nodeCount} узлов, {edgeCount} ребер · маршрут{' '}
                <code>{v.route.slug}</code> · интерактивное представление — слот{' '}
                {v.route.owner_slot} серии.
              </p>
            </article>
          );
        })}
      </section>
    </div>
  );
}
