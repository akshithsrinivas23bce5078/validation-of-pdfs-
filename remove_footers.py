import json
import re

filepath = r"c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\TN_Vision_2023(PHASE 1).jsonl"
with open(filepath, "r", encoding="utf-8") as f:
    chunks = [json.loads(line) for line in f if line.strip()]

footers_to_remove = [
    r"25\s+Estimate based on public domain information",
    r"1\s+US\$\s*=\s*Rs\.\s*45",
    r"Refer to Appendix 2 for a list of Upper Middle Income countries",
    r"Source:\s*CSO Estimates.*?US\$\)",
    r"Source:\s*Doing Business 2012.*?Bank",
    r"Non-manufacturing sector is mostly constituted by Construction, Mining, and Electricity generation\.",
    r"Does not include recurring expenses on training, maintenance and quality improvement",
    # Catch any superscript-like number at the start of a sentence that looks like a footnote
    # But be careful not to remove valid numbered lists!
]

for c in chunks:
    text = c["text"]
    for footer in footers_to_remove:
        text = re.sub(footer, "", text, flags=re.IGNORECASE)
    
    # clean up multiple spaces
    text = re.sub(r'\s+', ' ', text).strip()
    c["text"] = text

with open(filepath, "w", encoding="utf-8") as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=True) + "\n")

print("Footers removed.")
