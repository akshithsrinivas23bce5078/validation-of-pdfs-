import json

bounds = [
    (0, 23, "1"),
    (24, 35, "2"),
    (36, 62, "3"),
    (63, 88, "4"),
    (89, 113, "5"),
    (114, 161, "6"),
    (162, 177, "7"),
    (178, 207, "8"),
    (208, 234, "9"),
    (235, 258, "10"),
    (259, 290, "11"),
    (291, 325, "12"),
    (326, 329, "13"),
    (330, 356, "14"),
    (357, 376, "15"),
    (377, 402, "16"),
    (403, 411, "17"),
    (412, 417, "18"),
    (418, 423, "19"),
    (424, 429, "20"),
    (430, 459, "21"),
    (460, 467, "22")
]

with open('new_toc_mapping.json', 'r', encoding='utf-8') as f:
    toc = json.load(f)

headings = list(toc.values())
heading_to_chapter = {}

for start, end, chapter in bounds:
    for i in range(start, end + 1):
        heading_to_chapter[headings[i]] = chapter

file_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\RAM_2022_Sixth_Edition_fixed.jsonl'
with open(file_path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

for c in chunks:
    h = c.get('heading')
    if h in heading_to_chapter:
        c['chapter'] = heading_to_chapter[h]

with open(file_path, 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c) + '\n')

print("Chapters fixed in RAM_2022_Sixth_Edition_fixed.jsonl!")
