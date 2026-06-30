import json
import re

jsonl_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\18. Account Principle Accounting Manual Part__State Audit West Ben.jsonl'
output_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\18. Account Principle Accounting Manual Part__State Audit West Ben_split.jsonl'

with open(jsonl_path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

new_chunks = []
for c in chunks:
    if c.get('chapter') == '2':
        text = c.get('text', '')
        # Split text by 2.1, 2.2... 
        # Using regex to find all matches of 2.X followed by space
        # We split the string keeping the delimiter
        parts = re.split(r'(2\.[1-8]\s)', text)
        
        # parts will be ['', '2.1 ', 'This chapter contains...', '2.2 ', 'The Financial Statements...', ...]
        # if there is any leading text before 2.1, it's parts[0]
        # Let's group them
        
        # Reconstruct the chunks
        sub_chunks = []
        current_text = ""
        current_num = ""
        
        for p in parts:
            if re.match(r'^2\.[1-8]\s$', p):
                if current_num:
                    sub_chunks.append((current_num, current_text.strip()))
                current_num = p.strip()
                current_text = p
            else:
                current_text += p
        
        if current_num:
            sub_chunks.append((current_num, current_text.strip()))
            
        for num, sub_text in sub_chunks:
            new_c = c.copy()
            new_c['heading'] = f"{num} INTRODUCTION"
            new_c['text'] = sub_text
            new_chunks.append(new_c)
            
    else:
        new_chunks.append(c)

with open(output_path, 'w', encoding='utf-8') as f:
    for c in new_chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

print(f"Split chapter 2 into {len(new_chunks) - len(chunks) + 1} chunks.")
