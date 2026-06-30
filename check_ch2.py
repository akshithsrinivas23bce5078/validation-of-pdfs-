import json
chunks = [json.loads(line) for line in open(r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl', encoding='utf-8')]
ch2 = [c for c in chunks if str(c.get('chapter')) == '2'][:5]
for i, c in enumerate(ch2):
    print(f"Chunk {c['doc_id']}: {c['heading']} (len={len(c.get('text',''))})")
