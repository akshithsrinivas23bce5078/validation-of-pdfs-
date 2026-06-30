import json

FILE_PATH = r'chunks after validation\20. Chart of Account Accounting Manual Part_4_State Audit West Ben.jsonl'

with open(FILE_PATH, encoding='utf-8') as f:
    chunks = [json.loads(x) for x in f]

print(f"Total chunks: {len(chunks)}")
null_headings = []
for i, c in enumerate(chunks):
    if c.get('heading') is None:
        null_headings.append(i)

if null_headings:
    print(f"Found {len(null_headings)} chunks with null headings: {null_headings}")
else:
    print("No null headings found!")
