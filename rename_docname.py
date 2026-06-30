import json

val_path = r'chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'

with open(val_path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

for c in chunks:
    # Rename doc_name to DOC_NAME
    if 'doc_name' in c:
        val = c.pop('doc_name')
        # Re-insert at the beginning
        new_c = {"DOC_NAME": val}
        new_c.update(c)
        c.clear()
        c.update(new_c)

with open(val_path, 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

print("Updated doc_name to DOC_NAME.")
print(f"Sample: {json.dumps(chunks[0], ensure_ascii=False)[:200]}")
