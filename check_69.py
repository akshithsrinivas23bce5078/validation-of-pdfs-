import json
with open(r'chunks after validation\19__Opening_Balance_Sheet_Accounting_Manual_P_State_Audit_West_Ben.jsonl', encoding='utf-8') as f:
    chunks = [json.loads(x) for x in f]

for c in chunks:
    if c.get('chapter') == '6' and c.get('heading') in ('6.8', '6.9', '6.10'):
        print(f"{c.get('heading')} - page={c.get('page.no')}")
