#!/usr/bin/env python3
# Inject per-§ anchors into the Zaliznyak Ocherk MDX so the Talmud companion's
# <ZRef> chips can deep-link to the exact §. H241, Opus 4.8.
import re, sys
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

path = sys.argv[1]
with open(path, encoding='utf-8') as fh:
    lines = fh.readlines()

seen = set()
bold_re = re.compile(r'^\*\*§\s*(\d+)')          # **§ 1.** ...  /  **§ 12**. ...
head_re = re.compile(r'^(#+\s*)§\s*(\d+)(.*?)\s*$')  # #### § 42. Title
out = []
n_bold = n_head = 0
for ln in lines:
    m = bold_re.match(ln)
    if m:
        num = int(m.group(1))
        if num not in seen:
            seen.add(num)
            out.append(f'<span id="s{num}"></span>{ln}')
            n_bold += 1
            continue
    mh = head_re.match(ln)
    if mh:
        num = int(mh.group(2))
        if num not in seen:
            seen.add(num)
            # Docusaurus explicit heading id
            out.append(f'{mh.group(1)}§ {num}{mh.group(3)} '.rstrip() + f' {{#s{num}}}\n')
            n_head += 1
            continue
    out.append(ln)

with open(path, 'w', encoding='utf-8', newline='') as fh:
    fh.writelines(out)

print(f'anchors injected: {n_bold} inline-span + {n_head} heading-id = {len(seen)} distinct §§')
print(f'range: {min(seen)}..{max(seen)}')
# sanity: report any gaps
gaps = [i for i in range(min(seen), max(seen)+1) if i not in seen]
print(f'missing §§ in range (defined elsewhere / sub-lettered): {gaps}')
