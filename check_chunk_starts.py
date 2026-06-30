import json

filepath = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\TN_Vision_2023(PHASE 1).jsonl'
with open(filepath, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f if line.strip()]

for i in range(5, 14):
    print(f"Chunk {i+1} ({chunks[i]['heading']}) starts: {chunks[i]['text'][:100]}")
