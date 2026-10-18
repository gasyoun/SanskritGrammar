// Единый источник поисковых контекстов (H6553) + ПОРЯДОК ПРИОРИТЕТА
// ранжирования (H6672, рулинг MG 13-10 «приоритет разделов»): массив
// упорядочен от важных к служебным — при близких скорах lunr результат из
// более раннего раздела стоит выше. Книги вперёд (Кочергина — первая, исходный
// запрос MG), инструменты и санграм — в хвосте. path — маршрут внутри сайта
// БЕЗ baseUrl, тем же префиксом плагин режет индексы и воркер считает
// приоритет.
export const searchContexts = [
  { label: 'Кочергина', path: 'grammars/KocherginaUchebnik_1998' },
  { label: 'Бюлер', path: 'grammars/BuhlerLeitfaden_1923' },
  { label: 'Кнауэр', path: 'grammars/KnauerFrazy_1908' },
  { label: 'Апте', path: 'grammars/ApteSyntax_1885' },
  { label: 'Уитни', path: 'grammars/WhitneyGrammar_1889' },
  { label: 'Зализняк 1975', path: 'grammars/ZalizniakMorphology_1975' },
  { label: 'Зализняк 1978', path: 'grammars/ZalizniakOcherk_1978' },
  { label: 'Зализняк 2004', path: 'grammars/ZalizniakKonspekt_2004' },
  { label: 'Толчельников', path: 'grammars/TolchelnikovTalmud_2026' },
  { label: 'Дхату', path: 'grammars/GasunsDhatu_2014' },
  { label: 'Библиотека', path: 'grammars/BibliothecaSanscritica' },
  { label: 'Конкорданс', path: 'grammars/Concordance' },
  { label: 'Конкорданс занятий', path: 'grammars/LessonConcordance' },
  { label: 'Грамматические связи', path: 'grammars/GrammarRelations' },
  { label: 'Предметный конкорданс', path: 'grammars/SubjectConcordance' },
  { label: 'Санграм', path: 'grammars/sangram' },
];
