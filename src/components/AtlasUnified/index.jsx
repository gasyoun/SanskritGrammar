// Unified five-view route of the Sangram public atlas (slot B6, H621).
// One route hosts all five declared views (bundle.views order) behind an
// accessible tablist; the selected node lives in the ?node= query param and is
// PRESERVED across view switches (?view= param). Views render in controlled
// mode ({selectedId, onSelect}) so they never touch the URL themselves.
// Sibling slots B2-B5 integrate by adding one import + one VIEW_REGISTRY line;
// an unregistered view renders its bundle declaration as a placeholder card,
// so this route builds and works at every intermediate merge state.
import React, { useEffect, useMemo, useRef, useState } from 'react';
import { useHistory, useLocation } from '@docusaurus/router';
import AtlasProvenance from '@site/src/components/AtlasProvenance';
import AtlasAttentionView from '@site/src/components/AtlasAttentionView';
import AtlasValueChain from '@site/src/components/AtlasValueChain';

const VIEW_REGISTRY = {
  provenance: AtlasProvenance,
  attention: AtlasAttentionView, // slot B2 (H629) — bundle-only, no controlled selection yet
  'value-chain': AtlasValueChain, // slot B4 (H627)
  // reuse: AtlasReuseView,              — slot B3 (H630)
  // dependencies: AtlasDependencies,    — slot B5 (H620)
};

const tabStyle = (isActive, isReady) => ({
  padding: '0.4rem 0.8rem',
  fontSize: '0.85rem',
  border: 'none',
  borderBottom: isActive
    ? '3px solid var(--ifm-color-primary)'
    : '3px solid transparent',
  background: 'transparent',
  color: isReady
    ? 'var(--ifm-font-color-base)'
    : 'var(--ifm-color-emphasis-600)',
  fontWeight: isActive ? 700 : 400,
  cursor: 'pointer',
});
const placeholderStyle = {
  border: '1px dashed var(--ifm-color-emphasis-400)',
  borderRadius: 'var(--ifm-card-border-radius, 8px)',
  padding: '0.75rem 1rem',
  margin: '1rem 0',
};
const selectionNoteStyle = {
  fontSize: '0.85rem',
  color: 'var(--ifm-color-emphasis-700)',
  margin: '0.5rem 0 0',
};

export default function AtlasUnified({ bundle }) {
  const history = useHistory();
  const location = useLocation();
  const tabRefs = useRef([]);

  const views = bundle.views;
  const byId = useMemo(
    () => Object.fromEntries(bundle.nodes.map((n) => [n.id, n])),
    [bundle]
  );

  // Query params are read only after mount: SSG HTML is param-less, and a
  // param-driven first render would break hydration (React #418/#423).
  const [mounted, setMounted] = useState(false);
  useEffect(() => setMounted(true), []);
  const params = new URLSearchParams(mounted ? location.search : '');
  const viewParam = params.get('view');
  const active =
    views.find((v) => v.id === viewParam)?.id ||
    views.find((v) => VIEW_REGISTRY[v.id])?.id ||
    views[0].id;
  const selected = params.get('node');
  const selectedNode = selected ? byId[selected] : null;

  const setParams = (patch) => {
    const next = new URLSearchParams(location.search);
    for (const [k, v] of Object.entries(patch)) {
      if (v) next.set(k, v);
      else next.delete(k);
    }
    history.replace({ search: next.toString(), hash: location.hash });
  };

  const activeView = views.find((v) => v.id === active);
  const ActiveComponent = VIEW_REGISTRY[active];
  // In the view iff its kind is declared — and provenance additionally
  // scopes stage nodes to its own chain.
  const activeHoldsSelection =
    !!selectedNode &&
    activeView.node_kinds.includes(selectedNode.kind) &&
    (active !== 'provenance' ||
      selectedNode.kind === 'source-class' ||
      selectedNode.chain === 'provenance');

  const onTabKeyDown = (e, idx) => {
    if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
    e.preventDefault();
    const delta = e.key === 'ArrowRight' ? 1 : -1;
    const next = (idx + delta + views.length) % views.length;
    tabRefs.current[next]?.focus();
    setParams({ view: views[next].id });
  };

  return (
    <div>
      <div
        role="tablist"
        aria-label="Пять представлений атласа"
        style={{
          display: 'flex',
          flexWrap: 'wrap',
          gap: '0.25rem',
          borderBottom: '1px solid var(--ifm-color-emphasis-300)',
        }}
      >
        {views.map((v, idx) => (
          <button
            key={v.id}
            ref={(el) => {
              tabRefs.current[idx] = el;
            }}
            type="button"
            role="tab"
            id={`atlas-tab-${v.id}`}
            aria-selected={active === v.id}
            aria-controls={`atlas-panel-${v.id}`}
            tabIndex={active === v.id ? 0 : -1}
            style={tabStyle(active === v.id, !!VIEW_REGISTRY[v.id])}
            onClick={() => setParams({ view: v.id })}
            onKeyDown={(e) => onTabKeyDown(e, idx)}
          >
            {v.title_ru}
            {!VIEW_REGISTRY[v.id] && ' (готовится)'}
          </button>
        ))}
      </div>

      {selectedNode && (
        <p style={selectionNoteStyle} aria-live="polite">
          Выбранный узел сохраняется между представлениями:{' '}
          <strong>{selectedNode.label_ru}</strong>
          {!activeHoldsSelection &&
            ' — в текущем представлении этот узел не участвует, но выбор не сброшен.'}{' '}
          <button
            type="button"
            style={{
              border: '1px solid var(--ifm-color-emphasis-400)',
              borderRadius: '6px',
              background: 'var(--ifm-background-surface-color)',
              color: 'var(--ifm-font-color-base)',
              cursor: 'pointer',
              fontSize: '0.78rem',
              padding: '0.1rem 0.45rem',
            }}
            onClick={() => setParams({ node: null })}
          >
            сбросить выбор
          </button>
        </p>
      )}

      <div
        role="tabpanel"
        id={`atlas-panel-${active}`}
        aria-labelledby={`atlas-tab-${active}`}
      >
        {ActiveComponent ? (
          <ActiveComponent
            bundle={bundle}
            selectedId={selected}
            onSelect={(id) => setParams({ node: id })}
          />
        ) : (
          <article style={placeholderStyle} aria-label={activeView.title_ru}>
            <h2 style={{ marginBottom: '0.25rem' }}>{activeView.title_ru}</h2>
            <p style={{ marginBottom: '0.25rem' }}>{activeView.question_ru}</p>
            <p style={{ marginBottom: 0, color: 'var(--ifm-color-emphasis-700)' }}>
              Данные для представления уже в bundle (
              {bundle.nodes.filter((n) => activeView.node_kinds.includes(n.kind)).length}{' '}
              узлов,{' '}
              {bundle.edges.filter((e) => activeView.edge_kinds.includes(e.kind)).length}{' '}
              ребер) · маршрут <code>{activeView.route.slug}</code> ·
              интерактивное представление подключается слотом{' '}
              {activeView.route.owner_slot} серии.
            </p>
          </article>
        )}
      </div>
    </div>
  );
}
