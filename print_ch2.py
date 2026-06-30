import json
path = r'unvalidated chunks\Local Fund Audit Depart Manual  Vol - II.jsonl'
with open(path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

for c in chunks:
    if 80 <= c.get('start_page', 0) <= 85:
        if c.get('heading'):
            print(f"Page {c['start_page']} | Heading: {c['heading']}")
