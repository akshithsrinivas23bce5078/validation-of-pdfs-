import json
filepath = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\17__Introduction_Accounting_Manual_Part_1_Wes_State_Audit_West_Ben.jsonl'
with open(filepath, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

for c in chunks[:10]:
    print(f"Chapter: {c['chapter']}, Heading: {c['heading']}, Title: {c['title']}")
