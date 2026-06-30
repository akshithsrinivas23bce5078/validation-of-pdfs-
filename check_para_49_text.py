import json
path = r'unvalidated chunks\Local Fund Audit Depart Manual  Vol - II.jsonl'
with open(path, 'r', encoding='utf-8') as f:
    for line in f:
        c = json.loads(line)
        if c.get('start_page') in [139, 140]:
            print(f"Page {c.get('start_page')}:")
            print(c.get('content')[:200].encode('ascii', 'ignore').decode('ascii'))
