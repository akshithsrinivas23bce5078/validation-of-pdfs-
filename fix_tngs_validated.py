import json, re, copy, sys
from collections import defaultdict

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ── Read from UNVALIDATED source directly (full rebuild) ──────────────────────
UNVAL   = r"unvalidated chunks\TNGS_ClassXII_chunks.jsonl"
VAL_OUT = r"chunks after validation\TNGS_ClassXII_validated.jsonl"
BOLD    = r"tngs_bold_texts.json"
TABLES  = r"tngs_tables.json"

CLASS_MAP = {
    "Class XII":      "12",
    "Class XII-A":    "12.1",
    "Class XII-B":    "12.2",
    "Class XII-B(1)": "12.3",
    "Class XII-C":    "12.4",
    "Class XII-D":    "12.5",
    "Class XII-D(1)": "12.6",
    "Class XII-E":    "12.7",
}

# Title map for each chapter
TITLE_MAP = {
    "12":    "Tamil Nadu General Service \u2013 Class XII",
    "12.1":  "Deputy Secretary to Government, Finance Department (Not IAS Cadre)",
    "12.2":  "Joint Secretary to Government (Non-IAS) \u2013 General Secretariat Departments",
    "12.3":  "Senior Principal Private Secretary \u2013 General Secretariat Departments",
    "12.4":  "Additional Secretary to Government (Non-IAS) \u2013 General Secretariat Departments",
    "12.5":  "Joint Secretary to Government (Non-IAS) \u2013 Finance & Planning Departments",
    "12.6":  "Senior Principal Private Secretary \u2013 Finance & Planning Departments",
    "12.7":  "Director & Assistant Director (Tamil Translation), Law Department",
}

# Words that directly exclude a chunk (in heading OR title)
EXCLUDE_WORDS = [
    "annexure", "appendix", "appendices",
    "foreword", "preface", "diagram", "flowchart",
]

# ── load ──────────────────────────────────────────────────────────────────────
with open(BOLD, "r", encoding="utf-8") as f:
    bold_texts = sorted(list(set(json.load(f))), key=len, reverse=True)

with open(TABLES, "r", encoding="utf-8") as f:
    tables_data = json.load(f)

with open(UNVAL, "r", encoding="utf-8") as f:
    unval_chunks = [json.loads(line) for line in f if line.strip()]

# ── page → tables ─────────────────────────────────────────────────────────────
page_tables = defaultdict(list)
for td in tables_data:
    page_tables[td["page_num"]].append(td["table_html"])

# ── helpers ───────────────────────────────────────────────────────────────────
def first_page(page_str):
    m = re.search(r'\((\d+)-', page_str)
    if not m:
        m = re.search(r'(\d+)', page_str)
    return int(m.group(1)) if m else None

def heading_excluded(chunk):
    combined = (chunk.get("heading","") + " " + chunk.get("class_title","")).lower()
    return any(w in combined for w in EXCLUDE_WORDS)

MIN_LEN = 8   # minimum heading chars to attempt upward bold-expand

def match_bold(h):
    h = h.strip()
    if not h:
        return " "
    for bt in bold_texts:
        if len(bt) <= 5:
            continue
        if h == bt:
            return bt
        if h.startswith(bt):
            return bt                              # bt is valid prefix of h
        if bt.startswith(h) and len(h) >= MIN_LEN:
            return bt                              # expand h to bt (only if h is long enough)
    return h

# ── process unvalidated chunks ────────────────────────────────────────────────
in_annexure      = False
annexure_chapter = None
valid_chunks     = []
excluded_count   = 0

for uc in unval_chunks:
    uc = copy.deepcopy(uc)

    # Resolve chapter
    cls     = uc.get("class", "")
    chapter = CLASS_MAP.get(cls, cls)
    title   = uc.get("class_title", TITLE_MAP.get(chapter, ""))

    # ── 1. Direct heading exclusion ───────────────────────────────────────────
    if heading_excluded(uc):
        excluded_count += 1
        heading_lo = uc.get("heading", "").lower()
        if "annexure" in heading_lo:
            in_annexure      = True
            annexure_chapter = chapter
            print(f"  [EXCLUDE-ANNEXURE] ch={chapter} page={uc.get('page.no','')}")
        else:
            print(f"  [EXCLUDE] '{uc.get('heading','')[:50]}' page={uc.get('page.no','')}")
        continue

    # ── 2. Cascade-exclude annexure content ───────────────────────────────────
    if in_annexure:
        if chapter == annexure_chapter:
            excluded_count += 1
            print(f"  [EXCL-ANNEX-CONT] ch={chapter} page={uc.get('page.no','')} heading='{uc.get('heading','')[:50]}'")
            continue
        else:
            # New chapter = annexure block is over
            in_annexure      = False
            annexure_chapter = None

    # ── 3. Build validated chunk ───────────────────────────────────────────────
    c = {
        "DOC_NAME":   uc.get("DOC_NAME", "TNGS_ClassXII_11032022"),
        "doc_id":     "TNGS-B45718F47C",
        "heading":    "",
        "text":       uc.get("text", " ") or " ",
        "page.no":    uc.get("page.no", ""),
        "has_table":  False,
        "table_html": "{}",
        "chapter":    chapter,
        "title":      title,
    }

    # ── 4. Heading ─────────────────────────────────────────────────────────────
    raw_h = uc.get("heading", "").strip()
    # If raw heading equals class title, treat as blank
    if raw_h == title or raw_h == cls:
        raw_h = ""
    c["heading"] = match_bold(raw_h) if raw_h else " "

    # ── 5. Table injection ────────────────────────────────────────────────────
    page_num = first_page(c["page.no"])
    if page_num is not None and page_tables.get(page_num):
        c["has_table"]  = True
        c["table_html"] = page_tables[page_num].pop(0)
        safe = c["heading"][:55].encode("ascii","replace").decode()
        print(f"  [TABLE] page={page_num} heading='{safe}'")

    valid_chunks.append(c)

# ── write ─────────────────────────────────────────────────────────────────────
with open(VAL_OUT, "w", encoding="utf-8") as f:
    for c in valid_chunks:
        f.write(json.dumps(c, ensure_ascii=False) + "\n")

table_count = sum(1 for c in valid_chunks if c["has_table"])
remaining   = {p: ts for p, ts in page_tables.items() if ts}

print()
print(f"[OK] Written {len(valid_chunks)} chunks  (excluded: {excluded_count})")
print(f"     Chunks with has_table=true : {table_count}")
if remaining:
    print(f"     TOC-page tables (no chunks to inject into): pages {list(remaining.keys())}")
else:
    print("     All tables injected.")

# ── verification ──────────────────────────────────────────────────────────────
print()
print("=== CHUNK SUMMARY ===")
for i, c in enumerate(valid_chunks, 1):
    tbl  = "TABLE" if c["has_table"] else "     "
    safe = c["heading"][:60].encode("ascii","replace").decode()
    print(f"  [{i:02d}] ch={c['chapter']:<5} page={c['page.no']:<12} {tbl}  heading='{safe}'")
