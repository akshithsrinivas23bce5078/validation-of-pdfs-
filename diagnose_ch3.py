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

# Show all Chapter 3 chunks and what the PDF actually says for each heading
ch3_chunks = [(i, c) for i, c in enumerate(val_chunks) if str(c['chapter']) == '3']

# For each chunk, find the ACTUAL heading in the PDF using BOTH number AND title keyword
print("=== DIAGNOSTIC: Finding correct anchor for each Chapter 3 Para ===\n")

for idx, (i, c) in enumerate(ch3_chunks):
    para = c['para']
    heading = c['heading']
    # Extract the title part after the dash
    if '-' in heading:
        title_part = heading.split('-', 1)[1].strip()
    else:
        title_part = heading
    
    # Get first 2 significant words from the title
    words = [w for w in re.split(r'\W+', title_part) if len(w) >= 3]
    
    current_start = c['text'][:60]
    
    # Search in PDF for "para_num" followed by title words (with newlines allowed)
    if words:
        first_word = re.escape(words[0])
        # Pattern: number + (dot/space) + up to 200 chars + first significant title word
        pattern = re.escape(str(para)) + r'\b[\.\-\)\s](?:.|\n){0,200}?' + first_word
        matches = list(re.finditer(pattern, ch3_text, re.IGNORECASE))
        
        if matches:
            for m in matches:
                context = ch3_text[m.start():m.start()+80].replace('\n', ' ')
                print(f"Para {para}: MATCH at pos {m.start()}: {context}")
        else:
            print(f"Para {para}: NO MATCH for pattern with word '{words[0]}'")
    
    print(f"  CURRENT chunk starts: {current_start}")
    print()
