import json

filepath = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\TN_Vision_2023(PHASE 1).jsonl'
with open(filepath, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f if line.strip()]

for c in chunks:
    if c['heading'].startswith('3.') and '#' in c['heading']:
        c['heading'] = c['heading'].replace('#', '')

with open(filepath, 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=True) + "\n")

print("Successfully removed hashtags from headings!")
