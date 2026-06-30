import json
import glob
import os
from unidecode import unidecode

folder_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation'
jsonl_files = glob.glob(os.path.join(folder_path, '*.jsonl'))

def clean_dict(d):
    new_d = {}
    for k, v in d.items():
        if isinstance(v, str):
            # Convert any unicode character to its closest ASCII equivalent
            new_d[k] = unidecode(v)
        elif isinstance(v, dict):
            new_d[k] = clean_dict(v)
        elif isinstance(v, list):
            new_list = []
            for item in v:
                if isinstance(item, str):
                    new_list.append(unidecode(item))
                elif isinstance(item, dict):
                    new_list.append(clean_dict(item))
                else:
                    new_list.append(item)
            new_d[k] = new_list
        else:
            new_d[k] = v
    return new_d

for filepath in jsonl_files:
    print(f"Applying unidecode to {os.path.basename(filepath)}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    cleaned_chunks = []
    for line in lines:
        if not line.strip(): continue
        chunk = json.loads(line)
        cleaned_chunks.append(clean_dict(chunk))
            
    with open(filepath, 'w', encoding='utf-8') as f:
        for chunk in cleaned_chunks:
            # ensure_ascii=True is now safe and guaranteed to work natively
            # because unidecode already stripped everything down to raw ASCII
            f.write(json.dumps(chunk, ensure_ascii=True) + '\n')

print("Finished fully ASCII-sanitizing all files.")
