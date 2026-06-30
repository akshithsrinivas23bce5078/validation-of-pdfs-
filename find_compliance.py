import json
with open(r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\RAM_2022_Sixth_Edition.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        c = json.loads(line)
        h = c.get('heading', '')
        if 'Compliance' in h and 'Audit' in h:
            print(f"Chapter {c.get('chapter')}: {h}")
