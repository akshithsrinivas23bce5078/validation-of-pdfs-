import json
filepath = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\TAMIL_NADU_MINISTERIAL_SERVICE_RULES_validated.jsonl'
with open(filepath, 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        c = json.loads(line)
        if c.get('has_table'):
            print(f"Chunk {i+1}:")
            print(f"heading: {c['heading']}")
            print(f"has_table: {c['has_table']}")
            print(f"table_html: {c['table_html'][:100]}...")
            print('-'*20)
