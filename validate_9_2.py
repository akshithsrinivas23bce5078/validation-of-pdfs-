import json

filepath = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Chapter 9_2.jsonl'
with open(filepath, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f if line.strip()]

errors = []
doc_ids = set()
for i, c in enumerate(chunks):
    for key in ['chapter', 'title', 'heading', 'text', 'page.no', 'has_table', 'table_html', 'doc_id']:
        if key not in c:
            errors.append(f'Chunk {i} missing {key}')
            
    if not c['chapter'].isdigit():
        errors.append(f"Chunk {i} chapter not numeric: {c['chapter']}")
        
    doc_ids.add(c.get('doc_id'))

    avoid_words = ['foreword', 'preface', 'annexure', 'appendix', 'diagram', 'flowchart']
    combined = (c.get('title', '') + ' ' + c.get('heading', '')).lower()
    for w in avoid_words:
        if w in combined:
            errors.append(f"Chunk {i} contains avoided word: {w}")

if len(doc_ids) > 1:
    errors.append(f"doc_ids are not unique to the document! Found: {doc_ids}")

if errors:
    print('ERRORS FOUND:')
    for e in errors[:10]: print(e)
else:
    print('ALL CHUNKS VALID!')
