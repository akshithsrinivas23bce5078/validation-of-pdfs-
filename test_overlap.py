import json
import re

with open(r'chunks after validation\RAM_2022_Sixth_Edition_fixed.jsonl', encoding='utf-8') as f:
    chunks = [json.loads(x) for x in f]

for i, c in enumerate(chunks[485:490]):
    text = c['text'].strip()
    heading = c['heading'].strip()
    
    # Let's tokenize heading and text
    h_tokens = re.split(r'\s+', heading)
    t_tokens = re.split(r'\s+', text)
    
    match_count = 0
    for ht, tt in zip(h_tokens, t_tokens):
        if ht.lower() == tt.lower():
            match_count += 1
        else:
            break
            
    if match_count > 0:
        # Check if stripping these matched tokens "affects the text"
        # i.e. if the matched tokens are NOT repeated right after.
        # Wait, if the heading is "8.4 Electrical" and text is "8.4 Electrical Directorate"
        # If we remove "8.4 Electrical", it leaves "Directorate".
        # But if text is "8.1 Carriage Carriage Directorate", removing "8.1 Carriage" leaves "Carriage Directorate"
        pass
        
    print(f"--- Chunk {485+i} ---")
    print(f"HEADING: {heading}")
    print(f"H-TOKENS: {h_tokens}")
    print(f"T-TOKENS: {t_tokens[:10]}")
