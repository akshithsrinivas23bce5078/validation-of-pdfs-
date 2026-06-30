import pdfplumber
import json
import re

def table_to_html(table):
    html = "<table>"
    for row in table:
        html += "<tr>"
        for cell in row:
            if cell is None:
                cell = ""
            cell_text = str(cell).replace('\n', '<br>')
            html += f"<td>{cell_text}</td>"
        html += "</tr>"
    html += "</table>"
    return html

def is_valid_table(table):
    # A table must have more than 1 row and more than 1 column
    if len(table) <= 1:
        return False
    if len(table[0]) <= 1:
        return False
    return True

tables_info = []

with pdfplumber.open(r'assigned pdfs\RAM 2022 Sixth Edition.pdf') as pdf:
    # Start scanning from page 31 (where the content begins)
    for i, page in enumerate(pdf.pages[30:], start=31):
        print(f"Processing page {i}...", flush=True)
        extracted_tables = page.find_tables()
        for t in extracted_tables:
            table_data = t.extract()
            if is_valid_table(table_data):
                bbox = t.bbox
                # Extract text above the table on the same page
                text_above = page.crop((0, 0, page.width, bbox[1])).extract_text()
                
                # Find the last significant line above the table to act as a clue
                last_line = ""
                if text_above:
                    lines = [l.strip() for l in text_above.split('\n') if l.strip()]
                    if lines:
                        last_line = lines[-1]
                
                html = table_to_html(table_data)
                tables_info.append({
                    "page": i,
                    "preceding_text": last_line,
                    "html": html,
                    "rows": len(table_data),
                    "cols": len(table_data[0])
                })

print(f"Found {len(tables_info)} valid tables.")
with open('extracted_tables.json', 'w', encoding='utf-8') as f:
    json.dump(tables_info, f, indent=2, ensure_ascii=False)
