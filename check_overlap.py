import json

path = r'unvalidated chunks\Local Fund Audit Depart Manual  Vol - II.jsonl'
with open(path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

for c in chunks:
    if str(c.get('page_no')) == '62' or str(c.get('page_no')) == '(62)':
        t = c.get('text') or ''
        print(f"H: {c.get('heading')}")
        print(f"P: {c.get('page_no')}")
        print(f"T: {t[:100]}...")
        print(f"T_last: {t[-100:]}")
        print("---")
