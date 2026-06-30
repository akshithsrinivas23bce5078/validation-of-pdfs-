import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\The Secretariat Office Manual.jsonl'

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

out = open(r'c:\Users\Akshith Srinivas\chunk-validator-one\som_all_headings.txt', 'w', encoding='utf-8')
print(f"Total chunks: {len(lines)}", file=out)

for i, line in enumerate(lines):
    d = json.loads(line)
    h = d.get('heading', '')
    ch = d.get('chapter', '')
    print(f"Line {i+1:3d} | Ch {ch:>5s} | {h}", file=out)

out.close()
print("Done. Written to som_all_headings.txt")
