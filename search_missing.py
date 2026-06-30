import json

with open(r'chunks after validation\RAM_2022_Sixth_Edition_fixed.jsonl', 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

# Ch 5, heading '3. Roles Of The Department' - what's the text?
for c in chunks:
    if c.get('chapter') == '5' and c.get('heading', '').startswith('3. '):
        print('Heading:', c['heading'])
        print('Text:', c['text'])
        print()

# The 3.1 heading should be 'At Railway Board Level' based on Ch4's pattern
print('=== Searching for At Railway Board Level ===')
for c in chunks:
    if c.get('chapter') == '5':
        text = c.get('text', '')
        if 'Railway Board Level' in text:
            h = c.get('heading', '')
            idx = text.find('Railway Board Level')
            print('Found in heading', h, 'at pos', idx)
            print(text[max(0,idx-80):idx+100])
            print('---')

# Also check what Ch 18 heading 1 text should be
print('\n=== Ch 18 chunks ===')
for c in chunks:
    if c.get('chapter') == '18':
        h = c.get('heading', '')
        text = c.get('text', '')[:200]
        print('Heading:', h)
        print('Text:', text)
        print()
