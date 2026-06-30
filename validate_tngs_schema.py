import json
import re

unval_file = r"unvalidated chunks\TNGS_ClassXII_chunks.jsonl"
val_file = r"chunks after validation\TNGS_ClassXII_validated.jsonl"
bold_file = r"tngs_bold_texts.json"
tables_file = r"tngs_tables.json"

CLASS_MAP = {
    'Class XII': '12',
    'Class XII-A': '12.1',
    'Class XII-B': '12.2',
    'Class XII-B(1)': '12.3',
    'Class XII-C': '12.4',
    'Class XII-D': '12.5',
    'Class XII-D(1)': '12.6',
    'Class XII-E': '12.7'
}

with open(bold_file, "r", encoding="utf-8") as f:
    bold_texts = json.load(f)
    # Sort by length descending to match longest first
    bold_texts = sorted(list(set(bold_texts)), key=len, reverse=True)

with open(tables_file, "r", encoding="utf-8") as f:
    tables_data = json.load(f)

with open(unval_file, "r", encoding="utf-8") as f:
    chunks = [json.loads(line) for line in f if line.strip()]

avoid_words = ['foreword', 'preface', 'annexure', 'appendix', 'diagram', 'flowchart']

valid_chunks = []
for c in chunks:
    # 1. Normalize schema
    c['doc_id'] = 'TNGS-B45718F47C'
    
    cls = c.get('class', '')
    c['chapter'] = CLASS_MAP.get(cls, cls)
    if 'class' in c: del c['class']
    
    if 'class_title' in c:
        c['title'] = c['class_title']
        del c['class_title']
        
    # Remove rule_no if it exists, it's not part of the standard schema
    if 'rule_no' in c:
        del c['rule_no']
        
    # 2. Content filtering (avoid words)
    title_lower = c.get('title', '').lower()
    text_lower = c.get('text', '').lower()
    
    # We only drop the chunk completely if avoid_words is in title
    if any(word in title_lower for word in avoid_words):
        continue
        
    # 3. Heading logic
    h = c.get('heading', '').strip()
    t = c.get('text', '').strip()
    
    # Let's find if h or the start of t matches any bold text
    # Since the extracted chunks might have mangled headings due to tables,
    # we check if `h` exactly matches or is a substantial prefix of a bold text.
    matched_bold = None
    # Just check if h is strongly related to a bold text
    for bt in bold_texts:
        if len(bt) > 5 and (bt.startswith(h) or h.startswith(bt)):
            matched_bold = bt
            break
            
    if matched_bold:
        c['heading'] = matched_bold
    else:
        c['heading'] = " "
        
    # If text is empty, ensure it's " "
    if not c.get('text'):
        c['text'] = " "
        
    # 4. Table logic
    c['has_table'] = False
    c['table_html'] = "{}"
    page_str = c.get('page.no', '')
    m = re.search(r'\((\d+)-', page_str)
    if not m:
        m = re.search(r'(\d+)', page_str)
        
    if m:
        page_num = int(m.group(1))
        # Find tables for this page
        # In reality, a chunk might span pages or there might be multiple tables.
        # We will inject all tables from that page if they haven't been injected already.
        # But wait, it's safer to inject tables into the first chunk of the page.
        pass # Will handle below
        
    valid_chunks.append(c)

# Table injection logic:
# For each table, find the first chunk on that page_num and inject it.
# If multiple tables on the same page, combine them or put in subsequent chunks.
page_to_tables = {}
for t_data in tables_data:
    p = t_data['page_num']
    if p not in page_to_tables:
        page_to_tables[p] = []
    page_to_tables[p].append(t_data['table_html'])

for c in valid_chunks:
    page_str = c.get('page.no', '')
    m = re.search(r'\((\d+)-', page_str)
    if not m:
        m = re.search(r'(\d+)', page_str)
    if m:
        page_num = int(m.group(1))
        if page_num in page_to_tables and page_to_tables[page_num]:
            # Inject table
            # If there's more than one table, maybe we join them, but usually 1 table per chunk.
            c['has_table'] = True
            c['table_html'] = page_to_tables[page_num].pop(0)
            
with open(val_file, "w", encoding="utf-8") as f:
    for c in valid_chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

print(f"Generated {len(valid_chunks)} chunks in {val_file}")
