import json
import os

filepath = r'c:\Users\Akshith Srinivas\chunk-validator-one\unvalidated chunks\Handbook_slb_wsss.jsonl'
with open(filepath, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f if line.strip()]

print(f'Total chunks in unvalidated JSONL: {len(chunks)}')
print('First chunk keys:', list(chunks[0].keys()))

for i in range(min(5, len(chunks))):
    print(f"Chunk {i}: heading='{chunks[i].get('heading')}' pages={chunks[i].get('start_page')}-{chunks[i].get('end_page')}")

# Also let's find the PDF
pdf_dir1 = r'c:\Users\Akshith Srinivas\chunk-validator-one\assigned pdfs'
pdf_dir2 = r'c:\Users\Akshith Srinivas\chunk-validator-one\pdfs'
pdf_dir3 = r'c:\Users\Akshith Srinivas\chunk-validator-one'

for d in [pdf_dir1, pdf_dir2, pdf_dir3]:
    if os.path.exists(d):
        for f in os.listdir(d):
            if 'Handbook_slb_wsss' in f:
                print(f"Found PDF in: {os.path.join(d, f)}")
