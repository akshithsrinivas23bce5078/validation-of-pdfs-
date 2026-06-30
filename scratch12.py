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
    
    # Check if there is an internal heading inside the text
    # e.g. "(33) REVISION PETITIONS:-" inside Para 33
    # If found, this means all the text before this belongs to Para (p-1)
    
    m = re.search(r'\b(?:\(' + str(p) + r'\)|' + str(p) + r'\.)\s+([A-Z][A-Z\s]+)', text)
    if m and m.start() > 10:
        # We found a delayed heading!
        print(f"Para {p} has internal heading: {m.group(0)} at position {m.start()}")
        
        # The text BEFORE this heading belongs to the PREVIOUS paragraph (p-1)
        # Wait, is the previous paragraph guaranteed to be at lines[i-1]?
        # Usually yes. Let's check lines[i-1]
        if i > 0:
            prev_data = json.loads(lines[i-1])
            if prev_data.get('para') == p - 1:
                print(f"  Transferring {m.start()} chars to Para {p-1}")
                prev_text_to_add = text[:m.start()].strip()
                prev_data['text'] = prev_data['text'] + ' ' + prev_text_to_add
                lines[i-1] = json.dumps(prev_data, ensure_ascii=False) + '\n'
                changed_lines += 1
                
                # Now remove that from current para
                # And also remove the internal heading!
                # Since the actual heading should already be in `heading`
                # Let's verify heading
                print(f"  Current heading: {data['heading']}")
                
                new_text = text[m.end():].lstrip(' \t\n\r:-')
                data['text'] = new_text
                lines[i] = json.dumps(data, ensure_ascii=False) + '\n'
                changed_lines += 1
            else:
                print(f"  ERROR: Prev para is not {p-1}")

with open(output_path, 'w', encoding='utf-8') as fout:
    fout.writelines(lines)
    
os.replace(output_path, file_path)
print(f'Total chunks changed: {changed_lines}')
