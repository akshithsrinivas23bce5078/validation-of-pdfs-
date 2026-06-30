import json
path = r'unvalidated chunks\Local Fund Audit Depart Manual  Vol - II.jsonl'
pages = set()
with open(path, 'r', encoding='utf-8') as f:
    for line in f:
        c = json.loads(line)
        pages.add(c.get('start_page'))
for p in range(115, 135):
    print(f"{p} exists: {p in pages}")
