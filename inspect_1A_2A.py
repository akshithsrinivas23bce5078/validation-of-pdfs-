import json

filepath = r'c:\Users\Akshith Srinivas\chunk-validator-one\unvalidated chunks\TAMIL_NADU_MINISTERIAL_SERVICE_RULES.jsonl'
with open(filepath, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

for rule in ['1A', '2A']:
    r_chunks = [c for c in chunks if c.get('rule_no') == rule]
    if r_chunks:
        print(f"--- Rule {rule} ---")
        for i, c in enumerate(r_chunks):
            print(f"Chunk {i} text: {c.get('text')}")
