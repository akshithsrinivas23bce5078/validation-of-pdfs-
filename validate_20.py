import json
import os
import re

INPUT_FILE = r"c:\Users\Akshith Srinivas\chunk-validator-one\unvalidated chunks\20. Chart of Account Accounting Manual Part_4_State Audit West Ben.jsonl"
OUTPUT_FILE = r"c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\20. Chart of Account Accounting Manual Part_4_State Audit West Ben.jsonl"

TITLE_MAP = {
    "1": "Introduction",
    "2": "Objective",
    "3": "Structure of Function Code",
    "4": "Structure of the Functionary Code",
    "5": "Structure of the Field Code",
    "6": "Structure of the Fund Code",
    "7": "Structure of Accounting Code",
    "8": "Identification Code for ULB",
    "9": "Procedure for the Change in the Chart of Accounts",
    "10": "Format for Change Request Form",
    "11": "Format for Change Authorised Form"
}

HEADING_MAP = {
    "7.1": "Primary Accounting Code",
    "7.2": "Major Head Code",
    "7.3": "Major Head Code",
    "7.4": "Minor Head Code",
    "7.5": "Secondary accounting code",
    "7.6": "Secondary accounting code",
    "7.7": "Secondary accounting code",
    "9.1": "Function Code",
    "9.2": "Function Code",
    "9.3": "Function Code",
    "9.4": "Functionary Code",
    "9.5": "Field Code",
    "9.6": "Fund Code",
    "9.7": "Primary Accounting Code",
    "9.8": "Primary Accounting Code",
    "9.9": "Primary Accounting Code",
    "9.10": "Secondary Accounting Code"
}

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
            title = TITLE_MAP.get(chapter_num, chunk.get("title", ""))
            
            m_paragraph = re.match(r'^(\d+\.\d+)', original_heading)
            paragraph_id = m_paragraph.group(1) if m_paragraph else None

            # User wants to avoid annexure, appendix, diagram, flowchart, preface, foreword.
            skip = False
            for kw in ['foreword', 'preface', 'annexure', 'appendix', 'diagram', 'flowchart']:
                if kw in title.lower() or kw in original_heading.lower():
                    skip = True
                    break
            
            # Don't skip if the user explicitly provided a mapping for this chunk
            if paragraph_id in HEADING_MAP:
                skip = False
            
            if "Annexure" in chunk.get('text', '') and chapter_num == "11" and not original_heading.startswith('11.'):
                skip = True
                
            if skip:
                continue

            text = chunk.get('text', '').strip()
            
            # The first chunk contains preamble. Let's discard it since 1.1 covers the actual chapter start.
            if chapter_num == "1" and original_heading == "1":
                continue
                
            # Handle chunk 11.1 which has reverse-spelled annexure and forward spelled annexures
            if chapter_num == "11" and original_heading.startswith("11.1"):
                idx = text.find("I-eruxennA")
                if idx != -1:
                    text = text[:idx].strip()
                idx2 = text.find("Annexure i")
                if idx2 != -1:
                    text = text[:idx2].strip()

            # Ensure the original sentence is reconstructed because the raw jsonl split it.
            if original_heading and not text.startswith(original_heading):
                text = original_heading + " " + text

            # Assign heading according to the map
            new_heading = HEADING_MAP.get(paragraph_id, None)

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
    print("Validation and formatting (unmerged chunks with headings) complete.")
