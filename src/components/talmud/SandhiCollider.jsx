// SandhiCollider — «Коллайдер сандхи» (§VII). Two vowels move toward each other,
// collide and merge into the surface result; a plashka names the rule family
// (саварна-диргха / гуна / вриддхи / янь-сандхи). Covers the vowel-sandhi rules
// of §VII.1; consonant sandhi (assimilation, ruki, visarga) is left to the text.
import React, { useState } from 'react';
import styles from './styles.module.css';

const LEFT = ['a', 'ā', 'i', 'ī', 'u', 'ū', 'ṛ'];
const RIGHT = ['a', 'ā', 'i', 'ī', 'u', 'ū', 'ṛ', 'e', 'ai', 'o', 'au'];

// Compute vowel sandhi. Returns { out, rule, ref } where ref is the §VII sub-rule.
function sandhi(L, R) {
  const aLeft = L === 'a' || L === 'ā';
  const iLeft = L === 'i' || L === 'ī';
  const uLeft = L === 'u' || L === 'ū';
  const rLeft = L === 'ṛ' || L === 'ṝ';

  if (aLeft) {
    if (R === 'a' || R === 'ā') return { out: 'ā', rule: 'Саварна-диргха (слияние одинаковых)' };
    if (R === 'i' || R === 'ī') return { out: 'e', rule: 'Гуна-сандхи' };
    if (R === 'u' || R === 'ū') return { out: 'o', rule: 'Гуна-сандхи' };
    if (R === 'ṛ' || R === 'ṝ') return { out: 'ar', rule: 'Гуна-сандхи' };
    if (R === 'e' || R === 'ai') return { out: 'ai', rule: 'Вриддхи-сандхи' };
    if (R === 'o' || R === 'au') return { out: 'au', rule: 'Вриддхи-сандхи' };
  }
  // Savarna for like homorganic long
  if (iLeft && (R === 'i' || R === 'ī')) return { out: 'ī', rule: 'Саварна-диргха (слияние одинаковых)' };
  if (uLeft && (R === 'u' || R === 'ū')) return { out: 'ū', rule: 'Саварна-диргха (слияние одинаковых)' };
  if (rLeft && (R === 'ṛ' || R === 'ṝ')) return { out: 'ṝ', rule: 'Саварна-диргха (слияние одинаковых)' };

  // Yan-sandhi: i/u/ṛ before a dissimilar vowel → semivowel + that vowel
  if (iLeft) return { out: `y${R}`, rule: 'Яⁿ-сандхи (i → y перед иной гласной)' };
  if (uLeft) return { out: `v${R}`, rule: 'Яⁿ-сандхи (u → v перед иной гласной)' };
  if (rLeft) return { out: `r${R}`, rule: 'Яⁿ-сандхи (ṛ → r перед иной гласной)' };

  return { out: `${L}${R}`, rule: '—' };
}

export default function SandhiCollider() {
  const [left, setLeft] = useState('a');
  const [right, setRight] = useState('i');
  const [collided, setCollided] = useState(true);

  const res = sandhi(left, right);

  function collide(nextL, nextR) {
    setCollided(false);
    setLeft(nextL);
    setRight(nextR);
    // Re-trigger the slide animation on the next frame.
    requestAnimationFrame(() => requestAnimationFrame(() => setCollided(true)));
  }

  return (
    <div className={styles.widget}>
      <p className={styles.title}>💥 Коллайдер сандхи — столкновение гласных</p>

      <div className={styles.row}>
        <span className={styles.label}>Левая гласная:</span>
        {LEFT.map((v) => (
          <button
            key={v}
            className={`${styles.pill} ${v === left ? styles.pillActive : ''}`}
            onClick={() => collide(v, right)}
          >
            {v}
          </button>
        ))}
      </div>
      <div className={styles.row}>
        <span className={styles.label}>Правая гласная:</span>
        {RIGHT.map((v) => (
          <button
            key={v}
            className={`${styles.pill} ${v === right ? styles.pillActive : ''}`}
            onClick={() => collide(left, v)}
          >
            {v}
          </button>
        ))}
      </div>

      <div className={styles.collider}>
        <span className={`${styles.phoneme} ${collided ? styles.collidedL : styles.phonemeL}`}>
          {left}
        </span>
        <span className={styles.arrow}>+</span>
        <span className={`${styles.phoneme} ${collided ? styles.collidedR : styles.phonemeR}`}>
          {right}
        </span>
        <span className={styles.arrow}>=</span>
        <span key={`${left}${right}`} className={styles.result}>{res.out}</span>
      </div>

      <p className={styles.caption}>
        <span className={styles.rulePlate}>{res.rule}</span>{' '}
        Правило действует на стыке морфем или слов; при чтении текста сандхи «снимаются»
        первыми. Полный разбор — в тексте §VII (согласные сандхи, <code>ruki</code>,
        висарга и анусвара здесь не моделируются).
      </p>
    </div>
  );
}
