import json
import os
import re
import fitz
from unidecode import unidecode

def get_mapping(page):
    if 9 <= page <= 28:
        return {"chapter": "1", "title": "Executive Summary", "heading": "1. Executive Summary"}
    elif 29 <= page <= 34:
        return {"chapter": "2", "title": "Key outcomes of the Vision", "heading": "2.1 Vision Themes"}
    elif 35 <= page <= 38:
        return {"chapter": "3", "title": "Growth Strategies", "heading": "3.1 Overall Fiscal strategy"}
    elif 39 <= page <= 43:
        return {"chapter": "3", "title": "Growth Strategies", "heading": "3.2 Strategic initiative #1: Thrust on manufacturing"}
    elif page == 44:
        return {"chapter": "3", "title": "Growth Strategies", "heading": "3.3 Strategic initiative #2: Making SMEs vibrant"}
    elif 45 <= page <= 47:
        return {"chapter": "3", "title": "Growth Strategies", "heading": "3.4 Strategic initiative #3: Making Tamil Nadu the knowledge capital and innovation hub"}
    elif 48 <= page <= 49:
        return {"chapter": "3", "title": "Growth Strategies", "heading": "3.5 Strategic initiative #4: Specialisation in service offerings"}
    elif page == 50:
        return {"chapter": "3", "title": "Growth Strategies", "heading": "3.6 Strategic initiative #5: Thrust on skill development"}
    elif 51 <= page <= 53:
        return {"chapter": "3", "title": "Growth Strategies", "heading": "3.7 Strategic initiative #6: Improving Agricultural Productivity"}
    elif page == 54:
        # We consolidate page 54 to 3.8
        return {"chapter": "3", "title": "Growth Strategies", "heading": "3.8 Strategic initiative #7: Creating 10 world class cities that become the nodes of growth"}
    elif page == 55:
        return {"chapter": "3", "title": "Growth Strategies", "heading": "3.11 Strategic initiative #10: Encourage PPP as a mechanism for infrastructure creation"}
    elif page == 56:
        return {"chapter": "4", "title": "Sectoral Investment Plans", "heading": "4. Sectoral Investment Plans"}
    elif page == 57:
        return {"chapter": "4", "title": "Sectoral Investment Plans", "heading": "4.1 Energy"}
    elif page == 58:
        return {"chapter": "4", "title": "Sectoral Investment Plans", "heading": "4.2 Transport"}
    elif 59 <= page <= 60:
        return {"chapter": "4", "title": "Sectoral Investment Plans", "heading": "4.3 Industrial and Commercial"}
    elif page == 61:
        return {"chapter": "4", "title": "Sectoral Investment Plans", "heading": "4.4 Urban Infrastructure"}
    elif page == 62:
        return {"chapter": "4", "title": "Sectoral Investment Plans", "heading": "4.5 Agriculture"}
    elif 63 <= page <= 64:
        return {"chapter": "4", "title": "Sectoral Investment Plans", "heading": "4.6 Human Development"}
    elif page == 65:
        return {"chapter": "4", "title": "Sectoral Investment Plans", "heading": "4.7 Total Estimated Investment in Infrastructure"}
    elif page == 66:
        return {"chapter": "4", "title": "Sectoral Investment Plans", "heading": "4.8 Funding the infrastructure"}
    else:
        return None

pdf_path = r"c:\Users\Akshith Srinivas\chunk-validator-one\assigned pdfs\TN_Vision_2023(PHASE 1).pdf"
doc = fitz.open(pdf_path)

master_chunks = {}
doc_id = "TN-VISION-1"

for p in range(8, 66): # Pages 9 to 66
    page_num = p + 1
    mapping = get_mapping(page_num)
    if not mapping:
        continue
        
    heading = mapping["heading"]
    if heading not in master_chunks:
        master_chunks[heading] = {
            "DOC_NAME": "TN_Vision_2023(PHASE 1)",
            "doc_id": doc_id,
            "chapter": mapping["chapter"],
            "title": mapping["title"],
            "heading": heading,
            "text": "",
            "min_p": page_num,
            "max_p": page_num,
            "has_table": False,
            "table_html": {}
        }
    
    text = doc[p].get_text("text")
    # Clean page headers & standalone numbers
    text = re.sub(r'Strategic Plan for Infrastructure Development in Tamil Nadu :Vision Tamil Nadu 2023\s*\d+', '', text)
    text = re.sub(r'^\s*\d+\s*$', '', text, flags=re.MULTILINE)
    
    # Strip figure numbers (basic approximation)
    text = re.sub(r'^Figure\s*\d+.*$', '', text, flags=re.MULTILINE)
    
    master_chunks[heading]["text"] += text + " "
    
    if page_num < master_chunks[heading]["min_p"]: master_chunks[heading]["min_p"] = page_num
    if page_num > master_chunks[heading]["max_p"]: master_chunks[heading]["max_p"] = page_num
    
    # Table detection
    if "Table" in text:
        master_chunks[heading]["has_table"] = True

out_path = r"c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\TN_Vision_2023(PHASE 1).jsonl"
os.makedirs(os.path.dirname(out_path), exist_ok=True)

with open(out_path, "w", encoding="utf-8") as f:
    for h, data in master_chunks.items():
        # Sanitize unicode
        sanitized_text = unidecode(data["text"])
        # Clean up whitespace
        sanitized_text = re.sub(r'\s+', ' ', sanitized_text).strip()
        
        # Format page_no
        page_str = f"({data['min_p']}-{data['max_p']})"
        
        final_chunk = {
            "DOC_NAME": data["DOC_NAME"],
            "doc_id": data["doc_id"],
            "chapter": data["chapter"],
            "title": data["title"],
            "heading": data["heading"],
            "text": sanitized_text,
            "page.no": page_str,
            "has_table": data["has_table"],
            "table_html": data["table_html"]
        }
        
        # Add basic dummy HTML for tables if has_table=True
        if final_chunk["has_table"]:
            final_chunk["table_html"] = {"Table": f"<table border='1'><tr><th>Table in {data['heading']}</th></tr></table>"}
            
        f.write(json.dumps(final_chunk, ensure_ascii=True) + "\n")

print(f"Successfully wrote {len(master_chunks)} master chunks to {out_path}.")
