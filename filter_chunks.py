import json
import os
import re

# 1. Load user requirements
required = json.load(open('user_required_subdivisions.json', encoding='utf-8'))
toc = json.load(open('chapter_aware_toc.json', encoding='utf-8'))

# 2. Load the 521 successfully extracted chunks
extracted_chunks = []
with open(r'chunks after validation\RAM_2022_Sixth_Edition.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        extracted_chunks.append(json.loads(line))
        
# 3. Create a dictionary to easily lookup chunks by chapter and heading number
# A chunk's 'heading' might be "6.7 Software Aided...". The number is "6.7"
chunk_map = {}
for c in extracted_chunks:
    ch = str(c['chapter'])
    heading_text = c['heading']
    # Extract the leading number
    m = re.match(r'^(\d{1,2}(?:\.\d{1,2})?)\b', heading_text)
    if m:
        num = m.group(1)
    else:
        # fallback
        num = heading_text.split()[0].rstrip('.')
        
    key = f"{ch}_{num}"
    if key not in chunk_map:
        chunk_map[key] = []
    chunk_map[key].append(c)

# 4. Filter according to user order
final_chunks = []
for ch_num in range(1, 23):
    ch_num = str(ch_num)
    if ch_num not in required:
        continue
        
    for req in required[ch_num]:
        key = f"{ch_num}_{req}"
        
        # Did we extract this chunk?
        if key in chunk_map and len(chunk_map[key]) > 0:
            # We take the first one (usually there's only 1)
            # Ensure the heading has the exact expected format
            c = chunk_map[key][0]
            # Replace heading with the proper TOC title if possible
            toc_key = f"{ch_num}_{req}"
            c['heading'] = toc.get(toc_key, c['heading'])
            final_chunks.append(c)
        else:
            # Create an empty chunk so we don't break the user's required structure!
            print(f"Warning: Chunk {req} in Chapter {ch_num} was missing from extraction. Injecting empty chunk.")
            toc_key = f"{ch_num}_{req}"
            proper_heading = toc.get(toc_key, req)
            
            CHAPTER_TITLE_MAP = {
                "1":  "Introduction to Railway Audit Manual",
                "2":  "Audit of General Administration and Vigilance Department",
                "3":  "Audit of Accounts Department",
                "4":  "Audit of Personnel Department",
                "5":  "Audit of Medical Department",
                "6":  "Audit of Civil Engineering Department",
                "7":  "Audit of Railway Works",
                "8":  "Audit of Commercial Department",
                "9":  "Audit of Operating Department",
                "10": "Audit of Electrical Department",
                "11": "Audit of Signal and Telecommunication Department",
                "12": "Audit of Mechanical Department",
                "13": "Audit of Production Units",
                "14": "Audit of Stores Department",
                "15": "Audit of Safety Department",
                "16": "Audit of Security Department",
                "17": "Centre for Railway Information Systems",
                "18": "Rail Land Development Authority",
                "19": "Working of Railway Sports Promotion Board",
                "20": "Rail Public Sector Undertakings",
                "21": "Research Designs and Standards Organization",
                "22": "E-Office",
            }
            
            final_chunks.append({
                "DOC_NAME": "RAM 2022 Sixth Edition",
                "doc_id": "RAM-9A7560D8FA",
                "chapter": ch_num,
                "title": CHAPTER_TITLE_MAP.get(ch_num, f"Chapter {ch_num}"),
                "heading": proper_heading,
                "text": " ", # Empty text for missing extraction
                "page.no": "()",
                "has_table": False,
                "table_html": {}
            })

print(f"Built final array of {len(final_chunks)} chunks matching the exact user requirements.")

with open(r'chunks after validation\RAM_2022_Sixth_Edition_final.jsonl', 'w', encoding='utf-8') as f:
    for c in final_chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')
print("Done.")
