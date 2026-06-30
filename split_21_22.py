import json
import re

with open('debug_ch21_22.json', 'r', encoding='utf-8') as f:
    chunks = json.load(f)

# Group text by chapter
text_21 = ""
text_22 = ""
for c in chunks:
    ch = str(c.get('chapter', ''))
    if ch == '21' or 'RDSO' in str(c.get('title', '')):
        text_21 += c.get('text', '') + "\n"
    elif ch == '22' or 'E-Office' in str(c.get('title', '')):
        text_22 += c.get('text', '') + "\n"

# The headings for Chapter 21 are:
h_21 = [
    "1. Introduction",
    "2. Functions of RDSO",
    "3. Organizational Set Up",
    "4. System Of Audit",
    "5. Local Audit/Inspections",
    "6. Use of IT Applications in RDSO",
    "7. Audit Focus Areas",
    "8. Functions And Roles Of The Directorates",
    "8.1 Carr",
    "8.2 Engine Development",
    "8.3 Motive Power",
    "8.4 Electrical",
    "8.5 Research",
    "8.6 Signal",
    "8.7 Traction Installation",
    "8.8 Track Design",
    "8.9 Testing",
    "8.10 Telecommunication",
    "8.11 Track Machines And Monitoring",
    "8.12 Traffic",
    "8.13 Wagon",
    "8.14 Bridges And Structures",
    "8.15 Geo-Technical Engineering",
    "8.16 Metallurgical And Chemical",
    "8.17 Psycho",
    "8.18 Works",
    "8.19 Administration",
    "8.20 Quality Assurance",
    "8.21 Quality Assurance",
    "8.22 Quality Assurance",
    "8.23 Stores",
    "8.24 Finance And Accounts"
]

def split_text_by_headings(text, headings):
    results = []
    current_heading = headings[0]
    current_text = text
    
    for i in range(1, len(headings)):
        next_heading = headings[i]
        
        # Build regex to find next heading
        # e.g., "8.1 Carr" -> look for "8.1" followed by some words starting with "Carr"
        prefix = next_heading.split()[0]
        if next_heading.startswith('8.'):
            # strict match on "8.X"
            pattern = r"(?s)(.*?)\b(" + re.escape(prefix) + r"[ \t\n]+.*?)(?=\b8\.\d+|$)"
            # Wait, easier to just regex search the exact prefix "8.X"
            pattern = r"(?s)(.*?)(" + re.escape(prefix) + r"[ \t\n]+.*)"
        else:
            pattern = r"(?s)(.*?)(" + re.escape(prefix) + r"[ \t\n]+.*)"
            
        # Or just find the first index of "\n8.X " or "8.X "
        # We can just search for the number!
        m = re.search(r'\b' + re.escape(prefix) + r'\b\s+[A-Za-z]', current_text)
        if m:
            idx = m.start()
            results.append((current_heading, current_text[:idx].strip()))
            current_text = current_text[idx:]
            current_heading = next_heading
        else:
            # Not found? Just keep looking for the next one
            print(f"WARNING: Could not find heading {prefix} in text!")
    
    results.append((current_heading, current_text.strip()))
    return results

print("=== CH 21 ===")
res_21 = split_text_by_headings(text_21, h_21)
for h, t in res_21:
    print(f"{h}: {len(t)} chars")

h_22 = [
    "1. Introduction",
    "2. Enterprise-Wide System",
    "2.1",
    "2.2",
    "3. Empowering The Auditor",
    "4. Web-Based Solution",
    "5. Functionalities/Services Available",
    "5.1 Standard Procedure",
    "5.2 Representa Tion",
    "6. Compliance Audit",
    "7. Evaluation Of Internal Control Mechanism",
    "8. Adequacy Of Internal Audit System"
]

print("\n=== CH 22 ===")
res_22 = split_text_by_headings(text_22, h_22)
for h, t in res_22:
    print(f"{h}: {len(t)} chars")
