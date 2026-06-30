import json
import re
import os

file_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'
output_path = file_path + '.tmp'

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(len(lines)):
    data = json.loads(lines[i])
    p = data.get('para', 0)
    t = data.get('text', '').strip()
    h = data.get('heading', '')
    
    if p == 113 and t.startswith('THE TAMIL NADU TRANSPARENCY IN TENDER ACT 1998'):
        data['heading'] = h.strip() + ' THE TAMIL NADU TRANSPARENCY IN TENDER ACT 1998'
        data['text'] = re.sub(r'^THE TAMIL NADU TRANSPARENCY IN TENDER ACT 1998\s*(?:\(Act 43 / of 1998\))?\s*', '', t, flags=re.IGNORECASE).strip()
        lines[i] = json.dumps(data, ensure_ascii=False) + '\n'
        print("Fixed Para 113")

    elif p == 115 and t.startswith('PREMEASUREMENT AND POST MEASUREMENT OF WORKS'):
        data['heading'] = h.strip() + ' PREMEASUREMENT AND POST MEASUREMENT OF WORKS'
        data['text'] = re.sub(r'^PREMEASUREMENT AND POST MEASUREMENT OF WORKS\s*', '', t).strip()
        lines[i] = json.dumps(data, ensure_ascii=False) + '\n'
        print("Fixed Para 115")
        
    elif p == 117 and t.startswith('CONTRACTORS LEDGER'):
        data['heading'] = h.strip() + ' CONTRACTORS LEDGER'
        data['text'] = re.sub(r'^CONTRACTORS LEDGER\s*', '', t).strip()
        lines[i] = json.dumps(data, ensure_ascii=False) + '\n'
        print("Fixed Para 117")

with open(output_path, 'w', encoding='utf-8') as fout:
    fout.writelines(lines)
    
os.replace(output_path, file_path)
