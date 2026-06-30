import json

filepath = r'c:\Users\Akshith Srinivas\chunk-validator-one\unvalidated chunks\TAMIL_NADU_SECRETARIAT_SERVICE_RULES.jsonl'
with open(filepath, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f if line.strip()]

for i, c in enumerate(chunks):
    print(f"Chunk {i+1}:")
    print(f"Section: {c.get('section')}")
    print(f"Rule No: {c.get('rule_no')}")
    print(f"Heading: {c.get('heading')}")
    print(f"Title: {c.get('title')}")
    print(f"Text length: {len(c.get('text', ''))}")
    print('-'*40)
