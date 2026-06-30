import json
import re

FILE_PATH = r'chunks after validation\20. Chart of Account Accounting Manual Part_4_State Audit West Ben.jsonl'

with open(FILE_PATH, encoding='utf-8') as f:
    chunks = [json.loads(x) for x in f]

chapter_titles = {
    1: "Introduction",
    2: "Objective",
    3: "Structure of Function Code",
    4: "Structure of the Functionary Code",
    5: "Structure of the Field Code",
    6: "Structure of the Fund Code",
    7: "Structure of Accounting Code",
    8: "Identification Code for ULB",
    9: "Procedure for the Change in the Chart of Accounts",
    10: "Format for Change Request Form",
    11: "Format for Change Authorised Form"
}

# Preview trailing text that looks like chapter titles
for i, c in enumerate(chunks):
    text = c.get('text', '')
    match = re.search(r'\s+(\d+)\.\s+([A-Za-z\s]+)$', text, re.IGNORECASE)
    if match:
        print(f"Chunk {i} ends with chapter title: {match.group(1)}. {match.group(2).strip()}")

