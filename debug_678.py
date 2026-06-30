import json
import re
import fitz

val_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'
with open(val_path, 'r', encoding='utf-8') as f:
    val_chunks = [json.loads(line) for line in f]

doc = fitz.open(r'c:\Users\Akshith Srinivas\chunk-validator-one\assigned pdfs\Local Fund Audit Depart Manual  Vol - II.pdf')

# Build giant text for Chapter 3
ch3_text = ""
ch3_page_starts = {}
for p in range(323, 400):
    if p - 1 < len(doc):
        ch3_page_starts[p] = len(ch3_text)
        ch3_text += " " + doc[p-1].get_text()

ch3_chunks = [c for c in val_chunks if str(c['chapter']) == '3']

# Debug: try to find Para 6, 7, 8 manually with the strategy
for test_para in [6, 7, 8]:
    vc = [c for c in ch3_chunks if c['para'] == test_para][0]
    if '-' in vc['heading']:
        title_part = vc['heading'].split('-', 1)[1].strip()
    else:
        title_part = vc['heading']
    title_words = [w for w in re.split(r'\W+', title_part) if len(w) >= 4]
    
    print(f"\n=== Para {test_para}: {vc['heading']} ===")
    print(f"Title words: {title_words}")
    
    for tw in title_words[:3]:
        upper_word = tw.upper()
        # Search the ENTIRE chapter 3 text
        pattern = r'(?m)^\s*' + re.escape(str(test_para)) + r'\b[\.\-\)\s][\s\S]{0,30}?' + re.escape(upper_word)
        matches = list(re.finditer(pattern, ch3_text))
        for m in matches:
            matched_text = ch3_text[m.start():m.end()]
            has_upper = upper_word in matched_text
            print(f"  Match at {m.start()}: uppercase={has_upper}: {repr(matched_text[:60])}")
        if not matches:
            print(f"  No matches for '{upper_word}' with 30-char window")
        
        # Try 100 char window
        pattern2 = r'(?m)^\s*' + re.escape(str(test_para)) + r'\b[\.\-\)\s][\s\S]{0,100}?' + re.escape(upper_word)
        matches2 = list(re.finditer(pattern2, ch3_text))
        for m in matches2:
            if m.start() not in [mm.start() for mm in matches]:
                matched_text = ch3_text[m.start():m.end()]
                has_upper = upper_word in matched_text
                print(f"  Match@100 at {m.start()}: uppercase={has_upper}: {repr(matched_text[:60])}")
