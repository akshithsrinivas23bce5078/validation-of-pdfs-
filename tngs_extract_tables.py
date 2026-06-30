import pdfplumber
import json

pdf_path = r'assigned pdfs\TNGS_ClassXII_11032022.pdf'
tables_data = []

with pdfplumber.open(pdf_path) as pdf:
    for page_num, page in enumerate(pdf.pages):
        tables = page.extract_tables()
        for i, table in enumerate(tables):
            # Create HTML
            html = "<table border='1'>\n"
            for row in table:
                html += "  <tr>\n"
                for cell in row:
                    cell_text = cell.replace('\n', '<br>') if cell else ''
                    html += f"    <td>{cell_text}</td>\n"
                html += "  </tr>\n"
            html += "</table>"
            
            tables_data.append({
                "page_num": page_num + 1,
                "table_html": html
            })

with open("tngs_tables.json", "w", encoding="utf-8") as f:
    json.dump(tables_data, f, ensure_ascii=False, indent=2)

print(f"Extracted {len(tables_data)} tables.")
