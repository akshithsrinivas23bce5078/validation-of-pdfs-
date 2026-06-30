import json
with open(r'chunks after validation\RAM_2022_Sixth_Edition_fixed.jsonl', 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]
print("Chapter 21 chunks:")
for i, c in enumerate(chunks):
    if c.get("chapter") == "21":
        print(f"Index {i}: Heading: {c.get('heading')}, Title: {c.get('title')}")
