import json
import re
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

CANONICAL = {
    "12": [
        "1. Constitution",
        "2. Appointment",
        "2A. Appointing Authority",
        "2AA. Appointing Authority",
        "2B. Appointing Authority",
        "3. Qualification",
        "4. Probation in any department other than Law",
        "5. Probation in the Law Department",
        "5A. Probation for category 4",
        "5B. Probation for category 5",
        "5C. Probation for category 6",
        "6. Unit of appointment",
        "7. Tenure of appointment of Deputy Secretary in Law Department or Under Secretary or Section Officers of any department (including Law Department) recruited by transfer from any service other than Tamil Nadu Secretariat Service",
        "8. Non-applicability of certain General Rules",
        "9. Savings"
    ],
    "12.1": ["1. Constitution", "2. Appointment", "3. Promotion", "4. Probation"],
    "12.2": ["1. Constitution", "2. Appointment", "3. Promotion", "4. Preparation of approved list"],
    "12.3": ["1. Constitution", "2. Appointment", "3. Promotion", "4. Preparation of approved list"],
    "12.4": ["1. Constitution", "2. Appointment", "3. Promotion", "4. Preparation of approved list"],
    "12.5": ["1. Constitution", "2. Appointment", "3. Promotion", "4. Preparation of approved list"],
    "12.6": ["1. Constitution", "2. Appointment", "3. Promotion", "4. Preparation of approved list"],
    "12.7": ["1. Constitution", "2. Appointment", "3. Qualifications", "4. Appointing Authority", "5. Probation", "6. Pay", "7. Preparation of approved list"]
}

def clean_text_no_num(text):
    text = re.sub(r'^\d+[a-zA-Z]*\.', '', text)
    return re.sub(r'[^a-zA-Z]', '', text).lower()

with open("chunks after validation/TNGS_ClassXII_validated.jsonl", "r", encoding="utf-8") as f:
    chunks = [json.loads(line) for line in f if line.strip()]

new_chunks = []
from collections import defaultdict
chapter_chunks = defaultdict(list)
for c in chunks:
    chapter_chunks[c["chapter"]].append(c)

for ch, c_list in chapter_chunks.items():
    if ch not in CANONICAL:
        new_chunks.extend(c_list)
        continue
    
    canonical_list = CANONICAL[ch]
    active_idx = 0
    merged_by_heading = {}
    
    for c in c_list:
        heading_text = c.get("heading", "")
        # Fallback to a little bit of text if heading is empty, but be careful
        if not heading_text.strip():
            heading_text = c.get("text", "")[:50]
            
        cleaned_no_num = clean_text_no_num(heading_text)
        
        # Determine if this chunk represents a new canonical heading
        best_match_idx = active_idx
        # Search forwards to find the next valid match
        for i in range(active_idx, len(canonical_list)):
            c_clean = clean_text_no_num(canonical_list[i])
            idx = cleaned_no_num.find(c_clean) if c_clean else -1
            if c_clean and (cleaned_no_num.startswith(c_clean) or (idx != -1 and idx < 15)):
                best_match_idx = i
                break
            
            # Special case for "1. Constitution" which doesn't always have the word constitution
            if i == 0 and active_idx == 0:
                best_match_idx = 0
                
        # Manual overrides for Chapter 12
        if ch == "12":
            h_lower = heading_text.lower()
            if "2aa" in h_lower or "2aaappointing" in cleaned_no_num:
                best_match_idx = canonical_list.index("2AA. Appointing Authority")
            elif "2b" in h_lower or "2bappointing" in cleaned_no_num:
                best_match_idx = canonical_list.index("2B. Appointing Authority")
            elif "2c" in h_lower or "2d" in h_lower:
                best_match_idx = canonical_list.index("2B. Appointing Authority")
            elif "5aprobation" in cleaned_no_num:
                best_match_idx = canonical_list.index("5A. Probation for category 4")
            elif "5bprobation" in cleaned_no_num or "5-b" in h_lower:
                best_match_idx = canonical_list.index("5B. Probation for category 5")
            elif "5cprobation" in cleaned_no_num or "5-c" in h_lower:
                best_match_idx = canonical_list.index("5C. Probation for category 6")
            elif "5dprobation" in cleaned_no_num or "5-d" in h_lower:
                best_match_idx = canonical_list.index("5C. Probation for category 6")
            elif "unitofappointment" in cleaned_no_num:
                best_match_idx = canonical_list.index("6. Unit of appointment")
            elif "tenureofappointment" in cleaned_no_num:
                best_match_idx = canonical_list.index("7. Tenure of appointment of Deputy Secretary in Law Department or Under Secretary or Section Officers of any department (including Law Department) recruited by transfer from any service other than Tamil Nadu Secretariat Service")
            elif "nonapplicability" in cleaned_no_num:
                best_match_idx = canonical_list.index("8. Non-applicability of certain General Rules")
            elif "savings" in cleaned_no_num:
                best_match_idx = canonical_list.index("9. Savings")
            elif active_idx == 0 and ("2appointment" in clean_text_no_num(heading_text) or "appointment" in cleaned_no_num[:30]):
                best_match_idx = canonical_list.index("2. Appointment")
        
        active_idx = best_match_idx
        canonical_heading = canonical_list[active_idx]
        
        if canonical_heading not in merged_by_heading:
            merged_by_heading[canonical_heading] = {
                "DOC_NAME": c["DOC_NAME"],
                "doc_id": c["doc_id"],
                "heading": canonical_heading,
                "text": "",
                "page.no": c["page.no"],
                "has_table": False,
                "table_html": "{}",
                "chapter": ch,
                "title": c["title"]
            }
        
        m = merged_by_heading[canonical_heading]
        # Append text properly
        if c.get("heading") and c["heading"].strip() and c["heading"].strip() not in canonical_heading:
            m["text"] += c["heading"].strip() + "\n"
        if c.get("text") and c["text"].strip():
            m["text"] += c["text"].strip() + "\n"
        
        if c.get("has_table"):
            m["has_table"] = True
            if m["table_html"] == "{}":
                m["table_html"] = c["table_html"]
            else:
                m["table_html"] += "<br>" + c["table_html"]

    for h in canonical_list:
        if h in merged_by_heading:
            m = merged_by_heading[h]
            m["text"] = m["text"].strip()
            new_chunks.append(m)

with open("chunks after validation/TNGS_ClassXII_validated.jsonl", "w", encoding="utf-8") as f:
    for c in new_chunks:
        f.write(json.dumps(c, ensure_ascii=False) + "\n")

print(f"Re-mapped into {len(new_chunks)} merged chunks.")
