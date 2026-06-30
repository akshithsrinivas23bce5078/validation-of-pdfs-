import json
import re

path = r'unvalidated chunks\Local Fund Audit Depart Manual  Vol - II.jsonl'
with open(path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

for c in chunks:
    p = c.get('start_page')
    if not p: continue
    text = c.get('content', '').strip()
    
    # Try to extract a number at the end of the text
    match = re.search(r'(\d+)\s*$', text)
    if match:
        logical = int(match.group(1))
        if abs(logical - p) < 10:  # Shift shouldn't be more than 10
            print(f"Physical {p} -> Logical {logical} (Shift: {p - logical})")
