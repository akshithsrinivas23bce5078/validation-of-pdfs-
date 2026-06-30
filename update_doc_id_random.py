import json
import random
import string

# Generate 3 uppercase letters
prefix = "TNV"

# Generate 10 uppercase hex characters
hex_chars = "0123456789ABCDEF"
suffix = "".join(random.choice(hex_chars) for _ in range(10))

new_doc_id = f"{prefix}-{suffix}"

filepath = r"c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\TN_Vision_2023(PHASE 1).jsonl"
with open(filepath, "r", encoding="utf-8") as f:
    chunks = [json.loads(line) for line in f if line.strip()]

for c in chunks:
    c["doc_id"] = new_doc_id

with open(filepath, "w", encoding="utf-8") as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=True) + "\n")

print(f"Successfully updated doc_id to {new_doc_id} for {len(chunks)} chunks.")
