import json
with open(r'chunks after validation\20. Chart of Account Accounting Manual Part_4_State Audit West Ben.jsonl', encoding='utf-8') as f:
    chunks = [json.loads(x) for x in f]

for c in chunks[-15:]:
    print(f"hd={c.get('heading')} text={str(c.get('text'))[:40]}")
