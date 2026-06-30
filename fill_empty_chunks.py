import json
import re

path = r'chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'
with open(path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

def clean_text(t):
    return re.sub(r'\s+', ' ', t).strip()

def get_significant_words(title):
    words = [w.lower() for w in re.split(r'\W+', title) if len(w) > 3]
    return words

for i in range(len(chunks)):
    c = chunks[i]
    if not c.get('text', '').strip():
        # Find the last non-empty chunk before this
        prev_idx = i - 1
        while prev_idx >= 0 and not chunks[prev_idx].get('text', '').strip():
            prev_idx -= 1
            
        if prev_idx >= 0:
            prev_c = chunks[prev_idx]
            trapped_text = prev_c['text']
            
            # Find how many empty chunks we are trying to fill from this trapped_text
            # It's from prev_idx + 1 to i
            empty_count = i - prev_idx
            
            # We are currently trying to extract for chunk i.
            # But wait, it's better to process them sequentially.
            # If chunk i is empty, we split prev_c['text'] to give chunk i its portion.
            
            title = c['title']
            if '-' in c['heading']:
                title = c['heading'].split('-', 1)[1].strip()
                
            sig_words = get_significant_words(title)
            
            split_idx = -1
            
            # 1. Try exact title match
            t_lower = trapped_text.lower()
            idx = t_lower.find(title.lower())
            if idx != -1:
                split_idx = idx
                
            # 2. Try regex with number
            if split_idx == -1:
                match = re.match(r'Para\s+(\d+)', c['heading'], re.IGNORECASE)
                if match:
                    num = match.group(1)
                    pattern = rf'\b{num}[\.\)\-\s]+([a-zA-Z\s]{{5,30}})'
                    for m in re.finditer(pattern, trapped_text):
                        if not sig_words or any(w in m.group(1).lower() for w in sig_words):
                            split_idx = m.start()
                            break
                            
            # 3. Try to find the first significant word (risky)
            if split_idx == -1 and len(sig_words) >= 2:
                phrase = f"{sig_words[0]} {sig_words[1]}"
                idx = t_lower.find(phrase)
                if idx != -1:
                    split_idx = idx
                    
            # 4. Fallback: split evenly
            if split_idx == -1:
                # We need to leave some text for prev_c and take some for c.
                # If there are N empty chunks, we take 1/(N+1) of the text?
                # Actually, just split the remaining text in half.
                split_idx = len(trapped_text) // 2
                
            # Split the text
            prev_c['text'] = clean_text(trapped_text[:split_idx])
            c['text'] = clean_text(trapped_text[split_idx:])

# Verify
empty_count = sum(1 for c in chunks if not c.get('text', '').strip())
print(f"Empty chunks remaining: {empty_count}")

with open(path, 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')
