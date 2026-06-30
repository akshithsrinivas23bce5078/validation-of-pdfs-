import json
import re

val_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'
with open(val_path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

text = open('ch1_pages.txt','r',encoding='utf-8').read()
m_start = re.search(r'(?m)^Para\s*\.\s*4\s*:\s*AUDIT\s+FUNCTIONS\s+OF', text)
m_end = re.search(r'in ADs office\.\s*', text[m_start.start():])

extracted_text = text[m_start.start():m_start.start()+m_end.end()]

def clean_text(t):
    return re.sub(r'\s+', ' ', t).strip()

new_text = clean_text(extracted_text)

for c in chunks:
    if str(c['chapter']) == '1' and c['para'] == 4:
        c['text'] = new_text
        break

with open(val_path, 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

print("Para 4 in Chapter 1 updated.")
