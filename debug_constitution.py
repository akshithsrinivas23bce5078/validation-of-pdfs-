import json

with open("chunks after validation/TNGS_ClassXII_validated.jsonl", "r", encoding="utf-8") as f:
    chunks = [json.loads(line) for line in f if line.strip()]

for i, c in enumerate(chunks):
    if c["heading"] == "1. Constitution":
        print(f"=== [{i}] {c['chapter']} ===")
        print(f"text (first 200 chars): {c['text'][:200]}")
        print()
