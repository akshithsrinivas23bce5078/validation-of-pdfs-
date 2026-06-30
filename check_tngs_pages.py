import json, sys
from collections import Counter
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

with open("chunks after validation/TNGS_ClassXII_validated.jsonl", encoding="utf-8") as f:
    chunks = [json.loads(l) for l in f if l.strip()]

print(f"Total chunks: {len(chunks)}")
print()

# Check all required fields present
required = ["DOC_NAME","doc_id","heading","text","page.no","has_table","table_html","chapter","title"]
all_ok = True
for i, c in enumerate(chunks, 1):
    missing = [k for k in required if k not in c]
    if missing:
        print(f"  [MISSING FIELDS] chunk {i}: {missing}")
        all_ok = False
if all_ok:
    print("Schema check PASSED - all required fields present in every chunk.")

print()

# Table summary
tables = [(i, c) for i, c in enumerate(chunks, 1) if c["has_table"]]
print(f"Chunks with has_table=true: {len(tables)}")
for i, c in tables:
    pg  = c["page.no"]
    ch  = c["chapter"]
    hd  = c["heading"][:50]
    tbl = c["table_html"][:80].replace("\n", " ")
    print(f"  [{i:02d}] page={pg} chapter={ch}")
    print(f"       heading : {hd}")
    print(f"       table_html: {tbl}...")

print()

# Chapter distribution
ch_counts = Counter(c["chapter"] for c in chunks)
print("Chapter distribution:")
for ch, cnt in sorted(ch_counts.items()):
    title = chunks[next(j for j,x in enumerate(chunks) if x["chapter"]==ch)]["title"]
    print(f"  chapter {ch:<6}: {cnt:2d} chunks  ({title[:55]})")

print()

# Exclusion check
bad_words = ["annexure","appendix","foreword","preface","diagram","flowchart"]
found_bad = False
for i, c in enumerate(chunks, 1):
    h = c.get("heading","").lower()
    for w in bad_words:
        if w in h:
            print(f"  [WARN] chunk {i}: '{w}' in heading='{c['heading'][:50]}'")
            found_bad = True
if not found_bad:
    print("Exclusion check PASSED - no forbidden words found in headings.")

# table_html validity
print()
invalid_tbl = [(i,c) for i,c in enumerate(chunks,1) if c["has_table"] and not c["table_html"].strip().startswith("<table")]
if invalid_tbl:
    for i, c in invalid_tbl:
        print(f"  [WARN] chunk {i} has_table=True but table_html invalid: {c['table_html'][:50]}")
else:
    print("Table HTML check PASSED - all table_html values start with <table>.")
