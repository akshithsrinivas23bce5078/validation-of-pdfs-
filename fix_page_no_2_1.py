import json
import re

unvalidated_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\unvalidated chunks\Chapter 2_1.jsonl'
validated_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Chapter 2_1.jsonl'

with open(unvalidated_path, 'r', encoding='utf-8') as f:
    unvalidated_chunks = [json.loads(line) for line in f if line.strip()]

# Dictionary to hold all page numbers found for each 2.x prefix
prefix_pages = {}

for c in unvalidated_chunks:
    heading = c.get('heading', '')
    page_str = c.get('page.no', '')
    m = re.match(r'^(2\.\d+)', heading)
    if m and page_str:
        prefix = m.group(1)
        # page.no is usually format "(X-Y)"
        nums = re.findall(r'\d+', page_str)
        if nums:
            if prefix not in prefix_pages:
                prefix_pages[prefix] = []
            prefix_pages[prefix].extend([int(n) for n in nums])

with open(validated_path, 'r', encoding='utf-8') as f:
    validated_chunks = [json.loads(line) for line in f if line.strip()]

for c in validated_chunks:
    heading = c.get('heading', '')
    m = re.match(r'^(2\.\d+)', heading)
    if m:
        prefix = m.group(1)
        if prefix in prefix_pages:
            pages = prefix_pages[prefix]
            min_p = min(pages)
            max_p = max(pages)
            c['page.no'] = f"({min_p}-{max_p})"

with open(validated_path, 'w', encoding='utf-8') as f:
    for c in validated_chunks:
        f.write(json.dumps(c, ensure_ascii=True) + '\n')

print("page.no ranges successfully updated!")
