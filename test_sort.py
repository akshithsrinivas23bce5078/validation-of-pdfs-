import json
import re

with open(r'chunks after validation\19__Opening_Balance_Sheet_Accounting_Manual_P_State_Audit_West_Ben.jsonl', encoding='utf-8') as f:
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

# Test sort
sorted_chunks = sorted(chunks, key=sort_key)

for i, c in enumerate(sorted_chunks):
    hd = c.get('heading')
    text = c.get('text', '')[:30]
    print(f"{i}: ch={c.get('chapter')} hd={hd} text={text} page={c.get('page.no')}")
