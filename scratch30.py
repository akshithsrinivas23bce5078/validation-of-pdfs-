import json
import os

file_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'
output_path = file_path + '.tmp'

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(len(lines)):
    data = json.loads(lines[i])
    p = data.get('para', 0)
    t = data.get('text', '')
    h = data.get('heading', '')
    
    if p == 21 and 'Education Tax' in h:
        data['text'] = 'Education Tax ' + t
        lines[i] = json.dumps(data, ensure_ascii=False) + '\n'
        print("Fixed Para 21")
        
    elif p == 82 and 'Souvenir' in h:
        data['text'] = 'Souvenir ' + t
        lines[i] = json.dumps(data, ensure_ascii=False) + '\n'
        print("Fixed Para 82")

with open(output_path, 'w', encoding='utf-8') as fout:
    fout.writelines(lines)
    
os.replace(output_path, file_path)
