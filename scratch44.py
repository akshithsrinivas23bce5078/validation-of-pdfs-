"""
Remove the '18. ' prefix and '$' sign from definition headings and text.
"""
import json
import sys
import re
import os

sys.stdout.reconfigure(encoding='utf-8')

jsonl_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\The Secretariat Office Manual.jsonl'
output_path = jsonl_path + '.tmp'

with open(jsonl_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

updated = 0
in_definitions = False

for i in range(len(lines)):
    d = json.loads(lines[i])
    h = d.get('heading', '')
    
    # Check if we are in the definitions range (Para 18 sub-chunks)
    if h == '18. Arising reference.-':
        in_definitions = True
        
    if in_definitions and h.startswith('18.'):
        if h == '18.': # Skip the intro chunk
            continue
            
        old_h = h
        # Remove '18. ' prefix
        new_h = re.sub(r'^18\.\s*', '', h)
        
        # Remove '$' sign from heading
        new_h = new_h.replace('$', '')
        
        d['heading'] = new_h
        
        # Remove '$' sign from text
        if '$' in d['text']:
            d['text'] = d['text'].replace('$', '')
            
        lines[i] = json.dumps(d, ensure_ascii=False) + '\n'
        print(f"Line {i+1}: '{old_h}' -> '{new_h}'")
        updated += 1
        
        # Stop after Digital Signature
        if 'Digital Signature' in old_h:
            in_definitions = False
            break

with open(output_path, 'w', encoding='utf-8') as fout:
    fout.writelines(lines)

os.replace(output_path, jsonl_path)
print(f"Updated {updated} definition headings.")
