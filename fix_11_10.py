import json
import os

INPUT_FILE = r'chunks after validation\19__Opening_Balance_Sheet_Accounting_Manual_P_State_Audit_West_Ben.jsonl'
TEMP_FILE = r'chunks after validation\19__temp.jsonl'

with open(INPUT_FILE, encoding='utf-8') as f:
    chunks = [json.loads(x) for x in f]

# Find the chunk where heading is null, chapter is 11, and text starts with 11.10
for c in chunks:
    if c.get('chapter') == '11' and c.get('heading') is None:
        if c.get('text', '').startswith('11.10'):
            c['heading'] = '11.10'
            print("Updated heading for 11.10")

with open(TEMP_FILE, 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

os.replace(TEMP_FILE, INPUT_FILE)
print("Changes applied successfully.")
