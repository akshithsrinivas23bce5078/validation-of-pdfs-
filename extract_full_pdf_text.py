import fitz
import re
import json

PDF_FILE = r"c:\Users\Akshith Srinivas\chunk-validator-one\assigned pdfs\19. Opening Balance Sheet Accounting Manual P_State Audit West Ben.pdf"
JSONL_FILE = r"c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\19__Opening_Balance_Sheet_Accounting_Manual_P_State_Audit_West_Ben.jsonl"

def clean_text(text):
    text = text.replace('\ufffd', '-')
    text = text.replace('(cid:183)', '-')
    text = re.sub(r'Guidelines for Opening Balance Sheet', '', text)
    text = re.sub(r'(?m)^\s*\d+\s*$', '', text)
    text = re.sub(r'\n+', '\n', text)
    return text.strip()

def extract_pdf_blocks():
    doc = fitz.open(PDF_FILE)
    full_text = ""
    for i in range(7, len(doc)):
        full_text += doc[i].get_text() + "\n"
            
    full_text = clean_text(full_text)
    
    blocks = {}
    
    chapter_positions = []
    for i in range(1, 31):
        match = re.search(r'(?m)^' + str(i) + r'\.(?:$|\s)', full_text)
        if match:
            chapter_positions.append((i, match.start()))
            
    chapter_positions.sort(key=lambda x: x[1])
    
    annexure_match = re.search(r'(?m)^ANNEXURE 1(?:$|\s)', full_text)
    end_of_doc = annexure_match.start() if annexure_match else len(full_text)
    
    for idx, (ch_num, pos) in enumerate(chapter_positions):
        start_pos = pos
        if idx + 1 < len(chapter_positions):
            end_pos = chapter_positions[idx+1][1]
        else:
            end_pos = end_of_doc
            
        block_text = full_text[start_pos:end_pos].strip()
        blocks[str(ch_num)] = block_text
        
    return blocks

def update_jsonl():
    blocks = extract_pdf_blocks()
    
    with open(JSONL_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    out_lines = []
    for line in lines:
        if not line.strip(): continue
        chunk = json.loads(line)
        ch_num = chunk.get('chapter', '')
        
        if ch_num in blocks:
            text = blocks[ch_num]
            title = chunk.get('title', '')
            
            # Robust slice if ch_num.1 exists
            match = re.search(r'(?m)^' + ch_num + r'\.1\.?(?:\s|$)', text)
            if match:
                text = text[match.start():]
            else:
                text_lines = text.split('\n')
                if text_lines and re.match(r'^' + ch_num + r'\.?$', text_lines[0].strip()):
                    text_lines.pop(0)
                if text_lines and text_lines[0].strip().lower() == title.lower():
                    text_lines.pop(0)
                text = '\n'.join(text_lines).strip()
                
            chunk['text'] = text
            
        out_lines.append(json.dumps(chunk, ensure_ascii=False) + '\n')
        
    with open(JSONL_FILE, 'w', encoding='utf-8') as f:
        f.writelines(out_lines)

if __name__ == '__main__':
    update_jsonl()
    print("Done")
