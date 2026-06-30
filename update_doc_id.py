import json
import random
import string

filepath = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\18. Account Principle Accounting Manual Part__State Audit West Ben.jsonl'

# Generate a 10-character alphanumeric uppercase string
rand_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
new_doc_id = f"AM-{rand_str}"

updated_chunks = []
with open(filepath, 'r', encoding='utf-8') as f:
    for line in f:
        c = json.loads(line)
        c['doc_id'] = new_doc_id
        updated_chunks.append(c)

with open(filepath, 'w', encoding='utf-8') as f:
    for c in updated_chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

print(f"Updated doc_id to {new_doc_id} in {len(updated_chunks)} chunks.")
