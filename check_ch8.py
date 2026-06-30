import json

with open(r'chunks after validation\17__Introduction_Accounting_Manual_Part_1_Wes_State_Audit_West_Ben.jsonl', encoding='utf-8') as f:
    chunks = [json.loads(x) for x in f]

for c in chunks:
    try:
        ch = int(c.get('chapter', '0'))
        if ch >= 8:
            print(f"Ch: {c['chapter']}, Heading: {c['heading']}")
    except ValueError:
        pass
