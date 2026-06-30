import json
import re
import sys
import os

def parse_prefix(s):
    if not s: return []
    # Match numbering like 2, 2.1, 2.1.3
    m = re.match(r'^(\d+(?:\.\d+)*)', s.strip())
    if m:
        return [int(x) for x in m.group(1).split('.')]
    
    s_lower = s.lower()
    if 'annexure' in s_lower or 'appendix' in s_lower:
        return [999999]
    return [-1]

def sort_chunks(input_path):
    print(f"Sorting {os.path.basename(input_path)}...")
    with open(input_path, 'r', encoding='utf-8') as f:
        chunks = [json.loads(line) for line in f if line.strip()]
    
    def sort_key(c):
        ch = c.get('chapter', '')
        try:
            # Extract number from chapter (e.g. "Chapter 22" -> 22)
            ch_num = int(re.search(r'\d+', ch).group()) if re.search(r'\d+', ch) else 9999
        except Exception:
            ch_num = 9999
        
        heading = c.get('heading', '')
        heading_key = parse_prefix(heading)
        
        return (ch_num, heading_key)
        
    chunks.sort(key=sort_key)
    
    with open(input_path, 'w', encoding='utf-8') as f:
        for c in chunks:
            f.write(json.dumps(c) + '\n')
            
    print(f"Sorted {len(chunks)} chunks.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        for p in sys.argv[1:]:
            sort_chunks(p)
