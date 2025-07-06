# 小红书热门博客分析系统

一个基于Python的小红书热门博客分析系统，集成了智能爬取、AI分析和可视化展示功能。

## 🚀 功能特性

### 🕷️ 智能爬取
- 支持指定主题关键词搜索
- 可配置爬取数量（1-100条）
- 支持cookies登录状态
- 自动处理反爬机制
- 数据自动保存为CSV格式

### 🤖 AI分析
- 基于DeepSeek大模型的深度分析
- 多种分析类型：综合分析、趋势分析、AI深度分析
- 自动生成数据统计和可视化
- 提供可执行的策略建议

### 📊 可视化展示
- 现代化Web界面
- 实时数据展示
- 交互式图表
- 文件管理和下载

## 📋 系统要求

- Python 3.8+
- Chrome浏览器
- ChromeDriver（自动下载）

## 🛠️ 安装步骤

### 1. 克隆项目
```bash
git clone <repository-url>
cd xhs_py
```

### 2. 创建虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

### 3. 安装依赖
```bash
pip install -r requirements.txt
```

### 4. 配置环境变量
创建 `.env` 文件：
```env
# DeepSeek API配置
DEEPSEEK_API_KEY=your_api_key_here
DEEPSEEK_API_BASE=https://api.deepseek.com

# Flask配置
FLASK_SECRET_KEY=your-secret-key-here
FLASK_DEBUG=True
FLASK_HOST=0.0.0.0
FLASK_PORT=5000

# 日志配置
LOG_LEVEL=INFO
```

## 🎯 使用方法

### 命令行模式

#### 1. 爬取数据
```bash
# 基本爬取
python main.py crawl -t "美食" -l 20

# 爬取并自动分析
python main.py crawl -t "旅行" -l 50 -a

# 使用cookies爬取
python main.py crawl -t "美妆" -l 30 -c "your_cookies_string"
```

#### 2. 分析数据
```bash
# 综合分析
python main.py analyze -f data/xhs_美食_20241201.csv

# 趋势分析
python main.py analyze -f data/xhs_美食_20241201.csv -t trends

# AI深度分析
python main.py analyze -f data/xhs_美食_20241201.csv -t ai
```

#### 3. 启动Web应用
```bash
python main.py web
```

#### 4. 查看文件列表
```bash
python main.py list
```

### Web界面模式

1. 启动Web应用：
```bash
python main.py web
```

2. 打开浏览器访问：`http://localhost:5000`

3. 在Web界面中：
   - 配置API密钥和cookies
   - 输入搜索主题和数量
   - 执行爬取和分析
   - 查看可视化结果

## 📁 项目结构

```
xhs_py/
├── main.py                 # 主程序入口
├── config.py              # 配置文件
├── requirements.txt       # 依赖包列表
├── README.md             # 项目说明
├── .env                  # 环境变量（需创建）
├── crawler/              # 爬虫模块
│   └── xhs_crawler.py    # 小红书爬虫
├── ai_analyzer/          # AI分析模块
│   └── deepseek_analyzer.py  # DeepSeek分析器
├── web_app/              # Web应用
│   ├── app.py           # Flask应用
│   └── templates/       # 前端模板
│       └── index.html   # 主页面
├── data/                 # 数据存储目录
├── logs/                 # 日志目录
├── static/               # 静态文件
└── templates/            # 模板文件
```

## 🔧 配置说明

### DeepSeek API配置
1. 注册DeepSeek账号：https://platform.deepseek.com
2. 获取API密钥
3. 在Web界面或.env文件中配置API密钥

### Cookies配置（可选）
1. 登录小红书网页版
2. 打开开发者工具（F12）
3. 复制cookies字符串
4. 在Web界面中保存cookies

## 📊 数据格式

### 爬取数据（CSV格式）
```csv
title,author,likes,link,publish_time,image_url,crawl_time
笔记标题,作者名,点赞数,链接,发布时间,图片链接,爬取时间
```

### 分析结果（JSON格式）
```json
{
  "summary": {
    "total_notes": 20,
    "analysis_time": "2024-12-01 10:30:00"
  },
  "trends": {
    "top_authors": [...],
    "popular_topics": [...],
    "engagement_analysis": {...}
  },
  "statistics": {
    "basic_stats": {...},
    "engagement_stats": {...}
  },
  "recommendations": {
    "content_strategy": [...],
    "growth_tips": [...]
  }
}
```

## 🚨 注意事项

1. **合规使用**：请遵守小红书的用户协议和相关法律法规
2. **频率限制**：建议控制爬取频率，避免对目标网站造成压力
3. **数据使用**：爬取的数据仅供学习和研究使用
4. **API限制**：注意DeepSeek API的使用限制和配额

## 🐛 常见问题

### Q: ChromeDriver版本不匹配
A: 系统会自动下载匹配的ChromeDriver，如果失败请手动下载对应版本

### Q: 爬取失败或数据为空
A: 检查网络连接、cookies有效性，或尝试使用模拟数据模式

### Q: AI分析失败
A: 检查API密钥是否正确，或使用模拟分析模式

### Q: Web界面无法访问
A: 检查端口是否被占用，或修改配置文件中的端口设置

## 🤝 贡献指南

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 发起Pull Request

## 📄 许可证

本项目采用MIT许可证，详见LICENSE文件。

## 📞 联系方式

如有问题或建议，请通过以下方式联系：
- 提交Issue
- 发送邮件
- 项目讨论区

---

**免责声明**：本项目仅供学习和研究使用，使用者需自行承担使用风险，并遵守相关法律法规。