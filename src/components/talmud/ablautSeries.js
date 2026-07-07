// Table 2 (§II «Ряды чередования») encoded once, shared by the Ablaut machine
// and any widget that needs the ablaut calculus. Each series maps a
// morphological grade (weak / guna / vrddhi) to its surface vowel, with the
// pre-vowel allomorph in `.alt` where the Talmud lists one in parentheses.
// Source: TolchelnikovTalmud_2026/talmud-02-cheredovanie.mdx, Таблица 2.

// grade → { c: form before a consonant, v: allomorph before a vowel (null = same) }
export const SERIES = {
  'A₁': { weak: { c: 'ø', v: null }, guna: { c: 'a', v: null }, vrddhi: { c: 'ā', v: null } },
  'A₂': { weak: { c: 'ø', v: null }, guna: { c: 'ā', v: null }, vrddhi: { c: 'ā', v: null } },
  'I₁': { weak: { c: 'i', v: 'y' }, guna: { c: 'e', v: 'ay' }, vrddhi: { c: 'ai', v: 'āy' } },
  'I₂': { weak: { c: 'ī', v: 'y' }, guna: { c: 'e', v: 'ay' }, vrddhi: { c: 'ai', v: 'āy' } },
  'U₁': { weak: { c: 'u', v: 'v' }, guna: { c: 'o', v: 'av' }, vrddhi: { c: 'au', v: 'āv' } },
  'U₂': { weak: { c: 'ū', v: 'v' }, guna: { c: 'o', v: 'av' }, vrddhi: { c: 'au', v: 'āv' } },
  'R₁': { weak: { c: 'ṛ', v: 'r' }, guna: { c: 'ar', v: null }, vrddhi: { c: 'ār', v: null } },
  'R₂': { weak: { c: 'ṝ', v: 'ir/ur' }, guna: { c: 'ar', v: null }, vrddhi: { c: 'ār', v: null } },
  'L': { weak: { c: 'ḷ', v: 'l' }, guna: { c: 'al', v: null }, vrddhi: { c: 'āl', v: null } },
  'M₁': { weak: { c: 'm̥', v: 'am' }, guna: { c: 'am', v: null }, vrddhi: { c: 'ām', v: null } },
  'M₂': { weak: { c: 'm̥̄', v: null }, guna: { c: '—', v: null }, vrddhi: { c: 'ām', v: null } },
  'N₁': { weak: { c: 'n̥', v: 'an/aṇ' }, guna: { c: 'an/aṇ', v: null }, vrddhi: { c: 'ān/āṇ', v: null } },
  'N₂': { weak: { c: 'n̥̄', v: null }, guna: { c: '—', v: null }, vrddhi: { c: 'ān', v: null } },
};

export const SERIES_ORDER = [
  'A₁', 'A₂', 'I₁', 'I₂', 'U₁', 'U₂', 'R₁', 'R₂', 'L', 'M₁', 'M₂', 'N₁', 'N₂',
];

// The three grades a morphological position demands (Table 3, standard type «s»):
// Поз.1 → вриддхи, Поз.2 → гуна, Поз.3 → слабая.
export const GRADES = [
  { key: 'weak', ru: 'Слабая', pos: 'Поз. 3', cls: 'gradeWeak' },
  { key: 'guna', ru: 'Гуна', pos: 'Поз. 2', cls: 'gradeMid' },
  { key: 'vrddhi', ru: 'Вриддхи', pos: 'Поз. 1', cls: 'gradeStrong' },
];
