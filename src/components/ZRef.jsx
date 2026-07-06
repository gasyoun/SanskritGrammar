// <ZRef sec="42"/> → "→ Зализняк §42" — inline cross-reference chip from the
// Talmud companion text to A.A. Zaliznyak's Очерк (1978). Stub shipped by the
// H242 Phase-0 scaffold; H241 places the call-sites once the §-concordance
// (TolchelnikovTalmud_2026/zaliznyak-concordance.mdx) is filled.
import React from 'react';

export default function ZRef({sec, label}) {
  return (
    <span
      title="Грамматический очерк санскрита, А. А. Зализняк (1978)"
      style={{
        display: 'inline-block',
        padding: '0 0.4em',
        borderRadius: '0.6em',
        fontSize: '0.85em',
        background: 'var(--ifm-color-emphasis-200)',
        whiteSpace: 'nowrap',
      }}
    >
      → Зализняк §{sec}
      {label ? ` (${label})` : null}
    </span>
  );
}
