import json

filepath = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\TN_Vision_2023(PHASE 1).jsonl'
with open(filepath, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f if line.strip()]

print(f"Index 0: {chunks[0]['heading']} (Page {chunks[0].get('page.no', 'N/A')})")
print(f"Index 1: {chunks[1]['heading']} (Page {chunks[1].get('page.no', 'N/A')})")
