import json

filepath = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Chapter 9_2.jsonl'
with open(filepath, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f if line.strip()]

for c in chunks:
    if c.get('has_table'):
        print(f"Heading: {c['heading']}")
        print(f"Has table: {c['has_table']}")
        print(f"Table HTML: {c['table_html']}")
