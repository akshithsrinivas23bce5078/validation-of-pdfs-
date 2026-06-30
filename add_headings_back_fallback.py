import json
import re

val_file = r"chunks after validation\SECRETARIAT_OFFICE_MANUAL_validated.jsonl"
with open(val_file, "r", encoding="utf-8") as f:
    val_chunks = [json.loads(line) for line in f if line.strip()]

fixed_count = 0
for c in val_chunks:
    h = c.get('heading', '').strip()
    if h and h != "null" and h != " ":
        # It's a bold heading chunk! The text should start with the heading or the paragraph number.
        t = c.get('text', '').strip()
        m_h = re.match(r'^(\d{1,3})', h)
        m_t = re.match(r'^(\d{1,3})', t)
        
        if m_h:
            num = m_h.group(1)
            # Check if t already starts with the number
            if not m_t or m_t.group(1) != num:
                # Need to prepend the heading
                # Let's check how it ended. If it ends with '.', we add '— ' or space
                # Actually, the user's example "575. Sanction of Loans and Advances.— "
                # We can just check the original text from unvalidated if we want the exact punctuation
                prefix = f"{h}.\u2014 " if not h.endswith(".") else f"{h}\u2014 "
                
                # Check if t already starts with a dash
                if t.startswith("— ") or t.startswith("- "):
                    t = t[2:].strip()
                elif t.startswith("—") or t.startswith("-"):
                    t = t[1:].strip()
                    
                c['text'] = prefix + t
                fixed_count += 1

with open(val_file, "w", encoding="utf-8") as f:
    for c in val_chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

print(f"Prepended heading to {fixed_count} chunks.")
