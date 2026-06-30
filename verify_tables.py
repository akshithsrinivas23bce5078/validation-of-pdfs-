import json

with open("chunks after validation/TNGS_ClassXII_validated.jsonl", "r", encoding="utf-8") as f:
    chunks = [json.loads(line) for line in f if line.strip()]

for c in chunks:
    if c.get("has_table") == True:
        print(f"=== {c['chapter']} / {c['heading']} ===")
        print(f"text (first 200): {c['text'][:200]}")
        th = c.get("table_html", "{}")
        print(f"table_html (first 150): {str(th)[:150]}")
        print()
