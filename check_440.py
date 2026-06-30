import json

with open(r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\RAM_2022_Sixth_Edition_fixed.jsonl', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i in range(435, 450):
    if i < len(lines):
        c = json.loads(lines[i])
        print(f"{i}: Chapter={c.get('chapter')} Heading={c.get('heading')}")
