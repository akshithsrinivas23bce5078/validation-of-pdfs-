import json

jsonl_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\17__Introduction_Accounting_Manual_Part_1_Wes_State_Audit_West_Ben.jsonl'
output_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\17__Introduction_Accounting_Manual_Part_1_Wes_State_Audit_West_Ben_fix.jsonl'

with open(jsonl_path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

for c in chunks:
    chapter = c.get('chapter')
    
    if chapter == '11':
        c['heading'] = '11.1'
    elif chapter == '12':
        c['heading'] = '12.1'

with open(output_path, 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

print(f"Fixed headings for chapter 11 and 12.")
