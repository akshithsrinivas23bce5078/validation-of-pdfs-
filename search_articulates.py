import json

filepath = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\TN_Vision_2023(PHASE 1).jsonl'
with open(filepath, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f if line.strip()]

found = False
for i, c in enumerate(chunks):
    if 'articulates' in c['text'] or 'While Vision' in c['text']:
        print(f"Found articulates in chunk {i+1}: {c['heading']}")
        found = True

if not found:
    print('NOT FOUND ANYWHERE!')
