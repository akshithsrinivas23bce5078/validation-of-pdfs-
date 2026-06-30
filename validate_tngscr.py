import json
import re
import fitz

# ── Load PDF ────────────────────────────────────────────────────────────────
doc = fitz.open(r'assigned pdfs\tngscr_rules_1973_160625.pdf')
pdf_pages = {i+1: doc[i].get_text() for i in range(len(doc))}

# ── Load unvalidated chunks ─────────────────────────────────────────────────
with open(r'unvalidated chunks\tngscr_rules_1973_160625.jsonl', 'r', encoding='utf-8') as f:
    raw = [json.loads(line) for line in f]

DOC_NAME = 'tngscr_rules_1973_160625'
DOC_ID   = 'TNGSCR-548EA16904'

# ── Chunks 8-12 are sub-items embedded inside Rule 7; merge into Rule 7 ─────
rule7_extra = ' '.join(raw[i].get('text', '').strip() for i in range(8, 13))
SKIP_IDX = set(range(8, 13))

# ── Skip sections ────────────────────────────────────────────────────────────
SKIP_SECTIONS = {'SCHEDULE_I', 'SCHEDULE_II', 'SCHEDULE_III', 'SCHEDULE_IV'}
SKIP_RULE_KW  = {'FORM NO', 'VALUATION REPORT', 'SCHEDULE_'}

# ── Short titles for Supplementary Rules (Chapter 2) ─────────────────────────
SUPP2_SHORT = {
    '1': 'Consulting a medical practitioner for obtaining leave',
    '2': 'Recommendation',
    '3': 'Purchase of resignation',
    '4': 'Deleted',
    '5': 'Refusal to receive pay',
}

# ── Chapter definitions ────────────────────────────────────────────────────────
CH_DEFS = {
    '1': "THE TAMIL NADU GOVERNMENT SERVANTS' CONDUCT RULES, 1973",
    '2': 'SUPPLEMENTARY RULES',
    '3': "THE TAMIL NADU GOVERNMENT SERVANTS' APPLICATION FOR PRIVATE EMPLOYMENT RULES, 1973",
    '4': "THE TAMIL NADU GOVERNMENT SERVANTS' APPLICATION FOR POSTS UNDER THE CENTRAL GOVERNMENT RULES, 1973",
}

# ── Walk through chunks assigning chapter context sequentially ───────────────
# For SUPPLEMENTARY_RULES we track which sub-group we're in by detecting Rule 1
# that starts a new named group.
current_supp_ch = None   # will flip to '2', '3', '4' as we see group-starters

validated = []

for i, chunk in enumerate(raw):
    if i in SKIP_IDX:
        continue

    section   = chunk.get('section', '')
    rule_no   = chunk.get('rule_no', '').strip()
    title_raw = chunk.get('title', '').strip()
    raw_text  = chunk.get('text', '').strip()
    page_range = chunk.get('page_range', '')

    # Skip schedules / forms
    if section in SKIP_SECTIONS:
        continue
    if any(kw in rule_no.upper() for kw in SKIP_RULE_KW):
        continue
    if any(kw in title_raw.upper() for kw in ['FORM NO', 'VALUATION REPORT']):
        continue

    # ── Assign chapter ────────────────────────────────────────────────────────
    if section == 'RULES':
        chapter = '1'
    elif section == 'SUPPLEMENTARY_RULES':
        # Detect group-starters by their title content
        tl = title_raw.lower()
        if rule_no == '1' and 'consulting' in tl:
            current_supp_ch = '2'   # Supplementary Rules proper
        elif rule_no == '1' and 'application for posts' in tl:
            current_supp_ch = '4'   # Application for Posts Rules (check BEFORE private employment)
        elif rule_no == '1' and ('private employment' in tl or 'may be called' in tl):
            current_supp_ch = '3'   # Private Employment Rules
        # If we haven't detected a starter yet, default to '2'
        if current_supp_ch is None:
            current_supp_ch = '2'
        chapter = current_supp_ch
    else:
        chapter = '1'

    chapter_title = CH_DEFS.get(chapter, section)

    # ── Build heading ─────────────────────────────────────────────────────────
    if chapter == '2':
        # Short title for supplementary rules
        short = SUPP2_SHORT.get(rule_no, title_raw[:50])
        heading = rule_no + '. ' + short
    elif chapter in ('3', '4'):
        # Headings: just rule number (titles are full sentences)
        heading = rule_no + '.'
    else:
        # Chapter 1: rule_no. title
        heading = rule_no + '. ' + title_raw if title_raw else rule_no + '.'

    # ── Clean text (strip repeated leading heading) ────────────────────────────
    text = raw_text
    if chapter in ('3', '4'):
        # Heading is just rule_no. — only strip the number prefix, keep the full text content
        text = re.sub(r'^\d[\d\-A-Za-z]*\.\s*', '', text).strip()
    elif chapter == '2' and title_raw:
        # Strip full "rule_no. title_raw" from start (both are in heading)
        escaped = re.escape(rule_no + '. ' + title_raw)
        text = re.sub(r'^' + escaped + r'\s*[-–—]?\s*', '', text).strip()
        if not text:
            # fallback: strip just the number
            text = re.sub(r'^\d[\d\-A-Za-z]*\.\s*', '', raw_text).strip()
    elif title_raw:
        # Ch1: strip "rule_no. title" 
        escaped = re.escape(rule_no + '. ' + title_raw)
        text = re.sub(r'^' + escaped + r'\s*', '', text).strip()
    else:
        text = re.sub(r'^' + re.escape(rule_no + '.') + r'\s*', '', text).strip()

    # Merge sub-item text into Rule 7
    if i == 7:   # Rule 7 (index 7 in raw, not in validated)
        text = text.rstrip() + ' ' + rule7_extra.strip()

    # ── Page number ───────────────────────────────────────────────────────────
    m = re.search(r'\((\d+)', page_range)
    page_no = '(' + m.group(1) + ')' if m else ''

    # ── Table detection ───────────────────────────────────────────────────────
    has_table = bool(re.search(
        r'Group\s*-?\s*[A-D]|Rs\.\s*\d|Sl\.?\s*No\.|S\.No\.',
        text))

    validated.append({
        'DOC_NAME':   DOC_NAME,
        'doc_id':     DOC_ID,
        'chapter':    chapter,
        'title':      chapter_title,
        'heading':    heading,
        'text':       text,
        'page_no':    page_no,
        'has_table':  has_table,
        'table_html': '{}',
    })

print('Total validated chunks:', len(validated))
from collections import Counter
ch_count = Counter(c['chapter'] for c in validated)
for ch in sorted(ch_count):
    titles = set(c['title'] for c in validated if c['chapter'] == ch)
    print('  Ch ' + str(ch) + ' (' + str(ch_count[ch]) + ' chunks): ' + list(titles)[0][:70])

print()
print('All headings:')
for c in validated:
    print('  [Ch' + c['chapter'] + '] ' + c['heading'][:70])

# Verify doc_id uniqueness
doc_ids = set(c['doc_id'] for c in validated)
print('\nUnique doc_ids:', doc_ids)

# Save
out = r'chunks after validation\tngscr_rules_1973_160625_validated.jsonl'
with open(out, 'w', encoding='utf-8') as f:
    for c in validated:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')
print('Saved to:', out)
