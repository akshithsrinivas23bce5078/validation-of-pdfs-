import json

input_file = "chunks after validation/TNGS_ClassXII_validated.jsonl"
with open(input_file, "r", encoding="utf-8") as f:
    chunks = [json.loads(line) for line in f if line.strip()]

# Fix each Constitution chunk to remove the title prefix and OCR residue
# The pattern is: the text starts with the TITLE in ALL CAPS, then has
# "Constitution:- This Class shall consist of the joint Secretary to Government (Non- IAS) in the"
# which is OCR residue that leaks from the first sub-class, then has the actual correct text.

for c in chunks:
    if c["heading"] != "1. Constitution":
        continue
    if c["chapter"] == "CLASS XII":
        # Already fixed above
        continue
        
    text = c["text"]
    title = c["title"]
    
    # Remove the title header if it appears at the start of text
    # The title text appears as all-caps at the beginning, ending with a period or dash
    
    # Strategy: find the actual Constitution content
    # Pattern: text has TITLE...\nConstitution:- OCR residue\nActual text
    
    # Remove the OCR residue line "Constitution:- This Class shall consist of the joint Secretary to Government (Non- IAS) in the"
    ocr_residue = "Constitution:- This Class shall consist of the joint Secretary to Government (Non- IAS) in the"
    text = text.replace(ocr_residue + "\n", "")
    
    # For CLASS XII - A, also remove the meta-text about inserting rules
    if c["chapter"] == "CLASS XII - A":
        # Remove everything before the actual constitution text
        marker = "This class shall consist of the Deputy Secretary"
        idx = text.find(marker)
        if idx != -1:
            text = "1. Constitution.- " + text[idx:]
    
    elif c["chapter"] in ["CLASS XII - B", "CLASS XII - B(1)", "CLASS XII - C", 
                           "CLASS XII - D", "CLASS XII - D(1)"]:
        # Find "This class shall consist" or "This Class shall consist" which is the actual text
        for marker in ["This class shall consist", "This Class shall consist"]:
            idx = text.find(marker)
            if idx != -1:
                text = "1. Constitution.- " + text[idx:]
                break
    
    elif c["chapter"] == "CLASS XII - E":
        # This one already has the correct format, just clean it
        marker = "1. Constitution."
        idx = text.find(marker)
        if idx != -1:
            text = text[idx:]
    
    c["text"] = text

with open(input_file, "w", encoding="utf-8") as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + "\n")

print("Fixed all Constitution texts.")
