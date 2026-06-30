import json

file_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'
lines = open(file_path, 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines):
    d = json.loads(line)
    t = d.get('text', '').strip()
    if t and not t.endswith('.') and not t.endswith(')') and not t.endswith(':') and not t.endswith('-'):
        if t[-1].isalpha() or t[-1] == ',' or t[-1].isdigit():
            print(f"Para {d.get('para')} (line {i}): {repr(t[-80:])}")
