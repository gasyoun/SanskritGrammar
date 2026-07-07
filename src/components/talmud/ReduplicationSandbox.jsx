// ReduplicationSandbox — «Песочница редупликации» (§IV). Step through the
// generation of a reduplicated stem: copy the syllable [P']+[F'], then apply the
// mechanical simplification filters (lose aspiration, guttural→palatal, shorten
// the vowel) one at a time. The point of the widget (per visual-grammar.md) is
// that удвоение — не хаос, а строгий механический фильтр.
//
// Traces are CURATED and hand-verified against standard paradigms rather than
// produced by a general engine (which would over-claim on the irregular cases
// §IV explicitly flags). Each demonstrates a different §IV.1 filter.
import React, { useState } from 'react';
import styles from './styles.module.css';

const TRACES = [
  {
    root: 'bhū',
    gloss: 'быть',
    form: 'Перфект (PRFr), 3 sg → babhūva',
    steps: [
      { s: 'bhū', rule: 'Исходный корень [P]+[F] = bh + ū.' },
      { s: 'bhu·bhū', rule: 'Копия слога [P’]+[F’]; долгота гласного сокращена: ū → u.' },
      { s: 'bu·bhū', rule: 'Аспирата теряет придыхание: bh → b (правило §IV.1.1).' },
      { s: 'ba·bhū', rule: 'Гласный удвоения перфекта → a (шаблон PRFr).' },
      { s: 'babhūva', rule: 'Основа + окончание 3 sg перфекта -va.' },
    ],
  },
  {
    root: 'kṛ',
    gloss: 'делать',
    form: 'Перфект (PRFr), 3 sg → cakāra',
    steps: [
      { s: 'kṛ', rule: 'Исходный корень [P]+[F] = k + ṛ.' },
      { s: 'ka·kṛ', rule: 'Копия слога; слоговой сонант ṛ в удвоении даёт a (шаблон PRFr).' },
      { s: 'ca·kṛ', rule: 'Гуттуральный переходит в палатальный: k → c (правило §IV.1.2).' },
      { s: 'ca·kār', rule: 'Корень в сильной ступени (вриддхи) в 3 sg перфекта: ṛ → ār.' },
      { s: 'cakāra', rule: 'Основа + окончание -a.' },
    ],
  },
  {
    root: 'gam',
    gloss: 'идти',
    form: 'Перфект (PRFr), 3 sg → jagāma',
    steps: [
      { s: 'gam', rule: 'Исходный корень; в удвоение берётся только первый согласный g.' },
      { s: 'ga·gam', rule: 'Копия слога [P’]+[F’] = ga.' },
      { s: 'ja·gam', rule: 'Гуттуральный переходит в палатальный: g → j (правило §IV.1.2).' },
      { s: 'ja·gām', rule: 'Корень в сильной ступени в 3 sg: a → ā.' },
      { s: 'jagāma', rule: 'Основа + окончание -a.' },
    ],
  },
  {
    root: 'dā',
    gloss: 'давать',
    form: 'Настоящее, 3 класс (PRSr), 3 sg → dadāti',
    steps: [
      { s: 'dā', rule: 'Исходный корень [P]+[F] = d + ā.' },
      { s: 'da·dā', rule: 'Копия слога; долгота сокращена: ā → a. Придыхания и гуттурали нет.' },
      { s: 'dadā', rule: 'Удвоенная основа настоящего времени (3 класс).' },
      { s: 'dadāti', rule: 'Основа + личное окончание 3 sg -ti.' },
    ],
  },
];

export default function ReduplicationSandbox() {
  const [idx, setIdx] = useState(0);
  const [step, setStep] = useState(0);
  const trace = TRACES[idx];
  const maxStep = trace.steps.length - 1;

  function pick(i) {
    setIdx(i);
    setStep(0);
  }

  return (
    <div className={styles.widget}>
      <p className={styles.title}>🧬 Песочница редупликации — анатомия удвоения</p>

      <div className={styles.row}>
        <span className={styles.label}>Корень:</span>
        {TRACES.map((t, i) => (
          <button
            key={t.root}
            className={`${styles.pill} ${i === idx ? styles.pillActive : ''}`}
            onClick={() => pick(i)}
          >
            √{t.root}
          </button>
        ))}
      </div>

      <p className={styles.caption} style={{ marginTop: 0 }}>
        √{trace.root} «{trace.gloss}» — {trace.form}
      </p>

      <div className={styles.steps}>
        {trace.steps.map((st, i) => (
          <span
            key={i}
            className={`${styles.step} ${i === step ? styles.stepActive : ''}`}
            style={{ opacity: i <= step ? 1 : 0.35 }}
          >
            {st.s}
          </span>
        ))}
      </div>

      <div className={styles.row}>
        <button
          className={styles.pill}
          onClick={() => setStep((s) => Math.max(0, s - 1))}
          disabled={step === 0}
        >
          ← шаг назад
        </button>
        <button
          className={styles.pill}
          onClick={() => setStep((s) => Math.min(maxStep, s + 1))}
          disabled={step === maxStep}
        >
          шаг вперёд →
        </button>
        <span className={styles.label}>
          {step + 1} / {trace.steps.length}
        </span>
      </div>

      <p className={styles.caption}>
        <b>Фильтр:</b> {trace.steps[step].rule}
      </p>
    </div>
  );
}
