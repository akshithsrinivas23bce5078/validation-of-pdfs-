import json
import random
import string

filepath = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\TN_Vision_2023(PHASE 1).jsonl'
with open(filepath, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f if line.strip()]

doc_ids = set()

for c in chunks:
    # 1. Remove .pdf from DOC_NAME
    doc_name = c.get('DOC_NAME', '')
    if doc_name.endswith('.pdf'):
        c['DOC_NAME'] = doc_name[:-4]

    # 2. Ensure unique doc_id
    d_id = c.get('doc_id', '')
    if not d_id or d_id in doc_ids:
        # Generate unique ID if missing or duplicate
        while True:
            new_id = "TNV-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=10))
            if new_id not in doc_ids:
                c['doc_id'] = new_id
                doc_ids.add(new_id)
                break
    else:
        doc_ids.add(d_id)

with open(filepath, 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=True) + "\n")

print("Successfully cleaned up DOC_NAME and ensured all doc_ids are unique!")
