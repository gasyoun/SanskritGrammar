// AttestedClozeDrill — «Тренажёр пропущенного слова» (RQ2 cloze type).
//
// The generic Wave-2 deliverable "auto-drill generation with verified answer keys"
// (RQ2) names three drill shapes: sandhi-split (emeneo), paradigm-fill (the
// attested-cell declension trainer, H1296) and cloze. This widget is the third.
//
// Its answer key needs no generation step to agree or disagree with: the blank
// is filled by the CORPUS'S OWN word at that position in an attested DCS sentence
// -- the question and the answer come from the same source, so there is nothing
// to verify except the sentence that produced the question. Distractors are other
// attested forms of the same lemma in a different case/tense cell, never invented.
import React, { useMemo, useState } from 'react';
import styles from './styles.module.css';
import { ATTESTED_CLOZE_DRILLS } from './attestedClozeData';

const UPOS_RU = { NOUN: 'существительное', VERB: 'глагол' };

function shuffledOptions(item, seed) {
  const opts = [item.answer, ...item.distractors];
  // Deterministic per-item shuffle (Fisher-Yates keyed on a stable seed) so the
  // correct answer is not always in the same slot, but re-renders are stable.
  let s = seed;
  const rand = () => {
    s = (s * 1103515245 + 12345) & 0x7fffffff;
    return s / 0x7fffffff;
  };
  const arr = [...opts];
  for (let i = arr.length - 1; i > 0; i -= 1) {
    const j = Math.floor(rand() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
}

const ALL_UPOS = Array.from(new Set(ATTESTED_CLOZE_DRILLS.map((d) => d.upos)));

export default function AttestedClozeDrill() {
  const [upos, setUpos] = useState(ALL_UPOS[0] || 'NOUN');
  const [index, setIndex] = useState(0);
  const [answer, setAnswer] = useState(null);
  const [checked, setChecked] = useState(false);
  const [score, setScore] = useState({ right: 0, total: 0 });

  const pool = useMemo(
    () => ATTESTED_CLOZE_DRILLS.filter((d) => d.upos === upos),
    [upos],
  );
  const item = pool.length ? pool[index % pool.length] : null;
  const options = useMemo(
    () => (item ? shuffledOptions(item, item.sentenceId) : []),
    [item],
  );

  function reset(nextIdx) {
    setIndex(nextIdx);
    setAnswer(null);
    setChecked(false);
  }

  function check(choice) {
    if (checked || !item) return;
    setAnswer(choice);
    setChecked(true);
    setScore((s) => ({ right: s.right + (choice === item.answer ? 1 : 0), total: s.total + 1 }));
  }

  function next() {
    reset(index + 1);
  }

  function pickUpos(u) {
    setUpos(u);
    reset(0);
    setScore({ right: 0, total: 0 });
  }

  if (!item) {
    return (
      <div className={styles.widget}>
        <p className={styles.title}>Тренажёр пропущенного слова</p>
        <p className={styles.caption}>Для этой части речи нет материала.</p>
      </div>
    );
  }

  const correct = checked && answer === item.answer;

  return (
    <div className={styles.widget}>
      <p className={styles.title}>Тренажёр пропущенного слова (cloze)</p>

      <div className={styles.row}>
        <span className={styles.label}>Часть речи:</span>
        {ALL_UPOS.map((u) => (
          <button
            key={u}
            type="button"
            className={u === upos ? `${styles.pill} ${styles.pillActive}` : styles.pill}
            onClick={() => pickUpos(u)}
          >
            {UPOS_RU[u] || u}
          </button>
        ))}
        <span className={styles.label} style={{ marginLeft: 'auto' }}>
          {score.total > 0 ? `${score.right} / ${score.total}` : ' '}
        </span>
      </div>

      <div className={styles.drillCard}>
        <div className={styles.drillPrompt}>{item.cloze}</div>
        <div className={styles.row}>
          {options.map((opt) => {
            let cls = styles.pill;
            if (checked && opt === item.answer) cls = `${styles.pill} ${styles.pillActive}`;
            else if (checked && opt === answer) cls = styles.drillWrong;
            return (
              <button
                key={opt}
                type="button"
                className={cls}
                disabled={checked}
                onClick={() => check(opt)}
              >
                {opt}
              </button>
            );
          })}
        </div>
        <div className={styles.row}>
          <button type="button" className={styles.pill} onClick={checked ? next : undefined} disabled={!checked}>
            дальше →
          </button>
        </div>

        {checked && (
          <div className={correct ? styles.drillRight : styles.drillWrong}>
            <strong>{correct ? 'Верно' : 'Неверно'}</strong>
            {' · '}
            {item.lemma} ({item.cell})
            <div className={styles.drillEvidence}>
              <span className={styles.label}>полное предложение из корпуса:</span>{' '}
              <code>{item.full}</code>
              {item.sentId ? <> (DCS #{item.sentId})</> : null}
            </div>
          </div>
        )}
      </div>

      <p className={styles.caption}>
        Пропущенное слово — не порождённая форма, а слово, реально стоящее в этом
        месте в засвидетельствованном предложении корпуса DCS; отвлекающие варианты —
        тоже реально засвидетельствованные формы той же леммы, но в другой ячейке.
        Корпус: DCS (Oliver Hellwig), закреплённый снимок VisualDCS.
      </p>
    </div>
  );
}
