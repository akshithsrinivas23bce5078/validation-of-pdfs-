import json
import os

ORIGINAL_FILE = r'unvalidated chunks\19__Opening_Balance_Sheet_Accounting_Manual_P_State_Audit_West_Ben.jsonl'
MODIFIED_FILE = r'chunks after validation\19__Opening_Balance_Sheet_Accounting_Manual_P_State_Audit_West_Ben.jsonl'

if not os.path.exists(ORIGINAL_FILE):
    print("Original file not found. Skipping content comparison.")
else:
    with open(ORIGINAL_FILE, encoding='utf-8') as f:
        orig_chunks = [json.loads(x) for x in f]
    
    with open(MODIFIED_FILE, encoding='utf-8') as f:
        mod_chunks = [json.loads(x) for x in f]

    print(f"Original chunks: {len(orig_chunks)}")
    print(f"Modified chunks: {len(mod_chunks)}")

    # Check for missing content
    for c in mod_chunks:
        if c.get('heading') == '11.10':
            print("Fixing chunk 11.10 text...")
            c['text'] = c['text'].replace('11.10.', '', 1).strip()
            # If it starts with "Vehicles", maybe the user wants it like that
            print("New text:", c['text'][:30])

    # Save fixed file
    with open(MODIFIED_FILE, 'w', encoding='utf-8') as f:
        for c in mod_chunks:
            f.write(json.dumps(c, ensure_ascii=False) + '\n')
            
    print("Fixed chunk 11.10 text.")
