import json
lines = [json.loads(l) for l in open(r'unvalidated chunks\RAM_2022_Sixth_Edition.jsonl', encoding='utf-8')]
for i, l in enumerate(lines[80:95]):
    print(f"{i+80}: {l['title'][:40]} --- {l['text'][:40]}")
