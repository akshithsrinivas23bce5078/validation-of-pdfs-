import json

input_file = "chunks after validation/TNGS_ClassXII_validated.jsonl"
with open(input_file, "r", encoding="utf-8") as f:
    chunks = [json.loads(line) for line in f if line.strip()]

# Fix false positives: reset has_table to false and table_html to "{}"
for c in chunks:
    chapter = c.get("chapter", "")
    heading = c.get("heading", "")
    
    # CLASS XII - D(1) / 1. Constitution does NOT have a table
    if chapter == "CLASS XII - D(1)" and heading == "1. Constitution":
        c["has_table"] = False
        c["table_html"] = "{}"
    
    # CLASS XII - E / 4. Appointing Authority does NOT have a table
    if chapter == "CLASS XII - E" and heading == "4. Appointing Authority":
        c["has_table"] = False
        c["table_html"] = "{}"

# Write back
with open(input_file, "w", encoding="utf-8") as f:
    for c in chunks:
        ordered = {
            "DOC_NAME": c.get("DOC_NAME"),
            "doc_id": c.get("doc_id"),
            "chapter": c.get("chapter"),
            "title": c.get("title"),
            "heading": c.get("heading"),
            "text": c.get("text"),
            "page.no": c.get("page.no"),
            "has_table": c.get("has_table"),
            "table_html": c.get("table_html")
        }
        f.write(json.dumps(ordered, ensure_ascii=False) + "\n")

# Final summary
table_count = sum(1 for c in chunks if c.get("has_table") == True)
print(f"Done. {table_count} chunks now have has_table=true:")
for c in chunks:
    if c.get("has_table") == True:
        print(f"  - {c['chapter']} / {c['heading']}")
