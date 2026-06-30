import json

val_path = r'chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'

with open(val_path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

for c in chunks:
    # Handle doc_name / DOC_NAME
    if 'doc_name' in c:
        c.pop('doc_name')
    c['DOC_NAME'] = "Local Fund Audit Depart Manual Vol - II"
    
    # Re-order to make DOC_NAME first
    new_c = {"DOC_NAME": c['DOC_NAME']}
    for k, v in c.items():
        if k != 'DOC_NAME':
            new_c[k] = v
    c.clear()
    c.update(new_c)

with open(val_path, 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

print("Updated DOC_NAME.")
print(f"Sample: {json.dumps(chunks[0], ensure_ascii=False)[:200]}")
