import json
import re

filepath = r"c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\TN_Vision_2023(PHASE 1).jsonl"
with open(filepath, "r", encoding="utf-8") as f:
    chunks = [json.loads(line) for line in f if line.strip()]

sidebars = [
    r"Economic prosperity Tamil Nadu will be amongst India's most economically prosperous states by 2023",
    r"Inclusive growth Tamil Nadu will exhibit a highly inclusive growth pattern - it will largely be a poverty free state with opportunities for gainful and productive employment for all those who seek it, and will provide care for the disadvantaged, vulnerable and the destitute in the state\.",
    r"Health for all Tamil Nadu will be India's leading state on social development and will have the highest Human Development Index \(HDI\) amongst all Indian states\.",
    r"World class infrastructure Tamil Nadu will provide the best infrastructure services in India in terms of universal access to Housing, Water & Sanitation, Energy, Transportation, Irrigation, Connectivity, Healthcare, and Education\.",
    r"Healthy investment climate Tamil Nadu will be one of the top three preferred investment destinations in Asia and the most preferred in India with a reputation for efficiency and competitiveness\.",
    r"Knowledge hub and innovation capital Tamil Nadu will be known as the innovation hub and knowledge capital of India, on the strength of world class institutions in various fields and the best human talent\.",
    r"Peace, security and prosperity Tamil Nadu will ensure peace, security and prosperity for all citizens and business, enabling free movement and exchange of ideas, people and trade with other Indian States and rest of the World",
    r"Nurturing heritage and preserving ecology Tamil Nadu will preserve and care for its ecology and heritage\.",
    r"Protection against vulnerability Tamil Nadu will actively address the causes of vulnerability of the state and its people to uncertainties arising from natural causes, economic downturns, and other man-made reasons and mitigate their adverse effects",
    r"Improving the quality of institutions and governance Tamil Nadu will nurture a culture of responsive and transparent Governance that ensures progress, security, and equal opportunity to all stakeholders\."
]

for c in chunks:
    text = c["text"]
    
    # Clean footers/headers with page numbers
    text = re.sub(r'\d*\s*Vision Tamil Nadu 2023\s*:\s*Strategic Plan for Infrastructure Development in Tamil Nadu\s*\d*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\d*\s*Strategic Plan for Infrastructure Development in Tamil Nadu\s*:\s*Vision Tamil Nadu 2023\s*\d*', '', text, flags=re.IGNORECASE)
    
    # Clean sidebars
    for sb in sidebars:
        text = re.sub(sb, '', text, flags=re.IGNORECASE)
    
    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text).strip()
    
    c["text"] = text

with open(filepath, "w", encoding="utf-8") as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=True) + "\n")

print(f"Successfully cleaned unnecessary text from {len(chunks)} chunks.")
