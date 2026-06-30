import json
import fitz
import re

PDF_FILE = r"c:\Users\Akshith Srinivas\chunk-validator-one\assigned pdfs\18. Account Principle Accounting Manual Part__State Audit West Ben.pdf"
JSONL_FILE = r"c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\18. Account Principle Accounting Manual Part__State Audit West Ben.jsonl"

def normalize(text):
    # Remove non-alphanumeric characters for a robust comparison
    return re.sub(r'[^a-zA-Z0-9]', '', text).lower()

def main():
    # 1. Load JSONL text
    jsonl_text = ""
    chunks = []
    with open(JSONL_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip(): continue
            chunk = json.loads(line)
            chunks.append(chunk)
            jsonl_text += chunk.get("text", "") + " "
            
    # 2. Load PDF text from pages 8 to 21 (as per chunks page numbers)
    doc = fitz.open(PDF_FILE)
    pdf_text = ""
    for i in range(7, 21): # Pages 8 to 21 (0-indexed 7 to 20)
        if i < len(doc):
            pdf_text += doc[i].get_text() + " "
            
    norm_jsonl = normalize(jsonl_text)
    norm_pdf = normalize(pdf_text)
    
    print(f"JSONL Normalized Length: {len(norm_jsonl)}")
    print(f"PDF Normalized Length: {len(norm_pdf)}")
    
    # 3. Check if all chunks are in the PDF
    for i, chunk in enumerate(chunks):
        c_norm = normalize(chunk.get("text", ""))
        if c_norm not in norm_pdf:
            print(f"[!] INCONSISTENCY: Chunk {i} ({chunk['heading']}) not found in PDF.")
            # Let's find how much matched
            matched_len = 0
            for j in range(10, len(c_norm), 10):
                if c_norm[:j] in norm_pdf:
                    matched_len = j
                else:
                    break
            print(f"    Matched only up to {matched_len} characters out of {len(c_norm)}.")
        else:
            print(f"[OK] Chunk {i} ({chunk['heading']}) perfectly matches PDF content.")
            
    # 4. Rough check for missing large chunks in JSONL
    # We can slide a window over PDF text and see if it's in JSONL
    missing_from_jsonl = []
    window = 100
    for i in range(0, len(norm_pdf) - window, window):
        segment = norm_pdf[i:i+window]
        if segment not in norm_jsonl:
            missing_from_jsonl.append(segment)
            
    print(f"\nFound {len(missing_from_jsonl)} window segments (100 chars each) in PDF that are NOT in JSONL.")
    if missing_from_jsonl:
        print("Example missing segment:", missing_from_jsonl[0])

if __name__ == "__main__":
    main()
