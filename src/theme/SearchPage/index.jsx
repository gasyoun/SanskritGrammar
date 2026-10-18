// Глобальная страница поиска (MG 12-10-2026): /grammars/search?q= всегда
// открывается БЕЗ поискового контекста — входящий ?ctx= (его ставит SearchBar
// ссылкой «See all results within "{context}"») стрипается до первого рендера
// плагинной страницы, иначе она открылась бы суженной до раздела. Сам
// контекст-селектор страницы продолжает работать — это явный выбор пользователя.
import React, { useEffect } from 'react';
import { useHistory, useLocation } from '@docusaurus/router';
import SearchPage from '@theme-original/SearchPage';

export default function SearchPageGlobal(props) {
  const location = useLocation();
  const history = useHistory();
  const hasCtx = new URLSearchParams(location.search).has('ctx');

  useEffect(() => {
    if (!hasCtx) return;
    const params = new URLSearchParams(location.search);
    params.delete('ctx');
    history.replace({ ...location, search: params.toString() });
  }, [hasCtx, location, history]);

  // Пустой кадр на один проход: SearchPage фетчит индексы в эффекте раньше
  // родительского и без гейта успел бы ударить по суженному индексу.
  return hasCtx ? null : <SearchPage {...props} />;
}
