import json
import os

file_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'
output_path = file_path + '.tmp'

lines = open(file_path, 'r', encoding='utf-8').readlines()
changed_lines = 0

for i in range(len(lines)):
    data = json.loads(lines[i])
    if data.get('para') == 11 and data.get('heading') == 'Para 11 - ASSESSMENT OF PROPERTY TAX SECTION 84 AND 85':
        text = data.get('text', '')
        if text.startswith('of TNDM ACT-1920) '):
            # The user requested removing the ")" in all headings, so we omit the ")"
            data['heading'] = 'Para 11 - ASSESSMENT OF PROPERTY TAX SECTION 84 AND 85 of TNDM ACT-1920'
            data['text'] = text[len('of TNDM ACT-1920) '):]
            lines[i] = json.dumps(data, ensure_ascii=False) + '\n'
            changed_lines += 1
            print(f"Fixed Para 11")

with open(output_path, 'w', encoding='utf-8') as fout:
    fout.writelines(lines)
    
os.replace(output_path, file_path)
print(f'Total chunks changed: {changed_lines}')
