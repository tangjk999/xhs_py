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
    
    # Selenium配置
    SELENIUM_TIMEOUT = 30
    SELENIUM_IMPLICIT_WAIT = 10
    HEADLESS_MODE = True  # 是否使用无头模式
    
    # Flask配置
    FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'your-secret-key-here')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    FLASK_HOST = os.getenv('FLASK_HOST', '0.0.0.0')
    FLASK_PORT = int(os.getenv('FLASK_PORT', 5000))
    
    # 数据存储配置
    DATA_DIR = 'data'
    TEMPLATES_DIR = 'templates'
    STATIC_DIR = 'static'
    
    # AI分析配置
    MAX_TOKENS = 4000
    TEMPERATURE = 0.7
    ANALYSIS_TEMPLATE = 'templates/analysis_template.md'
    
    # 文件配置
    CSV_ENCODING = 'utf-8-sig'
    JSON_ENCODING = 'utf-8'
    
    # 日志配置
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = 'logs/app.log'
    
    # 安全配置
    ALLOWED_EXTENSIONS = {'csv', 'json', 'txt'}
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    
    @classmethod
    def ensure_directories(cls):
        """确保必要的目录存在"""
        directories = [cls.DATA_DIR, 'logs', 'static', 'templates']
        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory)
                print(f"创建目录: {directory}") 