import json

input_file = "chunks after validation/TNGS_ClassXII_validated.jsonl"
with open(input_file, "r", encoding="utf-8") as f:
    chunks = [json.loads(line) for line in f if line.strip()]

new_chunks = []
for c in chunks:
    # Build a new dict in the requested order
    ordered = {}
    ordered["DOC_NAME"] = c.get("DOC_NAME")
    ordered["doc_id"] = c.get("doc_id")
    ordered["chapter"] = c.get("chapter")
    ordered["title"] = c.get("title")
    
    # Copy the remaining keys
    for k in c:
        if k not in ordered:
            ordered[k] = c[k]
            
    new_chunks.append(ordered)

with open(input_file, "w", encoding="utf-8") as f:
    for c in new_chunks:
        f.write(json.dumps(c, ensure_ascii=False) + "\n")

print("Reordered JSON keys successfully.")
