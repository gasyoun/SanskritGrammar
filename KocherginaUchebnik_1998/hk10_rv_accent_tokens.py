# coding=utf-8
"""H1454 metodichka Zanyatie VI: fraction of running word-tokens in the accented
Rigveda Samhita (Devanagari) that bear a written accent mark.

Source: C:/Users/user/Documents/GitHub/rvlinks/rvhymns/rv*.html (1028 hymns),
<p class="sa"> blocks = accented Devanagari samhita text.
Marks counted: U+0951 (udatta/svarita stroke above), U+0952 (anudatta below),
plus any Vedic Extensions block chars U+1CD0-U+1CFF if present.
"""
import sys, re, glob, unicodedata
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')

SRC = r"C:\Users\user\Documents\GitHub\rvlinks\rvhymns\rv*.html"

SA_RE = re.compile(r'<p class="sa">(.*?)</p>', re.S)
TAG_RE = re.compile(r'<[^>]+>')

ACCENT_CHARS = {'॑', '॒'}  # canonical marks in this text
def is_vedic_ext(ch):
    return '᳐' <= ch <= '᳿'

def has_devanagari_letter(tok):
    return any('ऀ' <= c <= 'ॿ' and c not in ('।', '॥') for c in tok)

total = 0
accented = 0
per_mandala = {}
mark_inventory = Counter()
files = sorted(glob.glob(SRC))
print(f"files: {len(files)}")

for fp in files:
    mandala = fp[-11:-9]  # rvMM.NNN.html
    with open(fp, encoding='utf-8') as f:
        html = f.read()
    for block in SA_RE.findall(html):
        text = TAG_RE.sub(' ', block)
        # drop the mandala header line (unaccented editorial text, contains digits)
        lines = [ln for ln in text.split('\n')
                 if 'मण्डलं' not in ln and 'ऋग्वेदः' not in ln]
        text = ' '.join(lines)
        # separate dandas from words
        text = text.replace('।', ' ').replace('॥', ' ').replace('॥', ' ').replace('।', ' ')
        for tok in text.split():
            if not has_devanagari_letter(tok):
                continue
            if any(c.isdigit() for c in tok):
                continue
            total += 1
            marks = [c for c in tok if c in ACCENT_CHARS or is_vedic_ext(c)]
            for m in marks:
                mark_inventory[m] += 1
            m0, a0 = per_mandala.get(mandala, (0, 0))
            if marks:
                accented += 1
                per_mandala[mandala] = (m0 + 1, a0 + 1)
            else:
                per_mandala[mandala] = (m0, a0 + 1)

print(f"\ntotal Devanagari tokens : {total}")
print(f"tokens with >=1 accent mark: {accented}")
print(f"fraction accented          : {accented/total:.4f} ({100*accented/total:.2f}%)")
print(f"tokens with NO mark        : {total-accented} ({100*(total-accented)/total:.2f}%)")

print("\nmark inventory (codepoint : name : count):")
for ch, n in mark_inventory.most_common():
    try:
        name = unicodedata.name(ch)
    except ValueError:
        name = '?'
    print(f"  U+{ord(ch):04X} : {name} : {n}")

print("\nper-mandala breakdown (mandala, accented, total, %):")
for md in sorted(per_mandala):
    acc, tot = per_mandala[md]
    print(f"  {md}: {acc:6d} / {tot:6d} = {100*acc/tot:.2f}%")
