import json

filepath = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Chapter 9_2.jsonl'
with open(filepath, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f if line.strip()]

for c in chunks:
    if c.get('has_table'):
        html = c.get('table_html', '')
        if isinstance(html, str) and '' in html:
            c['table_html'] = html.replace('', '-')

with open(filepath, 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

print("Cleaned unicode replacement character in table_html.")
