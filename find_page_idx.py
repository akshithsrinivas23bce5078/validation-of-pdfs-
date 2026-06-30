import json
path = r'unvalidated chunks\Local Fund Audit Depart Manual  Vol - II.jsonl'
page_starts = {}
giant_text = ''
with open(path, 'r', encoding='utf-8') as f:
    for line in f:
        c = json.loads(line)
        p = c.get('start_page', 0)
        if 16 <= p <= 79:
            page_starts[p] = len(giant_text)
            giant_text += ' ' + c.get('content', '')
for p in sorted(page_starts.keys()):
    if page_starts[p] <= 86487 < page_starts.get(p+1, 9999999):
        print(f"Index 86487 is on physical page: {p}")
