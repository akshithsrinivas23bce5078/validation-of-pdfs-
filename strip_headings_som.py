import json
import re

val_file = r"chunks after validation\SECRETARIAT_OFFICE_MANUAL_validated.jsonl"

with open(val_file, "r", encoding="utf-8") as f:
    chunks = [json.loads(l) for l in f]

count = 0
for c in chunks:
    heading = c.get('heading', '').strip()
    text = c.get('text', '').strip()
    
    if heading and heading != " ":
        if text.startswith(heading):
            text = text[len(heading):]
            # Strip common punctuation that follows a heading: space, dot, em-dash, hyphen
            text = text.lstrip(' .\t-\u2014\u2015\u2013_')
            c['text'] = text
            count += 1
            
with open(val_file, "w", encoding="utf-8") as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + "\n")

print(f"Stripped headings from {count} chunks.")
