import json

val_file = r"chunks after validation\The Secretariat Office Manual.jsonl"

def int_to_roman(num):
    val = [
        1000, 900, 500, 400,
        100, 90, 50, 40,
        10, 9, 5, 4,
        1
        ]
    syb = [
        "M", "CM", "D", "CD",
        "C", "XC", "L", "XL",
        "X", "IX", "V", "IV",
        "I"
        ]
    roman_num = ''
    i = 0
    while num > 0:
        for _ in range(num // val[i]):
            roman_num += syb[i]
            num -= val[i]
        i += 1
    return roman_num

with open(val_file, "r", encoding="utf-8") as f:
    chunks = [json.loads(l) for l in f]

for c in chunks:
    chap_str = c.get('chapter', '')
    if chap_str.isdigit():
        c['chapter'] = int_to_roman(int(chap_str))

with open(val_file, "w", encoding="utf-8") as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + "\n")

print("Chapters successfully converted to Roman numerals.")
