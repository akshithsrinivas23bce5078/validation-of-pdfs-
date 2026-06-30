import json
import re

jsonl_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\18. Account Principle Accounting Manual Part__State Audit West Ben.jsonl'
output_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\18. Account Principle Accounting Manual Part__State Audit West Ben_fix.jsonl'

with open(jsonl_path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

for c in chunks:
    if c.get('chapter') == '2':
        # User wants "chapternumber.subdivision name" in heading
        c['heading'] = '2.1 INTRODUCTION'
        
        # Clean up the text so it doesn't redundantly start with INTRODUCTION
        text = c.get('text', '')
        if text.startswith('INTRODUCTION '):
            c['text'] = text[len('INTRODUCTION '):]
            
    elif c.get('chapter') == '1':
        # "chapter 1 ACRONYMS no headings"
        c['heading'] = None

with open(output_path, 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

print("Fixed chapters 1 and 2 in the second file.")
