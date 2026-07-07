// AblautMachine — «Машина аблаута» (§II). Pick a Ряд (ablaut series A₁…N₂) or a
// real Whitney root, then toggle Слабая ⇔ Гуна ⇔ Вриддхи and watch the nucleus
// vowel breathe. Every later chapter's derivations call this calculus, so it is
// built first (H241 Phase 2). Series table: ./ablautSeries.js; example roots:
// TolchelnikovTalmud_2026/data/widget_roots.json (derived Ряд, gated proposals).
import React, { useState } from 'react';
import styles from './styles.module.css';
import { SERIES, SERIES_ORDER, GRADES } from './ablautSeries';
import widgetData from '@site/TolchelnikovTalmud_2026/data/widget_roots.json';

const EXAMPLES = widgetData.ablaut_examples;

export default function AblautMachine() {
  const [series, setSeries] = useState('R₁');
  const [grade, setGrade] = useState('guna'); // weak | guna | vrddhi
  const [beforeVowel, setBeforeVowel] = useState(false);
  const [rootIdx, setRootIdx] = useState(''); // '' = free (no example root seated)

  const g = GRADES.find((x) => x.key === grade);
  const cell = SERIES[series][grade];
  const surface = beforeVowel && cell.v ? cell.v : cell.c;
  const example = rootIdx === '' ? null : EXAMPLES[Number(rootIdx)];

  function pickRoot(e) {
    const v = e.target.value;
    setRootIdx(v);
    if (v !== '') setSeries(EXAMPLES[Number(v)].ryad);
  }

  return (
    <div className={styles.widget}>
      <p className={styles.title}>⚙ Машина аблаута — тренажёр ступеней</p>

      <div className={styles.row}>
        <span className={styles.label}>Реальный корень:</span>
        <select className={styles.select} value={rootIdx} onChange={pickRoot}>
          <option value="">— свободный выбор ряда —</option>
          {EXAMPLES.map((r, i) => (
            <option key={i} value={i}>
              √{r.root} «{r.gloss}» — {r.ryad}
            </option>
          ))}
        </select>
      </div>

      <div className={styles.row}>
        <span className={styles.label}>Ряд:</span>
        {SERIES_ORDER.map((s) => (
          <button
            key={s}
            className={`${styles.pill} ${s === series ? styles.pillActive : ''}`}
            onClick={() => {
              setSeries(s);
              setRootIdx('');
            }}
          >
            {s}
          </button>
        ))}
      </div>

      <div className={styles.row}>
        <span className={styles.label}>Ступень:</span>
        {GRADES.map((x) => (
          <button
            key={x.key}
            className={`${styles.pill} ${x.key === grade ? styles.pillActive : ''}`}
            onClick={() => setGrade(x.key)}
          >
            {x.ru}
          </button>
        ))}
        <span className={styles.label} style={{ marginLeft: '0.6rem' }}>Позиция:</span>
        <button
          className={`${styles.pill} ${beforeVowel ? '' : styles.pillActive}`}
          onClick={() => setBeforeVowel(false)}
        >
          перед согласным
        </button>
        <button
          className={`${styles.pill} ${beforeVowel ? styles.pillActive : ''}`}
          onClick={() => setBeforeVowel(true)}
        >
          перед гласной
        </button>
      </div>

      <div className={styles.display}>
        {example && <span className={styles.formMuted}>√{example.root} →</span>}
        <span className={`${styles.form} ${styles[g.cls]}`}>{surface}</span>
        <span className={styles.formMuted}>
          {g.ru} · {g.pos} · ряд {series}
        </span>
      </div>

      <p className={styles.caption}>
        {example ? (
          <>
            √{example.root} «{example.gloss}» (кл.{' '}
            {example.class.length ? example.class.join(', ') : '—'}) отнесён к ряду{' '}
            <b>{example.ryad}</b>{' '}
            {example.ryad_confidence === 'high'
              ? '(ступень фонологически однозначна)'
              : example.ryad_confidence === 'low'
              ? '(ряд восстановлен по огласовке — низкая уверенность)'
              : '(ряд — предложение, требует проверки)'}
            . Показан только чередующийся элемент корня, не вся словоформа. Ряд —
            производная величина, не утверждение автора: см. footnote-proposals.
          </>
        ) : (
          <>
            Позиция окончания задаёт ступень (Поз. 1 → вриддхи, Поз. 2 → гуна,
            Поз. 3 → слабая, для стандартного типа «s»). В скобках Таблицы 2 —
            алломорф перед гласной; переключите «перед гласной», чтобы увидеть его.
          </>
        )}
      </p>
    </div>
  );
}
