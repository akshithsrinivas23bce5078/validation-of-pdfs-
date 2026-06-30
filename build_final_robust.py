import json
import re

with open(r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\RAM_2022_Sixth_Edition_fixed.jsonl', 'r', encoding='utf-8') as f:
    fixed_chunks = [json.loads(line) for line in f]

def clean_text(t):
    if not t: return t
    try:
        t = t.encode('latin1').decode('unicode_escape').encode('latin1').decode('utf-8')
    except:
        pass
    t = t.replace('\u2013', '-').replace('\u2019', "'").replace('\u201c', '"').replace('\u201d', '"').replace('\u2018', "'").replace('\u00a0', ' ')
    return t

final_chunks = []
for c in fixed_chunks:
    if c.get('chapter') not in ['21', '22']:
        c['text'] = clean_text(c.get('text'))
        c['heading'] = clean_text(c.get('heading'))
        c['title'] = clean_text(c.get('title'))
        final_chunks.append(c)

with open('debug_ch21_22.json', 'r', encoding='utf-8') as f:
    raw_21_22 = json.load(f)

text_21 = ''
for c in raw_21_22:
    if c.get('chapter') == '21' or 'RDSO' in str(c.get('title', '')):
        text_21 += clean_text(c.get('text', '')) + '\n'

ch21_headings = [
    ("1. Introduction", "1. INTRODUCTION"),
    ("2. Functions of RDSO", "2. FUNCTIONS OF RDSO"),
    ("3. Organizational Set Up", "3. ORGANIZATIONAL SET UP"),
    ("4. System Of Audit", "4. SYSTEM OF AUDIT"),
    ("5. Local Audit/Inspections", "5. LOCAL AUDIT/INSPECTIONS"),
    ("6. Use Of It Applications In Rdso", "6. USE OF IT APPLICATIONS IN RDSO"),
    ("7. Audit Focus Areas - Check List", "7. AUDIT FOCUS AREAS"),
    ("8. Functions And Roles Of The Directorates", "8. FUNCTIONS AND ROLES OF THE DIRECTORATES")
]

# Find indices
indices = []
for name, search_str in ch21_headings:
    idx = text_21.find(search_str)
    if idx == -1 and name.startswith("7."):
        # Fallback for 7
        idx = text_21.find("7. Audit Focus")
        if idx == -1: idx = text_21.find("7. AUDIT")
    if idx == -1:
        # Fallback for others
        idx = text_21.find(search_str.title())
    indices.append((name, idx))

# Filter out not found, sort by index
valid_indices = [(n, i) for n, i in indices if i != -1]
valid_indices.sort(key=lambda x: x[1])

ch21_text_blocks = {}
for i in range(len(valid_indices)):
    name, start_idx = valid_indices[i]
    if i < len(valid_indices) - 1:
        end_idx = valid_indices[i+1][1]
        ch21_text_blocks[name] = text_21[start_idx:end_idx].strip()
    else:
        ch21_text_blocks[name] = text_21[start_idx:].strip()

# Add 1 to 7 chunks (if found)
for i in range(7):
    name, _ = ch21_headings[i]
    if name in ch21_text_blocks:
        final_chunks.append({
            "chapter": "21",
            "title": "Research Designs and Standards Organization (RDSO)",
            "heading": name,
            "text": ch21_text_blocks[name],
            "page.no": "N/A",
            "has_table": False,
            "table_html": "N/A"
        })
    else:
        final_chunks.append({
            "chapter": "21",
            "title": "Research Designs and Standards Organization (RDSO)",
            "heading": name,
            "text": "",
            "page.no": "N/A",
            "has_table": False,
            "table_html": "N/A"
        })

dirs = [
    ("8.1 Carr Iage", "Carriage Directorate", "Engine Development Directorate"),
    ("8.2 Engine Development & Urban Transport & High Speed (Uths)", "Engine Development Directorate", "Motive Power Directorate"),
    ("8.3 Motive Power", "Motive Power Directorate", "Electrical Directorate"),
    ("8.4 Electrical", "Electrical Directorate", "Research Directorate"),
    ("8.5 Research", "Research Directorate", "Signal directorate"),
    ("8.6 Signal", "Signal directorate", "Traction Installation (TI) Directorate"),
    ("8.7 Traction Installation", "Traction Installation (TI) Directorate", "Track Design Directorate"),
    ("8.8 Track Design", "Track Design Directorate", "Testing Directorate"),
    ("8.9 Testing", "Testing Directorate", "Telecom Directorate"),
    ("8.10 Telecommunication", "Telecom Directorate", "The main functions of the directorate are as under"),
    ("8.11 Track Machines And Monitoring", "The main functions of the directorate are as under", "Traffic Directorate"),
    ("8.12 Traffic", "Traffic Directorate", "Wagon Directorate"),
    ("8.13 Wagon", "Wagon Directorate", "Bridge and Structures directorate"),
    ("8.14 Bridges And Structures", "Bridge and Structures directorate", "Geo-technical Engineering Directorate"),
    ("8.15 Geo-Technical Engineering", "Geo-technical Engineering Directorate", "Metallurgical and Chemical Directorate"),
    ("8.16 Metallurgical And Chemical", "Metallurgical and Chemical Directorate", "Psycho-Technical Unit"),
    ("8.17 Psycho", "Psycho-Technical Unit", "Works directorate"),
    ("8.18 Works", "Works directorate", "Administration-I"),
    ("8.19 Administration", "Administration-I", "Quality Assurance (Mechanical)"),
    ("8.20 Quality Assurance", "Quality Assurance (Mechanical)", "Quality Assurance (Civil)"),
    ("8.21 Quality Assurance", "Quality Assurance (Civil)", "Quality Assurance (S&T)"),
    ("8.22 Quality Assurance", "Quality Assurance (S&T)", "Stores Directorate"),
    ("8.23 Stores", "Stores Directorate", "Finance and Accounts Directorate"),
    ("8.24 Finance And Accounts", "Finance and Accounts Directorate", None)
]

text_8 = ch21_text_blocks.get("8. Functions And Roles Of The Directorates", "")

if text_8:
    idx_first_dir = text_8.lower().find(dirs[0][1].lower())
    intro_8 = text_8[:idx_first_dir].strip() if idx_first_dir != -1 else text_8
    final_chunks.append({
        "chapter": "21",
        "title": "Research Designs and Standards Organization (RDSO)",
        "heading": "8. Functions And Roles Of The Directorates",
        "text": intro_8,
        "page.no": "N/A",
        "has_table": False,
        "table_html": "N/A"
    })

    for i in range(len(dirs)):
        name, current_dir, next_dir = dirs[i]
        
        if current_dir == "Quality Assurance (Civil)":
            start_idx = text_8.find("Quality Assurance (Civil)")
            if start_idx == -1:
                start_idx = text_8.find("Quality Assurance-II (Civil)")
        else:
            start_idx = text_8.lower().find(current_dir.lower())
            
        if next_dir:
            if next_dir == "Quality Assurance (Civil)":
                end_idx = text_8.find("Quality Assurance (Civil)")
                if end_idx == -1:
                    end_idx = text_8.find("Quality Assurance-II (Civil)")
            else:
                end_idx = text_8.lower().find(next_dir.lower(), start_idx + len(current_dir))
        else:
            end_idx = len(text_8)
            
        if start_idx == -1:
            chunk_text = ""
        else:
            if end_idx == -1:
                end_idx = len(text_8)
            chunk_text = text_8[start_idx:end_idx].strip()
            
        final_chunks.append({
            "chapter": "21",
            "title": "Research Designs and Standards Organization (RDSO)",
            "heading": name,
            "text": chunk_text,
            "page.no": "N/A",
            "has_table": False,
            "table_html": "N/A"
        })
else:
    # If text_8 is empty for some reason
    final_chunks.append({
        "chapter": "21",
        "title": "Research Designs and Standards Organization (RDSO)",
        "heading": "8. Functions And Roles Of The Directorates",
        "text": "",
        "page.no": "N/A",
        "has_table": False,
        "table_html": "N/A"
    })
    for name, _, _ in dirs:
        final_chunks.append({
            "chapter": "21",
            "title": "Research Designs and Standards Organization (RDSO)",
            "heading": name,
            "text": "",
            "page.no": "N/A",
            "has_table": False,
            "table_html": "N/A"
        })


text_22 = ''
for c in raw_21_22:
    if c.get('chapter') == '22' or 'E-Office' in str(c.get('title', '')):
        text_22 += clean_text(c.get('text', '')) + '\n'

c22_intro_start = text_22.find("1. INTRODUCTION")
first_ch22_chunk = next((c for c in fixed_chunks if c.get('chapter') == '22'), None)
c22_intro_end = -1
if first_ch22_chunk:
    first_ch22_text = first_ch22_chunk.get('text', '')
    if len(first_ch22_text) > 50:
        c22_intro_end = text_22.find(first_ch22_text[:50])

intro_text = text_22[c22_intro_start:c22_intro_end].strip() if c22_intro_start != -1 and c22_intro_end != -1 else ""

final_chunks.append({
    "chapter": "22",
    "title": "E-Office",
    "heading": "1. Introduction",
    "text": intro_text,
    "page.no": "N/A",
    "has_table": False,
    "table_html": "N/A"
})

for c in fixed_chunks:
    if c.get('chapter') == '22':
        c['text'] = clean_text(c.get('text'))
        c['heading'] = clean_text(c.get('heading'))
        c['title'] = clean_text(c.get('title'))
        final_chunks.append(c)

with open('RAM_2022_Sixth_Edition_Fixed.jsonl', 'w', encoding='utf-8') as f:
    for c in final_chunks:
        f.write(json.dumps(c) + '\n')
print("Successfully generated RAM_2022_Sixth_Edition_Fixed.jsonl")
