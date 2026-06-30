import json
import re
import fitz

val_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'
with open(val_path, 'r', encoding='utf-8') as f:
    val_chunks = [json.loads(line) for line in f]

def clean_text(t):
    return re.sub(r'\s+', ' ', t).strip()

doc = fitz.open(r'c:\Users\Akshith Srinivas\chunk-validator-one\assigned pdfs\Local Fund Audit Depart Manual  Vol - II.pdf')

ch_ranges = {
    '1': (16, 78),
    '2': (79, 322),
    '3': (323, 398),
    '4': (399, 514)
}

ch_texts = {'1': "", '2': "", '3': "", '4': ""}

for ch, (s, e) in ch_ranges.items():
    for p in range(s, e + 1):
        if p < len(doc):
            text = doc[p].get_text()
            ch_texts[ch] += " " + text

found_count = 0
total_count = 0

for ch in ['1', '2', '3', '4']:
    vc_list = [c for c in val_chunks if str(c['chapter']) == ch]
    giant_text = ch_texts[ch].lower()
    orig_text = ch_texts[ch]
    
    indices = [0] * len(vc_list)
    last_idx = 0
    
    for i, vc in enumerate(vc_list):
        total_count += 1
        
        title = vc['title'] if '-' not in vc['heading'] else vc['heading'].split('-', 1)[1].strip()
        para_num = str(vc.get('para'))
        
        def build_regex(text):
            words = [re.escape(w) for w in re.split(r'\W+', text.strip()) if w]
            return r'\W+'.join(words)
            
        exact_title = f"{para_num}. {title}".lower()
        pattern_str = build_regex(exact_title)
        
        search_window = giant_text[last_idx:]
        
        m = re.search(pattern_str, search_window)
        if not m:
            m = re.search(build_regex(title.lower()), search_window)
            
        if not m:
            words = [w for w in re.split(r'\W+', title.lower()) if len(w) > 3]
            if len(words) >= 2:
                m = re.search(build_regex(f"{words[0]} {words[1]}"), search_window)
                
        if not m:
            if len(words) >= 3:
                m = re.search(build_regex(f"{words[1]} {words[2]}"), search_window)

        if m:
            indices[i] = last_idx + m.start()
            last_idx = indices[i]
            found_count += 1
        else:
            indices[i] = last_idx
            
    indices.append(len(giant_text))
    
    for i in range(len(vc_list)):
        start = indices[i]
        end = indices[i+1]
        vc_list[i]['text'] = clean_text(orig_text[start:end])

print(f"Found {found_count} out of {total_count} headings sequentially.")

# Apply all typo fixes
replacements = {
    r'\bmal practice\b': 'malpractice', r'\bMal practice\b': 'Malpractice',
    r'\bsub section\b': 'subsection', r'\bSub section\b': 'Subsection',
    r'\bwith out\b': 'without', r'\bWith out\b': 'Without',
    r'\bframe work\b': 'framework', r'\bFrame work\b': 'Framework',
    r'\bover sight\b': 'oversight', r'\bOver sight\b': 'Oversight',
    r'\bguide lines\b': 'guidelines', r'\bGuide lines\b': 'Guidelines',
    r'\bnote book\b': 'notebook', r'\bNote book\b': 'Notebook',
    r'\bpass book\b': 'passbook', r'\bPass book\b': 'Passbook',
    r'\bcheck list\b': 'checklist', r'\bCheck list\b': 'Checklist',
    r'\blog book\b': 'logbook', r'\bLog book\b': 'Logbook',
    r'\bsome times\b': 'sometimes', r'\bSome times\b': 'Sometimes',
    r'\bany thing\b': 'anything', r'\bAny thing\b': 'Anything',
    r'\bany where\b': 'anywhere', r'\bAny where\b': 'Anywhere',
    r'\bevery thing\b': 'everything', r'\bEvery thing\b': 'Everything',
    r'\bguide line\b': 'guideline', r'\bGuide line\b': 'Guideline',
    r'\bhand book\b': 'handbook', r'\bHand book\b': 'Handbook',
    r'\bwork shop\b': 'workshop', r'\bWork shop\b': 'Workshop',
    r'\bout standing\b': 'outstanding', r'\bOut standing\b': 'Outstanding',
    r'\bshort fall\b': 'shortfall', r'\bShort fall\b': 'Shortfall',
    r'\bear mark\b': 'earmark', r'\bEar mark\b': 'Earmark',
    r'\bear marked\b': 'earmarked', r'\bEar marked\b': 'Earmarked',
    r'\bwater works\b': 'waterworks', r'\bWater works\b': 'Waterworks',
    r'\bover head\b': 'overhead', r'\bOver head\b': 'Overhead',
    r'\bhead quarters\b': 'headquarters', r'\bHead quarters\b': 'Headquarters',
    r'\bbank rupt\b': 'bankrupt', r'\bBank rupt\b': 'Bankrupt',
    r'\bsub division\b': 'subdivision', r'\bSub division\b': 'Subdivision',
    r'\bover drawal\b': 'overdrawal', r'\bOver drawal\b': 'Overdrawal',
    r'\btime table\b': 'timetable', r'\bTime table\b': 'Timetable',
    r'\bnon availability\b': 'non-availability', r'\bNon availability\b': 'Non-availability',
    r'\bsub rule\b': 'subrule', r'\bSub rule\b': 'Subrule',
    r'\bover payment\b': 'overpayment', r'\bOver payment\b': 'Overpayment',
    r'\bwith drawal\b': 'withdrawal', r'\bWith drawal\b': 'Withdrawal',
    r'\bmis appropriation\b': 'misappropriation', r'\bMis appropriation\b': 'Misappropriation',
    r'\bover writing\b': 'overwriting', r'\bOver writing\b': 'Overwriting',
    r'\bin flow\b': 'inflow', r'\bIn flow\b': 'Inflow',
    r'\bout flow\b': 'outflow', r'\bOut flow\b': 'Outflow',
    r'\bunder ground\b': 'underground', r'\bUnder ground\b': 'Underground',
    r'\bsafe guard\b': 'safeguard', r'\bSafe guard\b': 'Safeguard',
    r'\bin adequate\b': 'inadequate', r'\bIn adequate\b': 'Inadequate',
    r'\bwork load\b': 'workload', r'\bWork load\b': 'Workload',
    r'\bpay load\b': 'payload', r'\bPay load\b': 'Payload',
    r'\bday book\b': 'daybook', r'\bDay book\b': 'Daybook',
    r'\bpass word\b': 'password', r'\bPass word\b': 'Password',
    r'\bweb site\b': 'website', r'\bWeb site\b': 'Website',
    r'\bthere fore\b': 'therefore', r'\bThere fore\b': 'Therefore',
    r'\bwhere ever\b': 'wherever', r'\bWhere ever\b': 'Wherever',
    r'\bwhat ever\b': 'whatever', r'\bWhat ever\b': 'Whatever',
    r'\bmean while\b': 'meanwhile', r'\bMean while\b': 'Meanwhile',
    r'\bfor ever\b': 'forever', r'\bFor ever\b': 'Forever',
    r'\bany body\b': 'anybody', r'\bAny body\b': 'Anybody',
    r'\bevery body\b': 'everybody', r'\bEvery body\b': 'Everybody',
    r'\bsome body\b': 'somebody', r'\bSome body\b': 'Somebody',
    r'\bnon receipt\b': 'non-receipt', r'\bNon receipt\b': 'Non-receipt',
    r'\bnon payment\b': 'non-payment', r'\bNon payment\b': 'Non-payment',
    r'\bwith in\b': 'within', r'\bWith in\b': 'Within',
    r'\bwhere as\b': 'whereas', r'\bWhere as\b': 'Whereas',
    r'\bthere by\b': 'thereby', r'\bThere by\b': 'Thereby',
    r'\bhere in\b': 'herein', r'\bHere in\b': 'Herein',
    r'\bthere in\b': 'therein', r'\bThere in\b': 'Therein',
    r'\bin to\b': 'into', r'\bIn to\b': 'Into',
    r'\bsome thing\b': 'something', r'\bSome thing\b': 'Something',
    r'\bsome how\b': 'somehow', r'\bSome how\b': 'Somehow',
    r'\bany how\b': 'anyhow', r'\bAny how\b': 'Anyhow',
    r'\btamper proof\b': 'tamper-proof', r'\bTamper proof\b': 'Tamper-proof',
    r'\bair tight\b': 'airtight', r'\bAir tight\b': 'Airtight',
    r'\bcheck post\b': 'checkpost', r'\bCheck post\b': 'Checkpost',
    r'\btax payer\b': 'taxpayer', r'\bTax payer\b': 'Taxpayer',
    r'\bstock holder\b': 'stockholder', r'\bStock holder\b': 'Stockholder',
    r'\bshare holder\b': 'shareholder', r'\bShare holder\b': 'Shareholder',
    r'\bwater mark\b': 'watermark', r'\bWater mark\b': 'Watermark',
    r'\bstore room\b': 'storeroom', r'\bStore room\b': 'Storeroom',
    r'\bco operation\b': 'cooperation', r'\bCo operation\b': 'Cooperation',
    r'\bco operative\b': 'cooperative', r'\bCo operative\b': 'Cooperative',
    r'\bco ordinate\b': 'coordinate', r'\bCo ordinate\b': 'Coordinate',
    r'\bpre requisite\b': 'prerequisite', r'\bPre requisite\b': 'Prerequisite',
    r'\bwith draw\b': 'withdraw', r'\bWith draw\b': 'Withdraw',
    r'\bwith drew\b': 'withdrew', r'\bWith drew\b': 'Withdrew',
    r'\bwith drawn\b': 'withdrawn', r'\bWith drawn\b': 'Withdrawn',
    r'\bwith holding\b': 'withholding', r'\bWith holding\b': 'Withholding',
    r'\bwith hold\b': 'withhold', r'\bWith hold\b': 'Withhold',
    r'\bout let\b': 'outlet', r'\bOut let\b': 'Outlet',
    r'\bin let\b': 'inlet', r'\bIn let\b': 'Inlet',
    r'\bout lay\b': 'outlay', r'\bOut lay\b': 'Outlay',
    r'\blay out\b': 'layout', r'\bLay out\b': 'Layout',
    r'\bturn over\b': 'turnover', r'\bTurn over\b': 'Turnover',
    r'\bpay roll\b': 'payroll', r'\bPay roll\b': 'Payroll',
    r'\btime sheet\b': 'timesheet', r'\bTime sheet\b': 'Timesheet',
    r'\btime span\b': 'timespan', r'\bTime span\b': 'Timespan',
    r'\bover view\b': 'overview', r'\bOver view\b': 'Overview',
}

changes_made = 0
for c in val_chunks:
    text = c.get('text', '')
    original_text = text
    for pattern, replacement in replacements.items():
        text = re.sub(pattern, replacement, text)
        
    title = c.get('title', '')
    original_title = title
    for pattern, replacement in replacements.items():
        title = re.sub(pattern, replacement, title)
        
    heading = c.get('heading', '')
    original_heading = heading
    for pattern, replacement in replacements.items():
        heading = re.sub(pattern, replacement, heading)
        
    if text != original_text or title != original_title or heading != original_heading:
        c['text'] = text
        c['title'] = title
        c['heading'] = heading
        changes_made += 1

print(f"Applied typo fixes in {changes_made} chunks")

with open(val_path, 'w', encoding='utf-8') as f:
    for c in val_chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

print("Replacement complete!")
