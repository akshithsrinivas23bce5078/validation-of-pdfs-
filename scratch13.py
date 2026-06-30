import json
import re
import os

file_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'
output_path = file_path + '.tmp'

lines = open(file_path, 'r', encoding='utf-8').readlines()
changed_lines = 0

for i in range(len(lines)):
    data = json.loads(lines[i])
    text = data.get('text', '')
    p = data.get('para', 0)
    
    # We use (?:^|\s) instead of \b
    m = re.search(r'(?:^|\s)(?:\(' + str(p) + r'\)|' + str(p) + r'\.)\s+([A-Z][A-Z\s]+)', text)
    if m and m.start() > 10:
        print(f"Para {p} has internal heading: {m.group(0)} at position {m.start()}")
        
        if i > 0:
            prev_data = json.loads(lines[i-1])
            # Only transfer if it actually matches previous paragraph, OR if previous paragraph exists and this is clearly a split.
            # Some paragraphs might be missing, so we just transfer to the immediately preceding chunk as long as it's the same chapter
            # Wait, better to just check if prev_data['para'] < p.
            if prev_data.get('para') < p:
                print(f"  Transferring {m.start()} chars to Para {prev_data.get('para')}")
                prev_text_to_add = text[:m.start()].strip()
                prev_data['text'] = prev_data['text'] + ' ' + prev_text_to_add
                lines[i-1] = json.dumps(prev_data, ensure_ascii=False) + '\n'
                changed_lines += 1
                
                # Check current heading
                print(f"  Current heading: {data['heading']}")
                
                new_text = text[m.end():].lstrip(' \t\n\r:-')
                data['text'] = new_text
                lines[i] = json.dumps(data, ensure_ascii=False) + '\n'
                changed_lines += 1
            else:
                print(f"  ERROR: Prev para is not < {p}")

with open(output_path, 'w', encoding='utf-8') as fout:
    fout.writelines(lines)
    
os.replace(output_path, file_path)
print(f'Total chunks changed: {changed_lines}')
