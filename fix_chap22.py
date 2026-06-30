import json
import fitz
import re
import html

jsonl_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\22__Transaction_Entries_Accounting_Manual_Par_State_Audit_West_Ben.jsonl'
output_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\22__Transaction_Entries_Accounting_Manual_Par_State_Audit_West_Ben_fix.jsonl'
pdf_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\assigned pdfs\22. Transaction Entries Accounting Manual Par_State Audit West Ben.pdf'

doc = fitz.open(pdf_path)

with open(jsonl_path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

for i, c in enumerate(chunks):
    if i == 0:
        c['heading'] = None
    elif i <= 18:
        c['heading'] = f'5.{i}'
    else:
        c['heading'] = f'5.{i}'
        
    page_no_str = c.get('page.no', '')
    match = re.search(r'\((\d+)(?:-(\d+))?\)', page_no_str)
    
    html_tables = []
    has_table = False
    
    if match:
        start_page = int(match.group(1))
        end_page = int(match.group(2)) if match.group(2) else start_page
        
        for p in range(start_page - 1, end_page):
            if p >= len(doc):
                continue
            page = doc[p]
            tables = page.find_tables()
            if tables.tables:
                for tab in tables.tables:
                    extracted = tab.extract()
                    if not extracted:
                        continue
                    has_table = True
                    html_table = "<table border='1'>"
                    for row_idx, row in enumerate(extracted):
                        html_table += "<tr>"
                        for cell in row:
                            cell_text = "" if cell is None else html.escape(str(cell).replace('\n', '<br>'))
                            if row_idx == 0:
                                html_table += f"<th>{cell_text}</th>"
                            else:
                                html_table += f"<td>{cell_text}</td>"
                        html_table += "</tr>"
                    html_table += "</table>"
                    html_tables.append(html_table)
    
    if has_table:
        c['has_table'] = True
        c['table_html'] = " ".join(html_tables)
    else:
        c['has_table'] = False
        c['table_html'] = {}

with open(output_path, 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

print("Fixed headings and added tables for 22. Transaction Entries")
