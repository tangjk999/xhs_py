# xhs_py - 小红书热门博客分析系统

## 项目简介

这是一个基于Python的小红书热门博客分析系统，集成了智能爬取、AI分析和可视化展示功能。

### 核心功能

1. **🕷️ 智能爬取**: 从小红书爬取指定主题的前N条热门博客数据
2. **🤖 AI分析**: 利用DeepSeek大模型对爬取的数据进行深度分析和整理
3. **📊 可视化展示**: 设计现代化网页界面，展示分析结果和图表

## 项目架构

```
xhs_py/
├── main.py                 # 主程序入口
├── config.py              # 配置文件
├── requirements.txt       # 依赖包列表
├── env_example.txt        # 环境变量示例
├── README.md             # 项目说明
├── crawler/              # 爬虫模块
│   └── xhs_crawler.py    # 小红书爬虫
├── ai_analyzer/          # AI分析模块
│   └── deepseek_analyzer.py  # DeepSeek分析器
├── web_app/              # Web应用
│   ├── app.py           # Flask应用
│   └── templates/       # 模板文件
│       └── index.html   # 主页面
├── templates/            # 分析模板
│   └── analysis_template.md  # RAG分析模板
├── data/                 # 数据存储目录
├── templates/            # Flask模板目录
└── static/              # 静态文件目录
```

## 安装和配置

### 1. 环境要求

- Python 3.8+
- Chrome浏览器（用于Selenium爬虫）

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

复制 `env_example.txt` 为 `.env` 并配置：

```bash
cp env_example.txt .env
```

编辑 `.env` 文件：

```env
# DeepSeek API配置
DEEPSEEK_API_KEY=your_deepseek_api_key_here
DEEPSEEK_API_BASE=https://api.deepseek.com

# Flask配置
FLASK_SECRET_KEY=your-secret-key-here
FLASK_DEBUG=True
```

### 4. 获取DeepSeek API密钥

1. 访问 [DeepSeek官网](https://platform.deepseek.com/)
2. 注册账号并获取API密钥
3. 将API密钥填入 `.env` 文件

## 使用方法

### 命令行模式

#### 1. 爬取数据

```bash
# 爬取美食主题的20条笔记
python main.py crawl -t "美食" -l 20

# 爬取并立即分析
python main.py crawl -t "旅行" -l 50 -a
```

#### 2. 分析数据

```bash
# 分析指定的CSV文件
python main.py analyze -f data/xhs_美食_20240101_120000.csv
```

#### 3. 启动Web服务

```bash
# 启动Web应用（默认端口5000）
python main.py web

# 指定端口启动
python main.py web -p 8080

# 调试模式启动
python main.py web -d
```

### Web界面模式

1. 启动Web服务：
```bash
python main.py web
```

2. 打开浏览器访问：`http://localhost:5000`

3. 在Web界面中：
   - 输入搜索主题和数量
   - 点击"开始爬取"
   - 选择数据文件进行AI分析
   - 查看可视化分析结果

## 功能特性

### 🕷️ 智能爬虫

- **反爬虫策略**: 使用Selenium模拟真实浏览器行为
- **数据提取**: 自动提取标题、作者、点赞数、发布时间等
- **错误处理**: 完善的异常处理和重试机制
- **数据存储**: 自动保存为CSV格式

### 🤖 AI分析

- **趋势分析**: 分析热门作者、关键词、互动数据
- **深度洞察**: 使用DeepSeek大模型进行深度分析
- **策略建议**: 生成内容策略和营销建议
- **模板化输出**: 支持自定义分析模板

### 📊 可视化展示

- **现代化UI**: 基于Bootstrap 5的响应式设计
- **实时图表**: 使用Chart.js展示数据图表
- **交互体验**: 流畅的用户交互和动画效果
- **数据导出**: 支持分析结果下载

## 数据格式

### 爬取数据格式 (CSV)

| 字段 | 说明 |
|------|------|
| title | 笔记标题 |
| author | 作者名称 |
| likes | 点赞数 |
| link | 笔记链接 |
| publish_time | 发布时间 |
| crawl_time | 爬取时间 |

### 分析结果格式 (JSON)

```json
{
  "trends": {
    "total_notes": 20,
    "top_authors": [...],
    "popular_topics": [...],
    "engagement_analysis": {...},
    "recommendations": [...]
  },
  "ai_analysis": {
    "ai_analysis": "AI分析文本",
    "data_summary": {...},
    "analysis_time": "2024-01-01 12:00:00"
  }
}
```

## 配置说明

### 主要配置项

- `DEEPSEEK_API_KEY`: DeepSeek API密钥
- `CRAWLER_DELAY`: 爬虫请求间隔（秒）
- `MAX_RETRIES`: 最大重试次数
- `FLASK_DEBUG`: Flask调试模式

### 自定义配置

可以在 `config.py` 中修改配置：

```python
class Config:
    # 修改爬虫配置
    CRAWLER_DELAY = 3  # 增加请求间隔
    MAX_RETRIES = 5    # 增加重试次数
    
    # 修改数据目录
    DATA_DIR = 'my_data'
```

## 故障排除

### 常见问题

1. **爬虫失败**
   - 检查网络连接
   - 确认Chrome浏览器已安装
   - 增加请求间隔时间

2. **AI分析失败**
   - 检查DeepSeek API密钥是否正确
   - 确认API配额是否充足
   - 检查网络连接

3. **Web服务启动失败**
   - 检查端口是否被占用
   - 确认Flask依赖已安装
   - 检查配置文件

### 调试模式

启用调试模式获取详细日志：

```bash
python main.py web -d
```

## 开发说明

### 扩展功能

1. **添加新的爬虫源**
   - 继承 `XHSCrawler` 类
   - 实现相应的爬取方法

2. **自定义分析模板**
   - 修改 `templates/analysis_template.md`
   - 在 `DeepSeekAnalyzer` 中使用

3. **添加新的图表类型**
   - 在 `index.html` 中添加新的Chart.js图表
   - 在JavaScript中处理数据

### 代码结构

- **模块化设计**: 各功能模块独立，便于维护
- **配置分离**: 配置与代码分离，便于部署
- **错误处理**: 完善的异常处理机制
- **文档注释**: 详细的代码注释和文档

## 许可证

本项目采用 MIT 许可证，详见 LICENSE 文件。

## 贡献

欢迎提交 Issue 和 Pull Request！

## 联系方式

如有问题或建议，请通过以下方式联系：

- 提交 GitHub Issue
- 发送邮件至项目维护者

---

**注意**: 请遵守小红书的用户协议和相关法律法规，合理使用爬虫功能。