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
    rule_no = c.get('rule_no')
    # Merge misclassified table rows back to their parent rules
    if rule_no in ['1A', '2A', '8A', '9A']:
        rule_no = rule_no[0]
    rules_dict[rule_no].append(c)

def extract_heading_from_text(text):
    match = re.split(r'\.\s*[-—]', text, maxsplit=1)
    if len(match) > 1:
        return match[0].strip()
    first_dot = text.find('.')
    if 0 < first_dot < 100:
        return text[:first_dot].strip()
    return text[:50].strip()

out_chunks = []

def sort_key(rule_str):
    num = re.sub(r'\D', '', rule_str)
    return int(num) if num else 999

doc_id = None

for rule_no in sorted(list(rules_dict.keys()), key=sort_key):
    r_chunks = rules_dict[rule_no]
    
    if not doc_id:
        doc_id = r_chunks[0].get('doc_id', 'TNMS-12345').upper()
        
    full_text = "\n".join([c.get('text', '') for c in r_chunks])
    
    first_title = r_chunks[0].get('title', '')
    if first_title in ["Open Competition", "Panchayat Assistants", "Superintendents."] or len(first_title) < 5:
        extracted = extract_heading_from_text(full_text)
        if extracted:
            first_title = extracted

    clean_first_title = first_title.split('.—')[0].split('.-')[0].split('.')[0].strip()
    heading = f"{rule_no}. {clean_first_title}"
    
    # Strip heading from text
    esc_title = re.escape(clean_first_title)
    esc_rule = re.escape(rule_no)
    pattern = rf"^(?:{esc_rule}\.\s*)?(?:{esc_title})[.\-—\s]*"
    new_text = re.sub(pattern, "", full_text, count=1, flags=re.IGNORECASE)
    
    if not new_text.strip():
        new_text = full_text  # fallback
    
    has_table = False
    table_html = "{}"
    
    # Check for tables
    table_match = re.split(r'\bTABLE\b', new_text, maxsplit=1, flags=re.IGNORECASE)
    if len(table_match) > 1:
        has_table = True
        table_content = table_match[1].strip()
        table_html = f"<table border='1'>\n<tbody>\n<tr>\n<td><pre>\nTABLE\n{table_content}\n</pre></td>\n</tr>\n</tbody>\n</table>"

    chunk = {
        "DOC_NAME": "TAMIL_NADU_MINISTERIAL_SERVICE_RULES",
        "doc_id": doc_id,
        "chapter": "1",
        "title": "TAMIL NADU MINISTERIAL SERVICE RULES",
        "heading": heading,
        "text": new_text.strip(),
        "page.no": r_chunks[0].get('page_no', '(1-1)'),
        "has_table": has_table,
        "table_html": table_html
    }
    out_chunks.append(chunk)

out_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\TAMIL_NADU_MINISTERIAL_SERVICE_RULES_validated.jsonl'
import os
os.makedirs(os.path.dirname(out_path), exist_ok=True)

with open(out_path, 'w', encoding='utf-8') as f:
    for c in out_chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

print(f"Generated {len(out_chunks)} consolidated chunks in {out_path} with table_html and merged misclassified rules.")
