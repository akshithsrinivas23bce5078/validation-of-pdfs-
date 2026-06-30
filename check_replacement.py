import json
filepath = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\TN_Vision_2023(PHASE 1).jsonl'
with open(filepath, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f if line.strip()]

for i in range(3):
    text = chunks[i]['text']
    idx = text.find('')
    if idx != -1:
        print(f"Chunk {i}: ...{text[max(0, idx-20):idx+20]}...")
