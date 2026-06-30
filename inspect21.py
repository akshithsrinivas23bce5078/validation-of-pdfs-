import json
filepath = r'c:\Users\Akshith Srinivas\chunk-validator-one\unvalidated chunks\21__Forms___Formats_Accounting_Manual_Part_5_State_Audit_West_Ben.jsonl'
with open(filepath, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

for c in chunks[:10]:
    print(f"section: {c.get('section')}, form_id: {c.get('form_id')}, title: {c.get('title')}")
