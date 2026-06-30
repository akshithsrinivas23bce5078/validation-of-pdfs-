import json
import os

file_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'
output_path = file_path + '.tmp'

# These are the ones where the text was incomplete and we prepended the heading.
# Let's restore them by prepending the heading back.
incomplete_paras = {
    "Para 23", "Para 43", "Para 44", "Para 77", "Para 131", "Para 5", 
    "Para 16", "Para 20", "Para 60", "Para 4", "Para 8", "Para 64", 
    "Para 71", "Para 72", "Para 76", "Para 82_Souvenir", "Para 91", "Para 110"
}

# Mapping specific para numbers to their exact fixed text from earlier, 
# or we can just run the logic from scratch17.py again for these specific paras.

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

changed = 0

for i in range(len(lines)):
    data = json.loads(lines[i])
    t = data.get('text', '').strip()
    h = data.get('heading', '')
    p = data.get('para', 0)
    
    original_t = t
    
    # Check if the text starts with a lowercase letter or specific verbs indicating a missing subject
    import re
    if re.match(r'^[a-z]', t) or t.startswith('is levied') or t.startswith('are those') or t.startswith('shall be') or t.startswith('was introduced') or t.startswith('can be levied') or t.startswith('are obtained') or t.startswith('are generally') or t.startswith('are the following') or t.startswith('has been extended'):
        # We need to prepend the heading text!
        core_heading = re.sub(r'^Para\s+\d+\s*-\s*', '', h, flags=re.IGNORECASE).strip()
        if core_heading:
            t = f"{core_heading} {t}"
    elif t.startswith('_ In the case of warrant fees'):
        # Fix the weird underscore left by scratch20
        t = t.replace('_ In the case of warrant fees', 'In the case of warrant fees')

    if t != original_t:
        data['text'] = t
        lines[i] = json.dumps(data, ensure_ascii=False) + '\n'
        changed += 1

with open(output_path, 'w', encoding='utf-8') as fout:
    fout.writelines(lines)
    
os.replace(output_path, file_path)
print(f"Total restored to complete sentences: {changed}")
