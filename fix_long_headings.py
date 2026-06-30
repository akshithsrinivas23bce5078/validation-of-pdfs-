import json
import re

original_titles = {}
with open(r'unvalidated chunks\Secretariat_Office_Manual_chunks.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        c = json.loads(line)
        para_no = c.get('para_no', '').strip()
        para_title = c.get('para_title', '').strip()
        if para_no:
            if para_no not in original_titles or len(para_title) < len(original_titles[para_no]):
                original_titles[para_no] = para_title

with open(r'chunks after validation\The Secretariat Office Manual.jsonl', 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

for c in chunks:
    h = c.get('heading', '').strip()
    if len(h.split()) > 10:
        m = re.match(r'^(\*?\d{1,3})\.', h)
        if m:
            num = m.group(1).replace('*', '')
            num_with_star = m.group(1)
            
            orig_title = original_titles.get(num, '')
            
            if not orig_title or len(orig_title.split()) > 7:
                new_h = f'{num_with_star}.'
            else:
                new_h = f'{num_with_star}. {orig_title}'
                if not new_h.endswith('.'):
                    new_h += '.'
            
            residual = h
            residual = re.sub(r'^\*?\d{1,3}\.\s*', '', residual)
            if orig_title and len(orig_title.split()) <= 7:
                clean_orig = re.sub(r'[^\w\s]', '', orig_title).lower()
                words_orig = clean_orig.split()
                if words_orig:
                    residual_words = residual.split()
                    residual = ' '.join(residual_words[len(words_orig):])
            
            # Clean up residual
            residual = residual.strip()
            if residual.endswith('\ufffd'):
                residual = residual[:-1].strip()
            if residual.endswith('.—'):
                residual = residual[:-2].strip()
            
            # Update chunk
            c['heading'] = new_h
            if residual:
                c['text'] = residual + ' ' + c.get('text', '')

with open(r'chunks after validation\The Secretariat Office Manual.jsonl', 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

print("Successfully updated long headings.")
