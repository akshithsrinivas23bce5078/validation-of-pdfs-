import json

jsonl_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\18. Account Principle Accounting Manual Part__State Audit West Ben.jsonl'
output_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\18. Account Principle Accounting Manual Part__State Audit West Ben_fix_heading.jsonl'

with open(jsonl_path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

for c in chunks:
    if c.get('chapter') == '2':
        heading = c.get('heading', '')
        if heading and heading.endswith(' INTRODUCTION'):
            c['heading'] = heading.replace(' INTRODUCTION', '')

with open(output_path, 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

print("Fixed headings for chapter 2.")
