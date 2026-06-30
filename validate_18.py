import json
import os
import re

INPUT_FILE = r"c:\Users\Akshith Srinivas\chunk-validator-one\unvalidated chunks\18. Account Principle Accounting Manual Part__State Audit West Ben.jsonl"
OUTPUT_FILE = r"c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\18. Account Principle Accounting Manual Part__State Audit West Ben.jsonl"

def map_heading(old_heading):
    old_heading = old_heading.strip()
    if old_heading.startswith("3.1"):
        return "3.1 INCOME"
    elif old_heading.startswith("3.2"):
        return "3.2 EXPENDITURE"
    elif old_heading.startswith("3.3"):
        return "3.3 ASSETS"
    elif old_heading.startswith("3.4"):
        return "3.4 GRANTS, BORROWINGS AND SPECIAL FUNDS"
    elif old_heading.startswith("3.5"):
        return "3.5 OTHERS"
    return None

def extract_chapter_num(chapter_str):
    m = re.search(r'\d+', str(chapter_str))
    if m:
        return m.group(0)
    return str(chapter_str)

def format_page_range(page_str):
    pm = re.search(r"\(?(\d+)(?:-(\d+))?\)?", str(page_str))
    if pm:
        start = int(pm.group(1))
        end = int(pm.group(2)) if pm.group(2) else start
        if start > end:
            start, end = end, start
        if start == end:
            return f"({start})"
        return f"({start}-{end})"
    return ""

def process():
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    with open(INPUT_FILE, 'r', encoding='utf-8') as fin, open(OUTPUT_FILE, 'w', encoding='utf-8') as fout:
        for line in fin:
            if not line.strip(): continue
            chunk = json.loads(line)
            
            original_heading = chunk.get('heading', '').strip()
            chapter_num = extract_chapter_num(chunk.get('chapter', ''))
            title = chunk.get("title", "")
            
            # User wants to avoid annexure, appendix, diagram, flowchart, preface, foreword.
            skip = False
            for kw in ['foreword', 'preface', 'annexure', 'appendix', 'diagram', 'flowchart']:
                if kw in title.lower() or kw in original_heading.lower():
                    skip = True
                    break
                
            if skip:
                continue

            text = chunk.get('text', '').strip()

            # Ensure the original sentence is reconstructed because the raw jsonl split it.
            if original_heading and not text.startswith(original_heading):
                text = original_heading + " " + text

            # Assign heading according to the map
            new_heading = map_heading(original_heading)

            final_chunk = {
                "DOC_NAME": chunk.get("DOC_NAME"),
                "doc_id": chunk.get("doc_id"),
                "chapter": chapter_num,
                "title": title,
                "heading": new_heading,
                "text": text,
                "page.no": format_page_range(chunk.get("page.no", "")),
                "has_table": bool(chunk.get("has_table", False)),
                "table_html": chunk.get("table_html", {})
            }
            fout.write(json.dumps(final_chunk, ensure_ascii=False) + '\n')

if __name__ == '__main__':
    process()
    print("Validation and formatting (unmerged chunks) complete for doc 18.")
