import json
import re

filepath = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\18. Account Principle Accounting Manual Part__State Audit West Ben.jsonl'

chunks = []
with open(filepath, 'r', encoding='utf-8') as f:
    for line in f:
        chunks.append(json.loads(line))

merged_chunks = []
grouped = {}

# Process chunks sequentially to maintain order
for c in chunks:
    heading = c.get('heading')
    if heading is None:
        merged_chunks.append(c)
    else:
        if heading not in grouped:
            grouped[heading] = []
            merged_chunks.append({"_group_marker": heading}) # Placeholder to maintain order
        grouped[heading].append(c)

def extract_pages(page_str):
    nums = re.findall(r'\d+', page_str)
    return [int(n) for n in nums]

# Reconstruct merged chunks
final_chunks = []
for item in merged_chunks:
    if "_group_marker" in item:
        heading = item["_group_marker"]
        group = grouped[heading]
        
        # Merge the group
        base = group[0].copy()
        
        all_text = []
        all_pages = []
        has_table = False
        table_html = "{}"
        
        for g in group:
            all_text.append(g.get('text', ''))
            all_pages.extend(extract_pages(g.get('page.no', '')))
            if g.get('has_table'):
                has_table = True
                if g.get('table_html') != "{}":
                    table_html = g.get('table_html')
        
        base['text'] = "\n\n".join(all_text)
        base['has_table'] = has_table
        base['table_html'] = table_html
        
        if all_pages:
            min_p = min(all_pages)
            max_p = max(all_pages)
            if min_p == max_p:
                base['page.no'] = f"({min_p})"
            else:
                base['page.no'] = f"({min_p}-{max_p})"
        
        final_chunks.append(base)
    else:
        final_chunks.append(item)

# Write back
with open(filepath, 'w', encoding='utf-8') as f:
    for c in final_chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

print(f"Original chunks: {len(chunks)}, Merged chunks: {len(final_chunks)}")
