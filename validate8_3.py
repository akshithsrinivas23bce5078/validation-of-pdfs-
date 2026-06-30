import json

filepath = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Chapter 8_3.jsonl'
with open(filepath, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

errors = []
for i, c in enumerate(chunks):
    for key in ['chapter', 'title', 'heading', 'text', 'page.no', 'has_table', 'table_html']:
        if key not in c:
            errors.append(f'Chunk {i} missing {key}')
            
    # Check if chapter is numeric
    if not c['chapter'].isdigit():
        errors.append(f"Chunk {i} chapter not numeric: {c['chapter']}")
        
    # Check for excluded words
    avoid_words = ['foreword', 'preface', 'annexure', 'appendix', 'diagram', 'flowchart']
    combined = (c.get('title', '') + ' ' + c.get('heading', '')).lower()
    for w in avoid_words:
        if w in combined:
            errors.append(f"Chunk {i} contains avoided word: {w}")

if errors:
    print('ERRORS FOUND:')
    for e in errors[:10]: print(e)
else:
    print('ALL CHUNKS VALID!')
