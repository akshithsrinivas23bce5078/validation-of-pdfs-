import json
import re
import os

INPUT_FILE = r'chunks after validation\19__Opening_Balance_Sheet_Accounting_Manual_P_State_Audit_West_Ben.jsonl'
TEMP_FILE = r'chunks after validation\19__temp.jsonl'

with open(INPUT_FILE, encoding='utf-8') as f:
    chunks = [json.loads(x) for x in f]

for c in chunks:
    if c.get('heading') is None:
        text = c.get('text', '')
        # Match "1 ", "2.", "15.10.", etc.
        m = re.match(r'^(\d+(?:\.\d+)*)\.?\s*', text)
        if m:
            c['heading'] = m.group(1)

with open(TEMP_FILE, 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

os.replace(TEMP_FILE, INPUT_FILE)
print("Applied single numbers as headings successfully.")
