import json
import os
import re

INPUT_FILE = r'chunks after validation\17__Introduction_Accounting_Manual_Part_1_Wes_State_Audit_West_Ben.jsonl'
TEMP_FILE = r'chunks after validation\17__temp.jsonl'

with open(INPUT_FILE, encoding='utf-8') as f:
    chunks = [json.loads(x) for x in f]

# 1. Revert the "8." prefix from Chapter 8 headings
for c in chunks:
    ch = c.get('chapter', '0')
    if ch == '8':
        heading = c.get('heading', '')
        if heading.startswith('8.'):
            # remove "8." 
            # e.g., "8.1. Account" -> "1. Account"
            c['heading'] = heading[2:]

# 2. Find where Chapter 8 starts
insert_index = -1
for i, c in enumerate(chunks):
    if c.get('chapter', '0') == '8':
        insert_index = i
        break

# 3. Create the new 8.1 chunk
new_chunk = {
    "DOC_NAME": "17__Introduction_Accounting_Manual_Part_1_Wes_State_Audit_West_Ben",
    "doc_id": "DTM-D086D09555",
    "chapter": "8",
    "title": "Definitions",
    "heading": "8.1",
    "text": "This section covers the definitions and relevant explanation of various terms and phrases that have been used in the Accounting Manual.",
    "page.no": "(14-14)",
    "has_table": False,
    "table_html": {}
}

# 4. Insert the new chunk
if insert_index != -1:
    chunks.insert(insert_index, new_chunk)
    print(f"Inserted 8.1 chunk at index {insert_index}")
else:
    print("Could not find Chapter 8!")

# 5. Write back to file
with open(TEMP_FILE, 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

os.replace(TEMP_FILE, INPUT_FILE)
print("Changes applied successfully.")
