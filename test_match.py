import re
import json

def norm(s):
    return re.sub(r'[^A-Z0-9]+', '', s.upper())

toc = json.load(open('toc_mapping.json'))
norm_toc = {norm(k): v for k, v in toc.items()}

chunks = [json.loads(l) for l in open(r'chunks after validation\RAM_2022_Sixth_Edition.jsonl', encoding='utf-8')]
missing = [c for c in chunks if not any(c['heading'].startswith(str(i)+'.') for i in range(1,23))]

matched_count = 0
for c in missing:
    nh = norm(c['heading'])
    # In validate_RAM_chunks, heading is derived from raw_title initially
    if nh in norm_toc:
        matched_count += 1
    else:
        # What if we match c['title'] which holds the raw string from unvalidated chunk?
        # wait, c['title'] in validated chunks is "Introduction to Railway..." 
        # so we can't test it directly here easily.
        pass

print('Total originally missing:', len(missing))
print('Total matched with robust norm:', matched_count)
