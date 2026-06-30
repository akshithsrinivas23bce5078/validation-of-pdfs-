import json
import re
import pdfplumber

def table_to_html(table_data):
    if not table_data:
        return ""
    
    html = "<table border='1'>\n"
    for i, row in enumerate(table_data):
        html += "  <tr>\n"
        for cell in row:
            # Handle None cells (merged or empty cells from pdfplumber)
            cell_text = str(cell).replace('\n', ' ') if cell is not None else ""
            if i == 0:
                html += f"    <th>{cell_text}</th>\n"
            else:
                html += f"    <td>{cell_text}</td>\n"
        html += "  </tr>\n"
    html += "</table>"
    return html

filepath = r"c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\TN_Vision_2023(PHASE 1).jsonl"
with open(filepath, "r", encoding="utf-8") as f:
    chunks = [json.loads(line) for line in f if line.strip()]

pdf_path = r"c:\Users\Akshith Srinivas\chunk-validator-one\assigned pdfs\TN_Vision_2023(PHASE 1).pdf"

with pdfplumber.open(pdf_path) as pdf:
    for c in chunks:
        page_str = c.get("page.no", "(0-0)")
        # Parse "(min-max)"
        match = re.search(r'\((\d+)-(\d+)\)', page_str)
        if match:
            min_p = int(match.group(1))
            max_p = int(match.group(2))
        else:
            continue
            
        tables_found = []
        for p in range(min_p, max_p + 1):
            # PDF pages are 0-indexed, so page p in the document is index p-1
            # But wait, my min_p max_p refer to the document's printed page number, which matches the index!
            # Let's verify: Page 9 printed is index 8. The loop range(8, 66) gives indices 8..65.
            # My min_p for Executive Summary was 9. The index should be min_p - 1.
            page_index = p - 1
            if 0 <= page_index < len(pdf.pages):
                page = pdf.pages[page_index]
                page_tables = page.extract_tables()
                if page_tables:
                    tables_found.extend(page_tables)
        
        if tables_found:
            c["has_table"] = True
            c["table_html"] = {}
            for i, tbl in enumerate(tables_found):
                c["table_html"][f"table_{i+1}"] = table_to_html(tbl)
        else:
            c["has_table"] = False
            c["table_html"] = {}

with open(filepath, "w", encoding="utf-8") as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=True) + "\n")

print(f"Successfully injected real HTML tables into {len(chunks)} chunks.")
