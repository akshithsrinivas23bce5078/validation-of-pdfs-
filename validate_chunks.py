import json
import re
import os

INPUT_FILE  = r"c:\Users\Akshith Srinivas\chunk-validator-one\unvalidated chunks\Maintenance manual of WAG-9 vol. III_PDA West Central Rai.jsonl"
OUTPUT_FILE = r"c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Maintenance manual of WAG-9 vol. III_PDA West Central Rai.jsonl"

# ─────────────────────────────────────────────────────────────────────────────
# Chapter-level title map
# ─────────────────────────────────────────────────────────────────────────────
CHAPTER_TITLE_MAP = {
    "6": "Air Supply & Pneumatic Brakes",
    "7": "Cab Equipment",
    "8": "Control Equipment",
}

# ─────────────────────────────────────────────────────────────────────────────
# Skip rules
# ─────────────────────────────────────────────────────────────────────────────
SKIP_SECTION_KEYWORDS = {
    "foreword", "preface", "annexure", "appendix",
    "diagram", "flowchart", "annex", "index",
}

def should_skip(section: str, text: str, chapter_no: str) -> bool:
    sec_lower = section.strip().lower()
    for kw in SKIP_SECTION_KEYWORDS:
        if kw in sec_lower:
            return True
    if not section.strip():
        if "7.7" in chapter_no:
            return False
        return True
    return False

# ─────────────────────────────────────────────────────────────────────────────
# Text cleaning — fixes OCR split-words, garbled characters, embedded
# page-headers/footers that do not belong to the actual content.
# ─────────────────────────────────────────────────────────────────────────────

# 1. Simple string substitutions (applied in order)
_STRING_FIXES = [
    # --- locomotive name ---
    ("W AG-9",        "WAG-9"),
    ("W A G-9",       "WAG-9"),
    ("V{AG-9",        "WAG-9"),
    ("vv A\\.r7",     "WAG-9"),
    ("WAG-9loco",     "WAG-9 loco"),
    ("TheWA G-9 loco","The WAG-9 loco"),
    ("TheWAG-9 loco", "The WAG-9 loco"),
    # --- split words caused by PDF line-break hyphenation ---
    ("pneu matic",    "pneumatic"),
    ("pneumatic system", "pneumatic system"),   # keep clean pass idempotent
    ("cool ing",      "cooling"),
    ("pis ton",       "piston"),
    ("resil ient",    "resilient"),
    ("suit able",     "suitable"),
    ("sup port",      "support"),
    ("flex ible",     "flexible"),
    ("discon nect",   "disconnect"),
    ("secur ing",     "securing"),
    ("de signed",     "designed"),
    ("com pressor",   "compressor"),
    ("ter minals",    "terminals"),
    ("con duit",      "conduit"),
    ("pro cedures",   "procedures"),
    ("molecu lar",    "molecular"),
    ("in gress",      "ingress"),
    ("loco motive",   "locomotive"),
    ("ma chine",      "machine"),
    ("res ervoir",    "reservoir"),
    ("equip ment",    "equipment"),
    ("dis connected", "disconnected"),
    ("pan tograph",   "pantograph"),
    ("atmos pheric",  "atmospheric"),
    ("in clude",      "include"),
    ("be tween",      "between"),
    ("impu rities",   "impurities"),
    ("sche matic",    "schematic"),
    ("stablize",      "stabilize"),
    ("sta bilize",    "stabilize"),
    ("locomo tive",   "locomotive"),
    ("stan dards",    "standards"),
    ("ve hicle",      "vehicle"),
    ("ve hi cle",     "vehicle"),
    ("hicle",         "hicle"),              # partial — do not over-correct
    ("facin·g",       "facing"),
    ("air dyer",      "air dryer"),
    ("inle.t",        "inlet"),
    # --- remaining specific fixes ---
    ("con nector",       "connector"),
    ("con nect",         "connect"),
    ("Air Dryer -13",    ""),
    (" II Remove",       " Remove"),
    ("Main Compressoe",  "Main Compressor"),
    ("Indian Railways WAG-9 Main Compressoe", ""),
    ("to wards",         "towards"),
    ("stan dards",       "standards"),
    ("locomo tive",      "locomotive"),
    ("TheWA G-9loco",    "The WAG-9 loco"),
    ("Com pressor",      "Compressor"),   # capital-C split word
    ("(4}",              "(4)"),          # curly-bracket OCR error
    ("(2}",              "(2)"),
    ("(3}",              "(3)"),
    ("(9}",              "(9)"),
    # IQ] and similar garbled checkbox/symbol sequences
    ("IQ] [] IQ] IQ] @", ""),
    ("IQ]",              ""),
    # Trailing OCR noise artifacts
    ("'l,",              ""),    # chunk 22 trailing
    ("pipe' unions",     "pipe unions"),  # apostrophe artifact in chunk 23
    # Remove stray 'Indian Railways' at tail after cleaning
    ("Indian Railways\n", ""),

    ("!dent. No.",    "Ident. No."),
    ("Ide nt. N o.",  "Ident. No."),
    ("lifres",        "litres"),
    ("Coren a P1 00", "Corena P100"),
    ("Contr91",       "Control"),
    ("Close th~",     "Close the"),
    ("{127.7)",       "(127.7)"),
    ("{SB2}",         "(SB2)"),
    ("{SB2)",         "(SB2)"),
    ("Fl2,",          "F12,"),
    ("Fl 2,",         "F12,"),
    ("F1·2,",         "F12,"),
    ("Fl2.",          "F12."),
    ("F1·2.",         "F12."),
    ("G 1,",          "G1,"),
    ("{3)",           "(3)"),
    ("{1)",           "(1)"),
    ("{4)",           "(4)"),
    ("{4}",           "(4)"),
    ("{2)",           "(2)"),
    ("{9)",           "(9)"),
    ("{4 )",          "(4)"),
    ("1 1 /4",        "1-1/4"),
    ("1 /4",          "1/4"),
    ("1 1/4",         "1-1/4"),
    ("10bar",         "10 bar"),
    ("ai :Jryer",     "air dryer"),
    ("panels \"A\", \"8\", \"C\" and \"0\"", "panels \"A\", \"B\", \"C\" and \"D\""),
    ("Panel \"8\"",   "Panel \"B\""),
    ("Panel \"0\"",   "Panel \"D\""),
    ("PanelS",        "Panel B"),
    ("PaneiB",        "Panel B"),
    ("PaneiC",        "Panel C"),
    ("PaneiD",        "Panel D"),
    ("Panef A",       "Panel A"),
    ("Memotet re corder", "Memotel recorder"),
    ("r>river's",     "Driver's"),
    ("released.lfnecessary", "released. If necessary"),
    ("0..~",          ""),
    ("r-an housing assembly", "1 Fan housing assembly"),
    ("256k8",         "256 kB"),
    ("locomo-",       "locomo"),   # partial split
    ("n .cn.r _.. ",  ""),
    ("n .cn.r _..",   ""),
    # --- specific recurring footer artifacts ---
    ("Ident. No. Indian Railways WAG-9 Main Compressor",  ""),
    ("Ident. No. Indian Railways WAG-9 Air Dryer",        ""),
    ("Ident. No. Indian Railways WAG-9 Loco-Loco Bus",    ""),
    ("!dent. No. Main Compressor Indian Railways WAG-9",  ""),
]

# 2. Regex patterns for more complex cleanups
_REGEX_FIXES = [
    # ── POWERFUL GENERAL RULE ──────────────────────────────────────────────
    # Remove ALL occurrences of embedded page footers in the form:
    #   "<Section Label> Indian Railways WAG-9 <Section Label>"
    # These appear whenever a page break fell inside a paragraph.
    # Pattern: word(s) + "Indian Railways WAG-9" + word(s) mid-text
    (r"\s+(?:[A-Za-z\-]+ )*Indian Railways WAG-9 (?:[A-Za-z\-]+ ){1,5}",
     " "),
    # Also catch when the section label before footer is multi-word
    (r"\s+[A-Z][a-zA-Z ]+ Indian Railways WAG-9 [A-Z][a-zA-Z ]+\s+",
     " "),
    # ── Specific mid-text footer patterns (page break mid-paragraph) ──────
    (r"Indian Railways WAG-9 Main Compressor\s+II\s*", ""),
    (r"Indian Railways WAG-9 Main Compressor\s*[\r\n]", " "),
    (r"Indian Railways WAG-9 Air Dryer\s*[\r\n]",      " "),
    (r"Indian Railways WAG-9 Reservoirs\s*[\r\n]",     " "),
    (r"Indian Railways WAG-9 Control Electronics\s*[\r\n]", " "),
    (r"Indian Railways WAG-9 Loco-Loco Bus\s*[\r\n]",  " "),
    (r"Indian Railways WAG-9 [A-Z][a-zA-Z ]+\s*[\r\n]", " "),
    # ── Trailing page footer + OCR garbage at very end of text ────────────
    (r"\s+Indian Railways WAG-9[\s\w~.,\"'\-\\()/?!]{0,40}$", ""),
    (r"\s+Indian Railways[\s\w~.,\"'\-\\()/?!]{0,20}$",       ""),
    (r"\s+Main Compressor[\s\d?'~.,\"\\]{0,10}$",              ""),
    (r"\s+Air Dryer[\s\d?'~.,\"\\]{0,10}$",                   ""),
    (r"\s+Loco-Loco Bus[\s\w~.'\"\\]{0,15}$",                 ""),
    (r"\s+Control Electronics[\s\w~.'\"\\]{0,15}$",            ""),
    (r"\s+Auxiliary Compressor[\s\w~.'\"\\]{0,15}$",           ""),
    (r"\s+Brake (?:Frame|Controller|Actuators)[\s\w~.'\"\\]{0,15}$", ""),
    (r"\s+Machine Room Control[\s\w~.'\"\\]{0,15}$",           ""),
    (r"\s+Cab Control[\s\w~.'\"\\]{0,15}$",                    ""),
    (r"\s+Reservoirs[\s\w~.'\"\\]{0,15}$",                     ""),
    (r"\s+Doors[\s\w~.'\"\\]{0,10}$",                          ""),
    (r"\s+Lighting[\s\w~.'\"\\]{0,10}$",                       ""),
    (r"\s+Blinds[\s\w~.'\"\\]{0,10}$",                         ""),
    (r"\s+Cab[\s\w~.'\"\\]{0,10}$",                            ""),
    (r"\s+Key Interlocking[\s\w~.'\"\\]{0,10}$",               ""),
    # ── Figure-reference artifacts embedded in text ───────────────────────
    (r"\s*0601004a\s*",                          " "),      # diagram tag
    (r"\s*3EH\\V\s+\d+.*?Main Compressor _",    ""),       # part number line
    (r"\s*Indian KauwaJ~.*?Main Compressor _",  ""),       # OCR garbage
    (r"\s*Id ent\. N o\.\s+Main Compressor.*?$",""),       # footer
    (r"\s*Ident\. No\. Main Compressor.*?$",    ""),       # footer
    (r"\s*Ident\. No\.\s*$",                    ""),       # trailing ident.
    # Diagram reference strings (garbled coordinates/arrows)
    (r"\s*-~--c:c---~-\d\s+.*?\d+\.?\d*\s+Raise", " Raise"),
    (r"\s*--\+---i\+---\d.*?~-\d+\.\d+\s*",     " "),
    (r"\s*G\"---=\"'=~-[\d.]+\s*",               " "),
    # Trailing page markers
    (r"\s+[\d?'~\"\\.\-]{1,8}\s*$",              ""),
    # Clean up multiple spaces
    (r"  +",                                     " "),
    # Trailing figure codes like "0804100n", "0804101n"
    (r"\s+\d{7}n\b",                             ""),
    # Remove stray single characters at end
    (r"\s+[A-Z~]\s*$",                           ""),
    # Remove noise like "'3 3 l" at end
    (r"\s+'[\d\s]+[a-z]?\s+Indian Railways",     " Indian Railways"),
    # Generic trailing bracket/quote noise
    (r"[\s'\"\\~]{1,5}$",                        ""),
    # C6xxxxx / C7xxxxx figure references embedded mid-text as page separators
    # e.g. "C603002 Remove..." -> "Remove..." or "C607018 Brake..." -> "Brake..."
    (r"\s+C603\s+\d+\s+",                        " "),
    (r"\s+C603\d{3,4}\s+",                       " "),   # C603002, C603006 etc.
    (r"\s+C607\d{3,4}\s+",                       " "),   # C607018, C607025 etc.
    (r"\s+C6\d{5}\s+",                           " "),   # any C6xxxxx
    (r"\s+C7\d{5}\s+",                           " "),   # any C7xxxxx
    (r"\s+C8\d{5}\s+",                           " "),   # any C8xxxxx
    # Remaining mid-text footer patterns with surrounding OCR garbage
    # e.g. "C607018 Brake Actuators Indian Railways WAG-9 WARNING:"
    (r"\s+C\d{6}\s+(?:[A-Za-z ]+ )?Indian Railways WAG-9 (?:[A-Za-z ]+ )?", " "),
    # Footers preceded by short OCR noise: "Reservoirs Indian Railways WAG-9 NOTE"
    # "Brake Actuators Indian Railways WAG-9 WARNING"
    (r"\s+Reservoirs Indian Railways WAG-9\s+", " "),
    (r"\s+Brake Actuators Indian Railways WAG-9\s+", " "),
    # Footers with OCR noise char before: "C\\ Indian Railways WAG-9 n,1 Cab"
    # "'? Indian Railways WAG-9 'V Cab"
    # "{A_ Indian Railways WAG-9 ..." — catch short-noise + Indian Railways + section
    (r"\s+[^\w\s]{0,5}\s*Indian Railways WAG-9\s+[^\w\s]{0,5}\s*[A-Z][a-zA-Z ]+\s+", " "),
    # Specific remaining cases with backslash/brace noise before footer
    # Chunk 162: "C\\ Indian Railways WAG-9 n,1 Cab Cab Heater" -> " Cab Heater"
    (r"C\\\\?\s+Indian Railways WAG-9\s+\S+\s+Cab\s+", " "),
    # Chunk 189: "{A_ Indian Railways WAG-9 ...'11 Machine Room Control"
    (r"\{[A-Z_]+\s+Indian Railways WAG-9\s+[^\s]+\s+Machine Room Control\s+", " "),
    # Broad catch: anything 1-5 chars (noise) + Indian Railways WAG-9 + anything 1-10 chars (noise) + Section
    (r"\s+\S{1,5}\s+Indian Railways WAG-9\s+\S{1,10}\s+(?:Cab|Machine Room Control|Brake|Control)\s+", " "),

    # Trailing "Indian Railways" lone at end (last regex pass)
    (r"\s+Indian Railways\s*$",                  ""),

    # Remove "AG~9" typo at end
    (r"AG~9\s*$",                                "AG-9"),
    # Remove stray punctuation artifact lines
    (r"\s+[?!,'\-~]{1,5}$",                      ""),
    # ── Add newlines before bullet points (e.g. - Battery voltmeter) ──────
    (r"(\S)\s+-\s+([A-Z])", r"\1\n- \2"),
    
    # ── Add newlines before Panel A/B/C/D subheadings ──────────────────────
    # Avoid triggering on "on Panel A", "to Panel B", etc.
    (r"(?<!\bon)(?<!\bin)(?<!\bto)(?<!\bthe)(?<!\band)(?<!\bfrom)\s+(Panel [A-D]\b)", r"\n\n\1"),
    
    # ── Add newlines before and after other known subheadings in chapter 7 ──────────
    (r"(\S)\s+(Cab Heater)\s+([A-Z])", r"\1\n\n\2\n\3"),
    (r"(\S)\s+(Cab Heater Control Switch)\s+([A-Z])", r"\1\n\n\2\n\3"),
    (r"(\S)\s+(Crew Fans)\s+([A-Z])", r"\1\n\n\2\n\3"),
    (r"(\S)\s+(Fire Extinguisher)\s+([A-Z])", r"\1\n\n\2\n\3"),
    (r"(\S)\s+(Horn Control)\s+([A-Z])", r"\1\n\n\2\n\3"),
    (r"(\S)\s+(Wiper/Washer Control)\s+([A-Z])", r"\1\n\n\2\n\3"),
    (r"(\S)\s+(TE/BE Master Controller)\s+([A-Z])", r"\1\n\n\2\n\3"),
    (r"(\S)\s+(Speedometer Recorder \(MEMOTEL\))\s+([A-Z])", r"\1\n\n\2\n\3"),
    (r"(\S)\s+(Parking Brake Pressure Gauge)\s+([A-Z])", r"\1\n\n\2\n\3"),
    (r"(\S)\s+(Cubicle F)\s+([A-Z])", r"\1\n\n\2\n\3"),
    (r"(\S)\s+(Foot Pedals)\s+([A-Z])", r"\1\n\n\2\n\3"),
    (r"(\S)\s+(Panels A, B, C, D)\s+([A-Z])", r"\1\n\n\2\n\3"),
    
    # ── Add newlines before structural cues (WARNING, NOTE, CAUTION) ──────
    (r"(\S)\s+(WARNING:)", r"\1\n\n\2"),
    (r"(\S)\s+(NOTE:)", r"\1\n\n\2"),
    (r"(\S)\s+(CAUTION:)", r"\1\n\n\2"),
    
    # ── Add logical paragraph breaks for 6.1 Functional Description ──────
    (r"(\.)\s+(Air from the atmosphere is drawn)", r"\1\n\n\2"),
    (r"(\.)\s+(The electric drive motor is connected)", r"\1\n\n\2"),
    (r"(\.)\s+(A sight glass is fitted)", r"\1\n\n\2"),
    (r"(\.)\s+(The compressors are mounted)", r"\1\n\n\2"),
    (r"(\.)\s+(Fault finding for the compressor is described)", r"\1\n\n\2"),
]

def clean_text(text: str) -> str:
    """Apply OCR correction rules to make text match the PDF content."""
    # Step 1: string substitutions
    for wrong, right in _STRING_FIXES:
        text = text.replace(wrong, right)

    # Step 2: regex substitutions
    for pattern, replacement in _REGEX_FIXES:
        text = re.sub(pattern, replacement, text, flags=re.DOTALL)

    # Step 3: collapse multiple spaces (but preserve newlines)
    lines = text.split("\n")
    lines = [re.sub(r" {2,}", " ", ln).strip() for ln in lines]
    text = "\n".join(lines)

    return text.strip()

# ─────────────────────────────────────────────────────────────────────────────
# Field builders
# ─────────────────────────────────────────────────────────────────────────────

def get_chapter_number(chapter_no: str) -> str:
    return str(chapter_no).split(".")[0].strip()

def get_title(chapter_num: str) -> str:
    return CHAPTER_TITLE_MAP.get(chapter_num, f"Chapter {chapter_num}")

def get_heading(chapter_str: str) -> str:
    return chapter_str.strip()

def normalize_table_html(raw) -> dict:
    if not raw:
        return {}
    if isinstance(raw, dict):
        return raw
    if isinstance(raw, str):
        s = raw.strip()
        if not s:
            return {}
        try:
            parsed = json.loads(s)
            if isinstance(parsed, dict):
                return parsed
        except Exception:
            pass
        return {"html": s}
    return {}

# ─────────────────────────────────────────────────────────────────────────────
# Validation helpers
# ─────────────────────────────────────────────────────────────────────────────

REQUIRED_FIELDS = {"DOC_NAME", "doc_id", "chapter", "title", "heading",
                   "text", "page.no", "has_table", "table_html"}

def validate_chunk(chunk: dict, lineno: int) -> list:
    errors = []
    for f in REQUIRED_FIELDS:
        if f not in chunk:
            errors.append(f"Line {lineno}: missing field '{f}'")
    ch = chunk.get("chapter", "")
    if not re.match(r"^\d+$", str(ch)):
        errors.append(f"Line {lineno}: chapter='{ch}' not a plain integer")
    title = chunk.get("title", "")
    if re.match(r"^\d", title):
        errors.append(f"Line {lineno}: title='{title}' must NOT start with a number")
    heading = chunk.get("heading", "")
    if not re.match(r"^\d+\.\d+", heading):
        errors.append(f"Line {lineno}: heading='{heading}' not in x.y format")
    if not chunk.get("text", "").strip():
        errors.append(f"Line {lineno}: text is empty")
    if not chunk.get("page.no", "").strip():
        errors.append(f"Line {lineno}: page.no is empty")
    if not isinstance(chunk.get("has_table"), bool):
        errors.append(f"Line {lineno}: has_table is not boolean")
    if not isinstance(chunk.get("table_html"), dict):
        errors.append(f"Line {lineno}: table_html is not a dict")
    if chunk.get("has_table") is True and "html" not in chunk.get("table_html", {}):
        errors.append(f"Line {lineno}: has_table=true but table_html missing 'html' key")
    return errors

# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def process():
    output_chunks = []
    skipped  = 0
    processed = 0
    skip_log  = []

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                raw = json.loads(line)
            except json.JSONDecodeError as e:
                print(f"  [WARN] Line {lineno}: JSON parse error - {e}")
                continue

            doc_name   = raw.get("doc_name", "")
            doc_id     = raw.get("doc_id", "")
            chapter_no = str(raw.get("chapter_no", ""))
            chapter_str= raw.get("chapter", "")
            section    = raw.get("section", "")
            text       = raw.get("text", "")
            page_range = raw.get("page_range", "")
            has_table  = raw.get("has_table", False)
            table_html = raw.get("table_html", "")

            if should_skip(section, text, chapter_no):
                skipped += 1
                msg = f"  [SKIP] Line {lineno}: chapter_no={chapter_no}, section='{section}'"
                skip_log.append(msg)
                print(msg)
                continue

            # Build fields
            chapter_num = get_chapter_number(chapter_no)
            title       = get_title(chapter_num)
            heading     = get_heading(chapter_str)
            page_no     = (page_range or "").strip()
            
            # Fix backward page ranges like (26-25) -> (25-26)
            pm = re.match(r"^\((\d+)-(\d+)\)$", page_no)
            if pm:
                start = int(pm.group(1))
                end = int(pm.group(2))
                if start > end:
                    page_no = f"({end}-{start})"
            
            tbl_html    = normalize_table_html(table_html)

            if not isinstance(has_table, bool):
                has_table = bool(has_table)

            # Prepend section label — always use "Section\n\nBody..." format
            sec_label = section.strip()
            body = text.strip()
            # Only prepend if text doesn't already start with "SectionLabel\n\n"
            if sec_label and not body.startswith(sec_label + "\n\n"):
                body = sec_label + "\n\n" + body

            # Apply OCR text cleaning
            body = clean_text(body)

            chunk = {
                "DOC_NAME":   doc_name,
                "doc_id":     doc_id,
                "chapter":    chapter_num,
                "title":      title,
                "heading":    heading,
                "text":       body,
                "page.no":    page_no,
                "has_table":  has_table,
                "table_html": tbl_html,
            }
            output_chunks.append(chunk)
            processed += 1

    # Write output
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for chunk in output_chunks:
            f.write(json.dumps(chunk, ensure_ascii=False) + "\n")

    # Validate all output chunks
    all_errors = []
    for i, chunk in enumerate(output_chunks, 1):
        errs = validate_chunk(chunk, i)
        all_errors.extend(errs)

    # Print report
    print("\n" + "="*60)
    print("CHUNK VALIDATION REPORT")
    print("="*60)
    print(f"Input chunks   : {processed + skipped}")
    print(f"Skipped        : {skipped}  (TOC pages / forbidden sections)")
    print(f"Output chunks  : {processed}")

    unique_chapters = sorted(set(c["chapter"] for c in output_chunks))
    unique_titles   = sorted(set(c["title"]   for c in output_chunks))
    unique_headings = sorted(set(c["heading"] for c in output_chunks))
    print(f"\nChapters found : {unique_chapters}")
    print(f"Titles found   : {unique_titles}")
    print(f"\nHeadings ({len(unique_headings)}):")
    for h in unique_headings:
        print(f"  {h}")

    with_table = sum(1 for c in output_chunks if c["has_table"])
    print(f"\nChunks with table : {with_table}")
    print(f"Chunks without    : {processed - with_table}")
    print(f"\nValidation errors : {len(all_errors)}")
    if all_errors:
        for e in all_errors:
            print(f"  [ERROR] {e}")
    else:
        print("  All chunks passed validation.")

    print(f"\nOutput -> {OUTPUT_FILE}")
    print("="*60)

    # Preview first 3 chunks
    print("\n--- First 3 chunks (preview) ---")
    for c in output_chunks[:3]:
        print(json.dumps(c, indent=2, ensure_ascii=False))
        print()

if __name__ == "__main__":
    process()
