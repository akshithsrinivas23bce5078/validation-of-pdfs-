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
        
    if p == 117 and t.startswith('CONTRACTORS LEDGER') or t.startswith('CONTRACTOR\ufffdS LEDGER'):
        data['heading'] = h.strip() + " CONTRACTOR'S LEDGER"
        data['text'] = t[19:].strip()
        lines[i] = json.dumps(data, ensure_ascii=False) + '\n'
        print("Fixed Para 117")

with open(output_path, 'w', encoding='utf-8') as fout:
    fout.writelines(lines)
    
os.replace(output_path, file_path)
