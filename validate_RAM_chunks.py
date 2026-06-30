"""
validate_RAM_chunks.py
======================
Transforms and validates the unvalidated RAM_2022_Sixth_Edition.jsonl file
into the correct schema matching the sample chunk file format.

Target schema per chunk:
  DOC_NAME   : str  — "RAM 2022 Sixth Edition"
  doc_id     : str  — "RAM-9A7560D8FA"
  chapter    : str  — plain integer e.g. "1", "2", ...
  title      : str  — chapter-level title (NOT section heading)
  heading    : str  — section heading from PDF (top-level or x.x sub-heading)
  text       : str  — body text content
  page.no    : str  — page range e.g. "(34-35)"
  has_table  : bool — True if chunk contains a table
  table_html : dict — {"html": "<table>...</table>"} or {}
"""

import json
import re
import os

# ─────────────────────────────────────────────────────────────────────────────
# Paths
# ─────────────────────────────────────────────────────────────────────────────
INPUT_FILE  = r"c:\Users\Akshith Srinivas\chunk-validator-one\unvalidated chunks\RAM_2022_Sixth_Edition.jsonl"
OUTPUT_FILE = r"c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\RAM_2022_Sixth_Edition_fixed.jsonl"
TOC_MAP_FILE = r"c:\Users\Akshith Srinivas\chunk-validator-one\new_toc_mapping.json"

with open(TOC_MAP_FILE, "r", encoding="utf-8") as f:
    TOC_MAPPING = json.load(f)

# ─────────────────────────────────────────────────────────────────────────────
# Chapter title map  (chapter number → proper chapter title)
# Derived from the actual PDF table of contents
# ─────────────────────────────────────────────────────────────────────────────
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

# ─────────────────────────────────────────────────────────────────────────────
# Skip keyword sets
# ─────────────────────────────────────────────────────────────────────────────
SKIP_KEYWORDS = {
    "foreword", "preface", "index",
    # NOTE: "making of ram" removed — it IS a valid section (1.1) in Chapter 1.
    "samprati",
    "constitution of audit review committee", "one iaad one system", "oios",
    "notes ___", "restricted circulation",
}

# ─────────────────────────────────────────────────────────────────────────────
# Helper: extract chapter number from the raw "chapter" field string
# Handles forms like:
#   "CHAPTER 1 – INTRODUCTION..."
#   "Chapter 1 – Introduction..."
#   "Chapter 22 –e-Office"
#   "CHAPTER 2 - AUDIT OF GENERAL ADMINISTRATION AND"
# ─────────────────────────────────────────────────────────────────────────────
def extract_chapter_number(chapter_str: str) -> str:
    """Return the first integer found in the chapter string, or '' if none."""
    m = re.search(r"\b(\d+)\b", chapter_str)
    return m.group(1) if m else ""


# ─────────────────────────────────────────────────────────────────────────────
# Helper: is this a TOC-dump line?
# TOC lines have the chapter field contain long dot-sequences like "........"
# or have text that is only roman numerals / single page numbers.
# Lines 1–81 of the file are all TOC.
# ─────────────────────────────────────────────────────────────────────────────
def is_toc_line(chapter_str: str, title_str: str, text_str: str) -> bool:
    # TOC chapter fields contain dot-runs like "........ 1" or "………….. 14"
    if re.search(r"\.{5,}", chapter_str):
        return True
    if re.search(r"\.{5,}", title_str):
        return True
    # Text is a pure roman numeral page marker (i, ii, iii … xxviii)
    stripped = text_str.strip()
    if re.fullmatch(r"[ivxlcdm]+", stripped, re.IGNORECASE):
        return True
    # Text is ONLY a small page number like "i 6." or "vi"
    if re.fullmatch(r"[ivxlcdm]+ ?\d*\.?", stripped, re.IGNORECASE):
        return True
    return False


# ─────────────────────────────────────────────────────────────────────────────
# Helper: should this chunk be skipped entirely?
# ─────────────────────────────────────────────────────────────────────────────
def should_skip(chapter_str: str, title_str: str, text_str: str) -> tuple[bool, str]:
    """Returns (True, reason) if the chunk should be skipped, else (False, '')."""

    # 1. TOC line check
    if is_toc_line(chapter_str, title_str, text_str):
        return True, "TOC line"

    # 2. Foreword / Preface in text body
    combined_lower = (chapter_str + " " + title_str + " " + text_str[:200]).lower()
    for kw in SKIP_KEYWORDS:
        if kw in combined_lower:
            return True, f"contains '{kw}'"

    # 2b. Explicitly skip titles that are purely Annexures or Appendices
    if re.match(r"^(annexure|appendix|annex)", title_str.strip(), re.IGNORECASE):
        return True, "annexure/appendix title"

    # 3. Text is too short to be meaningful (< 10 non-space chars)
    stripped_text = text_str.strip()
    if len(re.sub(r"\s+", "", stripped_text)) < 10:
        return True, "text too short / near-empty"

    # 4. Text is only "N Railway Audit Manual" (page footer remnant)
    if re.fullmatch(r"\d{1,3}\s+Railway Audit Manual", stripped_text):
        return True, "bare page footer"

    # 5. Text is only a page number like "688 Railway Audit Manaul"
    if re.fullmatch(r"\d{1,3}\s+Railway Audit Mana?ual?", stripped_text):
        return True, "bare page footer"

    # 6. Title is clearly a footnote/citation reference (starts with footnote patterns)
    if re.match(r"^\d{1,3}[A-Z]", title_str.strip()):
        return True, "footnote reference title"

    # 7. Title is a bibliography / letter-reference fragment
    bib_patterns = [
        r"^Ministry of Railways.*letter No\.",
        r"^Para \d+",
        r"^Source-\s*Para",
        r"^As per RB letter",
        r"^Such as Performance Audit",
        r"^CR, ER, ECR",
        r"^-\s*(Other Electrical|Training/HRD)",
        r"^The data has been taken",
        r"^\d{2}\s*(Zonal)?",
    ]
    for pat in bib_patterns:
        if re.match(pat, title_str.strip()):
            return True, "footnote/citation title"

    # 8. Chunks with "In Railways, e-office operates on" type footnote titles
    if "e-office operates on" in title_str.lower():
        return True, "footnote title"

    # 9. Chapter number extraction fails (can't identify chapter)
    ch_num = extract_chapter_number(chapter_str)
    if not ch_num:
        return True, "no chapter number found"

    # 10. Title is clearly a raw table-row fragment for Indian Railway Zones table
    # (title contains a zone name + HQ + division list pattern with no body text)
    zone_keywords = [
        # Full zone names
        "Northern Railway", "Northeast Frontier Railway", "South Eastern Railway",
        "South Central Railway", "Southern Railway", "Central Railway",
        "Western Railway", "South Western", "North Western", "West Central",
        "North Central", "South East Central", "East Coast Railway",
        "East Central Railway", "Kolkata Metro", "Northeast Frontier",
        # Abbreviated table-row forms (zone name truncated, starts with HQ city or division)
        "Northeast Guwahati", "South Eastern Kolkata", "South Central Secunderabad",
        "South East Bilaspur", "East Central Hajipur", "East Coast Bhubaneswar",
        "Northern Delhi", "Southern Chennai", "Central Mumbai", "Western Mumbai",
        "South Western Hubballi", "North Western Jaipur", "West Central Jabalpur",
        "North Central Allahabad",
    ]
    for zk in zone_keywords:
        if title_str.strip().startswith(zk):
            # These are individual table rows — skip, they'll be merged in table chunk
            return True, f"Indian Railway zones table row: {zk}"

    # 11. Title is just "Representation purpose only- not to scale" (map caption)
    if "representation purpose only" in title_str.lower():
        return True, "map caption"

    # 12. Title is "List of Indian Railway Zones..." (table header, skip; table merged separately)
    if "list of indian railway zones" in title_str.lower():
        return True, "zones table header"

    # 13. Lines from Appendix-I / SAMPRATI / APPENDIX / ANNEXURE in text
    # NOTE: "MAKING OF RAM" is intentionally excluded here — the title-level
    # skip via SKIP_KEYWORDS ("appendix"/"annexure") already handles the
    # Annexure-A block.  Section 1.1 (title=MAKING OF RAM) must NOT be skipped.
    appendix_markers = ["APPENDIX-I", "APPENDIX-II", "APPENDIX-III",
                        "ANNEXURE – 'A'", "SAMPRATI"]
    for m in appendix_markers:
        if m in text_str:
            return True, f"appendix marker in text: {m}"

    # 14. "NOTES" blank lines section
    if re.match(r"^_+$", stripped_text.replace("\n", "").replace(" ", "")):
        return True, "blank notes lines"

    # 15. Heading-only line 81 (foreword + preface are embedded in it) — detect by text start
    if "FOREWORD" in text_str[:200] or "PREFACE" in text_str[:200]:
        return True, "foreword/preface text"

    return False, ""


# ─────────────────────────────────────────────────────────────────────────────
# Helper: extract a numbered section heading embedded in body text
#
# The PDF OCR preserves section numbers inside the text body, e.g.:
#   "...9 4. GENERAL DUTIES OF THE RAILWAY AUDIT BRANCH 4.1. Functions of CAG"
#   "...3. ORGANIZATIONAL STRUCTURE OF MINISTRY OF RAILWAYS"
#   "1.1 Making of RAM"
# We extract the FIRST such numbered heading and use it as the heading field.
# ─────────────────────────────────────────────────────────────────────────────

# Sub-section pattern: "4.1. Functions of CAG" or "1.1 Making of RAM" or "4.1 Background"
# Appears anywhere in text, possibly after a space or punctuation.
_SUBSEC_PAT = re.compile(
    r'(?<![\w\d])(\d{1,2}\.\d{1,2}\.?\s+[A-Z][A-Za-z &,\(\)\/\-]{2,70}?)'
    r'(?=\s{2,}|\n|\d{1,2}\.\s*[A-Z]|[A-Z]{3,}\s+[A-Z]{3,}|$)',
    re.MULTILINE,
)

# Top-level section pattern: "4. GENERAL DUTIES OF THE RAILWAY AUDIT BRANCH"
# ALL-CAPS label ensures we don’t grab normal sentences like "3. The policy is..."
# Matches anywhere in text after any word boundary.
_TOPSEC_PAT = re.compile(
    r'(?<![\w])(\d{1,2}\.\s+[A-Z][A-Z\'\- \.&,\(\)\/]{3,75}?)'
    r'(?=\s{2,}|[A-Z][a-z]|\n|\d{1,2}\.\s+[A-Z]|$)',
    re.MULTILINE,
)


def _format_numbered_heading(raw: str) -> str:
    """Format a raw numbered heading string cleanly."""
    raw = raw.strip()
    m = re.match(r'^(\d+\.(?:\d+\.?)?)\s+(.+)$', raw)
    if not m:
        return raw
    number = m.group(1)
    label  = m.group(2).strip()
    # Convert ALL-CAPS label to Title Case
    if label == label.upper() and len(label) > 3:
        label = label.title()
    # Clean trailing footnote numbers
    label = re.sub(r'\d+$', '', label).strip()
    return f"{number} {label}"


def extract_numbered_heading_from_text(text: str) -> str:
    """
    Scan text body for the first numbered section or sub-section heading.
    Priority: sub-section (x.y) > top-level (x.) to prefer the more specific label.
    Returns a formatted heading string, or '' if nothing found.
    """
    # 1. Look for sub-section first (e.g. "4.1. Functions of CAG")
    m = _SUBSEC_PAT.search(text)
    if m:
        return _format_numbered_heading(m.group(1))

    # 2. Look for top-level section (e.g. "4. GENERAL DUTIES OF THE RAILWAY AUDIT BRANCH")
    m = _TOPSEC_PAT.search(text)
    if m:
        return _format_numbered_heading(m.group(1))

    return ''


# ─────────────────────────────────────────────────────────────────────────────
# Helper: derive a clean heading from title field + text body
# Heading rules (priority order):
#   1. Numbered heading extracted from text body (x. or x.y format)
#   2. Title field already has a number prefix — keep as-is
#   3. Plain descriptive title — clean and use
# ─────────────────────────────────────────────────────────────────────────────
def derive_heading(title_str: str, text_str: str) -> str:
    """Derive the heading, preferring numbered section labels from text body."""

    # ── Priority 1: extract numbered heading from text body ───────────────
    numbered = extract_numbered_heading_from_text(text_str)
    if numbered:
        return numbered

    # ── Priority 2: title field already carries a number prefix ──────────
    title_clean = title_str.strip()
    if re.match(r'^\d+\.', title_clean):         # e.g. "4.1. Functions of CAG"
        return _format_numbered_heading(title_clean)

    # ── Priority 3: clean the title field and use as plain heading ────────
    heading = title_clean

    # Clean trailing ellipsis / page refs
    heading = re.sub(r'\s*\.{3,}.*$', '', heading).strip()

    # Clean trailing footnote superscript numbers
    heading = re.sub(r'\d+$', '', heading).strip()

    # Remove leading/trailing dashes
    heading = heading.strip('\u2013\u2014-').strip()

    # Collapse multiple spaces
    heading = re.sub(r' {2,}', ' ', heading)

    # Fallback: first sentence of text
    if not heading:
        first_sentence = text_str.strip().split('.')[0].strip()[:100]
        heading = first_sentence if first_sentence else 'Section'

    # Capitalize if ALL CAPS
    if heading == heading.upper() and len(heading) > 3:
        heading = heading.title()

    return heading


# ─────────────────────────────────────────────────────────────────────────────
# Helper: detect whether a chunk's text contains a table
# We look for multi-column spacing patterns, pipe characters, or known table
# section headers.
# ─────────────────────────────────────────────────────────────────────────────
def detect_table(title_str: str, text_str: str) -> tuple[bool, dict]:
    """Return (has_table, table_html)."""

    title_lower = title_str.lower()
    text_lower  = text_str.lower()

    # Known table-bearing sections by title
    table_title_hints = [
        "list of activities",
        "audit focus areas",
        "checklist",
        "check list",
        "organisational hierarchy",
        "organizational hierarchy",
        "organisation hierarchy",
        "organizational set up",
        "organisational set up",
        "composition of railway board",
        "broad distribution of work",
        "unreserved ticketing system",
        "passenger reservation system",
        "parcel management system",
        "daily reports",
        "monthly reports",
        "periodical reports",
    ]

    # Title-level table detection
    for hint in table_title_hints:
        if hint in title_lower:
            return True, {}

    # Text-level: look for table-like patterns
    # 1. Lines with multiple consecutive uppercase words separated by spaces (column headers)
    lines = text_str.split("\n")
    cols_pattern = re.compile(r"[A-Z]{2,}(?:\s+[A-Z]{2,}){3,}")
    for line in lines:
        if cols_pattern.search(line):
            return True, {}

    # 2. Rows that contain repeated "  " (2+ spaces between columns) on ≥3 consecutive lines
    col_sep_lines = 0
    for line in lines:
        if re.search(r"\S  {2,}\S", line):
            col_sep_lines += 1
        else:
            col_sep_lines = 0
        if col_sep_lines >= 3:
            return True, {}

    # 3. Text contains a table marker phrase
    table_phrases = [
        "table-0", "table 1", "table 2", "table 3",
        "sl. no.", "s. no.", "s.no.", "sl.no",
        "level\tmain activity", "level main activity",
    ]
    for phrase in table_phrases:
        if phrase in text_lower:
            return True, {}

    return False, {}


# ─────────────────────────────────────────────────────────────────────────────
# Helper: clean page number format
# Input examples: "(38-38)", "(2-2)", "(9-10)"
# Output: "(38-38)" — unchanged normally, but normalise reversed ranges
# ─────────────────────────────────────────────────────────────────────────────
def clean_page_no(page_no: str) -> str:
    page_no = page_no.strip()
    m = re.match(r"^\((\d+)-(\d+)\)$", page_no)
    if m:
        start, end = int(m.group(1)), int(m.group(2))
        if start > end:
            page_no = f"({end}-{start})"
    return page_no


# ─────────────────────────────────────────────────────────────────────────────
# Helper: clean body text
# Remove embedded page headers/footers, page number artifacts, etc.
# ─────────────────────────────────────────────────────────────────────────────
_TEXT_CLEANUP = [
    # Remove "N Railway Audit Manual" page headers embedded mid-text
    (r"\b\d{1,3}\s+Railway Audit Mana?ual?\b",  " "),
    # Remove lone page numbers at the start (e.g. "3 of the Comptroller...")
    (r"^\d{1,3}\s+of\s+the\s+", "of the "),
    # Collapse multiple spaces
    (r"  +",                                     " "),
    # Remove trailing/leading whitespace per line
]

def clean_text(text: str) -> str:
    for pattern, replacement in _TEXT_CLEANUP:
        text = re.sub(pattern, replacement, text, flags=re.MULTILINE)
    lines = [ln.strip() for ln in text.split("\n")]
    text  = "\n".join(lines)
    return text.strip()


# ─────────────────────────────────────────────────────────────────────────────
# Validation helper
# ─────────────────────────────────────────────────────────────────────────────
REQUIRED_FIELDS = {"DOC_NAME", "doc_id", "chapter", "title", "heading",
                   "text", "page.no", "has_table", "table_html"}

def validate_chunk(chunk: dict, lineno: int) -> list:
    errors = []
    for f in REQUIRED_FIELDS:
        if f not in chunk:
            errors.append(f"Chunk {lineno}: missing field '{f}'")

    ch = chunk.get("chapter", "")
    if not re.match(r"^\d+$", str(ch)):
        errors.append(f"Chunk {lineno}: chapter='{ch}' not a plain integer")

    title = chunk.get("title", "")
    if not title.strip():
        errors.append(f"Chunk {lineno}: title is empty")

    heading = chunk.get("heading", "")
    if not heading.strip():
        errors.append(f"Chunk {lineno}: heading is empty")

    if not chunk.get("text", "").strip():
        errors.append(f"Chunk {lineno}: text is empty")

    if not chunk.get("page.no", "").strip():
        errors.append(f"Chunk {lineno}: page.no is empty")

    if not isinstance(chunk.get("has_table"), bool):
        errors.append(f"Chunk {lineno}: has_table is not boolean")

    if not isinstance(chunk.get("table_html"), dict):
        errors.append(f"Chunk {lineno}: table_html is not a dict")

    if chunk.get("has_table") is True and "html" not in chunk.get("table_html", {}):
        # table_html can be {} if we couldn't reconstruct HTML — warn but don't error
        pass

    return errors


# ─────────────────────────────────────────────────────────────────────────────
# Build the Indian Railway Zones table chunk
# This merges lines 95–110 (the fragmented zone table rows) into one chunk
# ─────────────────────────────────────────────────────────────────────────────
ZONES_TABLE_HTML = """<table>
<thead>
<tr><th>S.No.</th><th>Railway Zone</th><th>Zone Headquarters</th><th>Divisions</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>Northern Railway</td><td>Delhi</td><td>Delhi, Ambala, Firozpur, Lucknow NR, Moradabad</td></tr>
<tr><td>2</td><td>Northeast Frontier Railway</td><td>Guwahati</td><td>Alipurduar, Katihar, Rangiya, Lumding, Tinsukia</td></tr>
<tr><td>3</td><td>South Eastern Railway</td><td>Kolkata</td><td>Adra, Chakradharpur, Kharagpur, Ranchi</td></tr>
<tr><td>4</td><td>South Central Railway</td><td>Secunderabad</td><td>Secunderabad, Hyderabad, Vijayawada, Guntakal, Guntur, Nanded</td></tr>
<tr><td>5</td><td>Southern Railway</td><td>Chennai</td><td>Chennai, Tiruchirappalli, Madurai, Palakkad, Salem, Thiruvananthapuram</td></tr>
<tr><td>6</td><td>Central Railway</td><td>Mumbai</td><td>Mumbai, Bhusawal, Pune, Solapur, Nagpur</td></tr>
<tr><td>7</td><td>Western Railway</td><td>Mumbai</td><td>Mumbai WR, Ratlam, Ahmedabad, Rajkot, Bhavnagar, Vadodara</td></tr>
<tr><td>8</td><td>South Western Railway</td><td>Hubballi</td><td>Hubballi, Bengaluru, Mysuru</td></tr>
<tr><td>9</td><td>North Western Railway</td><td>Jaipur</td><td>Jaipur, Ajmer, Bikaner, Jodhpur</td></tr>
<tr><td>10</td><td>West Central Railway</td><td>Jabalpur</td><td>Jabalpur, Bhopal, Kota</td></tr>
<tr><td>11</td><td>North Central Railway</td><td>Allahabad</td><td>Allahabad, Agra, Jhansi</td></tr>
<tr><td>12</td><td>South East Central Railway</td><td>Bilaspur</td><td>Bilaspur, Raipur, Nagpur SEC</td></tr>
<tr><td>13</td><td>East Coast Railway</td><td>Bhubaneswar</td><td>Khurda Road, Sambalpur, Waltair</td></tr>
<tr><td>14</td><td>East Central Railway</td><td>Hajipur</td><td>Dhanbad, Mughalsarai, Samastipur, Sonpur</td></tr>
<tr><td>15</td><td>Kolkata Metro Railway</td><td>Kolkata</td><td>Kolkata</td></tr>
</tbody>
</table>"""

ZONES_TABLE_CHUNK = {
    "DOC_NAME":   "RAM 2022 Sixth Edition",
    "doc_id":     "RAM-9A7560D8FA",
    "chapter":    "1",
    "title":      "Introduction to Railway Audit Manual",
    "heading":    "3. Organizational Structure of Ministry of Railways",
    "text":       (
        "List of Indian Railway Zones, their Headquarters and Divisions\n\n"
        "S.No. | Railway Zone | Zone Headquarters | Divisions\n"
        "1. Northern Railway | Delhi | Delhi, Ambala, Firozpur, Lucknow NR, Moradabad\n"
        "2. Northeast Frontier Railway | Guwahati | Alipurduar, Katihar, Rangiya, Lumding, Tinsukia\n"
        "3. South Eastern Railway | Kolkata | Adra, Chakradharpur, Kharagpur, Ranchi\n"
        "4. South Central Railway | Secunderabad | Secunderabad, Hyderabad, Vijayawada, Guntakal, Guntur, Nanded\n"
        "5. Southern Railway | Chennai | Chennai, Tiruchirappalli, Madurai, Palakkad, Salem, Thiruvananthapuram\n"
        "6. Central Railway | Mumbai | Mumbai, Bhusawal, Pune, Solapur, Nagpur\n"
        "7. Western Railway | Mumbai | Mumbai WR, Ratlam, Ahmedabad, Rajkot, Bhavnagar, Vadodara\n"
        "8. South Western Railway | Hubballi | Hubballi, Bengaluru, Mysuru\n"
        "9. North Western Railway | Jaipur | Jaipur, Ajmer, Bikaner, Jodhpur\n"
        "10. West Central Railway | Jabalpur | Jabalpur, Bhopal, Kota\n"
        "11. North Central Railway | Allahabad | Allahabad, Agra, Jhansi\n"
        "12. South East Central Railway | Bilaspur | Bilaspur, Raipur, Nagpur SEC\n"
        "13. East Coast Railway | Bhubaneswar | Khurda Road, Sambalpur, Waltair\n"
        "14. East Central Railway | Hajipur | Dhanbad, Mughalsarai, Samastipur, Sonpur\n"
        "15. Kolkata Metro Railway | Kolkata | Kolkata"
    ),
    "page.no":    "(38-38)",
    "has_table":  True,
    "table_html": {"html": ZONES_TABLE_HTML},
}

# ─────────────────────────────────────────────────────────────────────────────
# Track whether the zones table chunk has already been inserted
# ─────────────────────────────────────────────────────────────────────────────
_zones_table_inserted = False


# ─────────────────────────────────────────────────────────────────────────────
# Main processing
# ─────────────────────────────────────────────────────────────────────────────
def process():
    # ── Robust TOC mapping setup ──────────────────────────────────────────
    valid_toc = {}
    with open('chapter_toc_mapping.json', 'r', encoding='utf-8') as f:
        ch_toc = json.load(f)
    for k, ch in ch_toc.items():
        # Remove leading numbers like "7.39 "
        k_no_num = re.sub(r'^\d+(\.\d+)*\s*', '', k)
        norm_k = re.sub(r'[^A-Z0-9]+', '', k_no_num.upper())
        valid_toc[(str(ch), norm_k)] = k
        # Also store the fully normalized one just in case
        norm_full = re.sub(r'[^A-Z0-9]+', '', k.upper())
        valid_toc[(str(ch), norm_full)] = k


    output_chunks = []
    skipped       = 0
    processed     = 0
    skip_log      = []
    last_valid_heading = ""

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                raw = json.loads(line)
            except json.JSONDecodeError as e:
                print(f"  [WARN] Line {lineno}: JSON parse error — {e}")
                continue

            chapter_str = raw.get("chapter", "")
            title_str   = raw.get("title",   "")
            text_str    = raw.get("text",    "")
            page_no_raw = raw.get("page.no", "")

            # ── Extract chapter number ────────────────────────────────────
            ch_num = extract_chapter_number(chapter_str)
            if not ch_num:
                skipped += 1
                skip_log.append(f"  [SKIP] Line {lineno}: no chapter number | chapter='{chapter_str[:60]}'")
                continue

            # Skip unvalidated chunks for Chapter 1, as we will inject perfect ones later!
            if ch_num == "1":
                skipped += 1
                continue

            # ── Skip decision ─────────────────────────────────────────────
            skip, reason = should_skip(chapter_str, title_str, text_str)
            if skip:
                skipped += 1
                msg = f"  [SKIP] Line {lineno}: {reason} | chapter='{chapter_str[:60]}' title='{title_str[:60]}'"
                skip_log.append(msg)
                continue

            # ── Chapter title from map ────────────────────────────────────
            chapter_title = CHAPTER_TITLE_MAP.get(ch_num, f"Chapter {ch_num}")

            # ── Derive heading from raw title field ───────────────────────
            raw_heading = derive_heading(title_str, text_str)

            # Robust heading normalisation and forward-filling
            # Strip trailing dots and page numbers from title
            clean_title_str = re.sub(r'[\.\s]+\d+$', '', title_str)
            
            # Sometimes title_str has numbers, sometimes not. Let's do both.
            title_no_num = re.sub(r'^\d+(\.\d+)*\s*', '', clean_title_str)
            raw_head_no_num = re.sub(r'^\d+(\.\d+)*\s*', '', raw_heading)
            
            norm_heading = re.sub(r'[^A-Z0-9]+', '', raw_heading.upper())
            norm_heading_no_num = re.sub(r'[^A-Z0-9]+', '', raw_head_no_num.upper())
            
            norm_title = re.sub(r'[^A-Z0-9]+', '', clean_title_str.upper())
            norm_title_no_num = re.sub(r'[^A-Z0-9]+', '', title_no_num.upper())
            
            if (ch_num, norm_heading) in valid_toc:
                heading = valid_toc[(ch_num, norm_heading)]
                last_valid_heading = heading
            elif (ch_num, norm_heading_no_num) in valid_toc:
                heading = valid_toc[(ch_num, norm_heading_no_num)]
                last_valid_heading = heading
            elif (ch_num, norm_title) in valid_toc:
                heading = valid_toc[(ch_num, norm_title)]
                last_valid_heading = heading
            elif (ch_num, norm_title_no_num) in valid_toc:
                heading = valid_toc[(ch_num, norm_title_no_num)]
                last_valid_heading = heading
            elif last_valid_heading:
                # Forward-fill if it's a broken paragraph or 3-level heading
                heading = last_valid_heading
            else:
                heading = raw_heading

            # ── Clean text ────────────────────────────────────────────────
            body = clean_text(text_str)

            # ── Page number ───────────────────────────────────────────────
            page_no = clean_page_no(page_no_raw)

            # ── Table detection ───────────────────────────────────────────
            has_table, table_html = detect_table(title_str, body)

            # ── Construct final chunk ─────────────────────────────────────────
            chunk = {
                "DOC_NAME":   "RAM 2022 Sixth Edition",
                "doc_id":     "RAM-9A7560D8FA",
                "chapter":    ch_num,
                "title":      chapter_title,
                "original_title": title_str,
                "heading":    heading,
                "text":       body,
                "page.no":    page_no,
                "has_table":  has_table,
                "table_html": table_html,
            }
            output_chunks.append(chunk)
            processed += 1

    # ── Inject perfect Chapter 1 chunks ───────────────────────────────────
    try:
        with open('ch1_extracted.jsonl', 'r', encoding='utf-8') as f:
            for line in f:
                c = json.loads(line)
                # Assign the zones table if it's chunk 3.2
                if c["heading"] == "3.2 List Of Indian Railway Zones, Their Headquarters And Divisions":
                    c["has_table"] = True
                    c["table_html"] = {"html": ZONES_TABLE_HTML}
                    _zones_table_inserted = True
                output_chunks.append(c)
                processed += 1
    except FileNotFoundError:
        print("  [WARN] ch1_extracted.jsonl not found. Run extract_chapter1.py first.")
    # ── Sort output chunks chapter-wise and by page number ────────────────
    def sort_key(chunk):
        ch = int(chunk["chapter"])
        # Extract the first page number from the page.no string e.g. "(35-36)" -> 35
        m = re.search(r"\((\d+)", chunk.get("page.no", ""))
        page_num = int(m.group(1)) if m else 0
        return (ch, page_num)

    output_chunks.sort(key=sort_key)

    # ── Write output ──────────────────────────────────────────────────────
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for chunk in output_chunks:
            f.write(json.dumps(chunk, ensure_ascii=False) + "\n")

    # ── Validate output chunks ────────────────────────────────────────────
    all_errors = []
    for i, chunk in enumerate(output_chunks, 1):
        errs = validate_chunk(chunk, i)
        all_errors.extend(errs)

    # ── Print report ──────────────────────────────────────────────────────
    print("\n" + "=" * 70)
    print("RAM 2022 CHUNK VALIDATION REPORT")
    print("=" * 70)
    print(f"Input lines processed  : {processed + skipped}")
    print(f"Skipped (TOC/forbidden): {skipped}")
    print(f"Output chunks written  : {len(output_chunks)}")
    print(f"  (includes {1 if _zones_table_inserted else 0} merged zones-table chunk)")

    unique_chapters = sorted(set(c["chapter"] for c in output_chunks), key=int)
    print(f"\nChapters found : {unique_chapters}")

    print(f"\nPer-chapter chunk counts:")
    for ch in unique_chapters:
        count = sum(1 for c in output_chunks if c["chapter"] == ch)
        title = CHAPTER_TITLE_MAP.get(ch, "?")
        print(f"  Chapter {ch:>2}: {count:>4} chunks — {title}")

    with_table    = sum(1 for c in output_chunks if c["has_table"])
    without_table = len(output_chunks) - with_table
    print(f"\nChunks with table    : {with_table}")
    print(f"Chunks without table : {without_table}")

    print(f"\nValidation errors    : {len(all_errors)}")
    if all_errors:
        for e in all_errors[:20]:
            print(f"  [ERROR] {e}")
        if len(all_errors) > 20:
            print(f"  ... and {len(all_errors) - 20} more errors")
    else:
        print("  All chunks passed validation [OK]")

    print(f"\nOutput -> {OUTPUT_FILE}")
    print("=" * 70)

    # ── Preview first 3 output chunks ────────────────────────────────────
    print("\n--- First 3 output chunks (preview) ---")
    for c in output_chunks[:3]:
        print(json.dumps(c, indent=2, ensure_ascii=False))
        print()


if __name__ == "__main__":
    process()
