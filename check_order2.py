import json
import glob
import os

files = glob.glob(r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\*.jsonl')
for file in files:
    if 'fixed' in file or 'validated' in file or 'RAM' in file: continue
    print(f"--- {os.path.basename(file)} ---")
    with open(file, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            c = json.loads(line)
            h = c.get('heading')
            if h:
                print(f"{i:3d}: {h}")
            if i > 50:
                print('...')
                break
