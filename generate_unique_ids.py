import json
import random
import string

filepath = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\TN_Vision_2023(PHASE 1).jsonl'
with open(filepath, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f if line.strip()]

doc_ids = set()

for c in chunks:
    # Generate unique ID
    while True:
        new_id = "TNV-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=10))
        if new_id not in doc_ids:
            doc_ids.add(new_id)
            c['doc_id'] = new_id
            break

with open(filepath, 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=True) + "\n")

print("Generated unique doc_ids for all chunks!")
