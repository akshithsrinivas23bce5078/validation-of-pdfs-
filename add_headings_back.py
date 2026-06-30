import json
import re

# Build map of original texts
unval_file = r"unvalidated chunks\Secretariat_Office_Manual_chunks.jsonl"
orig_texts = {}
with open(unval_file, "r", encoding="utf-8") as f:
    for line in f:
        if not line.strip(): continue
        c = json.loads(line)
        para_no = str(c.get('para_no', '')).strip()
        m = re.match(r'^(\d{1,3})', para_no)
        if m:
            num = m.group(1)
            # Only keep the first one we see, which is usually the main paragraph before lists
            if num not in orig_texts:
                orig_texts[num] = c.get('text', '').strip()

val_file = r"chunks after validation\SECRETARIAT_OFFICE_MANUAL_validated.jsonl"
with open(val_file, "r", encoding="utf-8") as f:
    val_chunks = [json.loads(line) for line in f if line.strip()]

fixed_count = 0
for c in val_chunks:
    h = c.get('heading', '').strip()
    if h and h != "null" and h != " ":
        # It's a bold heading chunk, meaning we stripped its text
        m = re.match(r'^(\d{1,3})\.', h)
        if m:
            para_num = m.group(1)
            orig_t = orig_texts.get(para_num)
            if orig_t:
                cur_t = c.get('text', '').strip()
                # We need to find the prefix in orig_t that is missing from cur_t
                # Let's take the first 30 chars of cur_t
                search_str = cur_t[:30]
                if not search_str:
                    continue
                
                # Find search_str in orig_t
                idx = orig_t.find(search_str)
                if idx > 0:
                    prefix = orig_t[:idx]
                    # Prepend prefix to cur_t
                    c['text'] = prefix + cur_t
                    fixed_count += 1
                elif idx == -1:
                    # Maybe there was a slight whitespace difference
                    # Let's try matching the first 15 chars
                    search_str = cur_t[:15]
                    idx = orig_t.find(search_str)
                    if idx > 0:
                        prefix = orig_t[:idx]
                        c['text'] = prefix + cur_t
                        fixed_count += 1
                    elif cur_t.startswith(para_num):
                        # It already has it!
                        pass
                    else:
                        # Fallback: Just construct it
                        prefix = f"{h}.\u2014 " if not h.endswith(".") else f"{h}\u2014 "
                        c['text'] = prefix + cur_t
                        fixed_count += 1

with open(val_file, "w", encoding="utf-8") as f:
    for c in val_chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

print(f"Added prefix back to {fixed_count} chunks.")
