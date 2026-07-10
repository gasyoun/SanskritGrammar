import React from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';

const books = [
  ['ApteSyntax_1885/Apte-unicode', 'Apte — Sanskrit Syntax (1885)'],
  ['BuhlerLeitfaden_1923/Buhler_Unicode', 'Bühler — Leitfaden (1923)'],
  ['KnauerFrazy_1908/Frazy-Knauer-03.05.2023', 'Knauer — Phrases (1908)'],
  ['KocherginaUchebnik_1998/Kochergina_unicode', 'Kochergina — Uchebnik (1998)'],
  ['ZalizniakKonspekt_2004/zalizniak-konspekt-2015-11-X_bd_t', 'Zalizniak — Konspekt (2004)'],
  ['ZalizniakOcherk_1978/Zalizniak-Ocherk_29-11-20-aligned', 'Zalizniak — Ocherk (1978)'],
];

export default function Home() {
  return (
    <Layout title="Sanskrit Grammar Sources" description="Digitized Sanskrit grammar & reader texts">
      <main style={{maxWidth: 760, margin: '0 auto', padding: '2rem 1rem'}}>
        <h1>Sanskrit Grammar Sources</h1>
        <p>Digitized Sanskrit grammar and reader texts, converted from Word sources to MDX with renderable declension and conjugation tables.</p>
        <ul>
          {books.map(([slug, title]) => (
            <li key={slug}><Link to={`/grammars/${slug}`}>{title}</Link></li>
          ))}
        </ul>
      </main>
    </Layout>
  );
}
