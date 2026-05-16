
# -*- coding: utf-8 -*-
"""
使用Python控制Chrome浏览器直接获取并解析PDF内容
"""

import time
import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pdfplumber
from io import BytesIO


def get_chrome_driver(headless=True):
    """配置并获取Chrome驱动"""
    chrome_options = Options()
    
    if headless:
        chrome_options.add_argument('--headless')
    
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def get_pdf_content_with_chrome(url):
    """使用Chrome浏览器获取PDF内容并解析"""
    driver = None
    try:
        print(f"正在启动Chrome浏览器...")
        driver = get_chrome_driver(headless=True)
        
        print(f"正在访问: {url}")
        driver.get(url)
        
        # 获取cookies
        cookies = driver.get_cookies()
        
        # 使用requests库下载PDF，带上cookies
        print("正在下载PDF内容...")
        session = requests.Session()
        for cookie in cookies:
            session.cookies.set(cookie['name'], cookie['value'])
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        response = session.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        print("正在解析PDF内容...")
        pdf_content = BytesIO(response.content)
        
        with pdfplumber.open(pdf_content) as pdf:
            print(f"✓ PDF加载成功，共 {len(pdf.pages)} 页")
            
            # 提取文本内容
            text_content = []
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text:
                    text_content.append(f"--- 第 {i+1} 页 ---\n{text}")
            
            full_text = '\n\n'.join(text_content)
            return full_text, len(pdf.pages)
            
    except Exception as e:
        print(f"错误: {e}")
        return None, 0
    finally:
        if driver:
            driver.quit()


def save_text_to_file(text, filename="pdf_content.txt"):
    """保存文本内容到文件"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"✓ PDF文本内容已保存到: {filename}")


def main():
    """主函数"""
    print("=" * 80)
    print("使用Chrome浏览器获取PDF内容工具")
    print("=" * 80)
    print()
    
    pdf_url = "https://static.cninfo.com.cn/finalpage/2026-03-10/1225002609.PDF"
    
    text_content, page_count = get_pdf_content_with_chrome(pdf_url)
    
    if text_content:
        print()
        print(f"✓ 成功获取PDF内容，共 {page_count} 页")
        print()
        
        # 显示前500个字符作为预览
        preview_length = min(500, len(text_content))
        print("内容预览:")
        print("-" * 80)
        print(text_content[:preview_length])
        print("-" * 80)
        print()
        
        # 保存到文件
        save_text_to_file(text_content, "chrome_pdf_content.txt")
    else:
        print()
        print("✗ 获取PDF内容失败")


if __name__ == "__main__":
    main()

