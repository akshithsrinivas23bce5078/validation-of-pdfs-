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

def extract_heading_from_text(text):
    match = re.split(r'\.\s*[-—]', text, maxsplit=1)
    if len(match) > 1:
        return match[0].strip()
    first_dot = text.find('.')
    if 0 < first_dot < 100:
        return text[:first_dot].strip()
    return text[:50].strip()

def sort_key(rule_str):
    num = re.sub(r'\D', '', rule_str)
    return int(num) if num else 999

for rule_no in sorted(list(rules_dict.keys()), key=sort_key)[:5]:
    r_chunks = rules_dict[rule_no]
    full_text = "\n".join([c.get('text', '') for c in r_chunks])
    
    first_title = r_chunks[0].get('title', '')
    if first_title in ["Open Competition", "Panchayat Assistants", "Superintendents."] or len(first_title) < 5:
        extracted = extract_heading_from_text(full_text)
        if extracted:
            first_title = extracted

    clean_first_title = first_title.split('.—')[0].split('.-')[0].split('.')[0].strip()
    heading = f"{rule_no}. {clean_first_title}"
    
    # Strip heading from the beginning of full_text
    # Patterns to match:
    # "Constitution. " or "Constitution.- " or "Constitution. " or "1. Constitution. "
    # We will just compile a regex that matches the rule_no and/or title at the start
    
    # Escape for regex
    esc_title = re.escape(clean_first_title)
    esc_rule = re.escape(rule_no)
    
    # Optional rule number matching "1. " or "1 "
    pattern = rf"^(?:{esc_rule}\.\s*)?(?:{esc_title})[.\-—\s]*"
    
    new_text = re.sub(pattern, "", full_text, count=1, flags=re.IGNORECASE)
    
    print(f"Heading: {heading}")
    print(f"Old Start: {full_text[:60]}")
    print(f"New Start: {new_text[:60]}")
    print('-'*40)
