import fitz
import json
import re
import os

def clean_heading(raw):
    # remove "Performance Indicator" or "Indicator"
    raw = re.sub(r'Performance Indicator.*', '', raw).strip()
    raw = re.sub(r'Indicator.*', '', raw).strip()
    
    # match the 2.1.x part and the text
    match = re.match(r'(2\.1\.\d+)\s+(.*)', raw)
    if match:
        prefix = match.group(1)
        text = match.group(2).title() # capitalize
        return f"{prefix} {text}"
    return raw

def table_to_html(tab_data):
    # check if table is just headers like "HANDBOOK ON SERVICE..."
    if len(tab_data) <= 1:
        return ""
    html = '<table border="1">\n'
    for row in tab_data:
        html += '  <tr>\n'
        for cell in row:
            cell_text = str(cell) if cell is not None else ''
            cell_text = cell_text.replace('\n', ' ').strip()
            html += f'    <td>{cell_text}</td>\n'
        html += '  </tr>\n'
    html += '</table>'
    return html

def extract_text_and_tables(doc, start_idx, end_idx):
    text_content = ""
    table_htmls = []
    
    for i in range(start_idx, end_idx + 1):
        page = doc[i]
        text = page.get_text()
        
        # very simple header/footer cleanup:
        lines = text.split('\n')
        clean_lines = []
        for line in lines:
            l = line.strip()
            # remove page numbers and headers
            if l in ["HANDBOOK ON SERVICE LEVEL BENCHMARKING", "WATER SUPPLY", "SERVICES", "2.1", "2.2", "2.3"] or l.isdigit():
                continue
            clean_lines.append(l)
        
        text_content += " ".join(clean_lines) + " "
        
        # tables
        tabs = page.find_tables()
        if tabs and tabs.tables:
            for tab in tabs.tables:
                html = table_to_html(tab.extract())
                if html:
                    table_htmls.append(html)
                    
    return text_content.strip(), "\n<br>\n".join(table_htmls)

pdf_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\assigned pdfs\Handbook_slb_wsss.pdf'
doc = fitz.open(pdf_path)

out_chunks = []
for i in range(0, len(doc), 2):
    page = doc[i]
    text = page.get_text()
    
    # Extract heading
    heading = f"2.1.{(i//2)+1} Section"
    match = re.search(r'2\.1\.\d+([^\n]+(\n[^\n]+)?)', text)
    if match:
        heading_raw = re.sub(r'\s+', ' ', match.group(0)).strip()
        heading = clean_heading(heading_raw)
        
    text_content, table_html = extract_text_and_tables(doc, i, min(i+1, len(doc)-1))
    
    chunk = {
        "DOC_NAME": "Handbook_slb_wsss",
        "doc_id": "FIRE-BFAAEC22",
        "chapter": "2.1",
        "title": "Water Supply Services",
        "heading": heading,
        "text": text_content,
        "page.no": f"({i+1}-{i+2})",
        "has_table": bool(table_html),
        "table_html": table_html if table_html else "{}"
    }
    out_chunks.append(chunk)

out_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Handbook_slb_wsss_validated.jsonl'
os.makedirs(os.path.dirname(out_path), exist_ok=True)

with open(out_path, 'w', encoding='utf-8') as f:
    for c in out_chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

print(f"Generated {len(out_chunks)} chunks in {out_path}")
