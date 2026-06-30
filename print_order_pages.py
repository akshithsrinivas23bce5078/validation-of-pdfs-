import json
import re

with open(r'chunks after validation\19__Opening_Balance_Sheet_Accounting_Manual_P_State_Audit_West_Ben.jsonl', encoding='utf-8') as f:
    chunks = [json.loads(x) for x in f]

for i, c in enumerate(chunks):
    page = c.get('page.no', '')
    print(f"{i}: ch={c.get('chapter')} hd={c.get('heading')} page={page}")
