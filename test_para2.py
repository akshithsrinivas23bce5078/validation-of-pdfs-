import fitz
import re

doc = fitz.open(r'c:\Users\Akshith Srinivas\chunk-validator-one\assigned pdfs\Local Fund Audit Depart Manual  Vol - II.pdf')
text = ""
for page in doc[78:82]:
    text += page.get_text() + "\n"

search_window = text.lower()
title = "Classification of municipalities"
para_num = "2"

def build_regex(text):
    words = [re.escape(w) for w in re.split(r'\W+', text.strip()) if w]
    return r'\W+'.join(words)

pattern_str = build_regex(f"{para_num}. {title}".lower())
print("Regex pattern:", pattern_str)

m = re.search(pattern_str, search_window)
if m:
    print("Found exact_title at:", m.start())
else:
    print("Not found exactly.")
    m = re.search(build_regex(title.lower()), search_window)
    if m:
        print("Found just title at:", m.start())
    else:
        print("Not found just title.")
