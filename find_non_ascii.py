import glob
import os
import re

folder_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation'
jsonl_files = glob.glob(os.path.join(folder_path, '*.jsonl'))

all_non_ascii = set()

for filepath in jsonl_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    non_ascii = set(re.findall(r'[^\x00-\x7F]', text))
    for char in non_ascii:
        all_non_ascii.add( (char, hex(ord(char))) )

print('All non-ASCII characters found across all files:')
for char, code in sorted(all_non_ascii, key=lambda x: int(x[1], 16)):
    print(f"Char: {char!r} : {code}")
