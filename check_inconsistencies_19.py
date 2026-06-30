import json
import fitz
import re

PDF_FILE = r"c:\Users\Akshith Srinivas\chunk-validator-one\assigned pdfs\19. Opening Balance Sheet Accounting Manual P_State Audit West Ben.pdf"
JSONL_FILE = r"c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\19__Opening_Balance_Sheet_Accounting_Manual_P_State_Audit_West_Ben.jsonl"

def normalize(text):
    return re.sub(r'[^a-zA-Z0-9]', '', text).lower()

def main():
    jsonl_text = ""
    chunks = []
    with open(JSONL_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip(): continue
            chunk = json.loads(line)
            chunks.append(chunk)
            jsonl_text += chunk.get("text", "") + " "
            
    doc = fitz.open(PDF_FILE)
    pdf_text = ""
    # According to JSONL page numbers, content is roughly on pages 8 to 26
    for i in range(7, 26):
        if i < len(doc):
            pdf_text += doc[i].get_text() + " "
            
    norm_jsonl = normalize(jsonl_text)
    norm_pdf = normalize(pdf_text)
    
    missing_from_jsonl = []
    window = 100
    for i in range(0, len(norm_pdf) - window, window):
        segment = norm_pdf[i:i+window]
        if segment not in norm_jsonl:
            missing_from_jsonl.append(segment)
            
    # We expect some mismatches due to Headers/Footers being in PDF but not JSONL
    print(f"Total window segments in PDF: {len(norm_pdf)//window}")
    print(f"Missing in JSONL (mostly headers/footers expected): {len(missing_from_jsonl)}")

if __name__ == "__main__":
    main()
