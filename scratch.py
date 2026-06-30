import json
file_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'
for line in open(file_path, 'r', encoding='utf-8'):
    data = json.loads(line)
    heading = data.get('heading', '')
    if 'Para 1 - ' in heading:
        print(f"Chap {data.get('chapter', '')}: {heading} => {data.get('text', '')[:50]}")
