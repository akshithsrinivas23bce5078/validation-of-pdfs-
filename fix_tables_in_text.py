import json
import re
import os

filepath = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\TAMIL_NADU_SECRETARIAT_SERVICE_RULES_validated.jsonl'
output_path = filepath + '.tmp'

count = 0
with open(filepath, 'r', encoding='utf-8') as f_in, open(output_path, 'w', encoding='utf-8') as f_out:
    for line in f_in:
        c = json.loads(line)
        text = c.get('text', '')
        if 'TABLE' in text:
            parts = re.split(r'\bTABLE\b', text, maxsplit=1)
            if len(parts) > 1:
                # Keep only the part before TABLE as text
                c['text'] = parts[0].strip()
                # Ensure has_table and table_html are set correctly
                c['has_table'] = True
                table_text = "TABLE " + parts[1].strip()
                c['table_html'] = f"<table border='1'><tr><td><pre>{table_text}</pre></td></tr></table>"
                count += 1
        f_out.write(json.dumps(c, ensure_ascii=False) + '\n')

os.replace(output_path, filepath)
print(f"Processed and cleaned {count} tables from text.")
