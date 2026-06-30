import json
path = r'chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'
with open(path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

empty = [c for c in chunks if not c['text'].strip()]
print(f"Total empty chunks: {len(empty)}")

from collections import defaultdict
by_ch = defaultdict(list)
for c in empty:
    by_ch[c['chapter']].append(c['heading'])

for ch, items in by_ch.items():
    print(f"Chapter {ch}: {len(items)} empty chunks")
    print(items[:5])
