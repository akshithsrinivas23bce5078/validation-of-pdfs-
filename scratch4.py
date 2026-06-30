import json
import os

file_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'
output_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl.tmp'

fixes = {
    "Para 108 - Administrative and Technical Sanction Sanction of Estimate Paragraph 77 of Municipal manual Volume I. Part I, and Paragraph 83 of Municipal Manual Volume I, Acceptance of tenders Paragraph 78 of Municipal Manual Measurement and check": "Para 108 - Administrative and Technical Sanction",
    "Para 110 - Cash book that the Cash and Bank columns are correctly used; that the entries in the receipts side have been correctly made from the chitta; Note": "Para 110 - Cash book",
    "Para 123 - Accounts Chart of Accounts Panchayat Union Accounts Receipts Expenditure Cash Cheques Bank Adjustments Voucher Adjustments Bills Received Chalan Register of Voucher Cheques Received Chitta Cash Book Pass Book Mis. Register of Receipts Bills Passed for Payment Posting Register Annual Accounts The accounts should be prepared in (the form prescribed (PU Form No. 82). The yearly total under each head as per posting register are noted in the annual account form together with opening and closing balances. In the annual account the budget figure under each head of account are also noted in column 5 against the expenditure in column 4. An abstract of account at page 2 of the annual account should then be prepared with reference to previous years account as regards opening balance and the body of present years account for receipt and expenditure. The closing balance should be worked out and tallied with the closing balance as per cash book. The following statements are appended to the Annual Accounts": "Para 123 - Accounts"
}

with open(file_path, 'r', encoding='utf-8') as fin, open(output_path, 'w', encoding='utf-8') as fout:
    for line in fin:
        data = json.loads(line)
        heading = data.get('heading', '')
        if heading in fixes:
            data['heading'] = fixes[heading]
            print(f"Fixed {fixes[heading]}")
        fout.write(json.dumps(data) + '\n')

os.replace(output_path, file_path)
