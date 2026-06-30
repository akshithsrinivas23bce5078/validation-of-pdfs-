import json

FILE = r"c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\19__Opening_Balance_Sheet_Accounting_Manual_P_State_Audit_West_Ben.jsonl"

def patch():
    with open(FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    out_lines = []
    for line in lines:
        if not line.strip(): continue
        chunk = json.loads(line)
        
        # 3. Replace (cid:183) with -
        text = chunk.get("text", "")
        text = text.replace("(cid:183)", "-")
        
        chapter = chunk.get("chapter", "")
        
        # 1. Chapter 21: add 21.1 and 21.2 before 21.3
        if chapter == "21":
            new_text = (
                "21.1. Other funds/ grants will constitute balances of all other funds.\n"
                "21.2. Details of grants will be available in Forms 1 and 75.\n"
                "21.3. Grants received against non-depreciable asset will be credited to Capital Reserve while those received against depreciable asset will be credited to Grant against Asset."
            )
            text = new_text
            
        # 2. Chapter 25: add 25.1
        if chapter == "25":
            if "25.1" not in text:
                text = "25.1. Contingent liabilities will appear as a note to the balance sheet.\n" + text.replace("25.2", "25.2.")
                # The text may have had "25.2 In case of compulsory..." let's ensure it has a dot or newline if needed.
                # Actually, wait, let's just do a simple prepend and make sure formatting is clean.
                # The unvalidated jsonl had 25.2, 25.3, 25.4.
                
        # 4. Chapter 29: correct text
        if chapter == "29":
            text = "29.1. The Executing agency will along with the balance sheet also provide a certificate in the prescribed format. The format forms a part of the guidelines as Annexure 3."
            
        chunk["text"] = text
        out_lines.append(json.dumps(chunk, ensure_ascii=False) + "\n")
        
    with open(FILE, "w", encoding="utf-8") as f:
        f.writelines(out_lines)

if __name__ == "__main__":
    patch()
    print("Done")
