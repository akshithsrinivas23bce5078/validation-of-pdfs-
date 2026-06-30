import json
import re

file_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'
lines = open(file_path, 'r', encoding='utf-8').readlines()
for i in range(len(lines)-1):
    d1 = json.loads(lines[i])
    d2 = json.loads(lines[i+1])
    t1 = d1.get('text', '').strip()
    t2 = d2.get('text', '').strip()
    if t1 and t2:
        # Check if t1 ends in a letter or comma
        if re.search(r'[a-zA-Z,]$', t1):
            # Check if t2 starts with a lower case letter
            if re.search(r'^[a-z]', t2):
                # Exclude roman numerals like 'i)', 'v.', 'a.', etc which usually mean list item
                if not re.search(r'^(i|ii|iii|iv|v|vi|vii|viii|ix|x|a|b|c|d|e)\b', t2):
                    print(f"Para {d1.get('para')} ends: '{t1[-40:]}'")
                    print(f"Para {d2.get('para')} starts: '{t2[:40]}'")
                    print("---")
