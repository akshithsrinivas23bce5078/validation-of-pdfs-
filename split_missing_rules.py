import json
import re

input_file = "chunks after validation/TNGS_ClassXII_validated.jsonl"
with open(input_file, "r", encoding="utf-8") as f:
    chunks = [json.loads(line) for line in f if line.strip()]

new_chunks = []

for c in chunks:
    chapter = c.get("chapter", "")
    heading = c.get("heading", "")
    text = c.get("text", "")
    
    # 1. CLASS XII: Split 2. Appointment from 1. Constitution
    if chapter == "CLASS XII" and heading == "1. Constitution" and "2.Appointment.-" in text:
        parts = text.split("2.Appointment.-", 1)
        
        c1 = c.copy()
        c1["text"] = parts[0].strip()
        new_chunks.append(c1)
        
        c2 = c.copy()
        c2["heading"] = "2. Appointment"
        c2["text"] = "2.Appointment.-" + parts[1]
        new_chunks.append(c2)
        continue

    # 2. CLASS XII: Split 7. Tenure from 6. Unit of appointment
    if chapter == "CLASS XII" and heading == "6. Unit of appointment" and "7❖. Tenure of appointment" in text:
        parts = text.split("7❖. Tenure of appointment", 1)
        
        c1 = c.copy()
        c1["text"] = parts[0].strip()
        new_chunks.append(c1)
        
        c2 = c.copy()
        c2["heading"] = "7. Tenure of appointment of Deputy Secretary in Law Department or Under Secretary or Section Officers of any department (including Law Department) recruited by transfer from any service other than Tamil Nadu Secretariat Service"
        c2["text"] = "7❖. Tenure of appointment" + parts[1]
        new_chunks.append(c2)
        continue

    # 3. CLASS XII: Split 9. Savings from 8. Non-applicability
    if chapter == "CLASS XII" and "Non-applicability" in heading and "9❖. Savings:-" in text:
        parts = text.split("9❖. Savings:-", 1)
        
        c1 = c.copy()
        c1["text"] = parts[0].strip()
        new_chunks.append(c1)
        
        c2 = c.copy()
        c2["heading"] = "9. Savings"
        c2["text"] = "9❖. Savings:-" + parts[1]
        new_chunks.append(c2)
        continue

    # 4. CLASS XII - A: Split 2. Appointment from 1. Constitution
    if chapter == "CLASS XII - A" and heading == "1. Constitution" and "(i) Appointment:-" in text:
        parts = text.split("(i) Appointment:-", 1)
        
        c1 = c.copy()
        c1["text"] = parts[0].strip()
        new_chunks.append(c1)
        
        c2 = c.copy()
        c2["heading"] = "2. Appointment"
        c2["text"] = "(i) Appointment:-" + parts[1]
        new_chunks.append(c2)
        continue

    # If no split matched, just append the chunk
    new_chunks.append(c)

with open(input_file, "w", encoding="utf-8") as f:
    for c in new_chunks:
        f.write(json.dumps(c, ensure_ascii=False) + "\n")

print(f"Successfully split missing rules. New chunk count: {len(new_chunks)}.")
