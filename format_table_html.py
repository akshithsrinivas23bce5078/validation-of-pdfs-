import json

filepath = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\TN_Vision_2023(PHASE 1).jsonl'
with open(filepath, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f if line.strip()]

for c in chunks:
    if c.get('has_table') and 'table_html' in c:
        table_data = c['table_html']
        if isinstance(table_data, dict):
            # Concatenate all tables into a single string
            html_string = "\n<br>\n".join(table_data.values())
            c['table_html'] = html_string

with open(filepath, 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=True) + "\n")

print("Successfully converted table_html to concatenated strings!")
