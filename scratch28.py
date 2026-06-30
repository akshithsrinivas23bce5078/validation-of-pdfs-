import json
import re
import os

file_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'
output_path = file_path + '.tmp'

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

total_changes = 0

for i in range(len(lines)):
    data = json.loads(lines[i])
    original_text = data.get('text', '')
    original_heading = data.get('heading', '')
    original_table = data.get('table_html', '')
    
    t = original_text
    h = original_heading
    table = original_table
    
    # Replace unicode replacement char () with apostrophe when followed by 's'
    t = re.sub(r'\ufffds\b', "'s", t)
    h = re.sub(r'\ufffds\b', "'s", h)
    table = re.sub(r'\ufffds\b', "'s", table)

    # General apostrophe replacements (e.g. within words like dont -> don't)
    t = re.sub(r'([a-zA-Z])\ufffd([a-zA-Z])', r"\1'\2", t)
    h = re.sub(r'([a-zA-Z])\ufffd([a-zA-Z])', r"\1'\2", h)
    table = re.sub(r'([a-zA-Z])\ufffd([a-zA-Z])', r"\1'\2", table)
    
    # Also fix curly quotes and dashes if they appear as unicode escapes or 
    t = t.replace('\u2018', "'").replace('\u2019', "'").replace('\u2013', '-').replace('\u2014', '-')
    h = h.replace('\u2018', "'").replace('\u2019', "'").replace('\u2013', '-').replace('\u2014', '-')
    table = table.replace('\u2018', "'").replace('\u2019', "'").replace('\u2013', '-').replace('\u2014', '-')
    
    # Finally, replace any remaining standalone  with a standard dash or space depending on context.
    # We will just remove it if it's stray or replace with '-'
    t = t.replace('\ufffd', '-')
    h = h.replace('\ufffd', '-')
    table = table.replace('\ufffd', '-')
    
    if t != original_text or h != original_heading or table != original_table:
        data['text'] = t
        data['heading'] = h
        data['table_html'] = table
        lines[i] = json.dumps(data, ensure_ascii=False) + '\n'
        total_changes += 1

with open(output_path, 'w', encoding='utf-8') as fout:
    fout.writelines(lines)
    
os.replace(output_path, file_path)
print(f"Fixed unicode / apostrophe issues in {total_changes} chunks.")
