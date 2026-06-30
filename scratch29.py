import json

file_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'
subject_paras = {23, 43, 44, 77, 131, 5, 16, 20, 60, 4, 8, 64, 71, 72, 76, 91, 110, 61, 62, 51, 27, 11, 33}

with open(file_path, 'r', encoding='utf-8') as f:
    for line in f:
        d = json.loads(line)
        t = d.get('text', '').strip()
        p = d.get('para', 0)
        h = d.get('heading', '')
        
        if p not in subject_paras and t:
            words = t.split()
            first_word = words[0] if words else ''
            
            # Check if text starts with lower case or specific verbs
            if first_word.islower() or first_word in ['is', 'are', 'may', 'can', 'should', 'has', 'have']:
                print(f"Para {p} ({h}) -> {t[:50]}")
