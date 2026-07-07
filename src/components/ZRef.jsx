// <ZRef sec="42"/> → a clickable "→ Зализняк §42" chip that deep-links to the
// §-addressable in-repo edition of A.A. Zaliznyak's Очерк (1978):
// ZalizniakOcherk_1978/Zaliznyak-Ocherk_29-11-20-aligned, whose every § carries
// an id="s<N>" anchor (injected by tools/inject_ocherk_anchors.py, H241).
//
// `sec` may be a single number or a human range like "50–57, 60" — the chip
// TEXT shows the whole string, and the LINK targets the first § in it (the
// anchor to scroll to). useBaseUrl keeps the URL correct under any baseUrl
// (GitHub Pages /SanskritGrammar/ or the samskrtam.ru deploy).
import React from 'react';
import useBaseUrl from '@docusaurus/useBaseUrl';

const OCHERK_PATH = '/grammars/ZalizniakOcherk_1978/Zaliznyak-Ocherk_29-11-20-aligned';

export default function ZRef({sec, label}) {
  const firstNum = String(sec).match(/\d+/)?.[0];
  const base = useBaseUrl(OCHERK_PATH);
  const href = firstNum ? `${base}#s${firstNum}` : base;
  return (
    <a
      href={href}
      title="Открыть Грамматический очерк санскрита А. А. Зализняка (1978) на нужном §"
      style={{
        display: 'inline-block',
        padding: '0 0.4em',
        borderRadius: '0.6em',
        fontSize: '0.85em',
        background: 'var(--ifm-color-emphasis-200)',
        color: 'inherit',
        textDecoration: 'none',
        whiteSpace: 'nowrap',
      }}
    >
      → Зализняк §{sec}
      {label ? ` (${label})` : null}
    </a>
  );
}
