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
        
    def init_driver(self):
        """初始化Selenium WebDriver"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # 无头模式
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument(f'--user-agent={self.config.USER_AGENT}')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        self.driver = webdriver.Chrome(
            service=webdriver.chrome.service.Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
    def search_notes(self, keyword, limit=20):
        """
        搜索小红书笔记
        :param keyword: 搜索关键词
        :param limit: 获取数量限制
        :return: 笔记数据列表
        """
        if not self.driver:
            self.init_driver()
            
        notes_data = []
        try:
            # 构建搜索URL
            search_url = f"{self.config.XHS_SEARCH_URL}?keyword={keyword}&type=note"
            self.driver.get(search_url)
            
            # 等待页面加载
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-type='note']"))
            )
            
            # 滚动加载更多内容
            for _ in range(limit // 10 + 1):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.uniform(1, 3))
                
            # 获取笔记元素
            note_elements = self.driver.find_elements(By.CSS_SELECTOR, "[data-type='note']")[:limit]
            
            for element in note_elements:
                try:
                    note_data = self._extract_note_data(element)
                    if note_data:
                        notes_data.append(note_data)
                        print(f"已获取笔记: {note_data.get('title', '无标题')}")
                except Exception as e:
                    print(f"提取笔记数据时出错: {e}")
                    continue
                    
        except Exception as e:
            print(f"搜索笔记时出错: {e}")
        finally:
            if self.driver:
                self.driver.quit()
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
    
    def crawl_hot_notes(self, topic, limit=20):
        """
        爬取指定主题的热门笔记
        :param topic: 主题关键词
        :param limit: 获取数量
        :return: 保存的文件路径
        """
        print(f"开始爬取主题 '{topic}' 的热门笔记...")
        notes_data = self.search_notes(topic, limit)
        
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