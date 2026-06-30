import json
from collections import defaultdict
import re

filepath = r'c:\Users\Akshith Srinivas\chunk-validator-one\unvalidated chunks\TAMIL_NADU_MINISTERIAL_SERVICE_RULES.jsonl'
with open(filepath, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

# Filter Annexure
valid_chunks = [c for c in chunks if c.get('section') != 'Annexure']

rules_dict = defaultdict(list)
for c in valid_chunks:
    rules_dict[c.get('rule_no')].append(c)

def clean_title(title):
    title = title.split('.')[0].split('.')[0]
    title = title.split('.-')[0]
    return title.strip()

for rule_no in sorted(list(rules_dict.keys()), key=lambda x: str(x)):
    r_chunks = rules_dict[rule_no]
    first_chunk = r_chunks[0]
    title_raw = first_chunk.get('title', '')
    title_clean = clean_title(title_raw)
    heading = f"{rule_no}. {title_clean}"
    
    full_text = "\n".join([c.get('text', '') for c in r_chunks])
    
    print(f"Heading: {heading}")
    print(f"Total chunks merged: {len(r_chunks)}")
    print(f"Combined Text Length: {len(full_text)}")
    print('-'*20)
