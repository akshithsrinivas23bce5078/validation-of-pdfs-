import json
path = r'unvalidated chunks\Local Fund Audit Depart Manual  Vol - II.jsonl'
with open(path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]
for c in chunks:
    p = c.get('start_page', 0)
    if 45 <= p <= 65:
        print(f"Page {p} | Heading: {c.get('heading', '')[:50]}")
