import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

filepath = r"c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\SECRETARIAT_OFFICE_MANUAL_validated.jsonl"

with open(filepath, "r", encoding="utf-8") as f:
    chunks = [json.loads(line) for line in f if line.strip()]

last_para_num = 0
current_main = None

merged_chunks = []
merge_count = 0

for c in chunks:
    heading = c['heading'].strip()
    m = re.match(r'^(\d{1,3})(?:\w)?[\.\s]', heading)
    
    is_main = False
    
    if m:
        num = int(m.group(1))
        if num >= last_para_num and num <= last_para_num + 15:
            last_para_num = num
            is_main = True
    
    if is_main:
        current_main = c
        merged_chunks.append(current_main)
    else:
        if current_main:
            # Merge this chunk into current_main
            h = c.get('heading', '').strip()
            t = c.get('text', '').strip()
            
            append_text = h
            if t and t != h and t != "None" and t != "null":
                append_text += " " + t
                
            # If the current main's text is " ", just replace it
            curr_text = current_main.get("text", "")
            if curr_text is None or curr_text.strip() == "":
                current_main["text"] = append_text
            else:
                current_main["text"] += " " + append_text
            
            # Merge page numbers
            p1 = current_main.get("page.no", "").strip("()")
            p2 = c.get("page.no", "").strip("()")
            
            # Helper to extract range
            def parse_pages(p):
                if not p: return []
                parts = p.split('-')
                if len(parts) == 2:
                    return [int(parts[0]), int(parts[1])]
                return [int(parts[0])]
            
            try:
                pages = parse_pages(p1) + parse_pages(p2)
                if pages:
                    min_p, max_p = min(pages), max(pages)
                    if min_p != max_p:
                        current_main["page.no"] = f"({min_p}-{max_p})"
                    else:
                        current_main["page.no"] = f"({min_p})"
            except:
                pass # ignore if page parsing fails
            
            # Merge tables
            if c.get("has_table"):
                current_main["has_table"] = True
                html1 = current_main.get("table_html", "{}")
                html2 = c.get("table_html", "{}")
                if html1 != "{}" and html2 != "{}":
                    current_main["table_html"] = html1 + "<br/>" + html2
                elif html2 != "{}":
                    current_main["table_html"] = html2
                    
            merge_count += 1
        else:
            # Sub-chunk without main? Shouldn't happen based on dry run, but just append
            merged_chunks.append(c)

with open(filepath, "w", encoding="utf-8") as f:
    for c in merged_chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

print(f"Successfully merged {merge_count} sub-chunks into their parent main chunks.")
print(f"Original chunks: {len(chunks)}, New chunks: {len(merged_chunks)}")
