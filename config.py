import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # DeepSeek API配置
    DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY', '')
    DEEPSEEK_API_BASE = os.getenv('DEEPSEEK_API_BASE', 'https://api.deepseek.com')
    
    # 小红书配置
    XHS_BASE_URL = 'https://www.xiaohongshu.com'
    XHS_SEARCH_URL = 'https://www.xiaohongshu.com/search_result'
    
    # 爬虫配置
    CRAWLER_DELAY = 2  # 请求间隔（秒）
    MAX_RETRIES = 3    # 最大重试次数
    USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    
    # Flask配置
    FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'your-secret-key-here')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    # 数据存储配置
    DATA_DIR = 'data'
    TEMPLATES_DIR = 'templates'
    STATIC_DIR = 'static' 