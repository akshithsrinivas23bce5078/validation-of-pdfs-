import json

jsonl_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\17__Introduction_Accounting_Manual_Part_1_Wes_State_Audit_West_Ben.jsonl'
output_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\17__Introduction_Accounting_Manual_Part_1_Wes_State_Audit_West_Ben_fix_2_5.jsonl'

with open(jsonl_path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

for c in chunks:
    if c.get('chapter') == '2' and c.get('heading') == '2.2 Objectives of the uniform Accounting Manual':
        c['heading'] = '2.2'
        c['text'] = 'Objectives of the uniform Accounting Manual\n' + c.get('text', '')
    elif c.get('chapter') == '5' and c.get('heading') == '5.1 Difference between Single- entry cash basis and double entry accrual basis of accounting AND DOUBLE ENTRY ACCRUAL BASIS OF ACCOUNTING':
        c['heading'] = '5.1'
        c['text'] = 'Difference between Single- entry cash basis and double entry accrual basis of accounting AND DOUBLE ENTRY ACCRUAL BASIS OF ACCOUNTING'

with open(output_path, 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

print("Fixed chunks 7 and 12.")
