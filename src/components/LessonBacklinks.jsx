import React from 'react';
import backlinks from '@site/src/lesson-backlinks.json';

const SITE = 'https://gasyoun.github.io/SanskritGrammar';

/**
 * Обратные ссылки «страница источника ⇐ поурочный конкорданс Бюлера» (E3–E4,
 * MG 02-10-2026: блок внизу страницы источника, серым и мельче). Данные —
 * src/lesson-backlinks.json, генерируется scripts/build_lesson_concordance.py
 * из LessonConcordance/topics.yml (каркас на 48 уроков, наполнение по мере
 * batch-минта). Использование в mdx книги: `<LessonBacklinks page="kochergina" />`.
 */
export default function LessonBacklinks({ page }) {
  const items = (backlinks.pages && backlinks.pages[page]) || [];
  if (!items.length) return null;
  return (
    <div className="lesson-backlinks" style={{ marginTop: '2.5rem' }}>
      <hr />
      <small style={{ color: 'var(--ifm-color-emphasis-600)' }}>
        ⇐ Поурочный конкорданс Бюлера:{' '}
        {items.map((it, i) => (
          <span key={i}>
            {i > 0 && ' · '}
            <a href={`${SITE}/grammars/LessonConcordance/catalog#:~:text=${encodeURIComponent(it.spot)}`}>{it.label}</a>
          </span>
        ))}
      </small>
    </div>
  );
}
