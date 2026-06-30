import json, re
with open('debug_ch21_22.json', 'r', encoding='utf-8') as f:
    chunks = json.load(f)
text_21 = ''
for c in chunks:
    ch = str(c.get('chapter', ''))
    if ch == '21' or 'RDSO' in str(c.get('title', '')):
        text_21 += c.get('text', '') + '\n'

idx = text_21.find('1. INTRODUCTION')
text_21 = text_21[idx:]

# The text for 8 starts at "8. FUNCTIONS AND ROLES OF THE DIRECTORATES"
idx_8 = text_21.find('8. FUNCTIONS AND ROLES OF THE DIRECTORATES')
if idx_8 != -1:
    text_8 = text_21[idx_8:]
    print("Found section 8.")
    
    # Directorate names in order
    dirs = [
        "Carriage Directorate",
        "Engine Development Directorate",
        "Motive Power Directorate",
        "Electrical Directorate",
        "Research Directorate",
        "Signal directorate",
        "Traction Installation (TI) Directorate",
        "Track Design Directorate",
        "Testing Directorate",
        "Telecom Directorate",
        "Track Machines And Monitoring", # "The main functions of the directorate are as under- I) Track Monitoring"
        "Traffic Directorate",
        "Wagon Directorate",
        "Bridge and Structures directorate",
        "Geo-technical Engineering Directorate",
        "Metallurgical and Chemical Directorate",
        "Psycho-Technical Unit",
        "Works directorate",
        "Administration-I",
        "Quality Assurance (Mechanical)",
        "Quality Assurance (Civil)",
        "Quality Assurance (S&T)",
        "Stores Directorate",
        "Finance and Accounts Directorate"
    ]
    
    for d in dirs:
        idx_d = text_8.lower().find(d.lower())
        if idx_d != -1:
            print(f"Found {d} at {idx_d}")
        else:
            print(f"MISSING {d}")
