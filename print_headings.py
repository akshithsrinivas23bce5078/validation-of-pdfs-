import json

with open(r'chunks after validation\17__Introduction_Accounting_Manual_Part_1_Wes_State_Audit_West_Ben.jsonl', encoding='utf-8') as f:
    chunks = [json.loads(x) for x in f]

for i, c in enumerate(chunks[32:36]):
    print(f"{i+32}: {c['heading']}")
