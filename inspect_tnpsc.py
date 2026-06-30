import json

filepath = r'c:\Users\Akshith Srinivas\chunk-validator-one\unvalidated chunks\TNPSC_AF_Rule_2022_chunks.jsonl'
with open(filepath, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f if line.strip()]

for i, c in enumerate(chunks):
    print(f'Chunk {i+1}:')
    print(f"Heading: {c.get('heading')}")
    print(f"Section: {c.get('section')}")
    print(f"Text length: {len(c.get('text', ''))}")
    print('-'*40)
