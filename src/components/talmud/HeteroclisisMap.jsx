// HeteroclisisMap — «Карта основ (гетероклиза)» (§X). The 8×3 case grid coloured
// by which stem each cell selects: сильная {Y} (red), средняя {X} (yellow),
// слабейшая {Z} (grey). Lets the student see the «география» of a word at a
// glance instead of reasoning out the {X/Y/Z} indices cell by cell.
//
// Scope: the animate (masc/fem) consonant-stem paradigm — the canonical
// сарванамастхана (strong-case) set. Neuter reshuffles the strong cases (only
// Nom/Acc/Voc pl are strong); that variant is left to the §X text rather than
// modelled here, to avoid over-claiming.
import React, { useState } from 'react';
import styles from './styles.module.css';

const CASES = ['Nom', 'Acc', 'Ins', 'Dat', 'Abl', 'Gen', 'Loc', 'Voc'];
const NUMS = [
  { key: 'sg', ru: 'ед.' },
  { key: 'du', ru: 'дв.' },
  { key: 'pl', ru: 'мн.' },
];

// Strong cells (сильная основа {Y}) for masc/fem consonant stems.
const STRONG = new Set([
  'Nom.sg', 'Nom.du', 'Nom.pl',
  'Voc.sg', 'Voc.du', 'Voc.pl',
  'Acc.sg', 'Acc.du',
]);
// Middle cells (средняя основа {X}) — endings that begin with a consonant
// (bhyām / bhis / bhyas / su). Everything else weak → weakest {Z}.
const MIDDLE = new Set([
  'Ins.du', 'Dat.du', 'Abl.du',
  'Ins.pl', 'Dat.pl', 'Abl.pl', 'Loc.pl',
]);

function strength(c, n) {
  const k = `${c}.${n}`;
  if (STRONG.has(k)) return 'Y';
  if (MIDDLE.has(k)) return 'X';
  return 'Z';
}

const CLS = { Y: styles.cellStrong, X: styles.cellMid, Z: styles.cellWeak };
const STEM_LABEL = {
  Y: 'сильная основа {Y}',
  X: 'средняя основа {X}',
  Z: 'слабейшая основа {Z}',
};

export default function HeteroclisisMap() {
  const [hover, setHover] = useState(null);

  return (
    <div className={styles.widget}>
      <p className={styles.title}>🗺 Карта основ — гетероклиза {`{X/Y/Z}`}</p>

      <table className={styles.grid}>
        <thead>
          <tr>
            <th></th>
            {NUMS.map((n) => (
              <th key={n.key}>{n.ru}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {CASES.map((c) => (
            <tr key={c}>
              <th>{c}</th>
              {NUMS.map((n) => {
                const s = strength(c, n.key);
                return (
                  <td
                    key={n.key}
                    className={CLS[s]}
                    onMouseEnter={() => setHover({ c, n: n.ru, s })}
                    onMouseLeave={() => setHover(null)}
                    title={`${c}.${n.ru} — ${STEM_LABEL[s]}`}
                  >
                    {s}
                  </td>
                );
              })}
            </tr>
          ))}
        </tbody>
      </table>

      <div className={styles.legend}>
        <span className={styles.legendItem}>
          <span className={styles.swatch} style={{ background: 'rgba(214,69,80,0.16)' }} />
          {'{Y}'} сильная (NOM/VOC/ACC ед. и дв., NOM/VOC мн.)
        </span>
        <span className={styles.legendItem}>
          <span className={styles.swatch} style={{ background: 'rgba(201,138,0,0.14)' }} />
          {'{X}'} средняя (перед согласным окончанием)
        </span>
        <span className={styles.legendItem}>
          <span className={styles.swatch} style={{ background: 'var(--ifm-color-emphasis-100)' }} />
          {'{Z}'} слабейшая (перед гласным окончанием)
        </span>
      </div>

      <p className={styles.caption}>
        {hover
          ? `${hover.c}.${hover.n} → ${STEM_LABEL[hover.s]}.`
          : 'Наведите на ячейку. Показана парадигма основ мужского/женского рода на согласный (сарванамастхана). Средний род перечисляет сильными только NOM/ACC/VOC мн. — см. текст §X.'}
      </p>
    </div>
  );
}
