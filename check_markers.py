import json

filepath = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\TN_Vision_2023(PHASE 1).jsonl'
with open(filepath, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f if line.strip()]

combined_text = ' '.join([c['text'] for c in chunks[5:14]])

markers = [
    'SMEs play a vital role in any economy',
    'The high levels of growth envisaged by Vision 2023 call for high growth rates',
    'While Vision 2023 articulates all round growth',
    'The single most important resource for the success of Vision 2023 would be the availability of trained',
    'Agriculture and allied activities provide subsistence',
    'Tamil Nadu is already the most urbanised state',
    'Vision 2023 targets an ambitious growth path and will deliver benefits',
    'Vision 2023 envisages the development of eleven marquee projects',
    'As observed in the section on fiscal strategy'
]

for m in markers:
    idx = combined_text.find(m)
    if idx == -1:
        print(f"NOT FOUND: {m}")
    else:
        print(f"Found: {m[:30]}... at {idx}")
