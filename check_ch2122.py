import json

with open(r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\RAM_2022_Sixth_Edition_fixed.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        c = json.loads(line)
        if c.get('chapter') in ['21', '22']:
            print(f"CH={c.get('chapter')} {c.get('heading')}")
