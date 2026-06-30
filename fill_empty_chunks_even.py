import json
import re

path = r'chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'
with open(path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

def clean_text(t):
    return re.sub(r'\s+', ' ', t).strip()

# Pass 1: Find blocks of empty chunks
i = 0
while i < len(chunks):
    if not chunks[i].get('text', '').strip():
        # Find start of the block (the last non-empty chunk)
        prev_idx = i - 1
        while prev_idx >= 0 and not chunks[prev_idx].get('text', '').strip():
            prev_idx -= 1
            
        # Find end of the block
        end_idx = i
        while end_idx < len(chunks) and not chunks[end_idx].get('text', '').strip():
            end_idx += 1
            
        source_idx = -1
        if prev_idx >= 0:
            source_idx = prev_idx
            num_chunks_to_fill = end_idx - prev_idx
        elif end_idx < len(chunks):
            source_idx = end_idx
            num_chunks_to_fill = end_idx - prev_idx
        
        if source_idx != -1:
            trapped_text = chunks[source_idx]['text']
            
            words = trapped_text.split()
            words_per_chunk = max(1, len(words) // num_chunks_to_fill)
            
            # Start distributing from prev_idx + 1 up to end_idx (inclusive if source_idx == end_idx?)
            start_dist = prev_idx + 1 if prev_idx >= 0 else 0
            end_dist = end_idx if prev_idx >= 0 else end_idx + 1
            
            for j, target_idx in enumerate(range(start_dist, end_dist)):
                start_w = j * words_per_chunk
                end_w = (j + 1) * words_per_chunk if j < num_chunks_to_fill - 1 else len(words)
                
                chunk_text = ' '.join(words[start_w:end_w])
                chunks[target_idx]['text'] = clean_text(chunk_text)
                
        i = end_idx
    else:
        i += 1

# Verify
empty_count = sum(1 for c in chunks if not c.get('text', '').strip())
print(f"Empty chunks remaining: {empty_count}")

with open(path, 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')
