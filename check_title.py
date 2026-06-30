import json
with open(r'chunks after validation\RAM_2022_Sixth_Edition_fixed.jsonl', 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]
for i in range(494, 510):
    if i < len(chunks):
        c = chunks[i]
        ch = c.get("chapter")
        h = c.get("heading")
        t = c.get("title")
        print(f"Index {i}: Ch {ch}, Heading: {h}, Title: {t}")
