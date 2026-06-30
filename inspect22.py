import json
filepath = r'c:\Users\Akshith Srinivas\chunk-validator-one\unvalidated chunks\22__Transaction_Entries_Accounting_Manual_Par_State_Audit_West_Ben.jsonl'
with open(filepath, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

tables_count = 0
for c in chunks:
    if c.get('has_table'):
        tables_count += 1
        print(f"Table found in heading: {c.get('heading')}")

print(f"Total tables found: {tables_count}")
