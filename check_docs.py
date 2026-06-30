import json
import glob
import os

folder_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation'
jsonl_files = glob.glob(os.path.join(folder_path, '*.jsonl'))

for filepath in jsonl_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        chunks = [json.loads(line) for line in f if line.strip()]
        
    if not chunks:
        continue
        
    doc_ids = set([c.get('doc_id') for c in chunks])
    print(f"{os.path.basename(filepath)}:")
    print(f"  Total chunks: {len(chunks)}")
    print(f"  Unique doc_ids: {len(doc_ids)}")
    if len(doc_ids) < 5:
        print(f"  doc_ids: {doc_ids}")
