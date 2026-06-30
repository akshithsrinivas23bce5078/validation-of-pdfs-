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
    
    if p == 4 and t.startswith('AUDIT FUNCTIONS OF ASSISTANT DIRECTORS:-'):
        data['text'] = t.replace('AUDIT FUNCTIONS OF ASSISTANT DIRECTORS:-', '').strip()
        lines[i] = json.dumps(data, ensure_ascii=False) + '\n'
        changed += 1
        print("Fixed Para 4")
        
    elif p == 51 and t.startswith('SEWAGE FARMS MAINTAINED BY MUNICIPALITIES DEPARTMENTALLY; -'):
        data['heading'] = 'Para 51 - SEWAGE FARMS MAINTAINED BY MUNICIPALITIES DEPARTMENTALLY'
        data['text'] = t.replace('SEWAGE FARMS MAINTAINED BY MUNICIPALITIES DEPARTMENTALLY; -', '').strip()
        lines[i] = json.dumps(data, ensure_ascii=False) + '\n'
        changed += 1
        print("Fixed Para 51")
        
    elif p == 61 and t.startswith('ON TRANSFER OF IMMOVABLE PROPERTY;-'):
        data['heading'] = 'Para 61 - SURCHARGE ON STAMP DUTY ON TRANSFER OF IMMOVABLE PROPERTY'
        data['text'] = t.replace('ON TRANSFER OF IMMOVABLE PROPERTY;-', '').strip()
        lines[i] = json.dumps(data, ensure_ascii=False) + '\n'
        changed += 1
        print("Fixed Para 61")
        
    elif p == 62 and t.startswith('BY LOCAL BODIES;-'):
        data['heading'] = 'Para 62 - OVERDRAWAL OF FUNDS BY LOCAL BODIES'
        data['text'] = t.replace('BY LOCAL BODIES;-', '').strip()
        lines[i] = json.dumps(data, ensure_ascii=False) + '\n'
        changed += 1
        print("Fixed Para 62")

with open(output_path, 'w', encoding='utf-8') as fout:
    fout.writelines(lines)
    
os.replace(output_path, file_path)
print(f"\nTotal fixed: {changed}")
