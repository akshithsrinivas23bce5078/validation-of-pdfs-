import json
import os

file_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'
output_path = file_path + '.tmp'

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(len(lines)):
    data = json.loads(lines[i])
    p = data.get('para', 0)
    h = data.get('heading', '')
    t = data.get('text', '')
    
    if p == 124 and 'i. Education Fund' in h:
        data['heading'] = h.replace(' i. Education Fund', '').strip()
        data['text'] = 'i. Education Fund ' + t
        lines[i] = json.dumps(data, ensure_ascii=False) + '\n'
        print(f"Fixed Para 124: Heading='{data['heading']}', Text starts with='{data['text'][:30]}...'")

with open(output_path, 'w', encoding='utf-8') as fout:
    fout.writelines(lines)
    
os.replace(output_path, file_path)
