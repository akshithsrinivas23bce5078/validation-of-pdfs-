import json
import re

with open(r'chunks after validation\The Secretariat Office Manual.jsonl', 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

# ── Fix 1: Chunk 31 (index 30) ─────────────────────────────────────────────
# heading = '31. Deleted (vide G.'   text = 'O.(Ms) No.36 ...'
# The heading got split mid-word at 'G.' + 'O.' across heading/text boundary
c30 = chunks[30]
full_deleted = c30['heading'].replace('31. ', '') + c30['text']
c30['heading'] = '31.'
c30['text'] = full_deleted.strip()
print('CHUNK 30 fixed:')
print('  heading:', c30['heading'])
print('  text:', c30['text'])

# ── Fix 2: Add .— to all headings ──────────────────────────────────────────
for c in chunks:
    h = c.get('heading', '').strip()
    if not h:
        continue

    # Skip Omitted / Deleted entries – they already have a note in the heading
    if 'Omitted' in h or 'Deleted' in h:
        continue

    # Already ends with .— → leave it
    if h.endswith('.—') or h.endswith('.\u2014'):
        continue

    # Ends with just a period → replace with .—
    if h.endswith('.'):
        h = h[:-1] + '.—'
    # Ends with nothing meaningful → just append .—
    else:
        h = h + '.—'

    c['heading'] = h

with open(r'chunks after validation\The Secretariat Office Manual.jsonl', 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

print('\nDone. .— appended to all headings and chunk 31 fixed.')
