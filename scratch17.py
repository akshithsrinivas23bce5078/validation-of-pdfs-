import json
import re
import os

file_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'
output_path = file_path + '.tmp'

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

changed = 0
for i in range(len(lines)):
    data = json.loads(lines[i])
    t = data.get('text', '').strip()
    h = data.get('heading', '')
    p = data.get('para', 0)
    
    m = re.search(r'Para \d+\s*-\s*(.+)', h)
    if not m:
        continue
    heading_text = m.group(1).strip()
    
    needs_fix = False
    prefix_to_add = heading_text
    
    # Specific fix for 'oan Assistance'
    if t.startswith('oan Assistance'):
        prefix_to_add = heading_text + " L"
        needs_fix = True
    elif t.startswith('s: The following'):
        prefix_to_add = heading_text
        needs_fix = True
    elif re.search(r'^[a-z]', t) or t.startswith('is ') or t.startswith('are ') or t.startswith('shall ') or t.startswith('may '):
        if not re.search(r'^(i|ii|iii|iv|v|vi|vii|viii|ix|x|a|b|c|d)\b[\.\)]', t, re.IGNORECASE):
            if not t.startswith('it should be seen'):
                prefix_to_add = heading_text
                needs_fix = True

    if needs_fix:
        # Proper spacing
        if t.startswith('s:'):
            new_text = prefix_to_add + t
        else:
            new_text = prefix_to_add + " " + t
            
        print(f"Para {p}:")
        print(f"  Old: {t[:60]}")
        print(f"  New: {new_text[:60]}")
        
        data['text'] = new_text
        lines[i] = json.dumps(data, ensure_ascii=False) + '\n'
        changed += 1

with open(output_path, 'w', encoding='utf-8') as fout:
    fout.writelines(lines)
    
os.replace(output_path, file_path)
print(f"\nTotal fixed: {changed}")
