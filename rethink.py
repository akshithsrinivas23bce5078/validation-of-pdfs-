import json
import re

user_str = """
Chapter 1:
1, 1.1, 1.2, 1.3, 1.4
Chapter 2:
1, 2, 3, 3.1, 3.2, 4, 5, 6, 7, 7.1, 7.2, 7.3
Chapter 3:
1, 2, 2.1, 2.2, 2.3, 3, 3.1, 3.2, 3.3, 4, 5, 5.1, 5.2, 5.3, 6, 7, 8, 9, 9.1, 9.2, 9.3, 9.4, 9.5, 9.6, 9.7, 9.8, 9.9, 9.10
Chapter 4:
1, 2, 3, 3.1, 3.2, 4, 5, 6, 6.1, 6.2, 6.3, 6.4, 6.5, 7, 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8, 7.9, 7.10, 7.11, 7.12, 7.13, 7.14
Chapter 5:
1, 2, 3, 3.1, 3.2, 3.3, 4, 5, 6, 6.1, 6.2, 7, 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8, 7.9, 7.10, 7.11, 7.12, 7.13, 7.14, 7.15, 7.16, 7.17, 7.18, 7.19, 7.20
Chapter 6:
1, 2, 2.1, 2.2, 3, 3.1, 3.2, 3.3, 4, 5, 6, 6.1, 6.2, 6.3, 6.4, 6.5, 7, 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8, 7.9, 7.10, 7.11, 7.12, 7.13, 7.14, 7.15, 7.16, 7.17, 7.18, 7.19, 7.20, 7.21, 7.22, 7.23, 7.24, 7.25, 7.26, 7.27, 7.28, 7.29, 7.30, 7.31, 7.32, 7.33, 7.34, 7.35, 7.36, 7.37, 7.38, 7.39
Chapter 7:
1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17
Chapter 8:
1, 2, 2.1, 2.2, 2.3, 2.4, 3, 3.1, 3.2, 3.3, 4, 5, 6, 6.1, 6.2, 6.3, 6.4, 6.5, 7, 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8, 7.9, 7.10, 7.11, 7.12, 7.13, 7.14, 7.15, 7.16, 8
Chapter 9:
1, 1.1, 1.2, 2, 2.1, 2.2, 3, 3.1, 3.2, 3.3, 4, 5, 6, 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 7, 7.1, 7.2, 7.3, 8, 8.1, 8.2, 8.3
Chapter 10:
1, 2, 2.1, 2.2, 2.3, 2.4, 2.5, 3, 4, 5, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 5.8, 5.9, 5.10, 5.11, 5.12, 5.13, 5.14, 5.15
Chapter 11:
1, 2, 2.1, 2.2, 2.3, 2.4, 3, 3.1, 3.2, 3.3, 4, 5, 5.1, 5.2, 5.3, 6, 7, 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 8, 8.1, 8.2, 8.3, 8.4, 8.5, 8.6, 8.7, 8.8, 8.9, 8.10, 8.11, 8.12, 8.13
Chapter 12:
1, 1.1, 2, 2.1, 2.2, 2.3, 2.4, 3, 3.1, 3.2, 3.3, 3.4, 4, 5, 6, 7, 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8, 7.9, 7.10, 7.11, 7.12, 7.13, 7.14, 7.15, 7.16, 7.17, 7.18, 7.19, 7.20, 7.21, 7.22, 7.23, 7.24, 7.25, 8
Chapter 13:
1, 2, 3, 4
Chapter 14:
1, 2, 3, 3.1, 3.2, 3.3, 4, 5, 6, 6.1, 6.2, 6.3, 7, 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8, 7.9, 7.10, 7.11, 7.12, 7.13, 7.14, 7.15, 7.16, 7.17, 7.18, 7.19, 7.20, 7.21
Chapter 15:
1, 2, 2.1, 2.2, 2.3, 3, 3.1, 3.2, 3.3, 3.4, 4, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 5, 5.1, 5.2, 6, 7, 7.1, 7.2, 7.3
Chapter 16:
1, 2, 3, 3.1, 3.2, 3.3, 4, 5, 6, 7, 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8, 7.9, 7.10, 7.11, 7.12, 7.13, 7.14, 7.15, 7.16, 7.17, 7.18, 7.19, 7.20, 7.21, 7.22, 7.23, 8
Chapter 17:
1, 2, 3, 4, 5, 6, 6.1, 7, 8
Chapter 18:
1, 2, 3, 4, 5, 6, 7, 7.1, 7.2
Chapter 19:
1, 2, 3, 3.1, 3.2, 4, 5, 6
Chapter 20:
1, 2, 3, 4, 5, 5.1, 5.2
Chapter 21:
1, 2, 3, 4, 5, 6, 7, 8, 8.1, 8.2, 8.3, 8.4, 8.5, 8.6, 8.7, 8.8, 8.9, 8.10, 8.11, 8.12, 8.13, 8.14, 8.15, 8.16, 8.17, 8.18, 8.19, 8.20, 8.21, 8.22, 8.23, 8.24
Chapter 22:
1, 2, 2.1, 2.2, 3, 4, 5, 5.1, 5.2, 6, 7, 8
"""

user_seq = []
current_chapter = None
for line in user_str.split('\n'):
    line = line.strip()
    if line.startswith('Chapter'):
        current_chapter = line.split()[1].replace(':', '')
    elif line and current_chapter:
        nums = [n.strip() for n in line.split(',') if n.strip()]
        for n in nums:
            user_seq.append({'chapter': current_chapter, 'num': n})

with open(r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\RAM_2022_Sixth_Edition.jsonl', 'r', encoding='utf-8') as f:
    raw_chunks = [json.loads(line) for line in f]

# Decode unicode properly
for c in raw_chunks:
    for k in ['text', 'heading', 'title']:
        if c.get(k):
            try:
                c[k] = c[k].encode('latin1').decode('unicode_escape').encode('latin1').decode('utf-8')
            except:
                pass

# Clean text from other unicode escapes
def clean_text(t):
    if not t: return t
    t = t.replace('\u2013', '-').replace('\u2019', "'").replace('\u201c', '"').replace('\u201d', '"').replace('\u2018', "'").replace('\u00a0', ' ')
    return t

for c in raw_chunks:
    c['text'] = clean_text(c.get('text'))
    c['heading'] = clean_text(c.get('heading'))

# Manually construct 520 exact chunks by iterating over the 759 chunks.
# BUT wait, the text isn't split properly for Chapter 21. We have to split text within a chunk!
# So instead of assigning chunks, let's just concatenate ALL text and tables, maintaining a structure.

def dump_all_text():
    # Not just text, we need tables too.
    # It's better to process chunk by chunk.
    # If a chunk contains multiple headings, split it into multiple new chunks.
    pass

# Wait, if we just want to ensure EVERY chunk in RAM_2022_Sixth_Edition_fixed.jsonl matches exactly,
# Maybe we can map `RAM_2022_Sixth_Edition_fixed.jsonl` (468 chunks) to user's 520 sequence,
# and for the missing ones, just add empty chunks, OR fix the split?
pass
