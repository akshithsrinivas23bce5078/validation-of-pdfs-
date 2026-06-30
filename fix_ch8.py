import json
import os
import re

INPUT_FILE = r'chunks after validation\17__Introduction_Accounting_Manual_Part_1_Wes_State_Audit_West_Ben.jsonl'
TEMP_FILE = r'chunks after validation\17__temp.jsonl'

with open(INPUT_FILE, encoding='utf-8') as f:
    chunks = [json.loads(x) for x in f]

for c in chunks:
    try:
        ch = int(c.get('chapter', '0'))
        if ch == 8:
            heading = c.get('heading', '')
            # If the heading starts with a number followed by a dot, prefix with "8."
            if re.match(r'^\d+\.', heading):
                c['heading'] = '8.' + heading
    except ValueError:
        pass

with open(TEMP_FILE, 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

os.replace(TEMP_FILE, INPUT_FILE)

print("Successfully prefixed '8.' to chapter 8 headings.")
