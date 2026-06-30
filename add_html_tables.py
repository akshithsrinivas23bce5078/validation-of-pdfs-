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

# Calculate end_page for each chunk
for i in range(len(chunks)):
    start_p = chunks[i]['p_num']
    if i < len(chunks) - 1:
        end_p = chunks[i+1]['p_num'] - 1
    else:
        end_p = 514
    
    # If end_p < start_p, they share the same page
    if end_p < start_p:
        end_p = start_p
    
    chunks[i]['start_p'] = start_p
    chunks[i]['end_p'] = end_p

# 3. Extract tables from PDF
pdf_path = r'assigned pdfs\Local Fund Audit Depart Manual  Vol - II.pdf'

tables_by_page = {}
with pdfplumber.open(pdf_path) as pdf:
    # Pages 16 to 514
    for p_num in range(16, 515):
        page = pdf.pages[p_num - 1]
        tables = page.extract_tables()
        if tables:
            tables_by_page[p_num] = tables

# 4. Assign tables to chunks
for c in chunks:
    c['has_table'] = False
    c['table_html'] = ""
    
    # For chunks that share the same start page, we only assign the table to the FIRST chunk that starts on that page
    # to avoid duplicating the table in both chunks. Actually, let's assign it to the one that encompasses the page.
    # Wait, if c1 is (16, 16) and c2 is (16, 23), both cover 16.
    # Let's just collect tables for the pages
    
    chunk_tables_html = []
    
    for p in range(c['start_p'], c['end_p'] + 1):
        if p in tables_by_page:
            for t in tables_by_page[p]:
                chunk_tables_html.append(table_to_html(t))
            # Delete from tables_by_page so it's not assigned to multiple chunks
            del tables_by_page[p]
            
    if chunk_tables_html:
        c['has_table'] = True
        c['table_html'] = '\n<br>\n'.join(chunk_tables_html)

# 5. Write back to JSONL
for c in chunks:
    del c['p_num']
    del c['start_p']
    del c['end_p']

with open(input_path, 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

print(f"Finished adding tables. Modified {sum(1 for c in chunks if c['has_table'])} chunks with tables.")
