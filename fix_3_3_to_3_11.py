import json

filepath = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\TN_Vision_2023(PHASE 1).jsonl'
with open(filepath, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f if line.strip()]

# Combine texts of chunks 5 to 13 (which map to 3.3 through 3.11)
combined_text = ' '.join([c['text'] for c in chunks[5:14]])

markers = [
    'SMEs play a vital role in any economy',
    'The high levels of growth envisaged by Vision 2023 call for',
    'The success of the Vision is incumbent upon adopting',
    'The single most important resource for the success',
    'Tamil Nadu is richly endowed with fertile lands',
    'Tamil Nadu is already the most urbanised state',
    'Vision 2023 targets an ambitious growth path and',
    'Vision 2023 envisages the development of eleven',
    'As observed in the section on fiscal strategy'
]

indices = [combined_text.find(m) for m in markers]
indices.append(len(combined_text))

for i in range(9):
    start = indices[i]
    end = indices[i+1]
    text_segment = combined_text[start:end].strip()
    
    # Assign the correctly split text to the chunk
    chunk_idx = 5 + i
    chunks[chunk_idx]['text'] = text_segment

with open(filepath, 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=True) + "\n")

print("Successfully reassigned text for chunks 3.3 through 3.11 based on exact paragraph markers!")
