# 小红书热门博客分析系统

一个基于Python的小红书热门博客分析系统，集成了智能爬取、AI分析和可视化展示功能。

## 🚀 功能特性

### 🕷️ 智能爬取
- 支持指定主题关键词搜索
- 可配置爬取数量（1-100条）
- 支持cookies登录状态
- 自动处理反爬机制
- 数据自动保存为CSV格式
- **新增：Cookie格式自动转换**
- **新增：定时自动更新Cookie状态**

### 🤖 AI分析
- 基于DeepSeek大模型的深度分析
- 多种分析类型：综合分析、趋势分析、AI深度分析
- 自动生成数据统计和可视化
- 提供可执行的策略建议

### 📊 可视化展示
- 现代化Web界面
- **新增：左右分栏布局设计**
- **新增：博客列表与详细分析分离显示**
- 实时数据展示
- 交互式图表
- 文件管理和下载
- **新增：Cookie状态实时监控**

### 🔧 系统管理
- **新增：Cookie有效性自动检查**
- **新增：Cookie格式转换器**
- **新增：清空Cookie功能**
- 自动文件管理
- 系统健康监控

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
   - **配置API密钥和cookies**
   - **使用Cookie转换器处理原始格式**
   - **实时监控Cookie状态**
   - 输入搜索主题和数量
   - 执行爬取和分析
   - **在左右分栏中查看博客列表和详细分析**

## 🔧 新功能详解

### Cookie管理功能

#### 1. Cookie格式转换
- 支持从浏览器复制的原始Cookie格式自动转换
- 格式：`name\tvalue\tdomain\tpath\texpires\tsize\t...`
- 自动转换为JSON格式保存

#### 2. Cookie状态监控
- 实时检查Cookie有效性
- 自动定时更新（每30分钟）
- 状态显示：有效/无效/检查失败

#### 3. Cookie操作
- 一键清空Cookie输入框
- 保存Cookie到本地文件
- 自动加载已保存的Cookie

### 界面优化

#### 1. 左右分栏布局
- **左侧：博客列表**
  - 显示所有爬取的博客
  - 包含标题、作者、互动数据
  - 点击选择查看详情
  
- **右侧：详细分析**
  - 选中博客的完整信息
  - 互动率分析
  - 内容质量评估
  - 热度等级和推荐指数

#### 2. 数据展示优化
- 博客卡片式展示
- 悬停效果和选中状态
- 响应式设计适配移动端

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
│       └── index.html   # 主页面（左右分栏布局）
├── data/                 # 数据存储目录
├── logs/                 # 日志目录
├── static/               # 静态文件
├── templates/            # 模板文件
├── xhs_cookies.json     # Cookie存储文件
└── api_key.json         # API密钥存储文件
```

## 🔧 配置说明

### DeepSeek API配置
1. 注册DeepSeek账号：https://platform.deepseek.com
2. 获取API密钥
3. 在Web界面或.env文件中配置API密钥

### Cookies配置（推荐使用Web界面）
1. 登录小红书网页版
2. 打开开发者工具（F12）
3. 复制cookies字符串（制表符分隔格式）
4. 在Web界面中使用Cookie转换器
5. 保存转换后的JSON格式

### Cookie格式示例
**原始格式（从浏览器复制）：**
```
a1	197db3f9380zg3ss63t73s4wccn6nj02mc272auy430000380633	.xiaohongshu.com	/	2026/7/5 23:41:06	54 B
web_session	0400698f99c131566b26056b5f3a4b0e526af5	.xiaohongshu.com	/	2026/7/6 15:19:08	49 B
```

**转换后格式（JSON）：**
```json
{
  "a1": "197db3f9380zg3ss63t73s4wccn6nj02mc272auy430000380633",
  "web_session": "0400698f99c131566b26056b5f3a4b0e526af5"
}
```

## 📊 数据格式

### 爬取数据（CSV格式）
```csv
title,author,likes,collects,comments,link,publish_time,image_url,crawl_time
笔记标题,作者名,点赞数,收藏数,评论数,链接,发布时间,图片链接,爬取时间
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
5. **Cookie安全**：Cookie包含敏感信息，请妥善保管，不要泄露给他人

## 🐛 常见问题

### Q: ChromeDriver版本不匹配
A: 系统会自动下载匹配的ChromeDriver，如果失败请手动下载对应版本

### Q: Cookie转换失败
A: 确保复制的Cookie格式正确，包含制表符分隔的字段

### Q: Cookie状态显示无效
A: 
1. 检查Cookie是否过期
2. 重新登录小红书获取新的Cookie
3. 使用Cookie转换器重新转换格式

### Q: 左右分栏显示异常
A: 确保浏览器支持现代CSS特性，建议使用Chrome、Firefox、Safari等现代浏览器

## 🔄 更新日志

### v1.1.0 (最新)
- ✨ 新增Cookie格式自动转换功能
- ✨ 新增左右分栏布局设计
- ✨ 新增Cookie状态实时监控
- ✨ 新增定时自动更新Cookie功能
- ✨ 新增博客详细分析页面
- ✨ 优化用户界面和交互体验
- 🐛 修复多个已知问题
- 📚 完善文档和说明

### v1.0.0
- 🎉 初始版本发布
- 基础爬取功能
- AI分析功能
- Web界面展示

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进项目！

## 📄 许可证

本项目采用MIT许可证，详见LICENSE文件。

## 📞 联系方式

如有问题或建议，请通过以下方式联系：
- 提交Issue
- 发送邮件
- 项目讨论区

## 🚀 部署指南

### Netlify部署

#### 方法一：手动部署
1. 安装Netlify CLI：
```bash
npm install -g netlify-cli
```

2. 运行部署脚本：
```bash
./deploy.sh
```

#### 方法二：GitHub Actions自动部署
1. 在GitHub仓库设置中添加Secrets：
   - `NETLIFY_AUTH_TOKEN`: Netlify API Token
   - `NETLIFY_SITE_ID`: Netlify Site ID

2. 推送代码到main分支，GitHub Actions会自动部署

#### 方法三：Netlify手动部署
1. 在Netlify控制台创建新站点
2. 连接GitHub仓库
3. 设置构建命令：`python -m pip install -r requirements.txt && python web_app/app.py`
4. 设置发布目录：`web_app/static`

### Docker部署
```bash
# 构建镜像
docker build -t xhs-analyzer .

# 运行容器
docker run -p 8080:8080 xhs-analyzer
```

---

**免责声明**：本项目仅供学习和研究使用，使用者需自行承担使用风险，并遵守相关法律法规。