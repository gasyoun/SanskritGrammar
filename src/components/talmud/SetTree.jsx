// SetTree — «Дерево решений для соединительной гласной seṭ/aniṭ» (§III). The
// student walks Да/Нет branches; the chosen path highlights and lands on an
// outcome: ставить соединительную i/ī, или оставить «голый» стык для сандхи.
// Encodes the {√}+{суффикс} conditions of §III (Таблица 4, ситуация 1) + the
// spec in visual-grammar.md. Real-root examples (author's seṭ/aniṭ/veṭ from
// Приложение 1) come from data/widget_roots.json (H329 Phase 3).
import React, { useState } from 'react';
import styles from './styles.module.css';
import widgetData from '@site/TolchelnikovTalmud_2026/data/widget_roots.json';

const SET_EXAMPLES = widgetData.set_examples;

// Node graph. `yes`/`no` point to another node id or to an outcome object.
const NODES = {
  q1: {
    q: 'Корень помечен как seṭ (принимает соединительную i)?',
    yes: 'q2',
    no: { kind: 'bare', text: 'aniṭ — соединительная не ставится. Стык «голый»: √ + суффикс сходятся напрямую, далее срабатывают сандхи. Пример: √kṛ + ta → kṛtá.' },
  },
  q2: {
    q: 'Суффикс начинается на согласный, кроме полугласных y и n?',
    yes: 'q3',
    no: { kind: 'bare', text: 'Правое условие нарушено: перед гласной либо перед y/n соединительная i не вставляется. Стык остаётся голым.' },
  },
  q3: {
    q: 'Корень оканчивается на долгую ā (или на слабую ступень чередующегося элемента)?',
    yes: { kind: 'bare', text: 'Левое условие нарушено: корни на ā (и слабую ступень) не берут i. Стык голый. Пример: √dā + ta → dattá / -tta.' },
    no: { kind: 'set', text: 'Ставится соединительная i / ī: √ → [√i], затем присоединяется суффикс. Пример: √pat (seṭ) + ta → patitá; √grah + ta → gṛhītá.' },
  },
};

export default function SetTree() {
  const [path, setPath] = useState([]); // [{id, answer}]
  const [current, setCurrent] = useState('q1');
  const [outcome, setOutcome] = useState(null);
  const [exIdx, setExIdx] = useState('');

  function answer(id, yes) {
    const node = NODES[id];
    const target = yes ? node.yes : node.no;
    const nextPath = [...path, { id, answer: yes }];
    setPath(nextPath);
    if (typeof target === 'string') {
      setCurrent(target);
      setOutcome(null);
    } else {
      setCurrent(null);
      setOutcome(target);
    }
  }

  function reset() {
    setPath([]);
    setCurrent('q1');
    setOutcome(null);
    setExIdx('');
  }

  function seatExample(e) {
    const v = e.target.value;
    setExIdx(v);
    if (v === '') {
      setPath([]);
      setCurrent('q1');
      setOutcome(null);
      return;
    }
    // Pre-answer Q1 from the root's author seṭ/aniṭ flag, seating the tree
    // directly (not via answer(), whose closure would read the pre-reset path).
    // veṭ is optional (both outcomes), so leave the tree unanswered for it.
    const r = SET_EXAMPLES[Number(v)];
    if (r.set !== 'seṭ' && r.set !== 'aniṭ') {
      setPath([]);
      setCurrent('q1');
      setOutcome(null);
      return;
    }
    const yes = r.set === 'seṭ';
    const target = yes ? NODES.q1.yes : NODES.q1.no;
    setPath([{ id: 'q1', answer: yes }]);
    if (typeof target === 'string') {
      setCurrent(target);
      setOutcome(null);
    } else {
      setCurrent(null);
      setOutcome(target);
    }
  }

  const ex = exIdx === '' ? null : SET_EXAMPLES[Number(exIdx)];

  return (
    <div className={styles.widget}>
      <p className={styles.title}>🌳 Дерево решений seṭ / aniṭ</p>

      <div className={styles.row}>
        <span className={styles.label}>Начать с корня:</span>
        <select className={styles.select} value={exIdx} onChange={seatExample}>
          <option value="">— вручную —</option>
          {SET_EXAMPLES.map((r, i) => (
            <option key={i} value={i}>
              √{r.root} «{r.gloss}» — {r.set}
            </option>
          ))}
        </select>
        <button className={styles.pill} onClick={reset}>↺ сброс</button>
      </div>

      {ex && (
        <p className={styles.caption}>
          √{ex.root}: p.p.p. <b>{ex.ppp}</b>; seṭ-параметр — <b>{ex.set}</b>
          {ex.set_code && ex.set_code !== ex.set?.[0] ? ` (${ex.set_code})` : ''}
          {ex.set === 'veṭ' ? ' — факультативно, возможны обе формы' : ''}{' '}
          по каталогу Приложения 1 руководства.
          {ex.z_url && (
            <>
              {' '}
              <a href={ex.z_url} target="_blank" rel="noopener noreferrer">
                проверить на samskrtam.ru/z/ ↗
              </a>
            </>
          )}
        </p>
      )}

      {/* Answered branches */}
      {path.map(({ id, answer: a }) => (
        <div key={id} className={styles.node}>
          {NODES[id].q}
          <div className={styles.branchRow}>
            <span className={`${styles.pill} ${a ? styles.pillActive : ''}`}>Да</span>
            <span className={`${styles.pill} ${!a ? styles.pillActive : ''}`}>Нет</span>
          </div>
        </div>
      ))}

      {/* Current question */}
      {current && (
        <div className={`${styles.node} ${styles.nodeActive}`}>
          {NODES[current].q}
          <div className={styles.branchRow}>
            <button className={styles.pill} onClick={() => answer(current, true)}>Да</button>
            <button className={styles.pill} onClick={() => answer(current, false)}>Нет</button>
          </div>
        </div>
      )}

      {/* Outcome */}
      {outcome && (
        <div
          className={`${styles.outcome} ${
            outcome.kind === 'set' ? styles.outcomeSet : styles.outcomeBare
          }`}
        >
          {outcome.kind === 'set' ? '→ Соединительная i / ī' : '→ Голый стык (сандхи)'}
          <p className={styles.caption} style={{ marginTop: '0.4rem' }}>{outcome.text}</p>
        </div>
      )}

      <p className={styles.caption}>
        Дерево охватывает базовый случай стыка <code>{'{√} + {суффикс}'}</code>{' '}
        (Таблица 4, ситуация 1). Особые исключения (причастие <code>us/vans/vat</code>,
        каузатив, аорист, неудвоительный перфект) описаны в тексте §III и здесь
        сознательно не автоматизированы.
      </p>
    </div>
  );
}
