import requests
import json
import time
import random
from bs4 import BeautifulSoup
from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
import pandas as pd
from datetime import datetime
import os
import sys
import subprocess

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config

class XHSCrawler:
    def __init__(self):
        self.config = Config()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': self.config.USER_AGENT,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        self.driver = None
        
    def _get_chrome_version(self):
        """获取Chrome浏览器版本"""
        try:
            result = subprocess.run(['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '--version'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                version_str = result.stdout.strip()
                # 提取版本号
                import re
                match = re.search(r'(\d+)\.(\d+)\.(\d+)\.(\d+)', version_str)
                if match:
                    return f"{match.group(1)}.{match.group(2)}.{match.group(3)}.{match.group(4)}"
        except Exception as e:
            print(f"获取Chrome版本失败: {e}")
        return None
    
    def _force_update_chromedriver(self):
        """强制更新ChromeDriver到匹配版本"""
        try:
            chrome_version = self._get_chrome_version()
            if not chrome_version:
                print("无法获取Chrome版本")
                return False
            
            print(f"Chrome版本: {chrome_version}")
            
            # 尝试使用webdriver-manager强制更新
            try:
                from webdriver_manager.chrome import ChromeDriverManager
                driver_path = ChromeDriverManager().install()
                print(f"ChromeDriver已更新到: {driver_path}")
                return True
            except Exception as e:
                print(f"webdriver-manager更新失败: {e}")
                return False
                
        except Exception as e:
            print(f"强制更新ChromeDriver失败: {e}")
            return False
        
    def init_driver(self, cookies=None):
        """初始化Selenium WebDriver"""
        try:
            chrome_options = Options()
            
            # 基本选项
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument(f'--user-agent={self.config.USER_AGENT}')
            
            # 无头模式
            chrome_options.add_argument('--headless=new')
            
            # 兼容性选项
            chrome_options.add_argument('--disable-extensions')
            chrome_options.add_argument('--disable-plugins')
            chrome_options.add_argument('--no-first-run')
            chrome_options.add_argument('--no-default-browser-check')
            chrome_options.add_argument('--disable-background-timer-throttling')
            chrome_options.add_argument('--disable-backgrounding-occluded-windows')
            chrome_options.add_argument('--disable-renderer-backgrounding')
            chrome_options.add_argument('--disable-gpu-sandbox')
            chrome_options.add_argument('--disable-software-rasterizer')
            
            # 网络选项
            chrome_options.add_argument('--ignore-certificate-errors')
            chrome_options.add_argument('--ignore-ssl-errors')
            chrome_options.add_argument('--ignore-certificate-errors-spki-list')
            chrome_options.add_argument('--ignore-ssl-errors-spki-list')
            
            # 反检测选项
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # 项目根目录的ChromeDriver路径
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            local_chromedriver = os.path.join(project_root, 'chromedriver')
            
            if not os.path.exists(local_chromedriver):
                print(f"本地ChromeDriver不存在: {local_chromedriver}")
                raise Exception("本地ChromeDriver不存在")
            
            print(f"找到本地ChromeDriver: {local_chromedriver}")
            
            # 先尝试标准Selenium WebDriver
            try:
                print("尝试使用标准Selenium WebDriver...")
                service = Service(local_chromedriver)
                self.driver = webdriver.Chrome(
                    service=service,
                    options=chrome_options
                )
                print("标准Selenium WebDriver初始化成功")
            except Exception as e:
                print(f"标准Selenium失败: {e}")
                print("尝试使用undetected_chromedriver...")
                try:
                    service = Service(local_chromedriver)
                    self.driver = uc.Chrome(
                        service=service,
                        options=chrome_options
                    )
                    print("undetected_chromedriver初始化成功")
                except Exception as e2:
                    print(f"undetected_chromedriver也失败: {e2}")
                    raise Exception(f"所有WebDriver初始化方法都失败: {e2}")
            
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.driver.set_page_load_timeout(30)
            self.driver.implicitly_wait(10)
            
            # 如果提供了cookies，先访问小红书主页然后添加cookies
            if cookies:
                try:
                    print("正在加载cookies...")
                    self.driver.get("https://www.xiaohongshu.com")
                    time.sleep(2)
                    
                    # 解析cookies字符串并添加到浏览器
                    if isinstance(cookies, str):
                        # 如果是字符串格式，尝试解析
                        cookie_pairs = cookies.split(';')
                        for pair in cookie_pairs:
                            if '=' in pair:
                                name, value = pair.strip().split('=', 1)
                                try:
                                    self.driver.add_cookie({
                                        'name': name,
                                        'value': value,
                                        'domain': '.xiaohongshu.com'
                                    })
                                except Exception as e:
                                    print(f"添加cookie失败 {name}: {e}")
                    elif isinstance(cookies, list):
                        # 如果是列表格式，直接添加
                        for cookie in cookies:
                            try:
                                self.driver.add_cookie(cookie)
                            except Exception as e:
                                print(f"添加cookie失败: {e}")
                    
                    print("cookies加载完成")
                except Exception as e:
                    print(f"加载cookies时出错: {e}")
            
            print("WebDriver初始化成功")
            return True
            
        except Exception as e:
            print(f"WebDriver初始化失败: {e}")
            return False
        
    def is_logged_in(self):
        """检测当前页面是否已登录（cookie是否有效）"""
        try:
            self.driver.get("https://www.xiaohongshu.com")
            time.sleep(2)
            # 检查是否有登录弹窗或手机号输入框
            try:
                # 检查手机号输入框
                phone_input = self.driver.find_elements(By.XPATH, "//input[@placeholder='输入手机号']")
                if phone_input:
                    print("【警告】检测到手机号输入框，未登录！")
                    return False
                # 检查登录按钮
                login_btn = self.driver.find_elements(By.XPATH, "//button[contains(text(), '登录')]")
                if login_btn:
                    print("【警告】检测到登录按钮，未登录！")
                    return False
                # 检查二维码登录弹窗
                qr_login = self.driver.find_elements(By.XPATH, "//div[contains(text(), '登录后查看更多搜索结果')]")
                if qr_login:
                    print("【警告】检测到二维码登录弹窗，未登录！")
                    return False
            except Exception as e:
                print(f"【警告】登录检测异常: {e}")
            # 检查已登录特征（如头像、消息、发布按钮等）
            try:
                avatar = self.driver.find_elements(By.CSS_SELECTOR, ".user-avatar, .avatar")
                if avatar:
                    print("检测到用户头像，已登录！")
                    return True
            except Exception as e:
                print(f"【警告】已登录特征检测异常: {e}")
            # 默认未登录
            print("【警告】未检测到已登录特征，判定为未登录！")
            return False
        except Exception as e:
            print(f"【警告】登录检测主流程异常: {e}")
            return False

    def search_notes(self, keyword, limit=20, cookies=None):
        """
        搜索指定关键词的笔记
        :param keyword: 搜索关键词
        :param limit: 获取数量限制
        :param cookies: 可选的cookies字符串
        :return: 笔记数据列表
        """
        print(f"🔍 开始搜索关键词: {keyword}")
        print(f"📊 目标获取数量: {limit}")
        
        max_retries = self.config.MAX_RETRIES
        notes_data = []
        
        for attempt in range(max_retries):
            print(f"\n🔄 第 {attempt + 1} 次尝试...")
            
            try:
                # 初始化WebDriver
                if not self.init_driver(cookies):
                    print("❌ WebDriver初始化失败")
                    continue
                
                # 检查登录状态
                if not self.is_logged_in():
                    print("❌ 未登录或cookie无效，请先配置有效的Cookie")
                    raise Exception("Cookie无效或未登录，无法获取真实数据")
                
                # 构建搜索URL
                search_url = f"{self.config.XHS_SEARCH_URL}?keyword={keyword}&type=note"
                print(f"🌐 访问搜索页面: {search_url}")
                
                self.driver.get(search_url)
                time.sleep(random.uniform(3, 5))
                
                # 等待页面加载
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                
                # 尝试多个选择器来定位笔记元素
                selectors = [
                    "div[data-type='note']",
                    ".note-item",
                    ".search-result-item",
                    "div[class*='note']",
                    "div[class*='item']",
                    "a[href*='/explore/']",
                    ".feed-item"
                ]
                
                note_elements = []
                for selector in selectors:
                    try:
                        elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        if elements:
                            print(f"✅ 使用选择器 '{selector}' 找到 {len(elements)} 个元素")
                            note_elements = elements[:limit]
                            break
                    except Exception as e:
                        print(f"❌ 选择器 '{selector}' 失败: {e}")
                        continue
                
                if not note_elements:
                    print("⚠️ 未找到笔记元素，尝试滚动加载更多内容...")
                    
                    # 滚动加载更多内容
                    for i in range(min(3, limit // 5 + 1)):
                        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(random.uniform(2, 4))
                        print(f"📜 滚动加载第 {i+1} 次")
                    
                    # 重新获取元素
                    for selector in selectors:
                        try:
                            elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                            if elements:
                                note_elements = elements[:limit]
                                print(f"✅ 滚动后找到 {len(note_elements)} 个元素")
                                break
                        except:
                            continue
                
                # 提取笔记数据
                for i, element in enumerate(note_elements):
                    try:
                        note_data = self._extract_note_data(element)
                        if note_data:
                            notes_data.append(note_data)
                            print(f"📝 已获取笔记 {i+1}: {note_data.get('title', '无标题')}")
                    except Exception as e:
                        print(f"❌ 提取笔记 {i+1} 数据时出错: {e}")
                        continue
                
                if notes_data:
                    print(f"✅ 成功获取 {len(notes_data)} 条笔记")
                    break
                else:
                    print("⚠️ 未获取到笔记数据")
                    raise Exception("未能从页面提取到任何笔记数据，请检查网络连接或页面结构")
                    
            except Exception as e:
                print(f"❌ 第 {attempt + 1} 次尝试失败: {e}")
                if self.driver:
                    try:
                        self.driver.quit()
                    except:
                        pass
                    self.driver = None
                
                if attempt < max_retries - 1:
                    wait_time = 5 * (attempt + 1)
                    print(f"⏳ 等待 {wait_time} 秒后重试...")
                    time.sleep(wait_time)
        
        # 清理资源
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
            self.driver = None
                
        return notes_data

    def _extract_note_data(self, element):
        """从笔记元素中提取数据"""
        try:
            # 尝试多种方式提取标题
            title_selectors = [
                ".title", ".note-title", "h3", "h4", 
                "[class*='title']", "[class*='name']",
                "a[href*='/explore/']", ".content"
            ]
            
            title = "无标题"
            for selector in title_selectors:
                try:
                    title_elem = element.find_element(By.CSS_SELECTOR, selector)
                    title = title_elem.text.strip()
                    if title:
                        break
                except:
                    continue
            
            # 尝试多种方式提取作者
            author_selectors = [
                ".author", ".user-name", ".nickname",
                "[class*='author']", "[class*='user']",
                ".creator", ".publisher"
            ]
            
            author = "未知作者"
            for selector in author_selectors:
                try:
                    author_elem = element.find_element(By.CSS_SELECTOR, selector)
                    author = author_elem.text.strip()
                    if author:
                        break
                except:
                    continue
            
            # 尝试多种方式提取点赞数
            likes_selectors = [
                ".likes", ".like-count", ".count",
                "[class*='like']", "[class*='count']",
                ".interaction", ".stats"
            ]
            
            likes = "0"
            for selector in likes_selectors:
                try:
                    likes_elem = element.find_element(By.CSS_SELECTOR, selector)
                    likes_text = likes_elem.text.strip()
                    # 提取数字
                    import re
                    numbers = re.findall(r'\d+', likes_text)
                    if numbers:
                        likes = numbers[0]
                        break
                except:
                    continue
            
            # 提取链接
            link = ""
            try:
                link_elem = element.find_element(By.TAG_NAME, "a")
                link = link_elem.get_attribute("href")
            except:
                try:
                    link = element.get_attribute("href")
                except:
                    pass
            
            # 提取发布时间
            time_selectors = [
                ".time", ".publish-time", ".date",
                "[class*='time']", "[class*='date']"
            ]
            
            publish_time = ""
            for selector in time_selectors:
                try:
                    time_elem = element.find_element(By.CSS_SELECTOR, selector)
                    publish_time = time_elem.text.strip()
                    if publish_time:
                        break
                except:
                    continue
            
            # 提取图片URL（如果有）
            image_url = ""
            try:
                img_elem = element.find_element(By.TAG_NAME, "img")
                image_url = img_elem.get_attribute("src")
            except:
                pass
            
            return {
                'title': title,
                'author': author,
                'likes': likes,
                'link': link,
                'publish_time': publish_time,
                'image_url': image_url,
                'crawl_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
        except Exception as e:
            print(f"❌ 提取笔记数据时出错: {e}")
            return None

    def _create_mock_data(self, keyword, limit):
        """创建模拟数据（已禁用 - 只获取真实数据）"""
        raise Exception("模拟数据功能已禁用，请配置有效的Cookie获取真实数据")
    
    def save_to_csv(self, data, filename=None):
        """保存数据到CSV文件"""
        if not filename:
            filename = f"xhs_notes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
        # 确保数据目录存在
        os.makedirs(self.config.DATA_DIR, exist_ok=True)
        filepath = os.path.join(self.config.DATA_DIR, filename)
        
        df = pd.DataFrame(data)
        df.to_csv(filepath, index=False, encoding='utf-8-sig')
        print(f"数据已保存到: {filepath}")
        return filepath
    
    def crawl_hot_notes(self, topic, limit=20, cookies=None):
        """
        爬取指定主题的热门笔记
        :param topic: 主题关键词
        :param limit: 获取数量
        :param cookies: 可选的cookies字符串
        :return: 保存的文件路径
        """
        print(f"开始爬取主题 '{topic}' 的热门笔记...")
        notes_data = self.search_notes(topic, limit, cookies)
        
        if notes_data:
            filename = f"xhs_{topic}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            filepath = self.save_to_csv(notes_data, filename)
            print(f"成功爬取 {len(notes_data)} 条笔记")
            return filepath
        else:
            print("未获取到任何笔记数据")
            return None

if __name__ == "__main__":
    # 测试爬虫
    crawler = XHSCrawler()
    result = crawler.crawl_hot_notes("美食", 10)
    print(f"爬取结果: {result}") 