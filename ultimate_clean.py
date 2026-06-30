import json
import glob
import os

folder_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation'
jsonl_files = glob.glob(os.path.join(folder_path, '*.jsonl'))

replacements = {
    '\u2018': "'", '\u2019': "'", '\u201c': '"', '\u201d': '"', '\u201f': '"',
    '\u2013': '-', '\u2014': '-', '\u2022': '*', '\u00a0': ' ', '\u00ad': '-', 
    '\u2026': '...', '\u00a3': 'Pounds ', '\u00a7': 'Section ', '\u00b0': ' degrees',
    '\u00b1': '+/-', '\u00b7': '-', '\u00e0': 'a'
}

def clean_text(text):
    if not isinstance(text, str):
        return text
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

def clean_dict(d):
    new_d = {}
    for k, v in d.items():
        if isinstance(v, str):
            new_d[k] = clean_text(v)
        elif isinstance(v, dict):
            new_d[k] = clean_dict(v)
        elif isinstance(v, list):
            new_list = []
            for item in v:
                if isinstance(item, str):
                    new_list.append(clean_text(item))
                elif isinstance(item, dict):
                    new_list.append(clean_dict(item))
                else:
                    new_list.append(item)
            new_d[k] = new_list
        else:
            new_d[k] = v
    return new_d

for filepath in jsonl_files:
    print(f"Cleaning {os.path.basename(filepath)}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    cleaned_chunks = []
    for line in lines:
        if not line.strip(): continue
        chunk = json.loads(line)
        cleaned_chunks.append(clean_dict(chunk))
            
    with open(filepath, 'w', encoding='utf-8') as f:
        for chunk in cleaned_chunks:
            f.write(json.dumps(chunk, ensure_ascii=False) + '\n')

print("Finished cleaning all files.")
