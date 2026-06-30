import json

FILE = r"c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\19__Opening_Balance_Sheet_Accounting_Manual_P_State_Audit_West_Ben.jsonl"

table_html = """<table>
  <tr>
    <th>UPDATING</th>
    <th>VERIFICATION</th>
    <th>COMPILATION</th>
  </tr>
  <tr>
    <td>
      <ul>
        <li>Updating of records and registers</li>
        <li>Preparation of records and registers</li>
        <li>Complete list of assets and liabilities</li>
      </ul>
    </td>
    <td>
      <ul>
        <li>Physical verification</li>
        <li>Cross-checking</li>
        <li>Checking with originals</li>
        <li>Valuation/ costing</li>
      </ul>
    </td>
    <td>
      <ul>
        <li>Filling in the formats</li>
        <li>Compilation of figures from various records and registers</li>
        <li>Certificate</li>
        <li>Approval by Board of councillors</li>
      </ul>
    </td>
  </tr>
</table>"""

flowchart_text = """VERIFICATION
COMPILATION
UPDATING
- Updating of records 
and registers
- Preparation of 
r e c o r d s  a n d  
registers
- Complete list of 
assets and liabilities
- Physical verifi- 
cation
- Cross-checking
- Checking with 
originals
- Valuation/ costing
- F i l l i n g  i n  t h e  
formats
- Compilation of 
f i g u r e s  f r o m  
various records and 
registers
- Certificate
- Approval by Board 
of councillors"""

def patch():
    with open(FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    out_lines = []
    for line in lines:
        if not line.strip(): continue
        chunk = json.loads(line)
        
        if chunk.get("chapter") == "4":
            chunk["has_table"] = True
            chunk["table_html"] = table_html
            
        elif chunk.get("chapter") == "6":
            # Remove the flowchart text
            import re
            text = chunk["text"]
            # To be safe against minor spacing issues, we use a regex that ignores whitespace variations
            # Actually simple string replace might fail if the spacing isn't exact.
            text = text.replace(flowchart_text + "\n", "")
            text = text.replace(flowchart_text, "")
            # Just in case there are spacing differences:
            # Let's replace the whole block by finding 'VERIFICATION' and 'of councillors\n'
            text = re.sub(r'VERIFICATION\s*COMPILATION\s*UPDATING.*?- Approval by Board \s*of councillors', '', text, flags=re.DOTALL)
            # Remove any double newlines left over
            text = re.sub(r'\n+', '\n', text)
            chunk["text"] = text.strip()
            
        out_lines.append(json.dumps(chunk, ensure_ascii=False) + "\n")
        
    with open(FILE, "w", encoding="utf-8") as f:
        f.writelines(out_lines)

if __name__ == "__main__":
    patch()
    print("Done")
