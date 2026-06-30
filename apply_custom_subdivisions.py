import json
import re

jsonl_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\17__Introduction_Accounting_Manual_Part_1_Wes_State_Audit_West_Ben.jsonl'
output_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\17__Introduction_Accounting_Manual_Part_1_Wes_State_Audit_West_Ben_numbered2.jsonl'

with open(jsonl_path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

current_chapter = None
sub_id = 1

for c in chunks:
    chapter = c.get('chapter')
    
    # Reset sub_id if chapter changes
    if chapter != current_chapter:
        current_chapter = chapter
        sub_id = 1

    heading = c.get('heading')
    original_heading = heading
    
    if heading:
        # Strip existing "X.Y " prefix
        m = re.match(r'^\d+\.\d+\s+(.*)', heading)
        if m:
            original_heading = m.group(1)
        else:
            m = re.match(r'^\d+\.\d+$', heading)
            if m:
                original_heading = None

    if chapter == '7' and original_heading == 'BALANCE SHEET':
        c['heading'] = 'BALANCE SHEET'
        sub_id += 1
        continue
        
    if chapter == '8':
        if original_heading:
            c['heading'] = f"{sub_id}. {original_heading}"
        else:
            c['heading'] = f"{sub_id}."
        sub_id += 1
        continue

    # Standard numbering
    if original_heading:
        c['heading'] = f"{chapter}.{sub_id} {original_heading}"
    else:
        c['heading'] = f"{chapter}.{sub_id}"
    
    sub_id += 1

with open(output_path, 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

print(f"Processed {len(chunks)} chunks and re-applied sequential subdivision numbers.")
