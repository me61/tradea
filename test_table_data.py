#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pdfplumber

pdf_path = "anfu_2025_report.pdf"

with pdfplumber.open(pdf_path) as pdf:
    page_15 = pdf.pages[14]
    tables = page_15.extract_tables()
    
    print("=== Table 1 ===")
    for row in tables[0]:
        print(row)
    
    print("\n=== Table 2 ===")
    for row in tables[1]:
        print(row)
