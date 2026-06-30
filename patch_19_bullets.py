import json

FILE = r"c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\19__Opening_Balance_Sheet_Accounting_Manual_P_State_Audit_West_Ben.jsonl"

def patch():
    with open(FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    out_lines = []
    for line in lines:
        if not line.strip(): continue
        chunk = json.loads(line)
        
        # Replace middle dot with hyphen
        if 'text' in chunk:
            text = chunk['text']
            import re
            # Replace spaces around \xb7 and the char itself with \n- 
            text = re.sub(r'\s*\xb7\s*', '\n- ', text)
            # Compress multiple newlines
            text = re.sub(r'\n+', '\n', text)
            chunk['text'] = text.strip()
            
        out_lines.append(json.dumps(chunk, ensure_ascii=False) + "\n")
        
    with open(FILE, "w", encoding="utf-8") as f:
        f.writelines(out_lines)

if __name__ == "__main__":
    patch()
    print("Done")
