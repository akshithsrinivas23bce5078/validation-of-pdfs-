import json
filepath = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\TN_Vision_2023(PHASE 1).jsonl'
with open(filepath, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f if line.strip()]

print(f'Total chunks: {len(chunks)}')
for i, c in enumerate(chunks):
    print(f"{i+1}. {c['heading']} ({len(c['text'])} chars)")
