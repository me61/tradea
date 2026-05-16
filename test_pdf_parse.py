#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试PDF解析功能 - 查看全部页面
"""

import pdfplumber
import requests
from io import BytesIO

def test_pdf_parsing():
    pdf_path = "anfu_2025_report.pdf"
    
    print(f"正在打开 PDF 文件: {pdf_path}")
    
    with pdfplumber.open(pdf_path) as pdf:
        print(f"PDF 总页数: {len(pdf.pages)}")
        print("\n" + "="*80)
        
        # 打印所有页的文本内容，特别关注表格
        for i, page in enumerate(pdf.pages):
            print(f"\n第 {i+1} 页:")
            print("-"*80)
                
            # 检查是否有表格
            tables = page.extract_tables()
            if tables:
                print(f"找到 {len(tables)} 个表格:")
                for j, table in enumerate(tables):
                    print(f"\n表格 {j+1}:")
                    for row in table:
                        print(row)
            else:
                # 如果没有表格，打印文本内容
                text = page.extract_text()
                if text:
                    print(text)
                else:
                    print("（无文本内容）")
            print("="*80)

if __name__ == "__main__":
    test_pdf_parsing()
