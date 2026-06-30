import json
import re

filepath = r"c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\TN_Vision_2023(PHASE 1).jsonl"
with open(filepath, "r", encoding="utf-8") as f:
    chunks = [json.loads(line) for line in f if line.strip()]

headers_to_remove = [
    r"\.?2\s+Transport",
    r"\.?5\s+Agriculture",
    r"\.?8\s+Funding the infrastructure",
    r"\.?1\s+Energy",
    r"\.?3\s+Industrial and Commercial",
    r"\.?4\s+Urban Infrastructure",
    r"\.?6\s+Human Development",
    r"\.?7\s+Total Estimated Investment in Infrastructure",
    r"4\.?\s+Sectoral Investment Plans"
]

for c in chunks:
    text = c["text"]
    for h in headers_to_remove:
        # 1. Strip if it is at the very beginning of the chunk text
        text = re.sub(r"^" + h + r"\s*", "", text, flags=re.IGNORECASE)
        
        # 2. Strip if it is floating in the text surrounded by spaces
        # (Be careful, this might match " 2 Transport " but we want that if it's a floating header)
        text = re.sub(r"(?<=\s)" + h + r"(?=\s|$)", "", text, flags=re.IGNORECASE)

    # Clean up double spaces
    text = re.sub(r'\s+', ' ', text).strip()
    c["text"] = text

with open(filepath, "w", encoding="utf-8") as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=True) + "\n")

print("Fixed floating broken headers.")
