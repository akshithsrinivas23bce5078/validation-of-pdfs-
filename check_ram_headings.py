import json
import re

toc_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\new_toc_mapping.json'
with open(toc_path, 'r', encoding='utf-8') as f:
    toc = json.load(f)

jsonl_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\RAM_2022_Sixth_Edition_fixed.jsonl'
with open(jsonl_path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

# We want to see if every heading value in toc exists as a chunk heading
toc_values = set(toc.values())
chunk_headings = set()

# Also try normalizing for comparison
def norm(t):
    return re.sub(r'\s+', ' ', t.lower()).strip()

norm_chunk_headings = set()
for c in chunks:
    h = c.get("heading", "")
    chunk_headings.add(h)
    norm_chunk_headings.add(norm(h))

missing = []
for v in toc_values:
    if norm(v) not in norm_chunk_headings:
        missing.append(v)

print(f"TOC entries: {len(toc_values)}")
print(f"Unique chunk headings: {len(chunk_headings)}")
print(f"Missing headings: {len(missing)}")
if missing:
    print("Some missing headings:")
    for m in missing[:10]:
        print(" -", m)
