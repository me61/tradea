# -*- coding: utf-8 -*-
"""
使用Python控制Chrome浏览器与DeepSeek对话
"""

import time
import os
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

COOKIE_FILE = "deepseek_cookies.json"
STORAGE_FILE = "deepseek_storage.json"


def load_cookies(driver, cookie_file=COOKIE_FILE):
    """加载保存的cookie"""
    if os.path.exists(cookie_file):
        try:
            with open(cookie_file, 'r', encoding='utf-8') as f:
                cookies = json.load(f)
            
            for cookie in cookies:
                try:
                    if 'sameSite' not in cookie:
                        cookie['sameSite'] = 'Lax'
                    driver.add_cookie(cookie)
                except Exception as e:
                    pass
            
            print(f"✓ 已加载 {len(cookies)} 个cookie")
            return True
        except Exception as e:
            print(f"加载cookie失败: {e}")
            return False
    return False


def save_cookies(driver, cookie_file=COOKIE_FILE):
    """保存当前cookie到文件"""
    try:
        cookies = driver.get_cookies()
        with open(cookie_file, 'w', encoding='utf-8') as f:
            json.dump(cookies, f, indent=2, ensure_ascii=False)
        print(f"✓ 已保存 {len(cookies)} 个cookie到 {cookie_file}")
        return True
    except Exception as e:
        print(f"保存cookie失败: {e}")
        return False


def load_local_storage(driver, storage_file=STORAGE_FILE):
    """加载保存的localStorage"""
    if os.path.exists(storage_file):
        try:
            with open(storage_file, 'r', encoding='utf-8') as f:
                storage_data = json.load(f)
            
            for key, value in storage_data.items():
                try:
                    driver.execute_script(f"localStorage.setItem('{key}', '{value}')")
                except Exception as e:
                    pass
            
            print(f"✓ 已加载 {len(storage_data)} 项localStorage")
            return True
        except Exception as e:
            print(f"加载localStorage失败: {e}")
            return False
    return False


def save_local_storage(driver, storage_file=STORAGE_FILE):
    """保存当前localStorage到文件"""
    try:
        storage_data = driver.execute_script("return window.localStorage")
        with open(storage_file, 'w', encoding='utf-8') as f:
            json.dump(storage_data, f, indent=2, ensure_ascii=False)
        print(f"✓ 已保存localStorage到 {storage_file}")
        return True
    except Exception as e:
        print(f"保存localStorage失败: {e}")
        return False


def check_login_status(driver):
    """检查是否已登录"""
    try:
        time.sleep(2)
        
        cookies = driver.get_cookies()
        session_cookies = [c for c in cookies if c.get('name') and (
            'session' in c['name'].lower() or 
            'token' in c['name'].lower() or 
            'ds_session' in c['name'].lower()
        )]
        if len(session_cookies) > 0:
            print(f"检测到会话cookie，认为已登录")
            return True
        
        login_indicators = ['登录', 'Login', 'Sign', '注册', 'Register']
        logout_indicators = ['退出', 'Logout', '登出']
        
        has_login = False
        has_logout = False
        
        elements = driver.find_elements(By.CSS_SELECTOR, 'button, div, span')
        for elem in elements:
            try:
                text = elem.text.strip()
                if any(indicator in text for indicator in login_indicators):
                    has_login = True
                if any(indicator in text for indicator in logout_indicators):
                    has_logout = True
            except:
                pass
        
        if has_logout:
            print("检测到退出按钮，认为已登录")
            return True
        if has_login:
            print("检测到登录按钮，认为未登录")
            return False
        
        print("未明确检测到登录状态，认为已登录")
        return True
    except Exception as e:
        print(f"登录检测异常: {e}")
        return True


def get_chrome_driver(headless=False):
    """配置并获取Chrome驱动"""
    chrome_options = Options()
    
    if headless:
        chrome_options.add_argument('--headless')
    
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    try:
        chromedriver_path = '/usr/local/bin/chromedriver'
        if os.path.exists(chromedriver_path):
            service = Service(chromedriver_path)
        else:
            service = Service(ChromeDriverManager().install())
    except Exception as e:
        print(f"ChromeDriver初始化警告: {e}")
        try:
            service = Service(ChromeDriverManager().install())
        except:
            from selenium.webdriver.chrome.service import Service as ChromeService
            service = ChromeService('/Users/huang/.wdm/drivers/chromedriver/mac64/131.0.6778.222/chromedriver-mac-arm64/chromedriver')
    
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def save_response_to_markdown(content, filename="deepseek_response"):

    current_timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"""{filename}_{current_timestamp}.md"""

    """保存回答内容到Markdown文件"""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    markdown_content = f"""# DeepSeek 专家模型回答

---

## 基本信息

| 项目 | 内容 |
|------|------|
| **提问时间** | {current_time} |
| **问题** | {content.get('question', '未记录')} |
| **模型** | 专家模式 |
| **思考模式** | 深度思考 |

---

## 回答内容

{content.get('answer', '')}

---

> 内容由 DeepSeek AI 生成，请仔细甄别

"""
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    print(f"✓ 回答内容已保存到: {filename}")


def switch_to_expert_model(driver, timeout=10):
    """自动切换到专家模式"""
    print("3/5: 正在自动切换到专家模式...")
    try:
        wait = WebDriverWait(driver, timeout)
        expert_radio = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[@role='radio' and contains(., '专家模式')]")
            )
        )
        if expert_radio.get_attribute("aria-checked") != "true":
            expert_radio.click()
            time.sleep(1)
            print("✓ 已自动切换到专家模式")
        else:
            print("✓ 专家模式已处于启用状态")
        return True
    except Exception as e:
        print(f"✗ 自动切换专家模式失败: {e}")
        return False


def enable_deep_thinking(driver, timeout=10):
    """自动启用深度思考"""
    print("4/5: 正在自动启用深度思考...")
    try:
        wait = WebDriverWait(driver, timeout)
        button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[@role='button' and contains(., '深度思考')]")
            )
        )
        if button.get_attribute("aria-pressed") != "true":
            button.click()
            time.sleep(1)
            print("✓ 已自动启用深度思考")
        else:
            print("✓ 深度思考已处于启用状态")
        return True
    except Exception as e:
        print(f"✗ 启用深度思考失败: {e}")
        return False


def get_last_message_content(driver):
    """获取最后一条消息内容 - 使用更精确的定位"""
    print("\n=== 正在获取回答内容 ===")
    
    time.sleep(1)
    
    try:
        xpath_patterns = [
            '//div[@data-author-role="assistant"]',
            '//div[@data-message-id and contains(@class, "assistant")]',
            '//div[contains(@class, "assistant") and contains(@class, "message")]',
            '//div[contains(@class, "response") and not(contains(@class, "user"))]',
            '//article[not(contains(@class, "user"))]',
            '//div[@role="listitem"]//div[contains(@class, "assistant")]',
        ]
        
        for xpath in xpath_patterns:
            try:
                messages = driver.find_elements(By.XPATH, xpath)
                if messages:
                    last_msg = messages[-1]
                    text = last_msg.text.strip()
                    if text and 20 < len(text) < 5000:
                        excluded_patterns = ['登录', 'Login', 'Sign', '注册', '快速模式', '专家模式', '深度思考', '推荐', '课程', '观看', 'API', '2026-03', 'LangGraph', 'LangChain']
                        if not any(pattern in text for pattern in excluded_patterns):
                            print(f"✓ 通过XPATH定位成功: {xpath}")
                            return text
            except Exception as e:
                continue
        
        css_patterns = [
            '[data-author-role="assistant"]',
            'div[data-message-id].assistant',
            '.assistant.message',
            '.response:not(.user)',
            'article:not(.user)',
        ]
        
        for selector in css_patterns:
            try:
                messages = driver.find_elements(By.CSS_SELECTOR, selector)
                if messages:
                    last_msg = messages[-1]
                    text = last_msg.text.strip()
                    if text and 20 < len(text) < 5000:
                        excluded_patterns = ['登录', 'Login', 'Sign', '注册', '快速模式', '专家模式', '深度思考', '推荐', '课程', '观看', 'API', '2026-03', 'LangGraph', 'LangChain']
                        if not any(pattern in text for pattern in excluded_patterns):
                            print(f"✓ 通过CSS定位成功: {selector}")
                            return text
            except Exception as e:
                continue
        
        all_divs = driver.find_elements(By.CSS_SELECTOR, 'div')
        max_length = 0
        best_text = ""
        for div in all_divs:
            try:
                text = div.text.strip()
                if len(text) > max_length and 30 < len(text) < 5000:
                    excluded_patterns = ['登录', 'Login', 'Sign', '注册', '快速模式', '专家模式', '深度思考', '开启新对话', '今天', '昨天', '推荐', '课程', '观看', 'API', '2026-03', 'LangGraph', 'LangChain', 'Hutool', 'Elasticsearch', 'Docker', 'Spring', 'LDAP']
                    if not any(pattern in text for pattern in excluded_patterns):
                        max_length = len(text)
                        best_text = text
            except:
                pass
        
        if best_text:
            print("✓ 通过兜底方式获取")
            return best_text
                
    except Exception as e:
        print(f"获取消息失败: {e}")
    
    return ""


def main():
    """主函数"""
    print("=" * 80)
    print("使用Chrome浏览器与DeepSeek对话")
    print("=" * 80)
    print()
    
    driver = None
    try:
        print("1/5: 正在启动Chrome浏览器...")
        driver = get_chrome_driver(headless=False)
        
        print("2/5: 正在访问DeepSeek网站...")
        driver.get("https://chat.deepseek.com/")
        
        if os.path.exists(COOKIE_FILE) or os.path.exists(STORAGE_FILE):
            print("3/5: 正在尝试加载已保存的认证信息...")
            
            if os.path.exists(COOKIE_FILE):
                load_cookies(driver)
            
            if os.path.exists(STORAGE_FILE):
                load_local_storage(driver)
            
            driver.refresh()
            time.sleep(1)
            
            if check_login_status(driver):
                print("✓ 自动登录成功，无需手动确认")
            else:
                print("自动登录失败，请手动登录")
                input("登录成功后按回车键继续...")
                save_cookies(driver)
                save_local_storage(driver)
        else:
            print("3/5: 请在浏览器中完成登录操作")
            input("登录成功后按回车键继续...")
            save_cookies(driver)
            save_local_storage(driver)
        
        switch_to_expert_model(driver)
        
        enable_deep_thinking(driver)
        
        print("\n4/5: 正在定位输入框...")
        input_box = None
        
        selectors = [
            (By.TAG_NAME, 'textarea'),
            (By.CSS_SELECTOR, '[contenteditable="true"]'),
            (By.CSS_SELECTOR, 'input[type="text"]'),
            (By.CSS_SELECTOR, 'input[placeholder]'),
            (By.CSS_SELECTOR, '.chat-input'),
            (By.CSS_SELECTOR, '[role="textbox"]'),
        ]
        
        for by, selector in selectors:
            try:
                input_box = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((by, selector))
                )
                if input_box:
                    print(f"✓ 找到输入框: {selector}")
                    break
            except:
                continue
        
        if not input_box:
            print("未找到输入框")
            return
        
        user_question = input("\n请输入你要问DeepSeek的问题: ")
        if user_question.strip():
            print(f"正在输入消息: {user_question}")
            input_box.send_keys(user_question)
            input_box.send_keys(Keys.ENTER)
            
            print("\n5/5: 等待回答中...")
            input("请在浏览器中确认回答完成后按回车键继续...")
            
            response_text = get_last_message_content(driver)
            
            if response_text and len(response_text) > 20:
                print("\n✓ 获取到回答:")
                print("-" * 80)
                print(response_text[:800] + "..." if len(response_text) > 800 else response_text)
                print("-" * 80)
                
                save_response_to_markdown({"question": user_question, "answer": response_text})
            else:
                print("✗ 未找到回答内容，请检查浏览器中的实际回答")
        else:
            print("未输入问题")
            
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if driver:
            print("\n正在关闭浏览器...")
            driver.quit()
            print("✓ 浏览器已关闭")


if __name__ == "__main__":
    main()