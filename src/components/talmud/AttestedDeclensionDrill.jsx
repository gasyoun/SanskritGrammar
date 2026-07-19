// AttestedDeclensionDrill — «Тренажёр засвидетельствованных падежных форм» (H1296).
//
// Every other declension drill in the project (kosha W1a / H946 included) drills the
// paradigm ENGINE: all 8 cases x 3 numbers, generated. The G2 coverage asset measured
// that only 10.44 % of the noun lemma x 24-cell space is ever corpus-attested. This
// widget drills the other side: ONLY cells the corpus actually attests, ordered by
// kosha frequency, grouped by Zaliznyak stem class.
//
// The pedagogical rule it enforces: where the engine and the corpus disagree, the
// learner is shown BOTH, never a silent pick. `mismatch` cells are excluded from
// drilling entirely — they are displayed as evidence in a separate panel, because a
// cell whose generated form is unattested has no authoritative answer to grade against.
import React, { useMemo, useState } from 'react';
import styles from './styles.module.css';
import { ATTESTED_DRILLS } from './attestedDrillData';

const CASE_RU = {
  Nom: 'Им.', Acc: 'Вин.', Ins: 'Твор.', Dat: 'Дат.',
  Abl: 'Отл.', Gen: 'Род.', Loc: 'Мест.', Voc: 'Зват.',
};
const NUMBER_RU = { Sing: 'ед.', Dual: 'дв.', Plur: 'мн.' };
const GENDER_RU = { Masc: 'м. р.', Neut: 'ср. р.', Fem: 'ж. р.' };

const STEM_CLASS_RU = {
  'a-stem': 'основы на -a',
  'ā-stem': 'основы на -ā',
  'i-stem': 'основы на -i',
  'ī-stem': 'основы на -ī',
  'u-stem': 'основы на -u',
  'ū-stem': 'основы на -ū',
  'consonant-stem': 'основы на согласный',
  indeclinable: 'неизменяемые (по Зализняку)',
};

function cellRu(cell) {
  const [c, n] = cell.split('.');
  return `${CASE_RU[c] || c} ${NUMBER_RU[n] || n}`;
}

// Accept any spelling the evidence supports: the generated form or any attested
// variant. Deliberately lenient on case/whitespace only — not on diacritics, which
// carry the paradigm distinction being taught.
function isCorrect(input, cell) {
  const given = input.trim().toLowerCase();
  if (!given) return false;
  const ok = [...cell.expected.split('|'), ...cell.attested.split('|')]
    .filter(Boolean)
    .map((f) => f.trim().toLowerCase());
  return ok.includes(given);
}

const ALL_CLASSES = Array.from(new Set(ATTESTED_DRILLS.map((l) => l.stemClass)));

export default function AttestedDeclensionDrill() {
  const [stemClass, setStemClass] = useState('a-stem');
  const [mode, setMode] = useState('form'); // 'form' = напиши форму, 'cell' = определи ячейку
  const [index, setIndex] = useState(0);
  const [answer, setAnswer] = useState('');
  const [checked, setChecked] = useState(false);
  const [score, setScore] = useState({ right: 0, total: 0 });

  const pool = useMemo(
    () => ATTESTED_DRILLS.filter((l) => l.stemClass === stemClass),
    [stemClass],
  );

  const lemma = pool.length ? pool[index % pool.length] : null;
  const drillable = useMemo(
    () => (lemma ? lemma.cells.filter((c) => c.drillable) : []),
    [lemma],
  );
  const flagged = useMemo(
    () => (lemma ? lemma.cells.filter((c) => !c.drillable) : []),
    [lemma],
  );

  const [cellIdx, setCellIdx] = useState(0);
  const cell = drillable.length ? drillable[cellIdx % drillable.length] : null;

  function reset(nextLemmaIdx, nextCellIdx) {
    setIndex(nextLemmaIdx);
    setCellIdx(nextCellIdx);
    setAnswer('');
    setChecked(false);
  }

  function check() {
    if (checked || !cell) return;
    const right = mode === 'form' ? isCorrect(answer, cell) : answer === cell.cell;
    setScore((s) => ({ right: s.right + (right ? 1 : 0), total: s.total + 1 }));
    setChecked(true);
  }

  function next() {
    const nextCell = cellIdx + 1;
    if (nextCell >= drillable.length) reset(index + 1, 0);
    else reset(index, nextCell);
  }

  function pickClass(cls) {
    setStemClass(cls);
    reset(0, 0);
    setScore({ right: 0, total: 0 });
  }

  if (!lemma || !cell) {
    return (
      <div className={styles.widget}>
        <p className={styles.title}>Тренажёр засвидетельствованных форм</p>
        <p className={styles.caption}>Для этого класса основ нет материала.</p>
      </div>
    );
  }

  const correct = checked && (mode === 'form' ? isCorrect(answer, cell) : answer === cell.cell);
  const attestedList = cell.attested.split('|').filter(Boolean);
  const expectedList = cell.expected.split('|').filter(Boolean);

  return (
    <div className={styles.widget}>
      <p className={styles.title}>
        Тренажёр засвидетельствованных падежных форм
      </p>

      <div className={styles.row}>
        <span className={styles.label}>Класс основы:</span>
        {ALL_CLASSES.map((cls) => (
          <button
            key={cls}
            type="button"
            className={cls === stemClass ? `${styles.pill} ${styles.pillActive}` : styles.pill}
            onClick={() => pickClass(cls)}
          >
            {STEM_CLASS_RU[cls] || cls}
          </button>
        ))}
      </div>

      <div className={styles.row}>
        <span className={styles.label}>Режим:</span>
        <button
          type="button"
          className={mode === 'form' ? `${styles.pill} ${styles.pillActive}` : styles.pill}
          onClick={() => { setMode('form'); reset(index, cellIdx); }}
        >
          напиши форму
        </button>
        <button
          type="button"
          className={mode === 'cell' ? `${styles.pill} ${styles.pillActive}` : styles.pill}
          onClick={() => { setMode('cell'); reset(index, cellIdx); }}
        >
          определи ячейку
        </button>
        <span className={styles.label} style={{ marginLeft: 'auto' }}>
          {score.total > 0 ? `${score.right} / ${score.total}` : ' '}
        </span>
      </div>

      <div className={styles.drillCard}>
        <div className={styles.drillLemma}>
          {lemma.lemma}
          <span className={styles.drillMeta}>
            {STEM_CLASS_RU[lemma.stemClass] || lemma.stemClass}
            {lemma.gender ? `, ${GENDER_RU[lemma.gender] || lemma.gender}` : ''}
            {' · '}
            засвидетельствовано {lemma.cells.length} из 24 ячеек
          </span>
        </div>

        {mode === 'form' ? (
          <>
            <div className={styles.drillPrompt}>
              {cellRu(cell.cell)} — какая форма?
            </div>
            <input
              className={styles.drillInput}
              value={answer}
              onChange={(e) => setAnswer(e.target.value)}
              onKeyDown={(e) => { if (e.key === 'Enter') (checked ? next() : check()); }}
              placeholder="IAST, напр. devaḥ"
              disabled={checked}
              aria-label="Введите форму в IAST"
            />
          </>
        ) : (
          <>
            <div className={styles.drillPrompt}>
              <span className={styles.drillForm}>{attestedList[0] || expectedList[0]}</span>
              {' — какая это ячейка?'}
            </div>
            <div className={styles.row}>
              {drillable.map((c) => (
                <button
                  key={c.cell}
                  type="button"
                  className={answer === c.cell ? `${styles.pill} ${styles.pillActive}` : styles.pill}
                  onClick={() => !checked && setAnswer(c.cell)}
                  disabled={checked}
                >
                  {cellRu(c.cell)}
                </button>
              ))}
            </div>
          </>
        )}

        <div className={styles.row}>
          <button type="button" className={styles.pill} onClick={checked ? next : check}>
            {checked ? 'дальше →' : 'проверить'}
          </button>
        </div>

        {checked && (
          <div className={correct ? styles.drillRight : styles.drillWrong}>
            <strong>{correct ? 'Верно' : 'Неверно'}</strong>
            {' · '}
            {cellRu(cell.cell)}
            {' · '}
            засвидетельствовано в корпусе {cell.count}{' '}
            {cell.count === 1 ? 'раз' : 'раз(а)'}
            <div className={styles.drillEvidence}>
              <span className={styles.label}>в корпусе:</span>{' '}
              {attestedList.map((f) => <code key={f}>{f}</code>).reduce(
                (acc, el) => (acc === null ? [el] : [...acc, ' · ', el]), null,
              )}
              {cell.agreement === 'variant' && (
                <>
                  <br />
                  <span className={styles.label}>порождено грамматикой:</span>{' '}
                  {expectedList.map((f) => <code key={f}>{f}</code>)}
                  <br />
                  <em>
                    Корпус даёт больше одной формы — ведийские и классические варианты
                    сосуществуют. Засчитана любая засвидетельствованная.
                  </em>
                </>
              )}
            </div>
          </div>
        )}
      </div>

      {flagged.length > 0 && (
        <div className={styles.drillFlagged}>
          <span className={styles.label}>
            Не даётся в тренажёре ({flagged.length}):
          </span>{' '}
          порождённая форма не встречается в корпусе в этой ячейке — авторитетного
          ответа нет, поэтому показываем обе стороны как свидетельство, а не как задание.
          <ul>
            {flagged.map((c) => (
              <li key={c.cell}>
                {cellRu(c.cell)}: грамматика <code>{c.expected || '—'}</code>, корпус{' '}
                <code>{c.attested || '—'}</code> ({c.count})
              </li>
            ))}
          </ul>
        </div>
      )}

      <p className={styles.caption}>
        Только засвидетельствованные ячейки: полная парадигма из 24 форм — объект
        порождённый, а не наблюдаемый (G2: засвидетельствовано лишь 10,44 % пространства
        лемма × ячейка). Формы приведены без сандхи. Корпус: DCS (Oliver Hellwig),
        закреплённый снимок VisualDCS; классы основ — индекс по Зализняку; порядок лемм —
        частотность kosha.
      </p>
    </div>
  );
}
