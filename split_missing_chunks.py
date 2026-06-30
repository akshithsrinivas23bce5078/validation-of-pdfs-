import json
import re

val_file = r'chunks after validation\The Secretariat Office Manual.jsonl'

with open(val_file, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

# Helper to find the main section number of a chunk
def get_main_section(c):
    # Try heading first
    m = re.match(r'^\*?(\d+)\.', c.get('heading', '').strip())
    if m:
        return int(m.group(1))
    
    # Try text
    m2 = re.match(r'^\*?(\d+)\.', c.get('text', '').strip())
    if m2:
        return int(m2.group(1))
    
    # Try anywhere in heading
    m3 = re.search(r'\b(\d+)\.', c.get('heading', ''))
    if m3:
        return int(m3.group(1))
    
    return None

new_chunks = []
total_splits = 0

for i, c in enumerate(chunks):
    text = c.get('text', '')
    
    # Find the section number for this chunk
    curr_sec = get_main_section(c)
    
    # Find the section number for the next chunk
    next_sec = None
    for j in range(i + 1, len(chunks)):
        ns = get_main_section(chunks[j])
        if ns is not None:
            next_sec = ns
            break
            
    # We only care if we have a valid curr_sec and next_sec
    if curr_sec is not None and next_sec is not None and next_sec > curr_sec:
        # We look for numbers strictly between curr_sec and next_sec
        expected_missing = set(range(curr_sec + 1, next_sec))
        
        if expected_missing:
            # Let's search the text for these missing numbers
            # A section starts with " N." or "N.(a)" etc.
            
            # We'll build a list of split points
            split_points = []
            
            # Find all potential section markers in the text
            # We look for space or start of string, then digits, then dot, then space or letter or parenthesis
            matches = list(re.finditer(r'(?:^|\s)\*?(\d{1,3})\.(?=[A-Za-z\s(])', text))
            
            for m in matches:
                num = int(m.group(1))
                if num in expected_missing:
                    # We found a missing section embedded in this chunk!
                    split_points.append((m.start(), num))
            
            if split_points:
                # We need to split the chunk!
                # Sort split points
                split_points.sort()
                
                # We will chop up the current chunk's text
                last_idx = 0
                
                # The first part belongs to the original chunk
                first_split_idx = split_points[0][0]
                orig_text = text[:first_split_idx].strip()
                c['text'] = orig_text
                new_chunks.append(c)
                
                # Now create new chunks for each split
                for k, sp in enumerate(split_points):
                    start_idx = sp[0]
                    num = sp[1]
                    
                    if k < len(split_points) - 1:
                        end_idx = split_points[k+1][0]
                    else:
                        end_idx = len(text)
                        
                    section_text = text[start_idx:end_idx].strip()
                    
                    new_chunk = {
                        'DOC_NAME': c['DOC_NAME'],
                        'doc_id': c['doc_id'],
                        'chapter': c['chapter'],
                        'title': c['title'],
                        'heading': ' ', # as per rule for non-bold headings
                        'text': section_text,
                        'page.no': c['page.no'],
                        'has_table': False,
                        'table_html': '{}'
                    }
                    new_chunks.append(new_chunk)
                    total_splits += 1
                    print(f"Extracted Section {num} from Chunk {i} (original {curr_sec})")
                
                continue # Skip the default append since we already appended 'c'
    
    # Default: just append the chunk if no splits happened
    new_chunks.append(c)

print(f"Total embedded sections extracted: {total_splits}")

with open(val_file, 'w', encoding='utf-8') as f:
    for c in new_chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')
