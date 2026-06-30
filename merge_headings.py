import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

filepath = r"c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\SECRETARIAT_OFFICE_MANUAL_validated.jsonl"

with open(filepath, "r", encoding="utf-8") as f:
    chunks = [json.loads(line) for line in f if line.strip()]

merged_chunks_dict = {}

for c in chunks:
    chapter = c.get("chapter", "")
    heading = c.get("heading", "")
    key = (chapter, heading)
    
    if key not in merged_chunks_dict:
        merged_chunks_dict[key] = c
    else:
        existing = merged_chunks_dict[key]
        
        # Merge text
        t1 = existing.get("text") or ""
        t2 = c.get("text") or ""
        # if both are empty/space, keep space. If one has text, combine properly
        if t1.strip() and t2.strip():
            existing["text"] = t1 + " " + t2
        elif t2.strip():
            existing["text"] = t2
            
        # Merge page numbers
        p1 = existing.get("page.no", "").strip("()")
        p2 = c.get("page.no", "").strip("()")
        if p1 != p2:
            existing["page.no"] = f"({p1}-{p2})"
            
        # Merge tables
        if c.get("has_table"):
            existing["has_table"] = True
            # For simplicity, if both have tables, we can just concatenate the HTML
            html1 = existing.get("table_html", "{}")
            html2 = c.get("table_html", "{}")
            if html1 != "{}" and html2 != "{}":
                existing["table_html"] = html1 + "<br/>" + html2
            elif html2 != "{}":
                existing["table_html"] = html2

with open(filepath, "w", encoding="utf-8") as f:
    for c in merged_chunks_dict.values():
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

print(f"Merged chunks. Original count: {len(chunks)}, New count: {len(merged_chunks_dict)}")
