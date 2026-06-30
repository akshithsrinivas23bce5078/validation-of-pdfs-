import json
import re
import fitz

unvalidated_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\unvalidated chunks\19__Opening_Balance_Sheet_Accounting_Manual_P_State_Audit_West_Ben.jsonl'
output_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\19__Opening_Balance_Sheet_Accounting_Manual_P_State_Audit_West_Ben.jsonl'
pdfpath = r'C:\Users\Akshith Srinivas\chunk-validator-one\assigned pdfs\19. Opening Balance Sheet Accounting Manual P_State Audit West Ben.pdf'

def get_pdf_text():
    doc = fitz.open(pdfpath)
    text = ""
    for p in doc:
        text += p.get_text()
    return text

def extract_from_pdf(key, text):
    pattern = r'(?s)\b' + re.escape(key) + r'\.(.*?)(?=(?:\n\d+\.\d+)|\n\d+\.\n|\Z)'
    m = re.search(pattern, text)
    if m:
        content = m.group(1).strip()
        content = re.split(r'\n\d+\.\s*\n', content)[0]
        content = " ".join(content.split())
        return f"{key} " + content
    return None

def format_page_range(pages):
    if not pages: return ""
    p = str(pages).replace(" ", "")
    parts = p.split("-")
    if len(parts) == 2 and parts[0] == parts[1]:
        return f"({parts[0]})"
    elif len(parts) == 2:
        return f"({parts[0]}-{parts[1]})"
    return f"({p})"

def sort_key(c):
    first_token = c['text'].split(' ')[0]
    parts = first_token.split('.')
    try:
        return [int(p) for p in parts]
    except ValueError:
        return [9999]

def main():
    # 1. Read unvalidated chunks
    with open(unvalidated_path, 'r', encoding='utf-8') as f:
        raw_chunks = [json.loads(line) for line in f]
        
    # Title mapping
    title_map = {
        "6": "Common Guidelines",
        "10": "Formats",
        "12": "Depreciation",
        "13": "Capital Works in Progress",
        "14": "Long Term Investments",
        "17": "Current Investments",
        "18": "Short Term Borrowings"
    }

    # 2. Apply validation logic
    validated = []
    for chunk in raw_chunks:
        section = str(chunk.get("section", chunk.get("chapter", "")))
        chapter_match = re.search(r'\d+', section)
        chapter_num = chapter_match.group(0) if chapter_match else section

        text = chunk.get("text", "").strip()
        prefix = chunk.get("heading", "")

        original_heading = str(chunk.get('heading', '')).strip()
        title = title_map.get(chapter_num, chunk.get("title", ""))
        
        # Skip logic
        skip = False
        title_lower = title.lower()
        if section.lower().startswith('a'):
            skip = True
        for kw in ['foreword', 'preface', 'annexure', 'appendix', 'diagram', 'flowchart']:
            if kw in title_lower or kw in original_heading.lower():
                skip = True
                break
        if skip:
            continue

        # Reconstruct text
        if prefix and text:
            if text.startswith(prefix):
                pass
            elif re.match(r'^\d+(\.\d+)*$', prefix.strip()):
                text = prefix.strip() + " " + text
        elif prefix and not text:
            text = prefix
            
        final_chunk = {
            "DOC_NAME": chunk.get("DOC_NAME"),
            "doc_id": chunk.get("doc_id"),
            "chapter": chapter_num,
            "title": title,
            "heading": None,
            "text": text,
            "page.no": format_page_range(chunk.get("page.no", "")),
            "has_table": bool(chunk.get("has_table", False)),
            "table_html": chunk.get("table_html", {})
        }
        validated.append(final_chunk)

    # 3. Split embedded chunks
    embedded_keys = ['2.3', '11.10', '11.11', '11.12', '11.13', '11.14', '15.10', '15.11', '15.12', '19.10', '19.11', '19.12', '19.13', '19.14']
    split_chunks = []
    for c in validated:
        text = c['text']
        keys = sorted(embedded_keys, reverse=True)
        positions = []
        for k in keys:
            pattern = r'(?<!\d)' + re.escape(k) + r'(?:\.|\s|[A-Z])'
            for match in re.finditer(pattern, text):
                positions.append((match.start(), k))
                
        if not positions:
            split_chunks.append(c)
            continue
            
        positions.sort()
        orig_key = re.match(r'^(\d+\.\d+)', text)
        if positions[0][0] != 0:
            positions.insert(0, (0, orig_key.group(1) if orig_key else ''))
            
        for i in range(len(positions)):
            start_idx = positions[i][0]
            end_idx = positions[i+1][0] if i+1 < len(positions) else len(text)
            
            part_text = text[start_idx:end_idx].strip()
            if not part_text:
                continue
            new_c = dict(c)
            new_c['text'] = part_text
            if i > 0:
                new_c['has_table'] = False
                new_c['table_html'] = {}
            split_chunks.append(new_c)

    # 4. Insert truly missing chunks
    truly_missing = ['6.9', '8.3', '10.3', '12.3', '13.3', '14.5', '17.4', '18.3', '21.1', '21.2', '23.2', '24.2', '25.1', '26.1']
    pdf_text = get_pdf_text()
    for k in truly_missing:
        chapter = k.split('.')[0]
        extracted_text = extract_from_pdf(k, pdf_text)
        if not extracted_text:
            print("Failed to extract from PDF:", k)
            continue
            
        template_chunk = next((c for c in split_chunks if c['chapter'] == chapter), split_chunks[0])
        new_c = dict(template_chunk)
        new_c['text'] = extracted_text
        new_c['has_table'] = False
        new_c['table_html'] = {}
        new_c['heading'] = None
        split_chunks.append(new_c)

    # 5. Sort and save
    def advanced_sort_key(c):
        ch = str(c['chapter'])
        chapter_val = int(ch) if ch.isdigit() else 9999
        
        first_token = c['text'].split(' ')[0]
        m = re.match(r'^(\d+(?:\.\d+)*)', first_token)
        if m:
            parts = m.group(1).split('.')
            sub_sort = [int(p) for p in parts]
        else:
            sub_sort = [9999]
            
        return (chapter_val, sub_sort)

    split_chunks.sort(key=advanced_sort_key)
    with open(output_path, 'w', encoding='utf-8') as f:
        for c in split_chunks:
            f.write(json.dumps(c, ensure_ascii=False) + '\n')
            
    print(f"Successfully built final 19...jsonl. Total chunks: {len(split_chunks)}")

if __name__ == '__main__':
    main()
