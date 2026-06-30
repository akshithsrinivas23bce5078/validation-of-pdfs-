import json
import re

file_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(len(lines)):
    data = json.loads(lines[i])
    t = data.get('text', '').strip()
    h = data.get('heading', '')
    p = data.get('para', 0)
    
    # Check if text starts with uppercase words followed by a colon or semicolon or hyphen
    m = re.match(r'^([A-Z0-9\s,\'\(\)&]+(?:;-|:-|:|;|-|_))\s*(.*)', t)
    if m:
        # Check if it looks like a continuation of the heading
        # Mostly if it's all uppercase and relatively short
        continuation = m.group(1).strip()
        rest_of_text = m.group(2).strip()
        if len(continuation) > 2 and continuation.isupper() or ';- ' in t[:50] or ':- ' in t[:50]:
            print(f"Para {p} heading: {h}")
            print(f"Para {p} text starts with: {t[:80]}")
            print(f"  --> Potential continuation: {continuation}")
            print()
