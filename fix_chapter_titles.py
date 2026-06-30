import json
import os

INPUT_FILE = r'chunks after validation\RAM_2022_Sixth_Edition_fixed.jsonl'
TEMP_FILE = r'chunks after validation\RAM_2022_Sixth_Edition_fixed_temp.jsonl'

# Correct chapter titles based on the official PDF Table of Contents
title_map = {
    "1": "Introduction to Railway Audit Manual",
    "2": "Audit of General Administration and Vigilance Department",
    "3": "Audit of Accounts Department",
    "4": "Audit of Personnel Department",
    "5": "Audit of Medical Department",
    "6": "Audit of Civil Engineering Department",
    "7": "Works Audit",
    "8": "Audit of Commercial Department",
    "9": "Operating Department",
    "10": "Audit of Electrical Department",
    "11": "Signal & Telecommunication Department",
    "12": "Audit of Mechanical Department",
    "13": "Audit of Production Units",
    "14": "Audit of Stores Department",
    "15": "Audit of Safety Department",
    "16": "Audit of Security Department",
    "17": "Centre for Railway Information Systems",
    "18": "Rail Land Development Authority",
    "19": "Working of Railway Sports Promotion Board",
    "20": "Rail Public Sector Undertakings",
    "21": "Research Designs and Standards Organization",
    "22": "E-Office"
}

with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

changed = 0
for c in chunks:
    chapter_num = c.get('chapter', '')
    if chapter_num in title_map:
        correct_title = title_map[chapter_num]
        if c.get('title') != correct_title:
            c['title'] = correct_title
            changed += 1

with open(TEMP_FILE, 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

os.replace(TEMP_FILE, INPUT_FILE)
print(f"Fixed titles for {changed} chunks.")
