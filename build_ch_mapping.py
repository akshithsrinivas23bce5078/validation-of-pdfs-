import json
import re

with open('toc_dump.txt', 'r', encoding='utf-8') as f:
    toc_lines = [line.strip() for line in f if line.strip()]

chapter_starts = [
    (1, "1. Background"),
    (2, "Brief On General Administration And Vigilance"),
    (3, "Brief About The Accounts Department"),
    (4, "Brief About The Department"), # Personnel
    (5, "Organisation Hierarchy Of Medic Al Department"),
    (6, "Brief About Civil Engineering Department"),
    (7, "Concept Of Railway Works"),
    (8, "Brief About The Department"), # Commercial
    (9, "Introduct Ion"), # Operating
    (10, "About The Department"), # Electrical
    (11, "Brief About Signal & Telecommunication"),
    (12, "Functions Of Mechanical Department"),
    (13, "Brief About The Production Units"),
    (14, "Introduc Tion"), # Stores
    (15, "Introduction"), # Safety
    (16, "Brief On Security Department"),
    (17, "Center For Railway Information"),
    (18, "Roles And Responsibility Of Rlda"),
    (19, "Railway Sports Promotion Board"),
    (20, "List Of Railway Psus"),
    (21, "Introduction"), # RDSO
    (22, "Introduction"), # E-Office
]

def norm(t): return re.sub(r'[^a-z0-9]', '', t.lower())

ch_mapping = {}
current_ch = 0
start_idx = 0

for line in toc_lines:
    if start_idx < len(chapter_starts):
        target = norm(chapter_starts[start_idx][1])
        n_line = norm(line)
        if target in n_line:
            # We rely on the exact sequential order to handle generic titles
            current_ch = chapter_starts[start_idx][0]
            start_idx += 1
            
    ch_mapping[line] = current_ch

with open('chapter_toc_mapping.json', 'w', encoding='utf-8') as f:
    json.dump(ch_mapping, f, indent=2)

print("Generated chapter_toc_mapping.json")
