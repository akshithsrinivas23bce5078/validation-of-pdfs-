import json
import re
import pdfplumber

def roman_to_int(s):
    if not s: return ""
    rom_val = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    int_val = 0
    s = s.upper().replace('CHAPTER', '').strip()
    for i in range(len(s)):
        if i > 0 and rom_val[s[i]] > rom_val[s[i - 1]]:
            int_val += rom_val[s[i]] - 2 * rom_val[s[i - 1]]
        else:
            int_val += rom_val[s[i]]
    return str(int_val)

def table_to_html(table_data):
    if not table_data:
        return ""
    html = "<table border='1'>\n"
    for i, row in enumerate(table_data):
        html += "  <tr>\n"
        for cell in row:
            cell_text = str(cell).replace('\n', ' ') if cell is not None else ""
            if i == 0:
                html += f"    <th>{cell_text}</th>\n"
            else:
                html += f"    <td>{cell_text}</td>\n"
        html += "  </tr>\n"
    html += "</table>"
    return html

input_file = r"c:\Users\Akshith Srinivas\chunk-validator-one\unvalidated chunks\Secretariat_Office_Manual_chunks.jsonl"
pdf_path = r"c:\Users\Akshith Srinivas\chunk-validator-one\assigned pdfs\The Secretariat Office Manual.pdf"
output_file = r"c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\SECRETARIAT_OFFICE_MANUAL_validated.jsonl"

with open(input_file, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f if line.strip()]

valid_chunks = []
doc_id = "SOM-13D46A86" # Ensure unique & uniform

# Filter words
avoid_words = ['foreword', 'preface', 'annexure', 'appendix', 'diagram', 'flowchart']

for c in chunks:
    title = c.get('chapter_title', '')
    text = c.get('text', '')
    
    # Filter out unwanted sections
    if any(word in title.lower() for word in avoid_words) or any(word in text.lower()[:200] for word in avoid_words):
        # Allow 'miscellaneous' which might contain word 'appendix' etc., but let's be strict on title.
        if any(word in title.lower() for word in avoid_words):
            continue

    new_chunk = {}
    new_chunk['DOC_NAME'] = "THE_SECRETARIAT_OFFICE_MANUAL"
    new_chunk['doc_id'] = doc_id
    new_chunk['chapter'] = roman_to_int(c.get('chapter', ''))
    new_chunk['title'] = title
    
    para_no = str(c.get('para_no', '')).strip()
    para_title = str(c.get('para_title', '')).strip()
    
    if para_no and para_title:
        new_chunk['heading'] = f"{para_no}. {para_title}"
    elif para_no:
        new_chunk['heading'] = f"{para_no}."
    else:
        new_chunk['heading'] = para_title

    # Only one heading per line check - we are just assigning the string
    new_chunk['text'] = text
    
    page_str = c.get('page_no', '').strip()
    if page_str:
        new_chunk['page.no'] = f"({page_str})"
    else:
        new_chunk['page.no'] = "()"
        
    new_chunk['has_table'] = False
    new_chunk['table_html'] = "{}"
    
    valid_chunks.append(new_chunk)

print("Injecting tables...")
# Table extraction
with pdfplumber.open(pdf_path) as pdf:
    for c in valid_chunks:
        page_str = c.get('page.no', '')
        # extract numbers from page_str e.g. "(19-20)" or "(19)"
        match = re.findall(r'\d+', page_str)
        if not match:
            continue
            
        min_p = int(match[0])
        max_p = int(match[-1])
        
        tables_found = []
        for p in range(min_p, max_p + 1):
            # Pages are 0 indexed in pdfplumber
            # But what is the mapping of printed page to absolute index?
            # We must be careful!
            page_index = p - 1 # Assuming index matches printed page
            if 0 <= page_index < len(pdf.pages):
                page = pdf.pages[page_index]
                page_tables = page.extract_tables()
                if page_tables:
                    tables_found.extend(page_tables)
                    
        if tables_found:
            c['has_table'] = True
            c['table_html'] = table_to_html(tables_found[0]) # For now, just taking the first table

import os
os.makedirs(os.path.dirname(output_file), exist_ok=True)
with open(output_file, 'w', encoding='utf-8') as f:
    for c in valid_chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

print(f"Generated {len(valid_chunks)} chunks in {output_file}")
