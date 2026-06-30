import json
import re
import fitz

filepath = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\19__Opening_Balance_Sheet_Accounting_Manual_P_State_Audit_West_Ben.jsonl'
pdfpath = r'C:\Users\Akshith Srinivas\chunk-validator-one\assigned pdfs\19. Opening Balance Sheet Accounting Manual P_State Audit West Ben.pdf'

def get_pdf_text():
    doc = fitz.open(pdfpath)
    text = ""
    for p in doc:
        text += p.get_text()
    return text

def extract_from_pdf(key, text):
    # Match the paragraph key (e.g. "6.9.") and stop at the next paragraph (e.g. "6.10." or "7.")
    pattern = r'(?s)\b' + re.escape(key) + r'\.(.*?)(?=(?:\n\d+\.\d+)|\n\d+\.\n|\Z)'
    m = re.search(pattern, text)
    if m:
        content = m.group(1).strip()
        # Sometimes it might catch the next chapter header if it's like "\n9.\n".
        # Let's clean it up: stop at any newline followed by digit dot newline.
        content = re.split(r'\n\d+\.\s*\n', content)[0]
        # remove newlines
        content = " ".join(content.split())
        return f"{key} " + content
    return None

def split_embedded(chunk, embedded_keys):
    # If the chunk's text contains embedded keys, split it into multiple chunks
    text = chunk['text']
    # Sort keys descending so we don't match 11.1 before 11.11
    keys = sorted(embedded_keys, reverse=True)
    
    # We'll iteratively find the keys and split
    # Actually, a better way is to find all positions of any key
    positions = []
    for k in keys:
        pattern = r'(?<!\S)' + re.escape(k) + r'(?!\S)'
        for match in re.finditer(pattern, text):
            # Only consider it if it's at the start or follows a sentence end, or is generally an embedded start
            positions.append((match.start(), k))
    
    if not positions:
        return [chunk]
        
    positions.sort()
    
    # Check if the chunk's original prefix is the first position, if not add it
    first_token = text.split(' ')[0]
    if not positions or positions[0][0] != 0:
        if first_token not in [p[1] for p in positions]:
            positions.insert(0, (0, first_token))
            
    chunks_out = []
    for i in range(len(positions)):
        start_idx = positions[i][0]
        end_idx = positions[i+1][0] if i+1 < len(positions) else len(text)
        
        part_text = text[start_idx:end_idx].strip()
        
        new_chunk = dict(chunk)
        new_chunk['text'] = part_text
        # We don't change chapter/title since they belong to the same chapter
        chunks_out.append(new_chunk)
        
    return chunks_out

def main():
    with open(filepath, 'r', encoding='utf-8') as f:
        chunks = [json.loads(line) for line in f]
        
    # Keys to split
    embedded_keys = ['2.3', '11.10', '11.11', '11.12', '11.13', '11.14', '15.10', '15.11', '15.12', '19.10', '19.11', '19.12', '19.13', '19.14']
    truly_missing = ['6.9', '8.3', '12.3', '17.4', '18.3', '21.1', '21.2', '23.2', '24.2', '25.1', '26.1']
    
    pdf_text = get_pdf_text()
    
    new_chunks = []
    for c in chunks:
        split_c = split_embedded(c, embedded_keys)
        new_chunks.extend(split_c)
        
    # Now add the truly missing chunks
    # We need to assign them chapter, title, page.no based on their neighbors
    # For instance, 6.9 goes after 6.8
    # We will just append them and then sort all chunks!
    
    for k in truly_missing:
        chapter = k.split('.')[0]
        extracted_text = extract_from_pdf(k, pdf_text)
        if not extracted_text:
            print("Failed to extract:", k)
            continue
            
        # Find a chunk with the same chapter to copy metadata
        template_chunk = next((c for c in new_chunks if c['chapter'] == chapter), None)
        if not template_chunk:
            template_chunk = new_chunks[0]
            
        new_c = dict(template_chunk)
        new_c['text'] = extracted_text
        new_c['has_table'] = False
        new_c['table_html'] = {}
        new_c['heading'] = None
        new_chunks.append(new_c)
        
    # Sort chunks by numeric prefix
    def sort_key(c):
        first_token = c['text'].split(' ')[0]
        # It's usually like "6.9" or "1"
        parts = first_token.split('.')
        try:
            return [int(p) for p in parts]
        except ValueError:
            return [9999] # Fallback for acronyms etc
            
    new_chunks.sort(key=sort_key)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        for c in new_chunks:
            f.write(json.dumps(c, ensure_ascii=False) + '\n')
            
    print(f"Successfully processed. Total chunks: {len(new_chunks)}")

if __name__ == '__main__':
    main()
