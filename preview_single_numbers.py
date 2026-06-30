import json
import re

with open(r'chunks after validation\19__Opening_Balance_Sheet_Accounting_Manual_P_State_Audit_West_Ben.jsonl', encoding='utf-8') as f:
    chunks = [json.loads(x) for x in f]

for i, c in enumerate(chunks):
    if c.get('heading') is None:
        text = c.get('text', '')
        # Match "1 ", "2.", "15.10.", etc.
        m = re.match(r'^(\d+(?:\.\d+)*)\.?\s*', text)
        if m:
            print(f"Index {i}, text starts with: {text[:20]} -> Will extract heading: {m.group(1)}")
        else:
            print(f"Index {i}, text starts with: {text[:20]} -> NO MATCH")
