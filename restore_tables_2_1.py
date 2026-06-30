import json
import re

unvalidated_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\unvalidated chunks\Chapter 2_1.jsonl'
validated_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Chapter 2_1.jsonl'

# Read unvalidated chunks to map prefix to table_html
with open(unvalidated_path, 'r', encoding='utf-8') as f:
    unvalidated_chunks = [json.loads(line) for line in f if line.strip()]

# Map each 2.x prefix to a list of table_html strings
prefix_to_tables = {}
for c in unvalidated_chunks:
    if c.get('has_table'):
        heading = c.get('heading', '')
        m = re.match(r'^(2\.\d+)', heading)
        if m:
            prefix = m.group(1)
            if prefix not in prefix_to_tables:
                prefix_to_tables[prefix] = []
            prefix_to_tables[prefix].append(c.get('table_html', ''))

# Update the validated chunks
with open(validated_path, 'r', encoding='utf-8') as f:
    validated_chunks = [json.loads(line) for line in f if line.strip()]

for c in validated_chunks:
    heading = c.get('heading', '')
    m = re.match(r'^(2\.\d+)', heading)
    if m:
        prefix = m.group(1)
        if prefix in prefix_to_tables:
            c['has_table'] = True
            # We can join the table_htmls if there are multiple, or just take the first one
            # The dummy HTMLs are usually just one table tag
            # So let's just concatenate them with a newline
            c['table_html'] = "\n".join(prefix_to_tables[prefix])

with open(validated_path, 'w', encoding='utf-8') as f:
    for c in validated_chunks:
        f.write(json.dumps(c, ensure_ascii=True) + '\n')

print("Table attributes restored.")
