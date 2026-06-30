import json

FILE = r"c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\19__Opening_Balance_Sheet_Accounting_Manual_P_State_Audit_West_Ben.jsonl"

def patch():
    with open(FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    out_lines = []
    for line in lines:
        if not line.strip(): continue
        chunk = json.loads(line)
        
        chapter = chunk.get("chapter", "")
        
        if chapter == "25":
            new_text = (
                "25.1. Contingent liabilities will appear as a note to the balance sheet.\n"
                "25.2. In case of compulsory acquisition of land, if the amount payable is under litigation, the extra amount that could be paid, will be identified as contingent liabilities.\n"
                "25.3. In case of any other legal cases that may be pending in any of the courts in the country or abroad and may have a financial impact on the ULB, an appropriate amount of compensation for these cases, will be disclosed as contingent liabilities, if ascertainable. Otherwise a fact of it should be disclosed.\n"
                "25.4. Any other obligation which is a result of past activities, which cannot be reliably estimated and outflow of economic resources is contingent to the happening/ non-happening of certain activities."
            )
            chunk["text"] = new_text
            
        out_lines.append(json.dumps(chunk, ensure_ascii=False) + "\n")
        
    with open(FILE, "w", encoding="utf-8") as f:
        f.writelines(out_lines)

if __name__ == "__main__":
    patch()
    print("Done")
