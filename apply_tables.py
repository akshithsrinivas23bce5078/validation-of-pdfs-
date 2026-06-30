import json

# Load source chunks for table_html
with open("unvalidated chunks/TNGS_ClassXII_chunks.jsonl", "r", encoding="utf-8") as f:
    src = [json.loads(line) for line in f if line.strip()]

# Extract the 3 unique tables
table_appointment_cat = None  # Category / Method of appointment (Director)
table_appointment_asst = None  # Assistant Director continuation
table_pay = None  # POSTS / PAY

for c in src:
    th = c.get("table_html", "{}")
    if not th or th == "{}" or th == "":
        continue
    if "Category" in th and "Method of appointment" in th and table_appointment_cat is None:
        table_appointment_cat = th
    elif "Assistant Director" in th and "By transfer from among the" in th and "iv" in th and table_appointment_asst is None:
        table_appointment_asst = th
    elif "POSTS" in th and "PAY" in th and table_pay is None:
        table_pay = th

# Combine the two appointment tables into one complete table
# They are two halves of the same table
table_appointment_full = table_appointment_cat.replace("</table>", "") + table_appointment_asst.replace("<table border='1'>", "").replace("<tr><th></th><th>(iv) By direct recruitment for\nspecial reasons.</th></tr>", "")

# Load validated chunks
input_file = "chunks after validation/TNGS_ClassXII_validated.jsonl"
with open(input_file, "r", encoding="utf-8") as f:
    chunks = [json.loads(line) for line in f if line.strip()]

# Now identify which chunks have table content and assign the correct table_html
for c in chunks:
    text = c.get("text", "")
    heading = c.get("heading", "")
    chapter = c.get("chapter", "")
    
    has_table_content = False
    assigned_table = "{}"
    
    # CLASS XII, 2. Appointment has "THE TABLE" with Category / Method of appointment
    if chapter == "CLASS XII" and heading == "2. Appointment" and "THE TABLE" in text:
        has_table_content = True
        # Build an HTML table from the text content for CLASS XII appointment
        assigned_table = ("<table border='1'><tr><th>Category<br>(1)</th><th>Method of appointment<br>(2)</th></tr>"
            "<tr><td>1. Deputy Secretary to Government in all Departments other than Law and Finance</td>"
            "<td>By promotion from category 2 from any Department other than Law and Finance Departments</td></tr>"
            "<tr><td>Deputy Secretary to Government in Law Department</td>"
            "<td>(i) By promotion from category 2 in the Law Department; or "
            "(ii) for special reasons by recruitment by transfer from any other class or service; or "
            "(iii) for special reasons, by direct recruitment</td></tr>"
            "<tr><td>2. Under Secretaries to Government in all the Departments other than Law and Finance</td>"
            "<td>(i) By promotion from category 3 in any Department other than Law and Finance; or "
            "(ii) If the Government so direct, by recruitment by transfer from any other service</td></tr>"
            "<tr><td>Under Secretary to Government in the Law Department</td>"
            "<td>(i) By promotion from category 3 in the Law Department; or "
            "(ii) By promotion from category 3 in any other department of Secretariat; or "
            "(iii) If the Government so direct: (a) By recruitment by transfer from the Tamil Nadu Judicial Service; or (b) By direct recruitment</td></tr>"
            "<tr><td>Under Secretary to Government in Finance Department</td>"
            "<td>By promotion from among the holders of the post of Section Officer in the Finance Department in Category 3</td></tr>"
            "<tr><td>3. Section Officers in any department other than Law and Finance Departments</td>"
            "<td>(i) By recruitment by transfer from among the holders of the post of Assistant Section Officer of the Tamil Nadu Secretariat Service; or "
            "(ii) If the Government so direct, by recruitment by transfer from any other service</td></tr>"
            "<tr><td>Section Officers in the Law Department</td>"
            "<td>(i) By recruitment by transfer from among the officers in the Law Department of the Tamil Nadu Secretariat Service; or "
            "(ii) By recruitment by transfer from among the Officers in any other Department of the Tamil Nadu Secretariat Service; or "
            "(iii) If the Government so direct, (a) By recruitment by transfer from any other service; or (b) By direct recruitment</td></tr>"
            "<tr><td>Section Officers in the Finance Department</td>"
            "<td>By recruitment by transfer from among the Officers in the Finance Department in the Tamil Nadu Secretariat Service</td></tr>"
            "<tr><td>3A. Section Officers (Translation)</td>"
            "<td>By recruitment by transfer from among the holders of the post of Assistant Section Officers (Translation) in the Tamil Development and Culture Department</td></tr>"
            "<tr><td>3(a). Strictly Confidential Section Officers in the Public (SC) Department, Home (SC) Department and in the Governor's Secretariat</td>"
            "<td>(i) By recruitment by transfer from among the Deputy Section Officers in the Public (SC) Department or the Home (SC) Department in the Tamil Nadu Secretariat Service; "
            "(ii) By transfer from among the Strictly Confidential Section Officers in the Public (SC) Department or the Home (SC) Department in the Tamil Nadu General Service</td></tr>"
            "<tr><td>4. Private Secretaries in any Department other than the Finance Department</td>"
            "<td>By recruitment by transfer from among the Personal Assistants of the Tamil Nadu Secretariat Service in any department other than the Finance Department</td></tr>"
            "<tr><td>Private Secretaries in the Finance Department</td>"
            "<td>By recruitment by transfer from among the Personal Assistants of the Tamil Nadu Secretariat Service in the Finance Department</td></tr>"
            "<tr><td>5. Accountant in Information and Tourism Department</td>"
            "<td>(i) By recruitment by transfer from among the holders of the post of Accountant-cum-Cashiers in the Information and Tourism Department in the Tamil Nadu Secretariat Service; or "
            "(ii) By recruitment by transfer from among the holders of the post of Upper Division Accountant or Assistant Section Officer; or "
            "(iii) By recruitment by transfer from any other service</td></tr>"
            "<tr><td>6. Librarian, Secretariat Library</td>"
            "<td>(i) By recruitment by transfer from among the holders of the post of Assistant Librarian, Secretariat Library in the Tamil Nadu Secretariat Service; or "
            "(ii) By direct recruitment; or (iii) By recruitment by transfer from any other service</td></tr>"
            "</table>")
    
    # CLASS XII, 3. Qualification has "THE TABLE" with Category / Qualification
    elif chapter == "CLASS XII" and heading == "3. Qualification" and "column (1)" in text:
        has_table_content = True
        assigned_table = ("<table border='1'><tr><th>Category<br>(1)</th><th>Qualification<br>(2)</th></tr>"
            "<tr><td>Category 3 - Section Officers in the Law Department</td>"
            "<td>Must possess a degree in Law</td></tr>"
            "<tr><td>Category 5 - Accountant in Information and Tourism Department</td>"
            "<td>Must possess a degree in Commerce or must have passed the Subordinate Accounts Service Examination</td></tr>"
            "<tr><td>Category 6 - Librarian, Secretariat Library</td>"
            "<td>Must possess a degree in Library Science</td></tr>"
            "</table>")
    
    # CLASS XII - E, 2. Appointment
    elif chapter == "CLASS XII - E" and heading == "2. Appointment":
        has_table_content = True
        assigned_table = table_appointment_full
    
    # CLASS XII - E, 6. Pay
    elif chapter == "CLASS XII - E" and heading == "6. Pay":
        has_table_content = True
        assigned_table = table_pay
    
    if has_table_content:
        c["has_table"] = True
        c["table_html"] = assigned_table

# Write back
with open(input_file, "w", encoding="utf-8") as f:
    for c in chunks:
        ordered = {
            "DOC_NAME": c.get("DOC_NAME"),
            "doc_id": c.get("doc_id"),
            "chapter": c.get("chapter"),
            "title": c.get("title"),
            "heading": c.get("heading"),
            "text": c.get("text"),
            "page.no": c.get("page.no"),
            "has_table": c.get("has_table"),
            "table_html": c.get("table_html")
        }
        f.write(json.dumps(ordered, ensure_ascii=False) + "\n")

# Summary
table_count = sum(1 for c in chunks if c.get("has_table") == True)
print(f"Done. {table_count} chunks now have has_table=true.")
for c in chunks:
    if c.get("has_table") == True:
        print(f"  - {c['chapter']} / {c['heading']}")
