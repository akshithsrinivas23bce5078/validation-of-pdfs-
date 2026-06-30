import json
import re

jsonl_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\19__Opening_Balance_Sheet_Accounting_Manual_P_State_Audit_West_Ben.jsonl'
output_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\19__Opening_Balance_Sheet_Accounting_Manual_P_State_Audit_West_Ben_fix.jsonl'

with open(jsonl_path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

for c in chunks:
    text = c.get('text', '').strip()
    
    # Check if text starts with X.Y
    match = re.match(r'^(\d+\.\d+)\s+', text)
    if match:
        num = match.group(1)
        c['heading'] = num
        # Remove the number from the beginning of the text
        c['text'] = text[match.end():].strip()
    else:
        # Check if text starts with just a number like "2. BACKGROUND"
        # We can just leave heading as null
        c['heading'] = None

with open(output_path, 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

print("Fixed headings for 19__Opening_Balance_Sheet")
