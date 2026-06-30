import json
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

EXPECTED_HEADINGS = {
    "12": [
        "1. Constitution",
        "2. Appointment",
        "2A. Appointing Authority",
        "2AA. Appointing Authority",
        "2B. Appointing Authority",
        "3. Qualification",
        "4. Probation in any department other than Law",
        "5. Probation in the Law Department",
        "5A. Probation for category 4",
        "5B. Probation for category 5",
        "5C. Probation for category 6",
        "6. Unit of appointment",
        "7. Tenure of appointment of Deputy Secretary in Law Department or Under Secretary or Section Officers of any department (including Law Department) recruited by transfer from any service other than Tamil Nadu Secretariat Service",
        "8. Non-applicability of certain General Rules",
        "9. Savings"
    ],
    "12.1": [
        "1. Constitution",
        "2. Appointment",
        "3. Promotion",
        "4. Probation"
    ],
    "12.2": [
        "1. Constitution",
        "2. Appointment",
        "3. Promotion",
        "4. Preparation of approved list"
    ],
    "12.3": [
        "1. Constitution",
        "2. Appointment",
        "3. Promotion",
        "4. Preparation of approved list"
    ],
    "12.4": [
        "1. Constitution",
        "2. Appointment",
        "3. Promotion",
        "4. Preparation of approved list"
    ],
    "12.5": [
        "1. Constitution",
        "2. Appointment",
        "3. Promotion",
        "4. Preparation of approved list"
    ],
    "12.6": [
        "1. Constitution",
        "2. Appointment",
        "3. Promotion",
        "4. Preparation of approved list"
    ],
    "12.7": [
        "1. Constitution",
        "2. Appointment",
        "3. Qualifications",
        "4. Appointing Authority",
        "5. Probation",
        "6. Pay",
        "7. Preparation of approved list"
    ]
}

with open("chunks after validation/TNGS_ClassXII_validated.jsonl", encoding="utf-8") as f:
    chunks = [json.loads(line) for line in f if line.strip()]

for c in chunks:
    print(f"ch={c['chapter']} | heading={c['heading'][:60]} | text={c['text'][:60]}")
