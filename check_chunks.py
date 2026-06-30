import json
with open(r'chunks after validation\20. Chart of Account Accounting Manual Part_4_State Audit West Ben.jsonl', encoding='utf-8') as f:
    chunks = [json.loads(x) for x in f]

for i, c in enumerate(chunks[:15]):
    print(f"{i}: ch={c.get('chapter')} hd={c.get('heading')} text={str(c.get('text'))[:60]}")
