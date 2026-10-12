// Единый источник поисковых контекстов (H6553): docusaurus.config.mjs читает
// список отсюда, чтобы конфиг и любые пост-обработки индексов не расходились.
// path — маршрут внутри сайта БЕЗ baseUrl, тем же префиксом плагин режет
// индексы (uri === path || uri.startsWith(`${path}/`)).
export const searchContexts = [
  { label: 'Апте', path: 'grammars/ApteSyntax_1885' },
  { label: 'Бюлер', path: 'grammars/BuhlerLeitfaden_1923' },
  { label: 'Библиотека', path: 'grammars/BibliothecaSanscritica' },
  { label: 'Конкорданс', path: 'grammars/Concordance' },
  { label: 'Дхату', path: 'grammars/GasunsDhatu_2014' },
  { label: 'Грамматические связи', path: 'grammars/GrammarRelations' },
  { label: 'Конкорданс занятий', path: 'grammars/LessonConcordance' },
  { label: 'Кнауэр', path: 'grammars/KnauerFrazy_1908' },
  { label: 'Кочергина', path: 'grammars/KocherginaUchebnik_1998' },
  { label: 'Санграм', path: 'grammars/sangram' },
  { label: 'Предметный конкорданс', path: 'grammars/SubjectConcordance' },
  { label: 'Толчельников', path: 'grammars/TolchelnikovTalmud_2026' },
  { label: 'Уитни', path: 'grammars/WhitneyGrammar_1889' },
  { label: 'Зализняк 1975', path: 'grammars/ZalizniakMorphology_1975' },
  { label: 'Зализняк 1978', path: 'grammars/ZalizniakOcherk_1978' },
  { label: 'Зализняк 2004', path: 'grammars/ZalizniakKonspekt_2004' },
];
