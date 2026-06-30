import json
import re
import os

INPUT_FILE = r'chunks after validation\19__Opening_Balance_Sheet_Accounting_Manual_P_State_Audit_West_Ben.jsonl'
TEMP_FILE = r'chunks after validation\19__temp.jsonl'

with open(INPUT_FILE, encoding='utf-8') as f:
    chunks = [json.loads(x) for x in f]

def sort_key(c):
    ch = int(c.get('chapter', '0'))
    
    page_str = c.get('page.no', '')
    m = re.search(r'(\d+)', page_str)
    page_start = int(m.group(1)) if m else 0
    
    hd = c.get('heading')
    if hd is None:
        text = c.get('text', '')
        m2 = re.match(r'^(\d+)\.(\d+)', text)
        if m2:
            hd_parts = [int(m2.group(1)), int(m2.group(2))]
        else:
            hd_parts = [-1]
    else:
        hd_parts = [int(x) for x in re.findall(r'\d+', hd)]
        
    return (ch, hd_parts, page_start)

# Sort the chunks
sorted_chunks = sorted(chunks, key=sort_key)

# Write to temp file
with open(TEMP_FILE, 'w', encoding='utf-8') as f:
    for c in sorted_chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

# Replace original file
os.replace(TEMP_FILE, INPUT_FILE)
print("Successfully ordered chunks in 19__Opening_Balance_Sheet_Accounting_Manual_P_State_Audit_West_Ben.jsonl.")
