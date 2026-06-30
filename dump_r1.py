import json

filepath = r'c:\Users\Akshith Srinivas\chunk-validator-one\unvalidated chunks\TAMIL_NADU_MINISTERIAL_SERVICE_RULES.jsonl'
with open(filepath, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

r1_chunks = [c for c in chunks if c.get('rule_no') == '1' and c.get('section') != 'Annexure']
print(f'Rule 1 has {len(r1_chunks)} chunks.')
for i, c in enumerate(r1_chunks[:10]):
    print(f'--- Chunk {i} ---')
    print(f"Heading: {c.get('heading')}")
    print(f"Title: {c.get('title')}")
    print(f"Text: {c.get('text')[:100]}...")
