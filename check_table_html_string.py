import json
filepath = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\TN_Vision_2023(PHASE 1).jsonl'
with open(filepath, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f if line.strip()]

for i, c in enumerate(chunks):
    if c.get('has_table'):
        print(f"Chunk {i+1}:")
        print(type(c['table_html']))
        print(c['table_html'][:100])
        break
