import json
import re

val_file = r'chunks after validation\The Secretariat Office Manual.jsonl'

with open(val_file, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

for c in chunks:
    h = c.get('heading', '').strip()
    t = c.get('text', '').strip()
    
    # We want to catch titles that were leaked into text.
    # Usually they end with .— or .\ufffd or .-
    # The heading must NOT already end with one of these.
    if not (h.endswith('\ufffd') or h.endswith('—') or h.endswith('.-') or h.endswith('Deleted)') or h.endswith('Deleted.')):
        # Check if the text starts with a title-like string ending in .\ufffd or .— or .-
        m = re.match(r'^(.*?(\.—|\.\ufffd|\.-))(?:\s+|$)(.*)', t, flags=re.DOTALL)
        if m:
            leaked = m.group(1).strip()
            rest_of_text = m.group(3).strip()
            # To avoid capturing huge paragraphs, check if length is reasonable and no newline
            if len(leaked.split()) < 30 and '\n' not in leaked:
                # Append leaked to heading, and update text
                c['heading'] = h + ' ' + leaked
                c['text'] = rest_of_text

with open(val_file, 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

print("Successfully merged leaked titles into headings.")
