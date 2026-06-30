import fitz
import json
import re

val_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'
with open(val_path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

doc = fitz.open(r'c:\Users\Akshith Srinivas\chunk-validator-one\assigned pdfs\Local Fund Audit Depart Manual  Vol - II.pdf')

def table_to_html(extracted_data):
    html = "<table>\n"
    for i, row in enumerate(extracted_data):
        html += "  <tr>\n"
        tag = "th" if i == 0 else "td"
        for cell in row:
            val = str(cell).strip() if cell is not None else ""
            val = val.replace('\n', '<br>')
            html += f"    <{tag}>{val}</{tag}>\n"
        html += "  </tr>\n"
    html += "</table>"
    return html

def clean_for_match(text):
    return re.sub(r'\s+', '', text).lower()

table_chunks_mapped = 0

for p_num in range(len(doc)):
    page = doc[p_num]
    tabs = page.find_tables()
    if not tabs or len(tabs.tables) == 0:
        continue
    
    for t in tabs.tables:
        data = t.extract()
        if not data or not any(any(c for c in row) for row in data):
            continue
            
        # Find some non-empty strings to match
        search_strings = []
        for row in data:
            for cell in row:
                if cell and len(str(cell).strip()) > 5:
                    search_strings.append(clean_for_match(str(cell)))
        
        if not search_strings:
            continue
        
        # We need to find which chunk this table belongs to.
        # Check chunks that have a page range covering this page, or just check all chunks.
        # We will score chunks based on how many search_strings are in their text.
        best_chunk = None
        best_score = 0
        
        for c in chunks:
            # Quick check if chunk is nearby based on page number
            # But just searching all chunks is safer since text matching is fast
            c_text_clean = clean_for_match(c['text'])
            score = sum(1 for s in search_strings[:10] if s in c_text_clean)
            if score > best_score:
                best_score = score
                best_chunk = c
        
        # If we matched enough strings, assign table to this chunk
        if best_chunk and best_score >= min(2, len(search_strings[:10])):
            best_chunk['has_table'] = True
            html = table_to_html(data)
            if best_chunk.get('table_html'):
                best_chunk['table_html'] += "\n<br>\n" + html
            else:
                best_chunk['table_html'] = html
            table_chunks_mapped += 1
            print(f"Mapped table from page {p_num+1} to Ch{best_chunk['chapter']} Para {best_chunk['para']}")

with open(val_path, 'w', encoding='utf-8') as f:
    for c in chunks:
        # ensure boolean
        c['has_table'] = bool(c.get('has_table', False))
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

print(f"Successfully mapped {table_chunks_mapped} tables to chunks.")
