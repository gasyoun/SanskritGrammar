import json
import sys
sys.stdout.reconfigure(encoding="utf-8")

d = json.load(open(r"C:\Users\user\Documents\GitHub\kosha\data\manifest\datasets.json", encoding="utf-8"))
print(list(d.keys()))
datasets = d.get("datasets")
if datasets is None:
    for k, v in d.items():
        if isinstance(v, list):
            print("list key:", k, len(v))
        elif isinstance(v, dict):
            print("dict key:", k, list(v.keys())[:5])
else:
    print(type(datasets), len(datasets))
    print(json.dumps(datasets[0], ensure_ascii=False, indent=2)[:1000])
