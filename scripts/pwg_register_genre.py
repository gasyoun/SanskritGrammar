#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PWG register / genre layer — the diachronic profile of each headword, from its citations.

PWG cites its attesting sources as `<ls>ṚV. 1,62,8</ls>`, `<ls>MBH. 12,10374</ls>`. This
one-pass extraction reads every `<ls>` per entry, normalises the source to its leading
text/author token, maps it to a (period, genre) via a curated table of the highest-frequency
sources (top ~90 tokens ≈ 89 % of the 566,678 citations), and derives per headword:
  - the set of attesting **periods** (vedic < brāhmaṇa < sūtra < epic < classical)
  - the **earliest** period (the diachronic anchor)
  - the set of **genres** (saṃhitā / brāhmaṇa-upaniṣad / sūtra / grammar / epic / kāvya /
    purāṇa / śāstra / lexicon / commentary / modern-ref)
  - **lexicon_only** — attested only in lexica/meta sources (a word known only from
    dictionaries, philologically notable), no dated-text attestation.

Homonym-precise (each row = one PWG entry, carrying `<h>`). Sources outside the curated table
count as genre `other` and do not set a period. Read-only over the committed pwg.txt.

Emits data/pwg_register_genre/pwg_register_genre.tsv + a summary. Deterministic.

    python scripts/pwg_register_genre.py
"""
import argparse
import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

# period ordering for the diachronic anchor; 'meta' = non-dated (lexicon/grammar/ref/comm)
PERIOD_ORDER = {'vedic': 0, 'brahmana': 1, 'sutra': 2, 'epic': 3, 'classical': 4}

# curated source-token → (period, genre); covers ~89% of citations (top ~90 tokens)
ABBR = {
    # Vedic saṃhitā
    'ṚV': ('vedic', 'samhita'), 'AV': ('vedic', 'samhita'), 'VS': ('vedic', 'samhita'),
    'TS': ('vedic', 'samhita'), 'KĀṬH': ('vedic', 'samhita'), 'SV': ('vedic', 'samhita'),
    'MAITRĀY': ('vedic', 'samhita'), 'ṚV.': ('vedic', 'samhita'),
    # Brāhmaṇa / Āraṇyaka / Upaniṣad
    'ŚAT': ('brahmana', 'brahmana-upanisad'), 'AIT': ('brahmana', 'brahmana-upanisad'),
    'TBR': ('brahmana', 'brahmana-upanisad'), 'PAÑCAV': ('brahmana', 'brahmana-upanisad'),
    'CHĀND': ('brahmana', 'brahmana-upanisad'), 'BṚH': ('brahmana', 'brahmana-upanisad'),
    'KAUṢ': ('brahmana', 'brahmana-upanisad'), 'GOP': ('brahmana', 'brahmana-upanisad'),
    'KAṬHOP': ('brahmana', 'brahmana-upanisad'), 'MUṆḌ': ('brahmana', 'brahmana-upanisad'),
    # Sūtra / Vedāṅga / grammar / dharmaśāstra
    'P': ('sutra', 'grammar'), 'PAT': ('sutra', 'grammar'), 'VOP': ('sutra', 'grammar'),
    'DHĀTUP': ('sutra', 'grammar'), 'UṆĀDIS': ('sutra', 'grammar'), 'UJJVAL': ('sutra', 'grammar'),
    'SIDDH': ('sutra', 'grammar'), 'NIR': ('sutra', 'grammar'), 'NAIGH': ('sutra', 'grammar'),
    'ṚV.PRĀT': ('sutra', 'grammar'), 'VS.PRĀT': ('sutra', 'grammar'),
    'KĀTY': ('sutra', 'sutra'), 'ĀŚV': ('sutra', 'sutra'), 'ŚĀṄKH': ('sutra', 'sutra'),
    'LĀṬY': ('sutra', 'sutra'), 'KAUŚ': ('sutra', 'sutra'), 'GOBH': ('sutra', 'sutra'),
    'PĀR': ('sutra', 'sutra'), 'ĀP': ('sutra', 'sutra'), 'BAUDH': ('sutra', 'sutra'),
    'M': ('sutra', 'dharmasastra'), 'YĀJÑ': ('sutra', 'dharmasastra'), 'GAUT': ('sutra', 'dharmasastra'),
    # Epic
    'MBH': ('epic', 'epic'), 'R': ('epic', 'epic'), 'HARIV': ('epic', 'epic'),
    'BHAG': ('epic', 'epic'),
    # Purāṇa
    'BHĀG': ('classical', 'purana'), 'MĀRK': ('classical', 'purana'), 'VP': ('classical', 'purana'),
    'PAÑCAR': ('classical', 'purana'), 'AGNI': ('classical', 'purana'), 'MATSYA': ('classical', 'purana'),
    'VĀYU': ('classical', 'purana'), 'GARUḌA': ('classical', 'purana'), 'PADMA': ('classical', 'purana'),
    # Classical kāvya / drama / story / historical
    'KATHĀS': ('classical', 'kavya'), 'RAGH': ('classical', 'kavya'), 'ŚĀK': ('classical', 'kavya'),
    'PAÑCAT': ('classical', 'kavya'), 'KUMĀRAS': ('classical', 'kavya'), 'HIT': ('classical', 'kavya'),
    'MEGH': ('classical', 'kavya'), 'MṚCCH': ('classical', 'kavya'), 'VIKR': ('classical', 'kavya'),
    'DAŚAK': ('classical', 'kavya'), 'BHAṬṬ': ('classical', 'kavya'), 'PRAB': ('classical', 'kavya'),
    'ŚIŚ': ('classical', 'kavya'), 'BHARTṚ': ('classical', 'kavya'), 'GĪT': ('classical', 'kavya'),
    'MĀLAV': ('classical', 'kavya'), 'KIR': ('classical', 'kavya'), 'N': ('classical', 'kavya'),
    'RĀJA-TAR': ('classical', 'kavya'), 'DHŪRTAS': ('classical', 'kavya'), 'VET': ('classical', 'kavya'),
    'ŚṚṄGĀR': ('classical', 'kavya'), 'AMAR': ('classical', 'kavya'), 'RATNĀV': ('classical', 'kavya'),
    # Śāstra (technical / scientific / philosophy / poetics)
    'SUŚR': ('classical', 'sastra'), 'VARĀH': ('classical', 'sastra'), 'SŪRYAS': ('classical', 'sastra'),
    'KĀM': ('classical', 'sastra'), 'SĀH': ('classical', 'sastra'), 'SARVADARŚANAS': ('classical', 'sastra'),
    'CARAKA': ('classical', 'sastra'), 'BHĀVAPR': ('classical', 'sastra'), 'ŚĀRṄG': ('classical', 'sastra'),
    # Lexicographic (koṣa / nighaṇṭu)
    'ŚKDR': ('meta', 'lexicon'), 'H': ('meta', 'lexicon'), 'AK': ('meta', 'lexicon'),
    'MED': ('meta', 'lexicon'), 'TRIK': ('meta', 'lexicon'), 'RĀJAN': ('meta', 'lexicon'),
    'HALĀY': ('meta', 'lexicon'), 'ŚABDAR': ('meta', 'lexicon'), 'HĀR': ('meta', 'lexicon'),
    'VYUTP': ('meta', 'lexicon'), 'ŚABDAC': ('meta', 'lexicon'), 'RATNAM': ('meta', 'lexicon'),
    'JAṬĀDH': ('meta', 'lexicon'), 'ŚABDAM': ('meta', 'lexicon'), 'ŚABDĀRTHAK': ('meta', 'lexicon'),
    'NIGH': ('meta', 'lexicon'), 'ŚĀŚV': ('meta', 'lexicon'), 'DHARAṆI': ('meta', 'lexicon'),
    # Commentary
    'SĀY': ('meta', 'commentary'), 'NĪLAK': ('meta', 'commentary'), 'KULL': ('meta', 'commentary'),
    'ŚAṂK': ('meta', 'commentary'), 'MAHĪDH': ('meta', 'commentary'),
    # Modern editions / catalogues / journals / anthologies (not a dated primary source)
    'Verz': ('meta', 'modern-ref'), 'Spr': ('meta', 'modern-ref'), 'Ind': ('meta', 'modern-ref'),
    'ed': ('meta', 'modern-ref'), 'COLEBR': ('meta', 'modern-ref'), 'WILS': ('meta', 'modern-ref'),
    'WILSON': ('meta', 'modern-ref'), 'WEBER': ('meta', 'modern-ref'), 'HALL': ('meta', 'modern-ref'),
    'Z': ('meta', 'modern-ref'), 'BURN': ('meta', 'modern-ref'), 'BENF': ('meta', 'modern-ref'),
    'Journ': ('meta', 'modern-ref'), 'ebend': ('meta', 'modern-ref'),
}

LS = re.compile(r'<ls>([^<]+)</ls>')
RE_L = re.compile(r'<L>(\d+)')
RE_K1 = re.compile(r'<k1>([^<]*)')
RE_H = re.compile(r'<h>(\d+)')
LEAD = re.compile(r'^([^0-9]+?)\s*[0-9]')


def source_token(citation):
    m = LEAD.match(citation.strip())
    key = (m.group(1) if m else citation).strip()
    return re.split(r'[ .]', key, maxsplit=1)[0].strip()


def entries(path):
    lid = k1 = hom = None
    buf, on = [], False
    for ln in open(path, encoding='utf-8'):
        ln = ln.rstrip('\n')
        if ln.startswith('<L>'):
            ml, mk = RE_L.search(ln), RE_K1.search(ln)
            if ml and mk:
                if on and lid:
                    yield lid, k1, hom, buf
                mh = RE_H.search(ln)
                lid, k1, hom = ml.group(1), mk.group(1), (mh.group(1) if mh else '')
                buf, on = [], True
                continue
        if on:
            if ln.startswith('<LEND>'):
                yield lid, k1, hom, buf
                on = False
            else:
                buf.append(ln)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pwg', default=None)
    ap.add_argument('--out', default=None)
    args = ap.parse_args()
    here = Path(__file__).resolve()
    repo, github = here.parents[1], here.parents[2]
    pwg = Path(args.pwg) if args.pwg else github / 'csl-orig' / 'v02' / 'pwg' / 'pwg.txt'
    if not pwg.exists():
        print('ERROR: pwg.txt not found: %s' % pwg, file=sys.stderr)
        return 1
    out = Path(args.out) if args.out else repo / 'data' / 'pwg_register_genre'
    out.mkdir(parents=True, exist_ok=True)

    rows = []
    reg_ctr = Counter()
    lex_only = 0
    cited_cov = mapped_cov = 0
    for lid, k1, hom, buf in entries(pwg):
        body = '\n'.join(buf)
        cites = LS.findall(body)
        if not cites:
            continue
        toks = [source_token(c) for c in cites]
        toks = [t for t in toks if t]
        periods, genres, sources = set(), set(), set()
        for t in toks:
            cited_cov += 1
            pg = ABBR.get(t)
            if pg:
                mapped_cov += 1
                per, gen = pg
                sources.add(t)
                genres.add(gen)
                if per in PERIOD_ORDER:
                    periods.add(per)
            else:
                genres.add('other')
        earliest = min(periods, key=lambda p: PERIOD_ORDER[p]) if periods else ''
        # lexicon_only: has curated sources, none of which is a dated text (all meta), no period
        curated_genres = genres - {'other'}
        is_lex_only = bool(curated_genres) and not periods and curated_genres <= {'lexicon', 'commentary', 'grammar', 'modern-ref'}
        if is_lex_only:
            lex_only += 1
        register = earliest if earliest else ('lexical' if curated_genres else 'uncategorised')
        reg_ctr[register] += 1
        rows.append((lid, k1, hom, len(cites),
                     '|'.join(sorted(periods, key=lambda p: PERIOD_ORDER[p])),
                     earliest, register, '1' if is_lex_only else '',
                     '|'.join(sorted(genres)), '|'.join(sorted(sources))))

    rows.sort(key=lambda r: int(r[0]))
    cols = ['L_id', 'k1', 'hom', 'n_citations', 'periods', 'earliest_period',
            'register', 'lexicon_only', 'genres', 'sources']
    tsv = out / 'pwg_register_genre.tsv'
    with tsv.open('w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, delimiter='\t')
        w.writerow(cols)
        for r in rows:
            w.writerow(r)

    summary = {
        'study': 'PWG register/genre layer (diachronic profile per headword from <ls> citations)',
        'as_of': '2026-07-19',
        'source': 'csl-orig/v02/pwg/pwg.txt (read-only)',
        'entries_with_citations': len(rows),
        'citation_tokens_seen': cited_cov,
        'citation_tokens_mapped_pct': round(100 * mapped_cov / cited_cov, 1) if cited_cov else 0,
        'curated_source_tokens': len(ABBR),
        'lexicon_only_headwords': lex_only,
        'by_register': dict(reg_ctr.most_common()),
    }
    (out / 'pwg_register_genre_summary.json').write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    print('entries %d | tokens mapped %.1f%% | lexicon-only %d | registers %s'
          % (len(rows), summary['citation_tokens_mapped_pct'], lex_only, dict(reg_ctr.most_common())),
          file=sys.stderr)
    print('wrote %s + summary' % tsv.name, file=sys.stderr)
    return 0


if __name__ == '__main__':
    sys.exit(main())
