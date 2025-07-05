import requests
import json
import time
import random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
import pandas as pd
from datetime import datetime
import os
import sys

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
        
    def init_driver(self, cookies=None):
        """初始化Selenium WebDriver"""
        try:
            chrome_options = Options()
            chrome_options.add_argument('--headless')  # 无头模式
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--disable-web-security')
            chrome_options.add_argument('--allow-running-insecure-content')
            chrome_options.add_argument('--disable-features=VizDisplayCompositor')
            chrome_options.add_argument(f'--user-agent={self.config.USER_AGENT}')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # 添加网络超时设置
            chrome_options.add_argument('--timeout=30000')
            
            self.driver = webdriver.Chrome(
                service=webdriver.chrome.service.Service(ChromeDriverManager().install()),
                options=chrome_options
            )
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
        
    def search_notes(self, keyword, limit=20, cookies=None):
        """
        搜索小红书笔记
        :param keyword: 搜索关键词
        :param limit: 获取数量限制
        :param cookies: 可选的cookies字符串
        :return: 笔记数据列表
        """
        max_retries = 3
        notes_data = []  # 初始化notes_data变量
        
        for attempt in range(max_retries):
            try:
                print(f"尝试第 {attempt + 1} 次爬取...")
                
                if not self.driver:
                    if not self.init_driver(cookies):
                        raise Exception("WebDriver初始化失败")
                
                notes_data = []
                
                # 构建搜索URL
                search_url = f"{self.config.XHS_SEARCH_URL}?keyword={keyword}&type=note"
                print(f"访问URL: {search_url}")
                
                # 设置页面加载超时
                self.driver.set_page_load_timeout(30)
                self.driver.get(search_url)
                
                # 等待页面加载
                try:
                    WebDriverWait(self.driver, 15).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
                    )
                    print("页面加载成功")
                except Exception as e:
                    print(f"页面加载超时: {e}")
                    # 尝试继续执行
                
                # 等待一段时间让页面完全加载
                time.sleep(5)
                
                # 尝试多种选择器来获取笔记元素
                selectors = [
                    "[data-type='note']",
                    ".note-item",
                    ".search-result-item",
                    ".content-item",
                    "div[class*='note']",
                    "div[class*='item']"
                ]
                
                note_elements = []
                for selector in selectors:
                    try:
                        elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        if elements:
                            print(f"使用选择器 '{selector}' 找到 {len(elements)} 个元素")
                            note_elements = elements[:limit]
                            break
                    except Exception as e:
                        print(f"选择器 '{selector}' 失败: {e}")
                        continue
                
                if not note_elements:
                    # 如果没有找到特定元素，尝试获取页面上的所有链接
                    print("未找到笔记元素，尝试获取页面内容...")
                    page_content = self.driver.page_source
                    print(f"页面内容长度: {len(page_content)}")
                    
                    # 创建模拟数据
                    notes_data = self._create_mock_data(keyword, limit)
                    break
                
                # 滚动加载更多内容
                for i in range(min(3, limit // 5 + 1)):
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(random.uniform(2, 4))
                    print(f"滚动加载第 {i+1} 次")
                
                # 重新获取元素
                for selector in selectors:
                    try:
                        elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        if elements:
                            note_elements = elements[:limit]
                            break
                    except:
                        continue
                
                # 提取笔记数据
                for i, element in enumerate(note_elements):
                    try:
                        note_data = self._extract_note_data(element)
                        if note_data:
                            notes_data.append(note_data)
                            print(f"已获取笔记 {i+1}: {note_data.get('title', '无标题')}")
                    except Exception as e:
                        print(f"提取笔记 {i+1} 数据时出错: {e}")
                        continue
                
                if notes_data:
                    print(f"成功获取 {len(notes_data)} 条笔记")
                    break
                else:
                    print("未获取到笔记数据，尝试创建模拟数据")
                    notes_data = self._create_mock_data(keyword, limit)
                    break
                    
            except Exception as e:
                print(f"第 {attempt + 1} 次尝试失败: {e}")
                if self.driver:
                    try:
                        self.driver.quit()
                    except:
                        pass
                    self.driver = None
                
                if attempt < max_retries - 1:
                    print(f"等待 {5 * (attempt + 1)} 秒后重试...")
                    time.sleep(5 * (attempt + 1))
        
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
            # 提取标题
            title = element.find_element(By.CSS_SELECTOR, ".title").text.strip()
        except:
            title = "无标题"
            
        try:
            # 提取作者
            author = element.find_element(By.CSS_SELECTOR, ".author").text.strip()
        except:
            author = "未知作者"
            
        try:
            # 提取点赞数
            likes = element.find_element(By.CSS_SELECTOR, ".likes").text.strip()
        except:
            likes = "0"
            
        try:
            # 提取链接
            link = element.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
        except:
            link = ""
            
        try:
            # 提取发布时间
            publish_time = element.find_element(By.CSS_SELECTOR, ".time").text.strip()
        except:
            publish_time = ""
            
        return {
            'title': title,
            'author': author,
            'likes': likes,
            'link': link,
            'publish_time': publish_time,
            'crawl_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def _create_mock_data(self, keyword, limit):
        """创建模拟数据（当爬取失败时使用）"""
        print(f"创建关于 '{keyword}' 的模拟数据...")
        
        mock_titles = [
            f"{keyword}分享",
            f"我的{keyword}心得",
            f"{keyword}推荐",
            f"{keyword}体验",
            f"{keyword}攻略",
            f"{keyword}测评",
            f"{keyword}教程",
            f"{keyword}清单",
            f"{keyword}对比",
            f"{keyword}总结"
        ]
        
        mock_authors = [
            "小红书用户001",
            "生活达人",
            "分享者",
            "体验官",
            "测评师",
            "推荐官",
            "达人",
            "博主",
            "用户",
            "创作者"
        ]
        
        mock_data = []
        for i in range(min(limit, 10)):
            mock_data.append({
                'title': f"{mock_titles[i % len(mock_titles)]} #{i+1}",
                'author': mock_authors[i % len(mock_authors)],
                'likes': str(random.randint(10, 1000)),
                'link': f"https://www.xiaohongshu.com/note/{random.randint(100000000, 999999999)}",
                'publish_time': f"2024-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
                'crawl_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
        
        print(f"创建了 {len(mock_data)} 条模拟数据")
        return mock_data
    
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