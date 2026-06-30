import json
import os

INPUT_FILE = r'chunks after validation\17__Introduction_Accounting_Manual_Part_1_Wes_State_Audit_West_Ben.jsonl'
TEMP_FILE = r'chunks after validation\17__temp.jsonl'

with open(INPUT_FILE, encoding='utf-8') as f:
    chunks = [json.loads(x) for x in f]

for c in chunks:
    # Check if the heading is what we mistakenly changed it to
    if c.get('heading') == '9. "Official Year" or "Year"':
        # Revert the heading
        c['heading'] = '9. Accounting Year'
        
        # Remove literal backslashes in the text that are escaping quotes
        text = c.get('text', '')
        # Replace literal backslash followed by double quote with just double quote
        # E.g. The \"Official Year\" -> The "Official Year"
        new_text = text.replace('\\"', '"')
        c['text'] = new_text
        print(f"Fixed chunk. New text: {new_text}")

with open(TEMP_FILE, 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

os.replace(TEMP_FILE, INPUT_FILE)
print("Changes applied successfully.")
