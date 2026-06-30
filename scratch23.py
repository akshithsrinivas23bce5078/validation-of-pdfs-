import json
import re
import os

file_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'
output_path = file_path + '.tmp'

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(len(lines)):
    data = json.loads(lines[i])
    
    # Check Para 127
    if data.get('para') == 127:
        t = data.get('text', '').strip()
        h = data.get('heading', '')
        
        # Check if the text starts with the split heading fragment
        if t.startswith('AND COUNCIL’S COMMON SEAL'):
            # Append it to the heading (and keep the 'Para 127 - ' prefix intact)
            data['heading'] = h.strip() + ' AND COUNCIL’S COMMON SEAL'
            # Remove from text
            data['text'] = re.sub(r'^AND COUNCIL’S COMMON SEAL\s*', '', t).strip()
            lines[i] = json.dumps(data, ensure_ascii=False) + '\n'
            print(f"Fixed Para 127.")
            break

with open(output_path, 'w', encoding='utf-8') as fout:
    fout.writelines(lines)
    
os.replace(output_path, file_path)
