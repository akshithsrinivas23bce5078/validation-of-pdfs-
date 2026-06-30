import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

filepath = r"c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\SECRETARIAT_OFFICE_MANUAL_validated.jsonl"

with open(filepath, "r", encoding="utf-8") as f:
    chunks = [json.loads(line) for line in f if line.strip()]

updated_chunks = []
modified_count = 0

for c in chunks:
    if c.get("text") is None:
        c["text"] = " "
        modified_count += 1

    updated_chunks.append(c)

with open(filepath, "w", encoding="utf-8") as f:
    for c in updated_chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

print(f"Replaced null with ' ' for {modified_count} chunks.")
