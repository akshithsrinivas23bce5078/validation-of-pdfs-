import json
import re

file_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(len(lines)):
    data = json.loads(lines[i])
    t = data.get('text', '').strip()
    h = data.get('heading', '')
    
    # Extract the heading text without 'Para n - '
    heading_text = ''
    m = re.search(r'Para \d+\s*-\s*(.+)', h)
    if m:
        heading_text = m.group(1).strip()
    
    # Check if text starts with lower case or 'is ', 'are ', 'which ', 'shall ', 'may ' etc.
    # Actually, any text starting with a lowercase letter is likely a continuation of the heading.
    if re.search(r'^[a-z]', t) or t.startswith('is ') or t.startswith('are ') or t.startswith('shall '):
        # Avoid list items like 'a.', 'i.', 'v.' etc.
        if not re.search(r'^(i|ii|iii|iv|v|vi|vii|viii|ix|x|a|b|c|d)\b[\.\)]', t, re.IGNORECASE):
            print(f"Para {data.get('para')} heading: {heading_text}")
            print(f"Para {data.get('para')} text: '{t[:60]}...'")
            print(f"Suggested fix: {heading_text} {t[:60]}...")
            print()
