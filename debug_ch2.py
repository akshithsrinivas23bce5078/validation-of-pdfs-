import json
import fitz
import re

val_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'
with open(val_path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

doc = fitz.open(r'c:\Users\Akshith Srinivas\chunk-validator-one\assigned pdfs\Local Fund Audit Depart Manual  Vol - II.pdf')

text = ""
for p in range(80, 85):
    text += doc[p-1].get_text() + "\n"

search_window = text.lower()
def build_regex(text):
    words = [re.escape(w) for w in re.split(r'\W+', text.strip()) if w]
    return r'\W+'.join(words)

for c in chunks:
    if str(c.get('chapter')) == '2' and str(c.get('para')) in ['1', '2', '3', '4', '5']:
        para = str(c['para'])
        title = c['title'] if '-' not in c['heading'] else c['heading'].split('-', 1)[1].strip()
        pattern_str = build_regex(f"{para}. {title}".lower())
        m = re.search(pattern_str, search_window)
        if not m:
            m = re.search(build_regex(title.lower()), search_window)
            
        if m:
            print(f"Para {para}: found at {m.start()}")
        else:
            print(f"Para {para}: NOT FOUND")
