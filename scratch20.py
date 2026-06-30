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
    
    original_t = t
    
    # 1. Remove paragraph numbers like "82 ) " or "82. " at the start of the text
    t = re.sub(rf'^{p}\s*[\)\.]\s*', '', t, flags=re.IGNORECASE).strip()
    
    # Extract the core heading text (without "Para N -")
    core_heading = re.sub(r'^Para\s+\d+\s*-\s*', '', h, flags=re.IGNORECASE).strip()
    
    # 2. Check if the core heading is repeated at the start of the text
    # We will do a case-insensitive match for the first N characters (or words) to be safe.
    # To handle slight variations (like "General Institutions" vs "General Instructions._"),
    # we can try to match the exact string or strip the matched part if it's highly similar.
    
    # Simple approach: If the text starts with the exact core heading (case-insensitive), remove it.
    # Escape the core heading for regex
    if core_heading:
        escaped_heading = re.escape(core_heading)
        # Match the heading followed by optional punctuation like :- or ._ or just space
        pattern = rf'^{escaped_heading}(?:[:;_\-\.]|\s)*'
        t = re.sub(pattern, '', t, flags=re.IGNORECASE).strip()
        
    # Let's also check for specific patterns like "CHECK OF COLLECTION – General Instructions._" for Para 35
    if p == 35 and t.upper().startswith('CHECK OF COLLECTION'):
        t = re.sub(r'^CHECK OF COLLECTION[^\w]*General Instructions[^\w]*', '', t, flags=re.IGNORECASE).strip()
        
    if p == 82 and t.upper().startswith('TRANSPORT OF BODY OFDECEASED EMPLOYEE'):
        t = re.sub(r'^TRANSPORT OF BODY OFDECEASED EMPLOYEE', '', t, flags=re.IGNORECASE).strip()

    if t != original_t:
        data['text'] = t
        lines[i] = json.dumps(data, ensure_ascii=False) + '\n'
        changed += 1
        print(f"Para {p} text cleaned:")
        print(f"  Old: {original_t[:80]}")
        print(f"  New: {t[:80]}\n")

with open(output_path, 'w', encoding='utf-8') as fout:
    fout.writelines(lines)
    
os.replace(output_path, file_path)
print(f"Total text fields cleaned from redundant headings/numbers: {changed}")
