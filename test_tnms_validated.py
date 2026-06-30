import json

filepath = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\TAMIL_NADU_MINISTERIAL_SERVICE_RULES_validated.jsonl'
with open(filepath, 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if i >= 5: break
        c = json.loads(line)
        print(f"Chunk {i+1}:")
        print(f"heading: {c['heading']}")
        print(f"text starts with: {c['text'][:100]}")
        print('-'*20)
