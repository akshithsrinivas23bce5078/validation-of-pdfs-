import json
import re

filepath = r"c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\TN_Vision_2023(PHASE 1).jsonl"
with open(filepath, "r", encoding="utf-8") as f:
    chunks = [json.loads(line) for line in f if line.strip()]

# Let's define exactly what to replace in the text for each chunk
text_headers_to_remove = [
    r"1\.\s+Executive Summary",
    r"2\.1\s+Vision Themes",
    r"3\.1\s+Overall fiscal strategy",
    r"3\.2\s+Strategic initiative 1:\s*Thrust on manufacturing",
    r"3\.3\s+Strategic initiative 2:\s*Making SMEs vibrant",
    r"3\.4\s+Strategic initiative 3:\s*Making Tamil Nadu the knowledge capital and innovation hub",
    r"3\.5\s+Strategic initiative 4:\s*Specialisation in service offerings",
    r"3\.6\s+Strategic initiative 5:\s*Thrust on skill development",
    r"3\.7\s+Strategic initiative 6:\s*Improving Agricultural Productivity",
    r"3\.8\s+Strategic initiative 7:\s*Transforming ten cities into world class cities that become the nodes of growth across the state",
    r"3\.9\s+Strategic initiative 8:\s*Care for the vulnerable sections of society",
    r"3\.10\s+Strategic initiative 9:\s*Signature projects",
    r"3\.11\s+Strategic initiative 10:\s*Encourage PPP as a mechanism for infrastructure creation",
    r"4\.\s+Sectoral Investment Plans",
    r"4\.1\s+Energy",
    r"4\.2\s+Transport",
    r"4\.3\s+Industrial and Commercial",
    r"4\.4\s+Urban Infrastructure",
    r"4\.5\s+Agriculture",
    r"4\.6\s+Human Development",
    r"4\.7\s+Total Estimated Investment in Infrastructure",
    r"4\.8\s+Funding the infrastructure",
]

for c in chunks:
    text = c["text"]
    for header_regex in text_headers_to_remove:
        # Replaces the header in the text (case-insensitive)
        text = re.sub(header_regex, "", text, flags=re.IGNORECASE).strip()
    c["text"] = text

with open(filepath, "w", encoding="utf-8") as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=True) + "\n")

print("Successfully removed internal headings from text.")
