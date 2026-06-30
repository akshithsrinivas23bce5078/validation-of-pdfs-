import json
with open('debug_ch21_22.json', 'r', encoding='utf-8') as f:
    raw_21_22 = json.load(f)

text_21 = ''
for c in raw_21_22:
    if c.get('chapter') == '21' or 'RDSO' in str(c.get('title', '')):
        # use the clean text
        t = c.get('text', '')
        try:
            t = t.encode('latin1').decode('unicode_escape').encode('latin1').decode('utf-8')
        except:
            pass
        t = t.replace('\u2013', '-').replace('\u2019', "'").replace('\u201c', '"').replace('\u201d', '"').replace('\u2018', "'").replace('\u00a0', ' ')
        text_21 += t + '\n'

idx_8 = text_21.find('8. FUNCTIONS AND ROLES OF THE DIRECTORATES')
text_8 = text_21[idx_8:].strip()

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

for name, current_dir, next_dir in dirs[:5]:
    start = text_8.lower().find(current_dir.lower())
    print(f"Testing {name}: start={start} for string '{current_dir}'")
