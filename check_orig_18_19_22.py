import json
import re

ORIG_FILE = r'chunks after validation\RAM_2022_Sixth_Edition.jsonl'
with open(ORIG_FILE, 'r', encoding='utf-8') as f:
    orig_chunks = [json.loads(line) for line in f]

def clean_text(t):
    if not t: return t
    t = t.replace('\u2013', '-').replace('\u2019', "'").replace('\u201c', '"')
    t = t.replace('\u201d', '"').replace('\u2018', "'").replace('\u00a0', ' ')
    return t

# Ch 18 original chunks
print("=== Ch 18 original chunks ===")
for c in orig_chunks:
    if c.get('chapter') == '18':
        h = c.get('heading', '')
        text = clean_text(c.get('text', ''))[:300]
        print(f"  Heading: {h}")
        print(f"  Text: {text}")
        print()

print("\n=== Ch 19 original chunks ===")
for c in orig_chunks:
    if c.get('chapter') == '19':
        h = c.get('heading', '')
        text = clean_text(c.get('text', ''))[:200]
        print(f"  Heading: {h}")
        print(f"  Text: {text}")
        print()

print("\n=== Ch 22 original chunks ===")
for c in orig_chunks:
    if c.get('chapter') == '22':
        h = c.get('heading', '')
        text = clean_text(c.get('text', ''))[:200]
        print(f"  Heading: {h}")
        print(f"  Text: {text}")
        print()
