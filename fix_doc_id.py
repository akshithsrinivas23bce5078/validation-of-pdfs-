import json

filepath = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Chapter 8_3.jsonl'
with open(filepath, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f if line.strip()]

# Take the doc_id from the very first chunk and apply it to all chunks
doc_id = chunks[0].get('doc_id')

for c in chunks:
    c['doc_id'] = doc_id

with open(filepath, 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

print(f"Successfully set doc_id to '{doc_id}' for all {len(chunks)} chunks in Chapter 8_3.jsonl")
