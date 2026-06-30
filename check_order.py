import json

file1 = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\22__Transaction_Entries_Accounting_Manual_Par_State_Audit_West_Ben.jsonl'
print('--- 22__Transaction_Entries_... ---')
with open(file1, 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        c = json.loads(line)
        print(f"{i:2d}: {c.get('heading')}")

print('\n--- RAM_2022 Chapter 22 ---')
file2 = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\RAM_2022_Sixth_Edition_fixed.jsonl'
with open(file2, 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        c = json.loads(line)
        if c.get('chapter') == '22':
            print(f"{i:3d}: {c.get('heading')}")
