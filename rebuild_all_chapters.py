"""
rebuild_all_chapters.py
======================
Reads the unvalidated JSONL and the toc_mapping.json to produce a perfectly
chapter-aware, heading-organized JSONL output file.

Key insight: The toc_mapping.json is ordered by chapter. We find chapter
boundaries by locating specific anchor keys, then assign each TOC heading
to its correct chapter.

Then for each chunk in the unvalidated JSONL, we look up its normalized 
title/heading against the chapter-specific TOC to find the correct proper heading.
"""
import json
import re
import os

INPUT_FILE  = r"unvalidated chunks\RAM_2022_Sixth_Edition.jsonl"
OUTPUT_FILE = r"chunks after validation\RAM_2022_Sixth_Edition.jsonl"
TOC_MAP_FILE = r"toc_mapping.json"
CH1_FILE    = r"ch1_extracted.jsonl"

with open(TOC_MAP_FILE, "r", encoding="utf-8") as f:
    TOC_MAPPING = json.load(f)

CHAPTER_TITLE_MAP = {
    "1":  "Introduction to Railway Audit Manual",
    "2":  "Audit of General Administration and Vigilance Department",
    "3":  "Audit of Accounts Department",
    "4":  "Audit of Personnel Department",
    "5":  "Audit of Medical Department",
    "6":  "Audit of Civil Engineering Department",
    "7":  "Audit of Railway Works",
    "8":  "Audit of Commercial Department",
    "9":  "Audit of Operating Department",
    "10": "Audit of Electrical Department",
    "11": "Audit of Signal and Telecommunication Department",
    "12": "Audit of Mechanical Department",
    "13": "Audit of Production Units",
    "14": "Audit of Stores Department",
    "15": "Audit of Safety Department",
    "16": "Audit of Security Department",
    "17": "Centre for Railway Information Systems",
    "18": "Rail Land Development Authority",
    "19": "Working of Railway Sports Promotion Board",
    "20": "Rail Public Sector Undertakings",
    "21": "Research Designs and Standards Organization",
    "22": "E-Office",
}

# Exact POSITION in toc_items list for each chapter's first entry
# Determined by inspection of the toc_mapping.json ordering
CHAPTER_FIRST_POS = {
    0:   "1",   # 1. Background
    28:  "2",   # 1. Brief On General Administration And Vigilance...
    46:  "3",   # 1. Brief About The Accounts Department
    157: "4",   # 1. Brief About The Department (Personnel)
    190: "5",   # 2. Organisation Hierarchy Of Medical Department
    212: "6",   # 2. Organisational Structure Of Civil Engineering...
    257: "7",   # 1. Preparation And Approval Of Drawings...
    266: "8",   # 1. About The Department (Commercial)
    319: "9",   # 1. Introduct Ion (Operating)
    384: "10",  # 2. Organisation Hierarchy Of Electrical Engineering...
    408: "11",  # 1. Brief About Signal & Telecommunication Department
    436: "12",  # 2. Organisational Setup Of Mechanical Engineering...
    480: "13",  # 1. Brief About The Production Units
    483: "14",  # 2. Organisation Hierarchy Of Stores Department
    540: "15",  # 2. Organisational Hirarchy (Safety)
    567: "16",  # 2. Organisation Hierarchy Of Security Department
    593: "17",  # 1. Introduc Tion (CRIS)
    601: "18",  # 2. Organisation Hierarchy Of RLDA
    607: "19",  # 1. Introduction (RSPB)
    613: "20",  # 2. Audit Jurisdiction (PSUs)
    619: "21",  # 2. Functions Of RDSO
    652: "22",  # 2. E-Office
}

def norm(s):
    return re.sub(r'[^A-Z0-9]+', '', s.upper())

# Build ordered list of TOC items
toc_items = list(TOC_MAPPING.items())  # [(key, value), ...]

# Use exact position-based chapter boundary assignment
chapter_start_pos = CHAPTER_FIRST_POS

sorted_starts = sorted(chapter_start_pos.items())
print("Chapter boundary positions found:")
for pos, ch in sorted_starts:
    print(f"  Chapter {ch}: pos {pos} -> {toc_items[pos][1]}")

# Assign each TOC item to a chapter
chapter_toc = {}  # ch -> list of (norm_key, proper_heading)
current_ch = "1"
anchor_set = dict(sorted_starts)

for i, (k, v) in enumerate(toc_items):
    if i in anchor_set:
        current_ch = anchor_set[i]
    if current_ch not in chapter_toc:
        chapter_toc[current_ch] = []
    # Only include 1-level and 2-level headings
    num_part = v.split()[0] if v else ""
    nums = [x for x in num_part.split('.') if x]
    if len(nums) <= 2 and re.match(r'^\d+(\.\d+)?$', num_part):
        chapter_toc[current_ch].append((norm(k), v))

print("\nChapter TOC sizes (1-level and 2-level only):")
for ch in sorted(chapter_toc.keys(), key=int):
    print(f"  Chapter {ch}: {len(chapter_toc[ch])} headings")
    for nk, v in chapter_toc[ch][:3]:
        print(f"    {v}")

# Build lookup dicts per chapter
chapter_lookup = {}  # ch -> {norm_key: proper_heading}
for ch, items in chapter_toc.items():
    chapter_lookup[ch] = {}
    for nk, v in items:
        if nk not in chapter_lookup[ch]:
            chapter_lookup[ch][nk] = v

# --- Helper functions ---
def extract_chapter_number(chapter_str):
    m = re.search(r'\b(\d+)\b', chapter_str)
    return m.group(1) if m else ''

SKIP_KEYWORDS = {
    "foreword", "preface", "samprati",
    "constitution of audit review committee", "one iaad one system",
    "notes ___", "restricted circulation",
}

def is_toc_line(chapter_str, title_str, text_str):
    if re.search(r'\.{5,}', chapter_str): return True
    if re.search(r'\.{5,}', title_str): return True
    stripped = text_str.strip()
    if re.fullmatch(r'[ivxlcdm]+', stripped, re.IGNORECASE): return True
    if re.fullmatch(r'[ivxlcdm]+ ?\d*\.?', stripped, re.IGNORECASE): return True
    return False

def should_skip(chapter_str, title_str, text_str):
    if is_toc_line(chapter_str, title_str, text_str):
        return True, "TOC line"
    combined_lower = (chapter_str + " " + title_str + " " + text_str[:200]).lower()
    for kw in SKIP_KEYWORDS:
        if kw in combined_lower:
            return True, f"contains '{kw}'"
    if re.match(r'^(annexure|appendix|annex)', title_str.strip(), re.IGNORECASE):
        return True, "annexure/appendix"
    stripped = text_str.strip()
    if len(re.sub(r'\s+', '', stripped)) < 10:
        return True, "text too short"
    if re.fullmatch(r'\d{1,3}\s+Railway Audit Mana?ual?', stripped):
        return True, "bare page footer"
    if re.match(r'^\d{1,3}[A-Z]', title_str.strip()):
        return True, "footnote ref title"
    if "FOREWORD" in text_str[:200] or "PREFACE" in text_str[:200]:
        return True, "foreword/preface"
    if re.match(r'^_+$', stripped.replace('\n', '').replace(' ', '')):
        return True, "blank notes lines"
    ch_num = extract_chapter_number(chapter_str)
    if not ch_num:
        return True, "no chapter number"
    return False, ''

def clean_text(text):
    text = re.sub(r'\b\d{1,3}\s+Railway Audit Mana?ual?\b', ' ', text, flags=re.MULTILINE)
    text = re.sub(r'  +', ' ', text)
    lines = [ln.strip() for ln in text.split('\n')]
    return '\n'.join(lines).strip()

def clean_page_no(page_no):
    page_no = page_no.strip()
    m = re.match(r'^\((\d+)-(\d+)\)$', page_no)
    if m:
        s, e = int(m.group(1)), int(m.group(2))
        if s > e:
            page_no = f'({e}-{s})'
    return page_no


# --- Main processing ---
output_chunks = []
skipped = 0

with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    for lineno, line in enumerate(f, 1):
        line = line.strip()
        if not line:
            continue
        try:
            raw = json.loads(line)
        except json.JSONDecodeError:
            continue

        chapter_str = raw.get('chapter', '')
        title_str   = raw.get('title', '')
        text_str    = raw.get('text', '')
        page_no_raw = raw.get('page.no', '')

        ch_num = extract_chapter_number(chapter_str)
        if not ch_num:
            skipped += 1
            continue

        # Skip Chapter 1 - we'll inject the perfect version
        if ch_num == '1':
            skipped += 1
            continue

        skip, reason = should_skip(chapter_str, title_str, text_str)
        if skip:
            skipped += 1
            continue

        chapter_title = CHAPTER_TITLE_MAP.get(ch_num, f'Chapter {ch_num}')

        # Look up the heading using the chapter-aware TOC
        ch_lookup = chapter_lookup.get(ch_num, {})
        
        norm_title = norm(title_str)
        
        heading = ''
        if norm_title in ch_lookup:
            heading = ch_lookup[norm_title]
        else:
            # Try extracting numbered heading from text body
            m = re.search(r'(?<![^\s])(\d{1,2}\.\d{1,2}\.?\s+[A-Z][A-Za-z &,\(\)\/\-]{2,70}?)(?=\s{2,}|\n|\d{1,2}\.\s*[A-Z]|[A-Z]{3,}\s+[A-Z]{3,}|$)', text_str, re.MULTILINE)
            if m:
                heading = m.group(1).strip()
            else:
                m = re.search(r'(?<![^\s])(\d{1,2}\.\s+[A-Z][A-Z\'\- \.\&,\(\)\/]{3,75}?)(?=\s{2,}|[A-Z][a-z]|\n|\d{1,2}\.\s+[A-Z]|$)', text_str, re.MULTILINE)
                if m:
                    heading = m.group(1).strip()

        if not heading:
            heading = title_str.strip()

        body = clean_text(text_str)
        page_no = clean_page_no(page_no_raw)

        chunk = {
            'DOC_NAME':   'RAM 2022 Sixth Edition',
            'doc_id':     'RAM-9A7560D8FA',
            'chapter':    ch_num,
            'title':      chapter_title,
            'heading':    heading,
            'text':       body,
            'page.no':    page_no,
            'has_table':  False,
            'table_html': {},
        }
        output_chunks.append(chunk)

# Inject Chapter 1 chunks
try:
    ch1_chunks = []
    with open(CH1_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            c = json.loads(line)
            ch1_chunks.append(c)
    output_chunks = ch1_chunks + output_chunks
    print(f"\nInjected {len(ch1_chunks)} Chapter 1 chunks from {CH1_FILE}")
except FileNotFoundError:
    print("  [WARN] ch1_extracted.jsonl not found!")

# Sort by chapter then page
def sort_key(c):
    ch = int(c['chapter'])
    m = re.search(r'\((\d+)', c.get('page.no', ''))
    pg = int(m.group(1)) if m else 0
    return (ch, pg)

output_chunks.sort(key=sort_key)

# Merge consecutive chunks with the same chapter AND same heading
merged = []
for c in output_chunks:
    if (merged and 
        merged[-1]['chapter'] == c['chapter'] and 
        merged[-1]['heading'] == c['heading']):
        # Append text
        existing_text = merged[-1]['text'].strip()
        new_text = c['text'].strip()
        if existing_text and new_text and new_text != ' ':
            merged[-1]['text'] = existing_text + '\n' + new_text
        elif new_text != ' ':
            merged[-1]['text'] = existing_text or new_text
    else:
        merged.append(c)

print(f"\nTotal chunks before merge: {len(output_chunks)}")
print(f"Total chunks after merge:  {len(merged)}")

os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    for c in merged:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

print(f"\nOutput: {OUTPUT_FILE}")

# Per-chapter summary
print("\nPer-chapter chunk counts:")
for ch in sorted(set(c['chapter'] for c in merged), key=int):
    count = sum(1 for c in merged if c['chapter'] == ch)
    title = CHAPTER_TITLE_MAP.get(ch, '?')
    print(f"  Chapter {ch:>2}: {count:>4} chunks — {title}")
