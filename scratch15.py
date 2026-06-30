import json

file_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(50, 56):
    data = json.loads(lines[i])
    print(f"--- Chunk {i+1} (Para {data.get('para')}) ---")
    print("Heading:", data.get('heading'))
    t = data.get('text', '')
    print("Starts with:", t[:100])
    print("Ends with:", t[-100:])
    print()
