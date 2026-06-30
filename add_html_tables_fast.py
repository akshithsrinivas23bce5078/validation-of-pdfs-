import json
import pdfplumber

def table_to_html(table):
    if not table: return ""
    html = '<table border="1">\n'
    for i, row in enumerate(table):
        html += "  <tr>\n"
        tag = "th" if i == 0 else "td"
        for cell in row:
            cell_text = str(cell) if cell is not None else ""
            cell_text = cell_text.replace('\n', '<br>')
            html += f"    <{tag}>{cell_text}</{tag}>\n"
        html += "  </tr>\n"
    html += "</table>"
    return html

# Find candidate pages using unvalidated chunks
raw_path = r'unvalidated chunks\Local Fund Audit Depart Manual  Vol - II.jsonl'
with open(raw_path, 'r', encoding='utf-8') as f:
    raw_chunks = [json.loads(line) for line in f]

candidate_pages = set()
for c in raw_chunks:
    text = c.get('content', '')
    lines = text.split('\n')
    is_table = False
    for line in lines:
        if line.count('  ') > 3 or '|' in line:
            is_table = True
            break
    if is_table:
        p = c.get('start_page', 0)
        if p >= 16:
            candidate_pages.add(p)
        # Also add end_page just in case
        ep = c.get('end_page', 0)
        if ep >= 16:
            candidate_pages.add(ep)

print(f"Candidate pages to scan for tables: {len(candidate_pages)}")
candidate_pages = sorted(list(candidate_pages))

# Extract tables only on candidate pages
pdf_path = r'assigned pdfs\Local Fund Audit Depart Manual  Vol - II.pdf'
tables_by_page = {}
with pdfplumber.open(pdf_path) as pdf:
    for p_num in candidate_pages:
        page = pdf.pages[p_num - 1]
        tables = page.extract_tables()
        if tables:
            tables_by_page[p_num] = tables

# 1. Load validated paragraphs
input_path = r'chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'
with open(input_path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

# 2. Extract page numbers
def get_page(page_str):
    if not page_str: return 0
    num = ''.join(c for c in page_str if c.isdigit())
    return int(num) if num else 0

for c in chunks:
    c['p_num'] = get_page(c['page_no'])

for i in range(len(chunks)):
    start_p = chunks[i]['p_num']
    if i < len(chunks) - 1:
        end_p = chunks[i+1]['p_num'] - 1
    else:
        end_p = 514
    if end_p < start_p:
        end_p = start_p
    chunks[i]['start_p'] = start_p
    chunks[i]['end_p'] = end_p

# 4. Assign tables to chunks
for c in chunks:
    c['has_table'] = False
    c['table_html'] = ""
    chunk_tables_html = []
    
    for p in range(c['start_p'], c['end_p'] + 1):
        if p in tables_by_page:
            for t in tables_by_page[p]:
                chunk_tables_html.append(table_to_html(t))
            del tables_by_page[p]
            
    if chunk_tables_html:
        c['has_table'] = True
        c['table_html'] = '\n<br>\n'.join(chunk_tables_html)

for c in chunks:
    del c['p_num']
    del c['start_p']
    del c['end_p']

with open(input_path, 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

print(f"Finished adding tables. Modified {sum(1 for c in chunks if c['has_table'])} chunks with tables.")
