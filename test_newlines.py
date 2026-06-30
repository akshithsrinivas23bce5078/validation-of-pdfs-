import json

with open(r'chunks after validation\RAM_2022_Sixth_Edition_fixed.jsonl', encoding='utf-8') as f:
    chunks = [json.loads(x) for x in f]

for i, c in enumerate(chunks[485:490]):
    print(f"--- Chunk {485+i} ---")
    print(f"HEADING: {repr(c['heading'])}")
    lines = c['text'].split('\n')
    print(f"TEXT LINES: {repr(lines[:3])}")
    
# Let's also check some earlier chunks like chapter 1
for i, c in enumerate(chunks[0:5]):
    print(f"--- Chunk {i} ---")
    print(f"HEADING: {repr(c['heading'])}")
    lines = c['text'].split('\n')
    print(f"TEXT LINES: {repr(lines[:3])}")
