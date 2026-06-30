import json
from collections import defaultdict

with open(r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\RAM_2022_Sixth_Edition_fixed.jsonl', 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

with open('new_toc_mapping.json', 'r', encoding='utf-8') as f:
    toc = json.load(f)
headings = list(toc.values())

for i, h in enumerate(headings):
    chapters = [c.get('chapter') for c in chunks if c.get('heading') == h]
    if chapters:
        # most common chapter
        from collections import Counter
        mc = Counter(chapters).most_common(1)[0][0]
        print(f"Index {i}: {mc} | {h}")
    else:
        print(f"Index {i}: NONE | {h}")
