"""
Fix the `Department` definition which was swallowed by `Demi-official correspondence` and placed in the wrong order.
"""
import json
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

jsonl_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\The Secretariat Office Manual.jsonl'
output_path = jsonl_path + '.tmp'

with open(jsonl_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

dept_line_idx = -1
demi_line_idx = -1

for i, l in enumerate(lines):
    d = json.loads(l)
    h = d.get('heading', '')
    if h == 'Department.-':
        dept_line_idx = i
    elif h == 'Demi-official correspondence.-':
        demi_line_idx = i

if dept_line_idx != -1 and demi_line_idx != -1:
    d_dept = json.loads(lines[dept_line_idx])
    d_demi = json.loads(lines[demi_line_idx])
    
    # Fix Demi-official correspondence text
    d_demi['text'] = "Demi-official correspondence.— Correspondence is called 'Demi- official' when Government officers correspond with each other or with any member of the public on administrative or official matters, without the formality of official procedure and with a view to the interchange of communication of opinion or information which may not necessarily be placed on official record in the proceedings of Government."
    
    # Fix Department text
    d_dept['text'] = "Department is a division of the Secretariat acting under the direction of the Minister in charge or otherwise acting on behalf of the Government in accordance with the provisions in the Business Rules and Secretariat Instructions."
    
    # Re-assign
    lines[dept_line_idx] = json.dumps(d_dept, ensure_ascii=False) + '\n'
    lines[demi_line_idx] = json.dumps(d_demi, ensure_ascii=False) + '\n'
    
    # Now we need to move the Department line to be after Demi-official correspondence
    # Extract Department line
    dept_line = lines.pop(dept_line_idx)
    
    # Find new index for Demi-official correspondence
    # Since we popped dept_line, if dept_line_idx < demi_line_idx, the new demi_line_idx is demi_line_idx - 1
    new_demi_line_idx = demi_line_idx - 1 if dept_line_idx < demi_line_idx else demi_line_idx
    
    # Insert Department line after Demi-official correspondence
    lines.insert(new_demi_line_idx + 1, dept_line)

    with open(output_path, 'w', encoding='utf-8') as fout:
        fout.writelines(lines)

    os.replace(output_path, jsonl_path)
    print("Successfully fixed and reordered 'Department' definition.")
else:
    print(f"Could not find chunks. dept_line_idx: {dept_line_idx}, demi_line_idx: {demi_line_idx}")

