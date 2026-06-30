import json
import re

jsonl_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\17__Introduction_Accounting_Manual_Part_1_Wes_State_Audit_West_Ben.jsonl'
output_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\17__Introduction_Accounting_Manual_Part_1_Wes_State_Audit_West_Ben_fix10.jsonl'

with open(jsonl_path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

sub_id = 1
for c in chunks:
    if c.get('chapter') == '10':
        text = c.get('text', '').strip()
        heading = c.get('heading', '') or ''
        
        # Remove any existing 10.X prefix from heading
        original_heading = heading
        m = re.match(r'^10\.\d+\s+(.*)', heading)
        if m:
            original_heading = m.group(1)
        else:
            m = re.match(r'^10\.\d+$', heading)
            if m:
                original_heading = None

        if original_heading == 'Procedure for review and change in the manual MANUAL':
            # Remove numbering from this chunk
            c['heading'] = original_heading
        else:
            if original_heading:
                c['heading'] = f"10.{sub_id} {original_heading}"
            else:
                c['heading'] = f"10.{sub_id}"
            sub_id += 1

with open(output_path, 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

print("Fixed chapter 10 numbering.")
