import json
import sys
sys.stdout.reconfigure(encoding="utf-8")

d = json.load(open(r"C:\Users\user\Documents\GitHub\kosha\data\manifest\datasets.json", encoding="utf-8"))
datasets = d["datasets"]
no_doi = [x for x in datasets if not x.get("doi")]
print(len(no_doi), "of", len(datasets), "have no doi")
for x in no_doi[:2]:
    print(json.dumps(x, ensure_ascii=False, indent=2))
print("ids tail:", [x["id"] for x in datasets[-5:]])
