文件说明：该文件为vibe-coding的提示词，请cursor智能编程工具根据该文件中的提示词完成编程。
下面全部为提示词内容：

## 项目简介

这是一个基于Python的小红书热门博客分析系统，集成了智能爬取、AI分析和可视化展示功能。

### 核心功能

1. **🕷️ 智能爬取**: 从小红书爬取指定主题的前N条热门博客数据
2. **🤖 AI分析**: 利用DeepSeek大模型对爬取的数据进行深度分析和整理
3. **📊 可视化展示**: 设计现代化网页界面，展示分析结果和图表

# 网站页面

简洁，美观。

# 爬取的数据展示

需要把爬取到的数据显示在网页中。
网页中显示的，不需要使用模拟数据，要用实际抓取的数据。
把爬取的数据按博客一条条展示在左边，在选择左边对应博客时，右边区域展示对应的博客的数据详细分析内容。

# cookie
我复制过来的cookie格式为：
a1	197db3f9380zg3ss63t73s4wccn6nj02mc272auy430000380633	.xiaohongshu.com	/	2026/7/5 23:41:06	54 B			
abRequestId	447e3d73-3c8d-5e95-86e4-ca62df5a0808	.xiaohongshu.com	/	2026/7/5 23:41:04	47 B			
access-token-creator.xiaohongshu.com	customer.creator.AT-68c517523865315084509674vre4gusxfbupuivv	.xiaohongshu.com	/	2025/7/13 15:20:04	96 B		✓	
acw_tc	0a00d98f17517984257496163e7ebfc3e43cefe6d645664f0c14b6f6dd7d28	www.xiaohongshu.com	/	2025/7/6 19:10:25	68 B		✓	
customer-sso-sid	68c517523865315084333631qej8vdgugpd85jeh	.xiaohongshu.com	/	2025/7/13 15:20:03	56 B		✓	
customerClientId	539047159862687	.xiaohongshu.com	/	2025/7/13 15:20:04	31 B		✓	
galaxy_creator_session_id	bwRNHv2jlNZzTCG3vxXVE6TOqcD5qqL2JYQ0	.xiaohongshu.com	/	2025/7/13 15:20:04	61 B		✓	
galaxy.creator.beaker.session.id	1751786404548086064278	.xiaohongshu.com	/	2025/7/13 15:20:04	54 B		✓	
gid	yjWfDqi0ff68yjWfDqijqS07Y8ukqMMKq9WqJv4M4ESSIWq8KIV8JJ888qY8Kqq820jDK4KY	.xiaohongshu.com	/	2026/8/10 18:40:34	75 B			
loadts	1751798427894	.xiaohongshu.com	/	2026/7/6 18:40:27	19 B			
sec_poison_id	1971e91a-38aa-407f-a30f-f6a38cb5ac7c	.xiaohongshu.com	/	2025/7/6 18:50:33	49 B			
unread	{%22ub%22:%22686a4330000000001202386f%22%2C%22ue%22:%22685537a20000000010026b66%22%2C%22uc%22:25}	.xiaohongshu.com	/	会话	103 B			
web_session	0400698f99c131566b26056b5f3a4b0e526af5	.xiaohongshu.com	/	2026/7/6 15:19:08	49 B	✓	✓	
webBuild	4.70.2	.xiaohongshu.com	/	会话	14 B			
webId	6ef185a9c4c3adac1e3dce8720f972bb	.xiaohongshu.com	/	2026/7/5 23:41:06	37 B			
websectiga	634d3ad75ffb42a2ade2c5e1705a73c845837578aeb31ba0e442d75c648da36a	.xiaohongshu.com	/	2025/7/9 18:40:28	74 B			
x-user-id-creator.xiaohongshu.com	5eed82790000000001003b70	.xiaohongshu.com	/	2025/7/13 15:20:04	57 B		✓	
xsecappid	xhs-pc-web	.xiaohongshu.com	/	2026/7/6 18:40:27	19 B			

需要在复制cookie时自动转换成符合要求的json格式。cookie复制框中要有一个清空按钮，方便重新填入。

Cookie相关内容放一起去。

需要定时自动更新小红书的cookie来维持登陆状态。

当检测到cookie无效时，直接停止当前的任务即可，并报错提示即可。

# 部署

需要通过github自动部署到netify上。

# 调试

在cursor自动编程完成后在本地启动网页进行调试。

# 代码上库

在cursor自动编程完成后立即自动同步到github上。

# readme文档

在cursor自动编程完成后立即更新readme.md文档。