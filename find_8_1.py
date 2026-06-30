import json
with open(r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\RAM_2022_Sixth_Edition.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        c = json.loads(line)
        text = c.get('text', '')
        if '8.1 ' in text and '8.2 ' in text:
            print(f"Chunk Title: {c.get('title')}, Heading: {c.get('heading')}, Text len: {len(text)}")
