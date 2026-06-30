import json
import re
import os

FILE_PATH = r'chunks after validation\20. Chart of Account Accounting Manual Part_4_State Audit West Ben.jsonl'
TEMP_PATH = r'chunks after validation\20__temp.jsonl'

with open(FILE_PATH, encoding='utf-8') as f:
    chunks = [json.loads(x) for x in f]

chapter_titles = {
    1: "Introduction",
    2: "Objective",
    3: "Structure of Function Code",
    4: "Structure of the Functionary Code",
    5: "Structure of the Field Code",
    6: "Structure of the Fund Code",
    7: "Structure of Accounting Code",
    8: "Identification Code for ULB",
    9: "Procedure for the Change in the Chart of Accounts",
    10: "Format for Change Request Form",
    11: "Format for Change Authorised Form"
}

# 1. Clean trailing titles and move any extra text to the next chunk
for i in range(len(chunks) - 1):
    text = chunks[i].get('text', '')
    # Match "\s+<Number>.\s+<Title Text>(?:\s+.*)?$"
    match = re.search(r'\s+(\d+)\.\s+([A-Za-z\s]+)$', text, re.IGNORECASE)
    if match:
        ch_num = int(match.group(1))
        title_matched = match.group(2).strip()
        
        # We know from check_trailing_titles.py what they look like.
        # Let's do a safe string replace.
        # We'll just replace the matched text with empty string.
        # But wait, we saw "7. STRUCTURE OF ACCOUNTING CODE Primary Accounting Code"
        # We can split it based on the known title.
        
        # Let's do a specific replace for known trailing texts to avoid bugs.
        trailing_strings = [
            "2. OBJECTIVE",
            "3. STRUCTURE OF FUNCTION CODE",
            "5. STRUCTURE OF THE FIELD CODE",
            "6. STRUCTURE OF THE FUND CODE",
            "7. STRUCTURE OF ACCOUNTING CODE Primary Accounting Code",
            "8. IDENTIFICATION CODE FOR ULB",
            "9. PROCEDURE FOR THE CHANGE IN THE CHART OF ACCOUNTS Function Code",
            "10. FORMAT FOR CHANGE REQUEST FORM",
            "11. FORMAT FOR CHANGE AUTHORISED FORM"
        ]
        
        for ts in trailing_strings:
            if text.endswith(ts):
                chunks[i]['text'] = text[:-len(ts)].strip()
                # If there are extra words like "Primary Accounting Code", prepend them to next chunk
                if ts == "7. STRUCTURE OF ACCOUNTING CODE Primary Accounting Code":
                    chunks[i+1]['text'] = "Primary Accounting Code " + chunks[i+1]['text']
                elif ts == "9. PROCEDURE FOR THE CHANGE IN THE CHART OF ACCOUNTS Function Code":
                    chunks[i+1]['text'] = "Function Code " + chunks[i+1]['text']
                break

# 2. Insert new chapter title chunks
new_chunks = []
inserted_chapters = set()

for c in chunks:
    ch = int(c.get('chapter', '0'))
    if ch in chapter_titles and ch not in inserted_chapters:
        # Create a new chunk
        new_c = c.copy()
        new_c['heading'] = str(ch)
        new_c['text'] = chapter_titles[ch]
        new_c['has_table'] = False
        new_c['table_html'] = {}
        new_chunks.append(new_c)
        inserted_chapters.add(ch)
    
    new_chunks.append(c)

with open(TEMP_PATH, 'w', encoding='utf-8') as f:
    for c in new_chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

os.replace(TEMP_PATH, FILE_PATH)
print("Applied chapter headings and cleaned trailing texts successfully.")
