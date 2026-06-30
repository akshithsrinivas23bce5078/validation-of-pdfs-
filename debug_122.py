import json
import re

CANONICAL = ['1. Constitution', '2. Appointment', '3. Promotion', '4. Preparation of approved list']
def clean_text_no_num(text):
    text = re.sub(r'^\d+[a-zA-Z]*\.', '', text)
    return re.sub(r'[^a-zA-Z]', '', text).lower()

c1 = 'Constitution:- This Class shall consist of the joint Secreta'
c2 = 'Appointment.-- Appointment to the post shall be made by prom'
c3 = 'Promotion: Promotion to the post shall be made on grounds of'
c4 = 'Preparation Of Approved List'

active_idx = 0
for heading_text in [c1, c2, c3, c4]:
    cleaned_no_num = clean_text_no_num(heading_text)
    best_match_idx = active_idx
    for i in range(active_idx, len(CANONICAL)):
        c_clean = clean_text_no_num(CANONICAL[i])
        if c_clean and (cleaned_no_num.startswith(c_clean) or cleaned_no_num.find(c_clean) < 15):
            best_match_idx = i
            break
        if i == 0 and active_idx == 0:
            best_match_idx = 0
    active_idx = best_match_idx
    print(f"[{cleaned_no_num}] -> {CANONICAL[active_idx]}")
