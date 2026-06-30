import json

CHAPTER_MAP = {
    "12": {
        "chapter": "CLASS XII",
        "title": "TAMIL NADU GENERAL SERVICE - CLASS XII"
    },
    "12.1": {
        "chapter": "CLASS XII - A",
        "title": "DEPUTY SECRETARY TO GOVERNMENT, FINANCE DEPARTMENT NOT BORNE ON THE INDIAN CIVIL ADMINISTRATIVE CADRE"
    },
    "12.2": {
        "chapter": "CLASS XII - B",
        "title": "JOINT SECRETARY TO GOVERNMENT UNDER ONE UNIT SYSTEM NOT BORNE ON THE INDIAN CIVIL ADMINISTRATIVE CADRE"
    },
    "12.3": {
        "chapter": "CLASS XII - B(1)",
        "title": "SENIOR PRINCIPAL PRIVATE SECRETARY UNDER ONE UNIT SYSTEM"
    },
    "12.4": {
        "chapter": "CLASS XII - C",
        "title": "ADDITIONAL SECRETARY TO GOVERNMENT UNDER ONE UNIT SYSTEM NOT BORNE ON THE INDIAN CIVIL ADMINISTRATIVE CADRE"
    },
    "12.5": {
        "chapter": "CLASS XII - D",
        "title": "JOINT SECRETARY TO GOVERNMENT (NON-IAS) IN FINANCE AND PLANNING, DEVELOPMENT AND SPECIAL INITIATE DEPARTMENTS"
    },
    "12.6": {
        "chapter": "CLASS XII - D(1)",
        "title": "SENIOR PRINCIPAL PRIVATE SECRETARY IN FINANCE AND PLANNING, DEVELOPMENT AND SPECIAL INITIATE DEPARTMENTS"
    },
    "12.7": {
        "chapter": "CLASS XII - E",
        "title": "DIRECTOR (TAMIL TRANSLATION) AND ASSISTANT DIRECTOR (TAMIL TRANSLATION), OFFICIAL LANGUAGE (LEGISLATIVE) WING, LAW DEPARTMENT"
    }
}

input_file = "chunks after validation/TNGS_ClassXII_validated.jsonl"
with open(input_file, "r", encoding="utf-8") as f:
    chunks = [json.loads(line) for line in f if line.strip()]

for c in chunks:
    old_ch = c.get("chapter", "")
    if old_ch in CHAPTER_MAP:
        c["chapter"] = CHAPTER_MAP[old_ch]["chapter"]
        c["title"] = CHAPTER_MAP[old_ch]["title"]

with open(input_file, "w", encoding="utf-8") as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + "\n")

print(f"Updated {len(chunks)} chunks with proper chapter and title fields.")
