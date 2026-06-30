import json
import re

FILE_PATH = r'chunks after validation\19__Opening_Balance_Sheet_Accounting_Manual_P_State_Audit_West_Ben.jsonl'

with open(FILE_PATH, encoding='utf-8') as f:
    chunks = [json.loads(x) for x in f]

errors = []

# 1. Check for null headings or empty text
for i, c in enumerate(chunks):
    if c.get('heading') is None:
        errors.append(f"Chunk {i}: Null heading found.")
    if not c.get('text') or str(c.get('text')).strip() == '':
        errors.append(f"Chunk {i}: Empty text found.")

# 2. Check for headings still present in text
for i, c in enumerate(chunks):
    hd = str(c.get('heading', ''))
    text = str(c.get('text', '')).strip()
    # Check if text starts with the exact heading + dot/space
    if hd and text.startswith(hd):
        # We need to make sure it's actually the heading prefix (e.g. "21." or "21 ")
        rest = text[len(hd):]
        if rest == '' or rest[0] in ['.', ' ', '-']:
            errors.append(f"Chunk {i}: Text still contains heading '{hd}' -> '{text[:30]}'")

# 3. Check chapter/heading sequence
last_ch = 0
for i, c in enumerate(chunks):
    ch_str = c.get('chapter')
    try:
        ch = int(ch_str)
        if ch < last_ch:
            errors.append(f"Chunk {i}: Chapter out of order ({last_ch} -> {ch})")
        last_ch = ch
    except Exception:
        pass

if not errors:
    print("Validation passed! No structural errors found.")
else:
    print(f"Found {len(errors)} errors:")
    for e in errors:
        print(e)
