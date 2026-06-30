import json

with open(r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\RAM_2022_Sixth_Edition_fixed.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        c = json.loads(line)
        h = c.get('heading', '')
        if h.startswith('8.'):
            print(f"Heading: {h:30s} | Chapter: {c.get('chapter')}")
