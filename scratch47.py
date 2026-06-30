"""
Remove heading term from the definition text.
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
    
    if h == 'Arising reference.-':
        in_definitions = True
        
    if in_definitions:
        term = h.replace('.-', '').strip()
        text = d.get('text', '')
        
        # Regex to remove the term at the start, and any following punctuation like dot, em-dash, dash, or replacement char
        pattern = re.compile(r'^' + re.escape(term) + r'(?:\s*[\.\-—]+\s*)?', re.IGNORECASE)
        new_text = pattern.sub('', text)
        
        # Capitalize the first letter if it starts with a letter and the original did?
        # Actually just strip leading whitespace
        new_text = new_text.lstrip()
        
        if new_text != text:
            d['text'] = new_text
            lines[i] = json.dumps(d, ensure_ascii=False) + '\n'
            print(f"[{term}] '{text[:40]}...' -> '{new_text[:40]}...'")
            updated += 1
            
        if term == 'Digital Signature':
            in_definitions = False
            break

with open(output_path, 'w', encoding='utf-8') as fout:
    fout.writelines(lines)

os.replace(output_path, jsonl_path)
print(f"Updated {updated} definition texts.")
