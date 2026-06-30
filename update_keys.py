import json

val_path = r'chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'

with open(val_path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

for c in chunks:
    c['doc_name'] = "Local Fund Audit Depart Manual Vol - II "
    
    # Check if page_number exists and rename to page.no
    if 'page_number' in c:
        val = c.pop('page_number')
        if isinstance(val, int):
            c['page.no'] = f"({c['chapter']}-{val})"
        elif isinstance(val, str) and not val.startswith('('):
            c['page.no'] = f"({c['chapter']}-{val})"
        else:
            c['page.no'] = str(val) # Already formatted
    elif 'page.no' in c:
        val = c['page.no']
        if isinstance(val, int):
            c['page.no'] = f"({c['chapter']}-{val})"
        elif isinstance(val, str) and not val.startswith('('):
            c['page.no'] = f"({c['chapter']}-{val})"
            
    # Ensure correct ordering of keys (optional, but good for readability)
    # new_c = {}
    # for k in ['doc_name', 'doc_id', 'chapter', 'title', 'heading', 'text', 'page.no', 'has_table', 'table_html', 'para']:
    #     if k in c: new_c[k] = c[k]
    # c.clear()
    # c.update(new_c)

with open(val_path, 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

print("Updated keys and format.")
print(f"Sample: {json.dumps(chunks[0], ensure_ascii=False)[:200]}")
