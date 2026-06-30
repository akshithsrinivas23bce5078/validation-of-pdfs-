import json

filepath = r"c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Chapter 2_1.jsonl"
with open(filepath, "r", encoding="utf-8") as f:
    chunks = [json.loads(line) for line in f if line.strip()]

inconsistencies = []

doc_id = chunks[0].get('doc_id')

for i, c in enumerate(chunks):
    keys = list(c.keys())
    print("Chunk " + str(i) + " keys: " + str(keys))
    
    # Check page.no
    if "page.no" in c:
        print("  page.no: " + str(c["page.no"]))
    else:
        inconsistencies.append(f"Chunk {i} missing page.no")
        
    # Check doc_id
    if c.get('doc_id') != doc_id:
        inconsistencies.append(f"Chunk {i} has mismatched doc_id: {c.get('doc_id')}")
        
    # Check chapter
    if c.get('chapter') != "2":
        inconsistencies.append(f"Chunk {i} has mismatched chapter: {c.get('chapter')}")
        
    # Check title
    if c.get('title') != "SEWER SYSTEMS":
        inconsistencies.append(f"Chunk {i} has mismatched title: {c.get('title')}")
        
    # Check table structure
    if 'has_table' not in c or 'table_html' not in c:
        inconsistencies.append(f"Chunk {i} missing table schema")

if inconsistencies:
    print("INCONSISTENCIES FOUND:")
    for inc in inconsistencies:
        print(" - " + inc)
else:
    print("No basic schema inconsistencies found.")
