import json
filepath = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Handbook_slb_wsss_validated.jsonl'
with open(filepath, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f if line.strip()]

for i, c in enumerate(chunks[:2]):
    print(f'Chunk {i+1}:')
    print(f"DOC_NAME: {c.get('DOC_NAME')}")
    print(f"doc_id: {c.get('doc_id')}")
    print(f"chapter: {c.get('chapter')}")
    print(f"heading: {c.get('heading')}")
    print(f"page.no: {c.get('page.no')}")
    print(f"has_table: {c.get('has_table')}")
    print(f"table_html length: {len(c.get('table_html', ''))}")
    print(f"text snippet: {c.get('text')[:200]}...")
    print('-'*40)
