import json
import re
import sys
import os

def merge_page_nos(p1, p2):
    if not p1: return p2
    if not p2: return p1
    n1 = [int(x) for x in re.findall(r'\d+', p1)]
    n2 = [int(x) for x in re.findall(r'\d+', p2)]
    all_n = n1 + n2
    if not all_n: return p1
    return f"({min(all_n)}-{max(all_n)})"

def merge_table_html(t1, t2):
    res = dict(t1)
    res.update(t2)
    return res

def process_file(input_path):
    print(f"Processing: {input_path}")
    
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    merged_chunks = []
    current_chunk = None
    
    for line in lines:
        if not line.strip(): continue
        chunk = json.loads(line)
        if current_chunk is None:
            current_chunk = chunk
        else:
            # Identify if chapter and heading match exactly
            if current_chunk.get('chapter') == chunk.get('chapter') and \
               current_chunk.get('heading') == chunk.get('heading'):
                
                # Merge texts
                text1 = current_chunk.get('text', '').strip()
                text2 = chunk.get('text', '').strip()
                if text1 and text2:
                    current_chunk['text'] = text1 + '\n\n' + text2
                else:
                    current_chunk['text'] = text1 or text2
                
                # Merge page numbers
                current_chunk['page.no'] = merge_page_nos(current_chunk.get('page.no', ''), chunk.get('page.no', ''))
                
                # Merge tables
                current_chunk['has_table'] = current_chunk.get('has_table', False) or chunk.get('has_table', False)
                current_chunk['table_html'] = merge_table_html(current_chunk.get('table_html', {}), chunk.get('table_html', {}))
            else:
                merged_chunks.append(current_chunk)
                current_chunk = chunk

    if current_chunk is not None:
        merged_chunks.append(current_chunk)
        
    # Write back to the same file
    with open(input_path, 'w', encoding='utf-8') as f:
        for c in merged_chunks:
            f.write(json.dumps(c) + '\n')
            
    print(f"Reduced from {len(lines)} chunks to {len(merged_chunks)} chunks.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        for p in sys.argv[1:]:
            process_file(p)
    else:
        print("Please provide a file path.")
