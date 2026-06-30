import json
import re

val_file = r'chunks after validation\The Secretariat Office Manual.jsonl'

with open(val_file, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

for c in chunks:
    # If the heading is missing/blank, we extract it from the text
    if c.get('heading', '').strip() == '':
        text = c.get('text', '')
        
        # Try to match Number. Title.— or Number. Title.
        # We look for:
        # ^(\*?\d{1,3}\.(?:\(\w+\))?  => start with number, optional asterisk, optional letter in parens e.g. 36.(a)
        # \s+.*?                      => some text (the title)
        # (?:\.—|\.|\.-|\.\s))        => ending with .— or .- or . or . followed by space
        # \s*(.*)                     => the rest of the text
        m = re.match(r'^(\*?\d{1,3}\.(?:\(\w+\))?\s+.*?(?:\.—|\.|\.-|(?<=\w)\.\s))\s*(.*)', text, flags=re.DOTALL)
        
        if m:
            c['heading'] = m.group(1).strip()
            c['text'] = m.group(2).strip()
        else:
            # Fallback: if there is no title, just extract the number
            m2 = re.match(r'^(\*?\d{1,3}\.(?:\(\w+\))?)\s*(.*)', text, flags=re.DOTALL)
            if m2:
                c['heading'] = m2.group(1).strip()
                c['text'] = m2.group(2).strip()

with open(val_file, 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

print("Successfully extracted headings from text for all chunks.")
