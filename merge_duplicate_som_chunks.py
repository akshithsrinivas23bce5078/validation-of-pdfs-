import json

jsonl_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\The Secretariat Office Manual.jsonl'
output_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\The Secretariat Office Manual_merged.jsonl'

with open(jsonl_path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

merged_chunks = []

for c in chunks:
    if not merged_chunks:
        merged_chunks.append(c)
        continue
    
    prev = merged_chunks[-1]
    
    # Check if heading is exactly the same
    if c.get('heading') == prev.get('heading'):
        # We need to merge c into prev
        text_prev = prev.get('text', '').strip()
        text_curr = c.get('text', '').strip()
        
        # Deduplication logic:
        # Check if text_prev is a prefix or substring of text_curr
        if text_prev in text_curr:
            # Just use text_curr
            merged_text = text_curr
        elif text_curr in text_prev:
            # Just use text_prev
            merged_text = text_prev
        else:
            # They might be different parts of the same section, concatenate them
            # Let's check for overlapping suffix/prefix
            overlap_len = 0
            for i in range(1, min(len(text_prev), len(text_curr)) + 1):
                if text_prev.endswith(text_curr[:i]):
                    overlap_len = i
            
            if overlap_len > 0:
                merged_text = text_prev + " " + text_curr[overlap_len:].strip()
            else:
                merged_text = text_prev + " " + text_curr
        
        prev['text'] = merged_text
        
        # Also merge tables if any
        if c.get('has_table'):
            prev['has_table'] = True
            # Assuming prev table_html might be empty
            if prev.get('table_html', '{}') == '{}':
                prev['table_html'] = c.get('table_html', '{}')
            else:
                # If both have tables, just append them (rare case)
                if c.get('table_html', '{}') != '{}' and c.get('table_html') not in prev.get('table_html', ''):
                    # We can't really merge JSON html safely without a parser, but let's just use string concat for now
                    pass 
    else:
        merged_chunks.append(c)

print(f"Original chunks: {len(chunks)}")
print(f"Merged chunks: {len(merged_chunks)}")

with open(output_path, 'w', encoding='utf-8') as f:
    for c in merged_chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')
