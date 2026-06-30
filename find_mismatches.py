import json
import re
import fitz

val_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'
with open(val_path, 'r', encoding='utf-8') as f:
    val_chunks = [json.loads(line) for line in f]

doc = fitz.open(r'c:\Users\Akshith Srinivas\chunk-validator-one\assigned pdfs\Local Fund Audit Depart Manual  Vol - II.pdf')

# Build giant text for Chapter 3
ch3_text = ""
page_starts = {}
for p in range(323, 400):
    if p - 1 < len(doc):
        page_starts[p] = len(ch3_text)
        ch3_text += " " + doc[p-1].get_text()

ch3_chunks = [(i, c) for i, c in enumerate(val_chunks) if str(c['chapter']) == '3']

# For EVERY chunk, check if the text it currently has actually starts
# with the correct heading by checking the first few words match the title
print("=== MISMATCHED CHUNKS ===\n")
for idx, (i, c) in enumerate(ch3_chunks):
    para = c['para']
    heading = c['heading']
    text = c['text']
    
    if '-' in heading:
        title_part = heading.split('-', 1)[1].strip()
    else:
        title_part = heading
    
    # Get first significant word from title
    words = [w for w in re.split(r'\W+', title_part) if len(w) >= 4]
    
    # Check if the text starts reasonably (para number + title word in first 80 chars)
    first_80 = text[:80].upper()
    title_word_found = any(w.upper() in first_80 for w in words[:2]) if words else True
    para_num_found = re.match(r'\s*' + re.escape(str(para)) + r'\b', text)
    
    if not title_word_found or not para_num_found:
        print(f"MISMATCH Para {para} [{heading}]")
        print(f"  Chunk starts: {text[:80]}")
        print(f"  Expected title words: {words[:3]}")
        print()
