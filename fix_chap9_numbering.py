import json
import re

jsonl_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\17__Introduction_Accounting_Manual_Part_1_Wes_State_Audit_West_Ben.jsonl'
output_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\17__Introduction_Accounting_Manual_Part_1_Wes_State_Audit_West_Ben_fix9.jsonl'

with open(jsonl_path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

for c in chunks:
    if c.get('chapter') == '9':
        text = c.get('text', '').strip()
        heading = c.get('heading', '') or ''
        
        # Remove any existing 9.X prefix from heading
        original_heading = heading
        m = re.match(r'^9\.\d+\s+(.*)', heading)
        if m:
            original_heading = m.group(1)
        else:
            m = re.match(r'^9\.\d+$', heading)
            if m:
                original_heading = None

        if original_heading == 'General Principle of double entry accrual basis of accounting ACCRUAL BASIS OF ACCOUNTING':
            # Remove numbering from this chunk
            c['heading'] = original_heading
        else:
            # We want to re-number starting from 9.1 for the chunk with text "The financial statements..."
            pass # We will do a sequential pass instead

# Sequential pass for chapter 9
sub_id = 1
for c in chunks:
    if c.get('chapter') == '9':
        heading = c.get('heading', '') or ''
        
        # Determine original heading
        original_heading = heading
        m = re.match(r'^9\.\d+\s+(.*)', heading)
        if m:
            original_heading = m.group(1)
        else:
            m = re.match(r'^9\.\d+$', heading)
            if m:
                original_heading = None
                
        # If it's the General Principle title, don't number it
        if original_heading == 'General Principle of double entry accrual basis of accounting ACCRUAL BASIS OF ACCOUNTING':
            c['heading'] = original_heading
            continue
            
        # Number other chunks
        if original_heading:
            c['heading'] = f"9.{sub_id} {original_heading}"
        else:
            c['heading'] = f"9.{sub_id}"
            
        sub_id += 1

with open(output_path, 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

print("Fixed chapter 9 numbering.")
