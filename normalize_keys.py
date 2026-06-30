import json

path = r'chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'
with open(path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

for c in chunks:
    # Ensure numeric chapter
    ch = str(c.get('chapter', '')).replace('CHAPTER ', '').replace('Chapter ', '').strip()
    if ch == 'I': ch = '1'
    elif ch == 'II': ch = '2'
    elif ch == 'III': ch = '3'
    elif ch == 'IV': ch = '4'
    c['chapter'] = ch
    
    # Rename page to page_number
    if 'page' in c:
        c['page_number'] = c['page']
        del c['page']
        
    # Check title mapping
    if ch == '1': c['title'] = 'GENERAL INSTRUCTIONS'
    elif ch == '2': c['title'] = 'AUDIT OF MUNICIPAL COUNCILS'
    elif ch == '3': c['title'] = 'AUDIT OF TOWN PANCHAYATS'
    elif ch == '4': c['title'] = 'AUDIT OF PANCHAYAT UNIONS'

    # Ensure has_table and table_html exist
    if 'has_table' not in c: c['has_table'] = False
    if 'table_html' not in c: c['table_html'] = ''

with open(path, 'w', encoding='utf-8') as f:
    for c in chunks:
        # Reorder keys
        ordered = {
            'doc_name': c.get('doc_name', 'Local Fund Audit Depart Manual Vol - II'),
            'doc_id': c.get('doc_id', 'LFA-9A7560D8FA'),
            'chapter': c['chapter'],
            'title': c['title'],
            'heading': c['heading'],
            'text': c.get('text', ''),
            'page_number': c.get('page_number', 0),
            'has_table': c['has_table'],
            'table_html': c['table_html']
        }
        f.write(json.dumps(ordered, ensure_ascii=False) + '\n')

print(f"Normalized keys and verified structure for {len(chunks)} chunks.")
