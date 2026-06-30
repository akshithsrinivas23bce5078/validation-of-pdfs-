import json
import re

filepath = r'c:\Users\Akshith Srinivas\chunk-validator-one\unvalidated chunks\TAMIL_NADU_SECRETARIAT_SERVICE_RULES.jsonl'

with open(filepath, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f if line.strip()]

# We want to drop the Annexure chunks (the last 2)
valid_chunks = [c for c in chunks if c.get('section', '').lower() != 'annexure']

out_chunks = []

def clean_title(title):
    # Remove trailing dashes or long sentences
    title = title.split('.—')[0].split('.')[0]
    title = title.split('.-')[0]
    return title.strip()

def build_html_table(text):
    # If there is a table in the text, we'll extract it and wrap in HTML.
    # The text usually has "TABLE Category Method of appointment (1) (2)..."
    # We will just wrap the tabular part in a simple pre-formatted HTML table to preserve structure.
    parts = re.split(r'\bTABLE\b', text, maxsplit=1)
    if len(parts) > 1:
        table_text = parts[1].strip()
        # Basic HTML table wrapper for the raw text so it qualifies as table_html
        return f"<table border='1'><tr><td><pre>{table_text}</pre></td></tr></table>"
    return "{}"

for i, c in enumerate(valid_chunks):
    rule_no = c.get('rule_no', str(i+1))
    title_raw = c.get('title', '')
    title_clean = clean_title(title_raw)
    
    heading = f"{rule_no}. {title_clean}"
    
    text = c.get('text', '')
    
    has_table = False
    table_html = "{}"
    if 'TABLE' in text:
        has_table = True
        table_html = build_html_table(text)
        
    chunk = {
        "DOC_NAME": "TAMIL_NADU_SECRETARIAT_SERVICE_RULES",
        "doc_id": "TNSS-761BB0AA77",
        "chapter": "1",
        "title": "TAMIL NADU SECRETARIAT SERVICE RULES",
        "heading": heading,
        "text": text,
        "page.no": c.get('page_no', '(1-1)'),
        "has_table": has_table,
        "table_html": table_html
    }
    out_chunks.append(chunk)

out_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\TAMIL_NADU_SECRETARIAT_SERVICE_RULES_validated.jsonl'
import os
os.makedirs(os.path.dirname(out_path), exist_ok=True)

with open(out_path, 'w', encoding='utf-8') as f:
    for c in out_chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

print(f"Generated {len(out_chunks)} chunks in {out_path}")
