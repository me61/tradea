
# -*- coding: utf-8 -*-
"""
使用Python控制Chrome浏览器获取PDF内容
"""

import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def get_chrome_driver(headless=False):
    """配置并获取Chrome驱动"""
    chrome_options = Options()
    
    if headless:
        chrome_options.add_argument('--headless')
    
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    
    # 禁用PDF预览插件，直接下载PDF
    chrome_options.add_experimental_option('prefs', {
        'plugins.always_open_pdf_externally': True,
        'download.default_directory': os.path.abspath('.'),
        'download.prompt_for_download': False,
        'download.directory_upgrade': True,
        'safebrowsing.enabled': True
    })
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def download_pdf_with_chrome(url, save_path="chrome_downloaded_pdf.pdf"):
    """使用Chrome浏览器下载PDF文件"""
    driver = None
    try:
        print(f"正在启动Chrome浏览器...")
        driver = get_chrome_driver(headless=False)
        
        print(f"正在访问: {url}")
        driver.get(url)
        
        # 等待下载完成
        print("等待PDF下载...")
        time.sleep(10)  # 根据网络情况调整等待时间
        
        # 查找最近下载的PDF文件
        download_dir = os.path.abspath('.')
        files = os.listdir(download_dir)
        pdf_files = [f for f in files if f.endswith('.pdf') and os.path.isfile(os.path.join(download_dir, f))]
        
        if pdf_files:
            # 找到最新的PDF文件
            pdf_files.sort(key=lambda x: os.path.getmtime(os.path.join(download_dir, x)), reverse=True)
            latest_pdf = pdf_files[0]
            
            if latest_pdf != save_path:
                os.rename(os.path.join(download_dir, latest_pdf), os.path.join(download_dir, save_path))
            
            print(f"✓ PDF 已成功下载: {save_path}")
            return save_path
        else:
            print("警告: 未找到下载的PDF文件")
            return None
            
    except Exception as e:
        print(f"错误: {e}")
        return None
    finally:
        if driver:
            driver.quit()


def main():
    """主函数"""
    print("=" * 80)
    print("使用Chrome浏览器下载PDF工具")
    print("=" * 80)
    print()
    
    pdf_url = "https://static.cninfo.com.cn/finalpage/2026-03-10/1225002609.PDF"
    save_path = "chrome_anfu_2025_report.pdf"
    
    downloaded_path = download_pdf_with_chrome(pdf_url, save_path)
    
    if downloaded_path:
        print()
        print("✓ 任务完成!")
    else:
        print()
        print("✗ 下载失败")


if __name__ == "__main__":
    main()

