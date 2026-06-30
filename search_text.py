import json

filepath = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\TN_Vision_2023(PHASE 1).jsonl'
with open(filepath, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f if line.strip()]

for i, c in enumerate(chunks):
    text = c['text']
    for keyword in ['Transport', 'Agricult', 'Funding']:
        idx = text.find(keyword)
        if idx != -1:
            snippet = text[max(0, idx-20):min(len(text), idx+20)]
            print(f"Chunk {i+1} ({c['heading']}) snippet: ...{snippet}...")
