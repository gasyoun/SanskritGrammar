// Interactive provenance view of the Sangram public atlas (slot B6, H621).
// Reads ONLY the sanitised bundle prop (contract rule for slots B2-B6): the
// provenance subgraph = all source-class nodes + stages of chain 'provenance'
// + the five ontology edge kinds between them. Layers are derived from edge
// kinds, not hardcoded ids, so a bundle rebuild re-layers automatically.
// Selection is either self-managed (synced to the ?node= query param) or
// controlled via {selectedId, onSelect} so a unified multi-view route can
// share one selected node across views.
import React, { useMemo, useState } from 'react';
import { useHistory, useLocation } from '@docusaurus/router';

const EDGE_KIND_LABELS = {
  replenishes: 'пополняет',
  generates: 'порождает',
  attests: 'аттестует',
  crosslinks: 'связывается',
  fills: 'наполняет',
};

const NODE_KIND_LABELS = {
  'source-class': 'Класс источников',
  stage: 'Ступень цепочки происхождения',
};

const tableWrap = { overflowX: 'auto' };
const layerStyle = {
  border: '1px solid var(--ifm-color-emphasis-300)',
  borderRadius: 'var(--ifm-card-border-radius, 8px)',
  padding: '0.5rem 0.6rem',
};
const layerTitleStyle = {
  fontSize: '0.8rem',
  fontWeight: 700,
  textTransform: 'uppercase',
  letterSpacing: '0.02em',
  color: 'var(--ifm-color-emphasis-700)',
  margin: '0 0 0.4rem',
};
const relationHintStyle = {
  fontSize: '0.75rem',
  color: 'var(--ifm-color-emphasis-600)',
  margin: '0 0 0.4rem',
};
const nodeButtonStyle = (isSelected) => ({
  display: 'block',
  width: '100%',
  textAlign: 'left',
  margin: '0 0 0.35rem',
  padding: '0.35rem 0.5rem',
  fontSize: '0.8rem',
  lineHeight: 1.3,
  borderRadius: '6px',
  cursor: 'pointer',
  border: isSelected
    ? '2px solid var(--ifm-color-primary)'
    : '1px solid var(--ifm-color-emphasis-300)',
  background: isSelected
    ? 'var(--ifm-color-primary-contrast-background, var(--ifm-background-surface-color))'
    : 'var(--ifm-background-surface-color)',
  color: 'var(--ifm-font-color-base)',
});
const branchButtonStyle = (isSelected) => ({
  ...nodeButtonStyle(isSelected),
  marginLeft: '0.75rem',
  width: 'calc(100% - 0.75rem)',
  fontSize: '0.75rem',
});
const detailPanelStyle = {
  border: '1px solid var(--ifm-color-emphasis-300)',
  borderRadius: 'var(--ifm-card-border-radius, 8px)',
  padding: '0.75rem 1rem',
  margin: '1rem 0',
};
const neighborButtonStyle = {
  margin: '0 0.35rem 0.35rem 0',
  padding: '0.2rem 0.5rem',
  fontSize: '0.78rem',
  borderRadius: '6px',
  border: '1px solid var(--ifm-color-emphasis-400)',
  background: 'var(--ifm-background-surface-color)',
  color: 'var(--ifm-font-color-base)',
  cursor: 'pointer',
};

function Evidence({ evidence }) {
  if (!evidence) return null;
  const isPublic = evidence.visibility === 'public';
  return (
    <span>
      {isPublic && evidence.url ? (
        <a href={evidence.url}>{evidence.label_ru}</a>
      ) : (
        evidence.label_ru
      )}{' '}
      <em>
        ({isPublic
          ? 'публичное свидетельство'
          : 'внутренний источник: назван, но не адресуется'})
      </em>
    </span>
  );
}

// Layer derivation. Feeding source-classes open the chain; top source-classes
// (grammar branches nested under their parent) form the three-source column;
// stages are ranked by the edge kind that first reaches them: 'generates' ->
// derived data, 'crosslinks' -> the linking layer, then 'fills' ranks resolved
// iteratively (consumers of consumers land one column further right).
function buildLayers(nodes, edges) {
  const classes = nodes.filter((n) => n.kind === 'source-class');
  const stages = nodes.filter((n) => n.kind === 'stage');
  const incoming = (id) => edges.filter((e) => e.target === id);

  const feeding = classes.filter((n) => n.tier === 'feeding');
  const tops = classes.filter((n) => n.tier === 'top' && !n.parent);
  const branchesOf = (id) => classes.filter((n) => n.parent === id);

  const generated = stages.filter((s) =>
    incoming(s.id).some((e) => e.kind === 'generates')
  );
  const crosswalk = stages.filter(
    (s) =>
      !generated.includes(s) &&
      incoming(s.id).some((e) => e.kind === 'crosslinks')
  );
  const placed = new Set(
    [...classes, ...generated, ...crosswalk].map((n) => n.id)
  );
  let remaining = stages.filter((s) => !placed.has(s.id));
  const fillLayers = [];
  while (remaining.length) {
    const ready = remaining.filter((s) =>
      incoming(s.id)
        .filter((e) => e.kind === 'fills')
        .every((e) => placed.has(e.source))
    );
    const batch = ready.length ? ready : remaining; // cycle guard
    fillLayers.push(batch);
    batch.forEach((s) => placed.add(s.id));
    remaining = remaining.filter((s) => !batch.includes(s));
  }

  const layers = [
    {
      id: 'feeding',
      title: 'Материалы, издания и питающие слои',
      relation: 'вспомогательные входы',
      items: feeding,
    },
    {
      id: 'sources',
      title: 'Три верхнеуровневых источника',
      relation: '⟵ пополняет · внутри: аттестует',
      items: tops,
      branchesOf,
    },
    {
      id: 'derived',
      title: 'Производные данные',
      relation: '⟵ порождает',
      items: generated,
    },
    {
      id: 'crosswalks',
      title: 'Связующий слой',
      relation: '⟵ связывается',
      items: crosswalk,
    },
  ];
  const fillTitles = [
    'Сборка и исследования',
    'Публичные поверхности и релизы',
  ];
  fillLayers.forEach((items, i) => {
    layers.push({
      id: `consumers-${i}`,
      title: fillTitles[i] || `Потребители (ярус ${i + 1})`,
      relation: '⟵ наполняет',
      items,
    });
  });
  return layers;
}

function NodeButton({ node, selected, onToggle, style }) {
  return (
    <button
      type="button"
      style={style(selected)}
      aria-pressed={selected}
      onClick={onToggle}
    >
      {node.label_ru}
    </button>
  );
}

export default function AtlasProvenance({ bundle, selectedId, onSelect }) {
  const history = useHistory();
  const location = useLocation();
  const controlled = typeof onSelect === 'function';

  const { nodes, edges, view } = useMemo(() => {
    const viewDecl = bundle.views.find((v) => v.id === 'provenance');
    const subNodes = bundle.nodes.filter(
      (n) =>
        n.kind === 'source-class' ||
        (n.kind === 'stage' && n.chain === 'provenance')
    );
    const ids = new Set(subNodes.map((n) => n.id));
    const subEdges = bundle.edges.filter(
      (e) =>
        viewDecl.edge_kinds.includes(e.kind) &&
        ids.has(e.source) &&
        ids.has(e.target)
    );
    return { nodes: subNodes, edges: subEdges, view: viewDecl };
  }, [bundle]);

  const layers = useMemo(() => buildLayers(nodes, edges), [nodes, edges]);
  const byId = useMemo(
    () => Object.fromEntries(nodes.map((n) => [n.id, n])),
    [nodes]
  );

  const queryNode = new URLSearchParams(location.search).get('node');
  const [internal, setInternal] = useState(
    queryNode && byId[queryNode] ? queryNode : null
  );
  const selected = controlled ? selectedId : internal;
  const selectedNode = selected ? byId[selected] : null;

  const select = (id) => {
    const next = id === selected ? null : id;
    if (controlled) {
      onSelect(next);
      return;
    }
    setInternal(next);
    const params = new URLSearchParams(location.search);
    if (next) params.set('node', next);
    else params.delete('node');
    history.replace({ search: params.toString(), hash: location.hash });
  };

  const incoming = selected ? edges.filter((e) => e.target === selected) : [];
  const outgoing = selected ? edges.filter((e) => e.source === selected) : [];

  return (
    <div>
      <section aria-labelledby="prov-chain">
        <h2 id="prov-chain">Цепочка происхождения</h2>
        <p>
          Выберите узел, чтобы увидеть его типизированные связи и свидетельства.
          Выбор сохраняется в адресе страницы (параметр <code>node</code>) —
          ссылкой можно делиться.
        </p>
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(170px, 1fr))',
            gap: '0.6rem',
            alignItems: 'start',
          }}
        >
          {layers.map((layer) => (
            <section key={layer.id} style={layerStyle} aria-label={layer.title}>
              <h3 style={layerTitleStyle}>{layer.title}</h3>
              <p style={relationHintStyle}>{layer.relation}</p>
              {layer.items.map((node) => (
                <React.Fragment key={node.id}>
                  <NodeButton
                    node={node}
                    selected={selected === node.id}
                    onToggle={() => select(node.id)}
                    style={nodeButtonStyle}
                  />
                  {layer.branchesOf &&
                    layer.branchesOf(node.id).map((branch) => (
                      <NodeButton
                        key={branch.id}
                        node={branch}
                        selected={selected === branch.id}
                        onToggle={() => select(branch.id)}
                        style={branchButtonStyle}
                      />
                    ))}
                </React.Fragment>
              ))}
            </section>
          ))}
        </div>
      </section>

      <section aria-labelledby="prov-detail" aria-live="polite">
        <h2 id="prov-detail" style={{ marginTop: '1.5rem' }}>
          Выбранный узел
        </h2>
        {!selectedNode && (
          <p>
            Ничего не выбрано. Узел можно выбрать мышью или с клавиатуры
            (Tab + Enter).
          </p>
        )}
        {selectedNode && (
          <div style={detailPanelStyle}>
            <h3 style={{ marginBottom: '0.25rem' }}>{selectedNode.label_ru}</h3>
            <p style={{ marginBottom: '0.5rem', color: 'var(--ifm-color-emphasis-700)' }}>
              {NODE_KIND_LABELS[selectedNode.kind] || selectedNode.kind}
              {selectedNode.tier
                ? selectedNode.tier === 'top'
                  ? ' · верхнеуровневый источник'
                  : ' · питающий слой'
                : ''}
              {selectedNode.parent && byId[selectedNode.parent]
                ? ` · ветвь класса «${byId[selectedNode.parent].label_ru}»`
                : ''}
              {selectedNode.thesis_refs?.length
                ? ` · тезисы ${selectedNode.thesis_refs.join(', ')}`
                : ''}
              {selectedNode.as_of ? ` · оценка от ${selectedNode.as_of}` : ''}
            </p>
            {selectedNode.evidence && (
              <p style={{ marginBottom: '0.5rem' }}>
                Свидетельство: <Evidence evidence={selectedNode.evidence} />
              </p>
            )}
            {[
              { title: 'Входящие связи', list: incoming, other: (e) => e.source },
              { title: 'Исходящие связи', list: outgoing, other: (e) => e.target },
            ].map(({ title, list, other }) => (
              <div key={title}>
                <h4 style={{ marginBottom: '0.25rem' }}>{title}</h4>
                {list.length === 0 && <p>нет</p>}
                {list.map((e) => (
                  <button
                    key={e.id}
                    type="button"
                    style={neighborButtonStyle}
                    onClick={() => select(other(e))}
                    aria-label={
                      title === 'Входящие связи'
                        ? `${byId[other(e)].label_ru} ${EDGE_KIND_LABELS[e.kind]} этот узел`
                        : `этот узел ${EDGE_KIND_LABELS[e.kind]} ${byId[other(e)].label_ru}`
                    }
                  >
                    <em>{EDGE_KIND_LABELS[e.kind]}</em>{' '}
                    {title === 'Входящие связи' ? '⟵' : '⟶'}{' '}
                    {byId[other(e)].label_ru}
                  </button>
                ))}
              </div>
            ))}
          </div>
        )}
      </section>

      <section aria-labelledby="prov-table">
        <h2 id="prov-table">Табличный эквивалент</h2>
        <p>
          Все {edges.length} типизированных ребер представления «{view.title_ru}»
          ({nodes.length} узлов); данные и интерактивная схема выше читают один
          и тот же bundle.
        </p>
        <div style={tableWrap}>
          <table>
            <thead>
              <tr>
                <th scope="col">Откуда</th>
                <th scope="col">Отношение</th>
                <th scope="col">Куда</th>
                <th scope="col">Свидетельство</th>
              </tr>
            </thead>
            <tbody>
              {edges.map((e) => (
                <tr key={e.id}>
                  <td>{byId[e.source].label_ru}</td>
                  <td>
                    <em>{EDGE_KIND_LABELS[e.kind]}</em>
                  </td>
                  <td>{byId[e.target].label_ru}</td>
                  <td>
                    <Evidence evidence={e.evidence} />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      <section aria-labelledby="prov-meta">
        <h2 id="prov-meta">Builder, версия и права</h2>
        <div style={tableWrap}>
          <table>
            <tbody>
              <tr>
                <th scope="row">Снимок данных</th>
                <td>{bundle.provenance.generated}</td>
              </tr>
              <tr>
                <th scope="row">Builder</th>
                <td>
                  <code>{bundle.provenance.generator}</code>, исполнитель{' '}
                  {bundle.provenance.generated_by}
                </td>
              </tr>
              <tr>
                <th scope="row">Версия контракта</th>
                <td>{bundle.contract_version}</td>
              </tr>
              <tr>
                <th scope="row">Источники bundle</th>
                <td>
                  {bundle.provenance.sources
                    .map((s) => s.name + (s.commit ? ` @ ${s.commit}` : ''))
                    .join(' · ')}
                </td>
              </tr>
              <tr>
                <th scope="row">Санитизация</th>
                <td>
                  denylist {bundle.provenance.sanitisation.denylist_version}:
                  отброшено {bundle.provenance.sanitisation.dropped_nodes} узлов
                  и {bundle.provenance.sanitisation.dropped_edges} ребер
                  приватного/неразрешимого яруса
                </td>
              </tr>
              <tr>
                <th scope="row">Права</th>
                <td>
                  Все элементы этого представления — устойчивая структура
                  (temperature <code>structural</code>); внутренние свидетельства
                  называются по имени, но никогда не адресуются ссылкой.
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}
