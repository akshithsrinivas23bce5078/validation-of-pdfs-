import json
path = r'c:\Users\Akshith Srinivas\chunk-validator-one\ch1_extracted.jsonl'
with open(path, 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if i >= 5: break
        c = json.loads(line)
        print(f'{i:02d}: P=[{c.get("page.no")}]')
