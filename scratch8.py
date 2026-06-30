import json
import re
import os

file_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'
output_path = file_path + '.tmp'

lines = open(file_path, 'r', encoding='utf-8').readlines()
changed_lines = 0

for i in range(len(lines)):
    data = json.loads(lines[i])
    heading = data.get('heading', '')
    p = data.get('para', 0)
    
    # Check for Para 27 specific issue: heading is 'Para 27 - -11-1987'
    if p == 27 and heading == 'Para 27 - -11-1987':
        # Fix Para 26 (line before it)
        if i > 0:
            prev_data = json.loads(lines[i-1])
            if prev_data.get('para') == 26:
                # append the missing part
                prev_data['text'] = prev_data['text'] + ' 27-11-1987 is removed.'
                lines[i-1] = json.dumps(prev_data, ensure_ascii=False) + '\n'
                changed_lines += 1
        
        # Fix Para 27
        text = data.get('text', '')
        # Remove 'is removed. ' from start
        if text.startswith('is removed. '):
            text = text[len('is removed. '):]
            
        # text starts with '27. REMISSION ON ACCOUNT OF INCLUSION OR EXCLUSION OF PARTICULAR AREA a) ...'
        m = re.match(r'^27\.\s+(REMISSION ON ACCOUNT OF INCLUSION OR EXCLUSION OF PARTICULAR AREA)\s+(a\)\s+.*)', text)
        if m:
            new_title = m.group(1).strip()
            data['heading'] = f'Para 27 - {new_title}'
            data['text'] = m.group(2)
            lines[i] = json.dumps(data, ensure_ascii=False) + '\n'
            changed_lines += 1

# Let's also check for any OTHER chunks where text contains something like 'NN. <HEADING>' where NN is para num
for i in range(len(lines)):
    data = json.loads(lines[i])
    text = data.get('text', '')
    p = data.get('para', 0)
    if not text: continue
    
    m = re.match(r'^' + str(p) + r'\.\s+([A-Z][A-Z0-9\s\-]+(?:\s+[a-z]+)?)', text[:200])
    if m:
        title = m.group(1).strip()
        if len(title) > 5 and title.isupper():
            print(f'Found trapped heading in Para {p}: {title!r}')
            # We can automatically fix this too
            data['heading'] = f'Para {p} - {title}'
            # strip the trapped heading from text
            data['text'] = text[m.end():].lstrip(' \t\n\r:-')
            lines[i] = json.dumps(data, ensure_ascii=False) + '\n'
            changed_lines += 1

with open(output_path, 'w', encoding='utf-8') as fout:
    fout.writelines(lines)
    
os.replace(output_path, file_path)
print(f'Total chunks changed: {changed_lines}')
