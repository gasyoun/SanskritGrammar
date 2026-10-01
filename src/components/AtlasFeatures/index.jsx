// Features view of the Sangram public atlas (contract 1.1.1, slot B7/H3509).
// Card list of `asset` families with their FEATURES_INDEX I-IV joins
// (`feature_ids`), plus the committed unmatched list. Cards only — no new
// graph library (plan fence R5.4).
import React from 'react';

const cardStyle = {
  border: '1px solid var(--ifm-color-emphasis-300)',
  borderRadius: 'var(--ifm-card-border-radius, 8px)',
  padding: '0.9rem 1rem',
  background: 'var(--ifm-background-surface-color)',
};

const chipStyle = {
  display: 'inline-block',
  border: '1px solid var(--ifm-color-emphasis-400)',
  borderRadius: '12px',
  padding: '0 0.45rem',
  margin: '0.15rem 0.25rem 0.15rem 0',
  fontSize: '0.78rem',
  fontFamily: 'var(--ifm-font-family-monospace)',
};

const rightsColor = {
  open: 'var(--ifm-color-success)',
  'rights-gated': 'var(--ifm-color-warning)',
  quarantine: 'var(--ifm-color-danger)',
};

function AssetCard({ node }) {
  const ids = node.feature_ids || [];
  return (
    <article style={cardStyle}>
      <h3 style={{ margin: '0 0 0.35rem', fontSize: '0.98rem' }}>
        {node.url ? (
          <a href={node.url}>{node.label_ru}</a>
        ) : (
          node.label_ru
        )}
      </h3>
      <p style={{ margin: '0 0 0.4rem', fontSize: '0.82rem', color: 'var(--ifm-color-emphasis-700)' }}>
        {node.asset_types.join(' · ')} ·{' '}
        <span style={{ color: rightsColor[node.rights] || 'inherit' }}>{node.rights}</span>
      </p>
      {ids.length > 0 ? (
        <div aria-label="Присоединённые строки каталога возможностей">
          {ids.map((id) => (
            <span key={id} style={chipStyle}>{id}</span>
          ))}
        </div>
      ) : (
        <p style={{ margin: 0, fontSize: '0.8rem', fontStyle: 'italic', color: 'var(--ifm-color-emphasis-600)' }}>
          Нет присоединённых строк каталога
        </p>
      )}
      {node.prohibition_ru && (
        <p style={{ margin: '0.5rem 0 0', fontSize: '0.8rem', color: 'var(--ifm-color-emphasis-700)' }}>
          ⛔ {node.prohibition_ru}
        </p>
      )}
    </article>
  );
}

export default function AtlasFeatures({ bundle, unmatched }) {
  const assets = bundle.nodes.filter((n) => n.kind === 'asset');
  const joined = assets.filter((n) => (n.feature_ids || []).length > 0);
  const rows = unmatched?.unmatched || [];
  return (
    <div>
      <p style={{ fontSize: '0.9rem' }}>
        {assets.length} публичных семейств активов ·{' '}
        {joined.length} с присоединёнными строками ·{' '}
        {rows.length} строк каталога пока не присоединено (причина у каждой).
      </p>

      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))',
          gap: '0.8rem',
        }}
      >
        {assets.map((n) => (
          <AssetCard key={n.id} node={n} />
        ))}
      </div>

      <h2 style={{ marginTop: '1.5rem' }}>Не присоединённые строки каталога</h2>
      <p style={{ fontSize: '0.85rem', color: 'var(--ifm-color-emphasis-700)' }}>
        Каждая строка FEATURES_INDEX I–IV либо присоединена к семейству выше,
        либо числится здесь с причиной — тихих потерь нет.
      </p>
      <table style={{ fontSize: '0.82rem', width: '100%' }}>
        <thead>
          <tr>
            <th style={{ textAlign: 'left' }}>ID</th>
            <th style={{ textAlign: 'left' }}>Строка</th>
            <th style={{ textAlign: 'left' }}>Причина</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((r) => (
            <tr key={`${r.id}-${r.title}`}>
              <td style={{ fontFamily: 'var(--ifm-font-family-monospace)', whiteSpace: 'nowrap' }}>{r.id}</td>
              <td>{r.title}</td>
              <td style={{ color: 'var(--ifm-color-emphasis-700)' }}>{r.reason}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
