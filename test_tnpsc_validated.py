import json

filepath = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\TNPSC_AF_Rule_2022_validated.jsonl'
with open(filepath, 'r', encoding='utf-8') as f:
    for line in f:
        c = json.loads(line)
        print(f"Chunk: {c['heading']}")
        print(f"DOC_NAME: {c['DOC_NAME']}")
        print(f"doc_id: {c['doc_id']}")
        print(f"chapter: {c['chapter']}")
        print(f"title: {c['title']}")
        print('-'*20)
