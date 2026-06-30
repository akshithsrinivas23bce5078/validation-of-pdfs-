import json

filepath = r'c:\Users\Akshith Srinivas\chunk-validator-one\unvalidated chunks\TAMIL_NADU_MINISTERIAL_SERVICE_RULES.jsonl'
with open(filepath, 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        c = json.loads(line)
        print(f"Chunk {i+1}:")
        print(f"Section: {c.get('section')}")
        print(f"Rule No: {c.get('rule_no')}")
        print(f"Heading: {c.get('heading')}")
        print(f"Title: {c.get('title')}")
        print(f"Text Length: {len(c.get('text', ''))}")
        if i >= 10:
            print('... showing first 10 chunks only ...')
            break
