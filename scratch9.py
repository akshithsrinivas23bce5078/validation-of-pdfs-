import json
import re

file_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'

for line in open(file_path, 'r', encoding='utf-8'):
    data = json.loads(line)
    text = data.get('text', '')
    p = data.get('para', 0)
    
    # Text starting with lowercase letter (excluding i., v., etc.)
    # or starting with a word that ends in ')'
    if text:
        first_word = text.split()[0]
        if first_word.islower() and not re.match(r'^[ivxlcdm]+\.$', first_word) and not text.startswith('a.'):
            print(f"Para {p}: Heading={data.get('heading')} | TextStart={text[:60]}")
        elif ')' in first_word and not text.startswith('a)'):
            print(f"Para {p}: Heading={data.get('heading')} | TextStart={text[:60]}")
