import json

path = r'unvalidated chunks\Local Fund Audit Depart Manual  Vol - II.jsonl'
with open(path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

for p in [100, 110, 120, 130, 140, 150, 160, 200, 250, 300, 350, 400, 450, 500]:
    for c in chunks:
        if c.get('start_page') == p:
            text = c.get('content', '')
            print(f"Page {p}: {text[:80].encode('ascii', 'ignore').decode('ascii')}...")
