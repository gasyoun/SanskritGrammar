// SamasaLadderDrill — «Лестница разбора композита справа налево» (H1298, W2-add-c).
//
// kosha's samāsa trainer (W1c, H948) drills *which type is this compound* and *where
// does it split*. This widget drills neither: it drills the **resolution method** — the
// head-first ladder of the German-Indological Klammerübersetzung tradition. In a
// determinative compound the syntactic head is the LAST member, so the analysis runs
// right → left: name the head, then ask the question it leaves open and let the next
// member leftwards answer it.
//
// What the widget refuses to do: assert a compound type. The type is not derivable from
// the split, and it is H948's subject anyway. Each modifier rung therefore shows a
// question *slot* (several candidate case-questions), never one "correct" question — the
// single ratified reading exists only for the 30 hand-checked compounds of the gold set.
import React, { useMemo, useState } from 'react';
import styles from './styles.module.css';
import { SAMASA_LADDERS } from './samasaLadderData';

const BANDS = ['ядро', 'частые', 'средние', 'редкие'];
const BAND_HINT = {
  ядро: '≥ 100 вхождений в DCS',
  частые: '30–99',
  средние: '10–29',
  редкие: '5–9',
};

function shuffledMembers(item) {
  // Deterministic per compound (no Math.random — the same card must look the same on
  // every render, otherwise the options reshuffle under the learner's cursor).
  const seed = item.surface.length + item.depth;
  return item.members
    .map((m, i) => ({ m, i, k: (i * 7 + seed * 13) % item.members.length }))
    .sort((a, b) => a.k - b.k)
    .map((x) => x);
}

export default function SamasaLadderDrill() {
  const [band, setBand] = useState('ядро');
  const [index, setIndex] = useState(0);
  const [headPick, setHeadPick] = useState(null);
  const [revealed, setRevealed] = useState(0);
  const [score, setScore] = useState({ right: 0, total: 0 });

  const pool = useMemo(() => SAMASA_LADDERS.filter((l) => l.band === band), [band]);
  const item = pool.length ? pool[index % pool.length] : null;

  function reset(nextIdx) {
    setIndex(nextIdx);
    setHeadPick(null);
    setRevealed(0);
  }

  function pickBand(b) {
    setBand(b);
    reset(0);
    setScore({ right: 0, total: 0 });
  }

  function pickHead(member, isLast) {
    if (headPick) return;
    setHeadPick(member);
    setRevealed(1);
    setScore((s) => ({ right: s.right + (isLast ? 1 : 0), total: s.total + 1 }));
  }

  if (!item) {
    return (
      <div className={styles.widget}>
        <p className={styles.title}>Лестница разбора композита</p>
        <p className={styles.caption}>Для этой полосы частотности нет материала.</p>
      </div>
    );
  }

  const headMember = item.members[item.members.length - 1];
  const headCorrect = headPick === headMember;
  const options = shuffledMembers(item);
  const done = revealed >= item.depth;

  return (
    <div className={styles.widget}>
      <p className={styles.title}>Лестница разбора композита: справа налево</p>

      <div className={styles.row}>
        <span className={styles.label}>Частотность:</span>
        {BANDS.map((b) => (
          <button
            key={b}
            type="button"
            title={BAND_HINT[b]}
            className={b === band ? `${styles.pill} ${styles.pillActive}` : styles.pill}
            onClick={() => pickBand(b)}
          >
            {b}
          </button>
        ))}
        <span className={styles.label} style={{ marginLeft: 'auto' }}>
          {score.total > 0 ? `голова: ${score.right} / ${score.total}` : ' '}
        </span>
      </div>

      <div className={styles.drillCard}>
        <div className={styles.drillLemma}>
          {item.surface}
          <span className={styles.drillMeta}>
            {item.depth} члена{item.depth > 2 ? '' : ''} · {item.freq} вхождений в корпусе
          </span>
        </div>

        {!headPick ? (
          <>
            <div className={styles.drillPrompt}>
              Какой член — <strong>голова</strong>? (то, чем эта вещь является)
            </div>
            <div className={styles.row}>
              {options.map(({ m, i }) => (
                <button
                  key={`${m}-${i}`}
                  type="button"
                  className={styles.pill}
                  onClick={() => pickHead(m, i === item.members.length - 1)}
                >
                  {m}
                </button>
              ))}
            </div>
          </>
        ) : (
          <>
            <div className={headCorrect ? styles.drillRight : styles.drillWrong}>
              <strong>{headCorrect ? 'Верно' : 'Неверно'}</strong> — голова это{' '}
              <code>{headMember}</code>, <em>последний</em> член.
              {!headCorrect && (
                <div className={styles.drillEvidence}>
                  Вы выбрали <code>{headPick}</code>. Правило одно и без исключений для
                  определительных композитов: синтаксическая вершина стоит справа,
                  поэтому и разбор идёт справа налево.
                </div>
              )}
            </div>

            <ol className={styles.steps}>
              {item.rungs.slice(0, revealed).map((r) => (
                <li key={r.step} className={styles.stepActive}>
                  <code>{r.tail}</code>
                  <div className={styles.stepRule}>
                    {r.step === 1 ? (
                      <>
                        <span className={styles.label}>что?</span> — {r.ru} (
                        <em>{r.member}</em>)
                      </>
                    ) : (
                      <>
                        <span className={styles.label}>вопрос:</span>{' '}
                        {r.questions.join(' · ')} — <strong>{r.ru}</strong> (
                        <em>{r.member}</em>)
                      </>
                    )}
                    {r.ru_variants && r.ru_variants.length > 1 && (
                      <div className={styles.formMuted}>
                        другие корпусные варианты: {r.ru_variants.slice(1).join(', ')}
                      </div>
                    )}
                  </div>
                </li>
              ))}
            </ol>

            <div className={styles.row}>
              {!done ? (
                <button
                  type="button"
                  className={styles.pill}
                  onClick={() => setRevealed((n) => n + 1)}
                >
                  ← следующая ступень влево
                </button>
              ) : (
                <button
                  type="button"
                  className={styles.pill}
                  onClick={() => reset(index + 1)}
                >
                  дальше →
                </button>
              )}
            </div>

            {done && (
              <div className={styles.drillEvidence}>
                <span className={styles.label}>прочтите лестницу обратно, слева направо:</span>{' '}
                {item.membersRu.join(' → ')}
                <br />
                <em>
                  Тип композита (татпуруша / кармадхарая / бахуврихи / двандва) здесь
                  сознательно не утверждается: из состава он не выводится, и вопрос на
                  каждой ступени дан как набор кандидатов, а не как ответ. Тип и
                  разбиение тренируются отдельно — в тренажёре kosha (W1c).
                </em>
              </div>
            )}
          </>
        )}
      </div>

      <p className={styles.caption}>
        Композиты — только засвидетельствованные корпусом, и у каждого проверен порядок
        членов относительно поверхностной формы: лестница справа налево имеет смысл лишь
        тогда, когда последний член действительно последний. Корпус: DCS (Oliver
        Hellwig), закреплённый снимок VisualDCS; русские глоссы членов — корпусный слой
        SanskritRussian (частотные варианты, поэтому иногда в косвенном падеже).
      </p>
    </div>
  );
}
