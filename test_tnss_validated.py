import json

filepath = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\TAMIL_NADU_SECRETARIAT_SERVICE_RULES_validated.jsonl'
with open(filepath, 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if i >= 5: break
        c = json.loads(line)
        print(f"Chunk {i+1}:")
        print(f"DOC_NAME: {c['DOC_NAME']}")
        print(f"doc_id: {c['doc_id']}")
        print(f"chapter: {c['chapter']}")
        print(f"title: {c['title']}")
        print(f"heading: {c['heading']}")
        print(f"has_table: {c['has_table']}")
        print(f"table length: {len(c['table_html'])}")
        print('-'*20)
