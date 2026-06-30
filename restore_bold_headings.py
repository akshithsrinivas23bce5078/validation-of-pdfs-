import json
import re

# Load unvalidated chunks to build a map of para_num -> original heading
unvalidated_file = r"unvalidated chunks\Secretariat_Office_Manual_chunks.jsonl"
orig_headings = {}
with open(unvalidated_file, "r", encoding="utf-8") as f:
    for line in f:
        if not line.strip(): continue
        c = json.loads(line)
        para_no = c.get('para_no', '').strip()
        para_title = c.get('para_title', '').strip()
        
        # para_no looks like "578"
        m = re.match(r'^(\d{1,3})', para_no)
        if m:
            # We want to format the heading like "578. Control."
            if not para_no.endswith('.'):
                para_no += '.'
            h = f"{para_no} {para_title}".strip()
            orig_headings[m.group(1)] = h

# Load para fonts
with open("para_fonts.json", "r") as f:
    fonts = json.load(f)
bold_paras = set(fonts['bold'])
non_bold_paras = set(fonts['non_bold'])

validated_file = r"chunks after validation\SECRETARIAT_OFFICE_MANUAL_validated.jsonl"
with open(validated_file, "r", encoding="utf-8") as f:
    validated_chunks = [json.loads(line) for line in f if line.strip()]

fixed_count = 0
for c in validated_chunks:
    t = c.get('text', '').strip()
    
    # Check if the text starts with a paragraph number
    m = re.match(r'^(\d{1,3})\.', t)
    if m:
        para_num = m.group(1)
        
        if para_num in bold_paras:
            # This is a bold heading! Restore the heading.
            orig_h = orig_headings.get(para_num)
            if orig_h:
                c['heading'] = orig_h
                
                # Now we need to remove the heading from the text if it's there.
                # Let's cleanly strip it
                if t.startswith(f"{orig_h}\u2014 "):
                    c['text'] = t[len(f"{orig_h}\u2014 "):].strip()
                elif t.startswith(f"{orig_h}.\u2014 "):
                    c['text'] = t[len(f"{orig_h}.\u2014 "):].strip()
                elif t.startswith(f"{orig_h}\u2014"):
                    c['text'] = t[len(f"{orig_h}\u2014"):].strip()
                elif t.startswith(f"{orig_h} "):
                    c['text'] = t[len(f"{orig_h} "):].strip()
                elif t.startswith(orig_h):
                    c['text'] = t[len(orig_h):].strip()
                else:
                    # Maybe orig_h was modified slightly?
                    pass
                
                # Ensure the text doesn't start with the em-dash if we missed it
                c['text'] = re.sub(r'^\.?\u2014\s*', '', c['text'])
                
                fixed_count += 1
        else:
            # It's non-bold, or not found. Keep heading as " "
            c['heading'] = " "
    else:
        # Does not start with a paragraph number. Keep heading as " "
        c['heading'] = " "

with open(validated_file, "w", encoding="utf-8") as f:
    for c in validated_chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

print(f"Restored {fixed_count} bold headings.")
