import json

with open(r'chunks after validation\RAM_2022_Sixth_Edition_fixed.jsonl', 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

# Chapter 1 has EXTRA headings (2-7.1). What's happening?
print('=== Chapter 1 current headings & titles ===')
for i, c in enumerate(chunks):
    if c.get('chapter') == '1':
        h = c.get('heading', '')
        t = c.get('title', '')[:60]
        print(f'  [{i}] heading={h}, title={t}')

print()
print('=== Chapter 2 current headings & titles ===')
for i, c in enumerate(chunks):
    if c.get('chapter') == '2':
        h = c.get('heading', '')
        t = c.get('title', '')[:60]
        print(f'  [{i}] heading={h}, title={t}')

# Check how many chunks there are for chapter 1
ch1_count = sum(1 for c in chunks if c.get('chapter') == '1')
print(f'\nChapter 1 has {ch1_count} chunks, user expects 5')

# The issue: Chapter 1 should only have 1, 1.1, 1.2, 1.3, 1.4
# But it has 24 chunks including 2-7.1 which belong to Chapter 2!
# This means the chapter numbering is WRONG for some chunks
