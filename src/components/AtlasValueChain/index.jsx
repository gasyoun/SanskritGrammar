// Interactive value-chain view of the Sangram public atlas (slot B4, H627).
// Reads ONLY the sanitised bundle prop (contract §5): stage nodes of the
// value chain plus the typed edges the view declaration lists. The three
// selectable contours are declared as (source, target, kind) triples and
// each link must resolve to a real bundle edge — an unresolved link renders
// as a visible error, never as a silently drawn arrow.
import React, { useMemo, useState } from 'react';
import styles from './styles.module.css';

const VIEW_ID = 'value-chain';

const EDGE_KIND_RU = {
  generates: 'порождает',
  fills: 'наполняет',
  creates: 'создают',
  strengthens: 'усиливает',
  funds: 'финансирует',
  scales: 'масштабируют',
};

// Role taxonomy of the view: sources and products are disjoint types by
// construction — no stage carries two roles (mission rule of slot B4).
const NODE_ROLES = {
  'stage:sources': { role: 'source', ru: 'Источник' },
  'stage:verified-data': { role: 'data', ru: 'Данные и методы' },
  'stage:research-pubs': { role: 'product', ru: 'Продукт' },
  'stage:edu-products': { role: 'product', ru: 'Продукт' },
  'stage:authority': { role: 'return', ru: 'Отдача' },
  'stage:revenue': { role: 'return', ru: 'Отдача' },
  'stage:agents': { role: 'multiplier', ru: 'Мультипликатор' },
};

// The three contours. Every link is a claim that MUST be proven by a bundle
// edge of exactly this (source, target, kind); resolution happens at render
// time against the live bundle.
const CHAINS = [
  {
    id: 'research',
    label: 'Исследовательский контур',
    color: 'var(--ifm-color-primary)',
    marker: 'avc-m-research',
    summary:
      'источники → проверенные данные → исследования и публикации → научный авторитет → обратно в данные',
    links: [
      ['stage:sources', 'stage:verified-data', 'generates'],
      ['stage:verified-data', 'stage:research-pubs', 'fills'],
      ['stage:research-pubs', 'stage:authority', 'creates'],
      ['stage:authority', 'stage:verified-data', 'strengthens'],
    ],
  },
  {
    id: 'education',
    label: 'Образовательный контур',
    color: 'var(--ifm-color-success)',
    marker: 'avc-m-education',
    summary:
      'источники → проверенные данные → образовательные продукты → выручка и аудитория → обратно в данные',
    links: [
      ['stage:sources', 'stage:verified-data', 'generates'],
      ['stage:verified-data', 'stage:edu-products', 'fills'],
      ['stage:edu-products', 'stage:revenue', 'creates'],
      ['stage:revenue', 'stage:verified-data', 'funds'],
    ],
  },
  {
    id: 'agents',
    label: 'Агентный контур',
    color: 'var(--ifm-color-danger)',
    marker: 'avc-m-agents',
    summary:
      'агенты, навыки и организационная память масштабируют данные, публикации и образовательные продукты',
    links: [
      ['stage:agents', 'stage:verified-data', 'scales'],
      ['stage:agents', 'stage:research-pubs', 'scales'],
      ['stage:agents', 'stage:edu-products', 'scales'],
    ],
  },
];

const SHARED_COLOR = 'var(--ifm-color-emphasis-800)';
const SHARED_MARKER = 'avc-m-shared';
const DIM_COLOR = 'var(--ifm-color-emphasis-300)';
const DIM_MARKER = 'avc-m-dim';

// Hand-laid layout of the seven value stages (presentation only; the data
// stays untouched bundle content). viewBox 0 0 940 470.
const NODE_W = 180;
const NODE_H = 58;
const NODE_POS = {
  'stage:sources': { x: 10, y: 165 },
  'stage:verified-data': { x: 250, y: 165 },
  'stage:research-pubs': { x: 500, y: 55 },
  'stage:edu-products': { x: 500, y: 275 },
  'stage:authority': { x: 740, y: 55 },
  'stage:revenue': { x: 740, y: 275 },
  'stage:agents': { x: 250, y: 390 },
};

// Edge geometry keyed by `${source}|${target}`; label position included.
const EDGE_PATHS = {
  'stage:sources|stage:verified-data': {
    d: 'M 190 194 L 250 194',
    lx: 220, ly: 186,
  },
  'stage:verified-data|stage:research-pubs': {
    d: 'M 430 183 C 470 183, 462 84, 500 84',
    lx: 464, ly: 130,
  },
  'stage:verified-data|stage:edu-products': {
    d: 'M 430 205 C 470 205, 462 304, 500 304',
    lx: 464, ly: 262,
  },
  'stage:research-pubs|stage:authority': {
    d: 'M 680 84 L 740 84',
    lx: 710, ly: 76,
  },
  'stage:edu-products|stage:revenue': {
    d: 'M 680 304 L 740 304',
    lx: 710, ly: 296,
  },
  'stage:authority|stage:verified-data': {
    d: 'M 830 55 C 830 8, 345 4, 341 163',
    lx: 585, ly: 22,
  },
  'stage:revenue|stage:verified-data': {
    d: 'M 830 333 C 830 372, 520 368, 434 216',
    lx: 640, ly: 360,
  },
  'stage:agents|stage:verified-data': {
    d: 'M 330 390 L 330 225',
    lx: 300, ly: 310,
  },
  'stage:agents|stage:research-pubs': {
    d: 'M 430 405 C 640 380, 600 200, 585 115',
    lx: 615, ly: 235,
  },
  'stage:agents|stage:edu-products': {
    d: 'M 430 419 C 480 419, 500 370, 545 335',
    lx: 505, ly: 400,
  },
};

const MODES = [
  { id: 'all', label: 'Все контуры' },
  ...CHAINS.map((c) => ({ id: c.id, label: c.label })),
];

function edgeKey(e) {
  return `${e.source}|${e.target}`;
}

export default function AtlasValueChain({ bundle }) {
  const [mode, setMode] = useState('all');
  const [selectedNode, setSelectedNode] = useState(null);

  const model = useMemo(() => {
    const view = bundle.views.find((v) => v.id === VIEW_ID);
    const stageNodes = bundle.nodes.filter(
      (n) => view.node_kinds.includes(n.kind) && n.chain === 'value',
    );
    const stageIds = new Set(stageNodes.map((n) => n.id));
    const edges = bundle.edges.filter(
      (e) =>
        view.edge_kinds.includes(e.kind) &&
        stageIds.has(e.source) &&
        stageIds.has(e.target),
    );
    const nodeById = Object.fromEntries(stageNodes.map((n) => [n.id, n]));

    // Prove every declared chain link with a real bundle edge.
    const chainIdsByEdge = {};
    const unproven = [];
    const chains = CHAINS.map((chain) => {
      const resolved = chain.links.map(([source, target, kind]) => {
        const edge = edges.find(
          (e) => e.source === source && e.target === target && e.kind === kind,
        );
        if (edge) {
          (chainIdsByEdge[edge.id] = chainIdsByEdge[edge.id] || []).push(chain.id);
        } else {
          unproven.push({ chain: chain.label, source, target, kind });
        }
        return { source, target, kind, edge };
      });
      return { ...chain, resolved };
    });

    // Top-tier source classes of the same bundle — the composition of the
    // sources stage (словари · корпуса · грамматики), shown in the detail
    // panel so source types stay explicit and never merge with products.
    const topSourceClasses = bundle.nodes.filter(
      (n) => n.kind === 'source-class' && n.tier === 'top' && !n.parent,
    );

    return { view, stageNodes, edges, nodeById, chains, chainIdsByEdge, unproven, topSourceClasses };
  }, [bundle]);

  const { view, stageNodes, edges, nodeById, chains, chainIdsByEdge, unproven, topSourceClasses } = model;

  const activeChain = chains.find((c) => c.id === mode) || null;
  const activeEdgeIds = new Set(
    activeChain
      ? activeChain.resolved.filter((l) => l.edge).map((l) => l.edge.id)
      : edges.map((e) => e.id),
  );
  const activeNodeIds = new Set(
    activeChain
      ? activeChain.resolved.flatMap((l) => [l.source, l.target])
      : stageNodes.map((n) => n.id),
  );

  function edgePaint(e) {
    if (!activeEdgeIds.has(e.id)) return { color: DIM_COLOR, marker: DIM_MARKER, dim: true };
    if (activeChain) return { color: activeChain.color, marker: activeChain.marker, dim: false };
    const owners = chainIdsByEdge[e.id] || [];
    if (owners.length > 1) return { color: SHARED_COLOR, marker: SHARED_MARKER, dim: false };
    const chain = chains.find((c) => c.id === owners[0]);
    return { color: chain.color, marker: chain.marker, dim: false };
  }

  const tableRows = edges
    .filter((e) => activeEdgeIds.has(e.id))
    .map((e) => ({
      ...e,
      chainLabels: (chainIdsByEdge[e.id] || [])
        .map((id) => chains.find((c) => c.id === id).label)
        .join(' · '),
    }));

  const detail = selectedNode ? nodeById[selectedNode] : null;
  const detailIn = detail ? edges.filter((e) => e.target === detail.id) : [];
  const detailOut = detail ? edges.filter((e) => e.source === detail.id) : [];

  return (
    <div className={styles.wrap}>
      {unproven.length > 0 && (
        <div className="alert alert--danger" role="alert">
          <strong>Недоказанные звенья:</strong> следующие заявленные звенья не
          нашли типизированного ребра в bundle и не отрисованы:{' '}
          {unproven
            .map((u) => `${u.chain}: ${u.source} —${u.kind}→ ${u.target}`)
            .join('; ')}
          . Контракт требует, чтобы каждое звено контура было доказано ребром bundle.
        </div>
      )}

      <p className={styles.counts}>
        Три контура · {chains.reduce((n, c) => n + c.resolved.length, 0)} звеньев ·{' '}
        {edges.length} типизированных ребер · {stageNodes.length} ступеней · снимок
        bundle {bundle.provenance.generated} ({bundle.provenance.generated_by}).
        Общее звено обоих производственных контуров — «источники → проверенные
        данные» — в режиме «Все контуры» выделено нейтральным цветом.
      </p>

      <div className={styles.toolbar} role="group" aria-label="Выбор контура цепочки ценности">
        {MODES.map((m) => (
          <button
            key={m.id}
            type="button"
            className={`button button--sm ${mode === m.id ? 'button--primary' : 'button--secondary'}`}
            aria-pressed={mode === m.id}
            onClick={() => setMode(m.id)}
          >
            {m.label}
          </button>
        ))}
      </div>

      {activeChain && (
        <p className={styles.chainSummary}>
          <strong>{activeChain.label}:</strong> {activeChain.summary}.
        </p>
      )}

      <div className={styles.diagramBox}>
        <svg
          className={styles.svg}
          viewBox="0 0 940 470"
          role="img"
          aria-label={
            'Диаграмма цепочки ценности: ' +
            (activeChain
              ? `${activeChain.label} — ${activeChain.summary}`
              : 'три контура — исследовательский, образовательный и агентный — над семью ступенями от источников до отдачи')
          }
        >
          <defs>
            {[
              ['avc-m-research', 'var(--ifm-color-primary)'],
              ['avc-m-education', 'var(--ifm-color-success)'],
              ['avc-m-agents', 'var(--ifm-color-danger)'],
              [SHARED_MARKER, SHARED_COLOR],
              [DIM_MARKER, DIM_COLOR],
            ].map(([id, fill]) => (
              <marker
                key={id}
                id={id}
                viewBox="0 0 10 10"
                refX="9"
                refY="5"
                markerWidth="7"
                markerHeight="7"
                orient="auto-start-reverse"
              >
                <path d="M 0 0 L 10 5 L 0 10 z" fill={fill} />
              </marker>
            ))}
          </defs>

          {/* lane headers — sources and products are separate lanes by design */}
          <g className={styles.laneHead} aria-hidden="true">
            <text x="100" y="30">Источники</text>
            <text x="340" y="30">Данные и методы</text>
            <text x="590" y="30">Продукты</text>
            <text x="830" y="30">Отдача</text>
          </g>

          {edges.map((e) => {
            const geo = EDGE_PATHS[edgeKey(e)];
            if (!geo) return null;
            const paint = edgePaint(e);
            return (
              <g key={e.id} className={paint.dim ? styles.dimEdge : undefined}>
                <path
                  d={geo.d}
                  fill="none"
                  stroke={paint.color}
                  strokeWidth={paint.dim ? 1.5 : 2.5}
                  markerEnd={`url(#${paint.marker})`}
                />
                <text className={styles.edgeLabel} x={geo.lx} y={geo.ly} textAnchor="middle" fill={paint.dim ? DIM_COLOR : paint.color}>
                  {EDGE_KIND_RU[e.kind]}
                </text>
              </g>
            );
          })}

          {stageNodes.map((n) => {
            const pos = NODE_POS[n.id];
            if (!pos) return null;
            const dim = !activeNodeIds.has(n.id);
            const role = NODE_ROLES[n.id];
            return (
              <g
                key={n.id}
                className={`${styles.node} ${dim ? styles.dimNode : ''} ${selectedNode === n.id ? styles.nodeSelected : ''}`}
                role="button"
                tabIndex={0}
                aria-pressed={selectedNode === n.id}
                aria-label={`${n.label_ru} — роль: ${role.ru}. Показать состав и связи ступени.`}
                onClick={() => setSelectedNode(selectedNode === n.id ? null : n.id)}
                onKeyDown={(ev) => {
                  if (ev.key === 'Enter' || ev.key === ' ') {
                    ev.preventDefault();
                    setSelectedNode(selectedNode === n.id ? null : n.id);
                  }
                }}
              >
                <rect x={pos.x} y={pos.y} width={NODE_W} height={NODE_H} rx="8" />
                <foreignObject x={pos.x} y={pos.y} width={NODE_W} height={NODE_H}>
                  <div xmlns="http://www.w3.org/1999/xhtml" className={styles.nodeLabel}>
                    <span className={`${styles.roleChip} ${styles['role_' + role.role]}`}>{role.ru}</span>
                    <span className={styles.nodeText}>{n.label_ru}</span>
                  </div>
                </foreignObject>
              </g>
            );
          })}
        </svg>
      </div>

      <div aria-live="polite">
        {detail && (
          <div className={styles.detail}>
            <h4 className={styles.detailTitle}>
              {detail.label_ru}{' '}
              <span className={`${styles.roleChip} ${styles['role_' + NODE_ROLES[detail.id].role]}`}>
                {NODE_ROLES[detail.id].ru}
              </span>
            </h4>
            <p className={styles.detailMeta}>
              <code>{detail.id}</code> · температура <code>{detail.temperature}</code> · цепочка{' '}
              <code>{detail.chain}</code>
            </p>
            {detail.id === 'stage:sources' && (
              <p className={styles.detailMeta}>
                Состав ступени по онтологии того же bundle — три верхнеуровневых
                класса источников:{' '}
                {topSourceClasses.map((c, i) => (
                  <React.Fragment key={c.id}>
                    {i > 0 && ' · '}
                    <strong>{c.label_ru}</strong>
                  </React.Fragment>
                ))}
                . Источники — отдельный тип: ни один класс источников не
                является продуктом, ни один продукт не входит в источники.
              </p>
            )}
            {detailIn.length > 0 && (
              <p className={styles.detailMeta}>
                Входящие:{' '}
                {detailIn
                  .map((e) => `${nodeById[e.source].label_ru} (${EDGE_KIND_RU[e.kind]})`)
                  .join(' · ')}
              </p>
            )}
            {detailOut.length > 0 && (
              <p className={styles.detailMeta}>
                Исходящие:{' '}
                {detailOut
                  .map((e) => `${nodeById[e.target].label_ru} (${EDGE_KIND_RU[e.kind]})`)
                  .join(' · ')}
              </p>
            )}
            <button type="button" className="button button--sm button--secondary" onClick={() => setSelectedNode(null)}>
              Закрыть
            </button>
          </div>
        )}
      </div>

      <h3>Звенья {activeChain ? `— ${activeChain.label.toLowerCase()}` : 'всех трех контуров'}</h3>
      <p className={styles.counts}>
        Таблично-текстовый эквивалент диаграммы. Каждое звено доказано
        типизированным ребром bundle; свидетельства с пометкой «внутренний»
        называют источник по имени, но по правилу контракта не адресуются
        ссылкой.
      </p>
      <div className={styles.tableWrap}>
        <table>
          <thead>
            <tr>
              <th scope="col">Контур</th>
              <th scope="col">Звено</th>
              <th scope="col">Тип ребра</th>
              <th scope="col">Ребро bundle</th>
              <th scope="col">Свидетельство</th>
            </tr>
          </thead>
          <tbody>
            {tableRows.map((e) => (
              <tr key={e.id}>
                <td>{e.chainLabels}</td>
                <td>
                  {nodeById[e.source].label_ru} → {nodeById[e.target].label_ru}
                </td>
                <td>
                  <code>{e.kind}</code> — {EDGE_KIND_RU[e.kind]}
                </td>
                <td>
                  <code>{e.id}</code>
                </td>
                <td>
                  {e.evidence ? (
                    <>
                      {e.evidence.label_ru}{' '}
                      <span className={styles.badgeInternal}>
                        {e.evidence.visibility === 'public' ? 'публичное' : 'внутренний реестр, без ссылки'}
                      </span>
                    </>
                  ) : (
                    '—'
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
