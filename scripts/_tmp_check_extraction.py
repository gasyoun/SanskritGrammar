import json

d = json.load(open("scripts/data/sentences.json", encoding="utf-8"))
for book in ("apte", "whitney"):
    rows = [s for s in d if s["book"] == book and s["script"] == "iast"]
    print(f"--- {book} iast ({len(rows)}) ---")
    for s in rows:
        print(s["id"], repr(s["text"][:140]))
