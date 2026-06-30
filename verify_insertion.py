import json
filepath = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\TN_Vision_2023(PHASE 1).jsonl'
with open(filepath, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f if line.strip()]

print(f"Index 0: {chunks[0]['heading']}")
print(f"Index 1: {chunks[1]['heading']}")
print(chunks[1]['text'])
print(f"Index 2: {chunks[2]['heading']}")
