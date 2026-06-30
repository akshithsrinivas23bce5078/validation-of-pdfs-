import json

with open(r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\RAM_2022_Sixth_Edition_fixed.jsonl', 'r', encoding='utf-8') as f:
    lines = list(f)
    for i, line in enumerate(lines[-60:]):
        c = json.loads(line)
        print(f"CH={c.get('chapter')} {c.get('heading')}")
