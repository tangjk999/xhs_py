import json
import pandas as pd
import os
import sys
from datetime import datetime
from typing import List, Dict, Any

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config

class DeepSeekAnalyzer:
    def __init__(self):
        self.config = Config()
        self.api_key = self.config.DEEPSEEK_API_KEY
        self.api_base = self.config.DEEPSEEK_API_BASE
        
        if not self.api_key:
            print("警告: 未设置DEEPSEEK_API_KEY，将使用模拟分析")
            self.use_mock = True
        else:
            self.use_mock = False
            
    def update_api_key(self, api_key: str):
        """更新API密钥"""
        self.api_key = api_key
        if api_key:
            self.use_mock = False
            print("API密钥已更新，将使用真实API")
        else:
            self.use_mock = True
            print("API密钥已清空，将使用模拟分析")
            
    def load_data(self, csv_file_path: str) -> pd.DataFrame:
        """加载CSV数据文件"""
        try:
            df = pd.read_csv(csv_file_path, encoding='utf-8-sig')
            print(f"成功加载数据文件: {csv_file_path}")
            print(f"数据行数: {len(df)}")
            return df
        except Exception as e:
            print(f"加载数据文件失败: {e}")
            return pd.DataFrame()
    
    def analyze_trends(self, data: pd.DataFrame) -> Dict[str, Any]:
        """分析热门趋势"""
        if data.empty:
            return {"error": "数据为空"}
            
        analysis = {
            "total_notes": len(data),
            "top_authors": [],
            "popular_topics": [],
            "engagement_analysis": {},
            "time_analysis": {},
            "recommendations": []
        }
        
        # 分析热门作者
        if 'author' in data.columns:
            author_counts = data['author'].value_counts().head(5)
            analysis["top_authors"] = [
                {"author": author, "count": count} 
                for author, count in author_counts.items()
            ]
        
        # 分析点赞数
        if 'likes' in data.columns:
            try:
                # 清理点赞数据
                likes_data = data['likes'].astype(str).str.extract('(\d+)')[0].astype(float)
                analysis["engagement_analysis"] = {
                    "avg_likes": likes_data.mean(),
                    "max_likes": likes_data.max(),
                    "min_likes": likes_data.min(),
                    "total_likes": likes_data.sum()
                }
            except:
                analysis["engagement_analysis"] = {"error": "无法解析点赞数据"}
        
        # 分析标题关键词
        if 'title' in data.columns:
            keywords = self._extract_keywords(data['title'].tolist())
            analysis["popular_topics"] = keywords[:10]
        
        # 生成建议
        analysis["recommendations"] = self._generate_recommendations(data)
        
        return analysis
    
    def _extract_keywords(self, titles: List[str]) -> List[Dict[str, Any]]:
        """提取标题中的关键词"""
        import re
        from collections import Counter
        
        # 合并所有标题
        all_text = ' '.join(titles)
        
        # 移除特殊字符，保留中文和英文
        cleaned_text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z\s]', '', all_text)
        
        # 分词（简单按空格分割）
        words = cleaned_text.split()
        
        # 过滤短词
        words = [word for word in words if len(word) > 1]
        
        # 统计词频
        word_counts = Counter(words)
        
        return [
            {"keyword": word, "frequency": count} 
            for word, count in word_counts.most_common(20)
        ]
    
    def _generate_recommendations(self, data: pd.DataFrame) -> List[str]:
        """生成分析建议"""
        recommendations = []
        
        if len(data) > 0:
            recommendations.append(f"共分析了 {len(data)} 条笔记")
            
            if 'likes' in data.columns:
                try:
                    likes_data = data['likes'].astype(str).str.extract('(\d+)')[0].astype(float)
                    avg_likes = likes_data.mean()
                    recommendations.append(f"平均点赞数: {avg_likes:.1f}")
                    
                    if avg_likes > 1000:
                        recommendations.append("该主题内容受欢迎程度较高")
                    elif avg_likes > 100:
                        recommendations.append("该主题内容受欢迎程度中等")
                    else:
                        recommendations.append("该主题内容受欢迎程度较低")
                except:
                    recommendations.append("无法分析点赞数据")
            
            if 'author' in data.columns:
                unique_authors = data['author'].nunique()
                recommendations.append(f"涉及 {unique_authors} 位作者")
                
                if unique_authors < len(data) * 0.3:
                    recommendations.append("建议关注头部作者的内容策略")
                else:
                    recommendations.append("内容创作者分布较为分散")
        
        return recommendations
    
    def analyze_with_ai(self, data: pd.DataFrame, template: str = None) -> Dict[str, Any]:
        """使用DeepSeek AI进行深度分析"""
        if self.use_mock:
            return self._mock_ai_analysis(data)
        
        try:
            # 准备数据摘要
            data_summary = self._prepare_data_summary(data)
            
            # 构建分析提示
            prompt = self._build_analysis_prompt(data_summary, template)
            
            # 调用DeepSeek API
            response = self._call_deepseek_api(prompt)
            
            return {
                "ai_analysis": response,
                "data_summary": data_summary,
                "analysis_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
        except Exception as e:
            print(f"AI分析失败: {e}")
            return {"error": f"AI分析失败: {str(e)}"}
    
    def _prepare_data_summary(self, data: pd.DataFrame) -> Dict[str, Any]:
        """准备数据摘要"""
        summary = {
            "total_notes": len(data),
            "columns": list(data.columns),
            "sample_titles": [],
            "sample_authors": []
        }
        
        if 'title' in data.columns:
            summary["sample_titles"] = data['title'].head(5).tolist()
        
        if 'author' in data.columns:
            summary["sample_authors"] = data['author'].head(5).tolist()
        
        return summary
    
    def _build_analysis_prompt(self, data_summary: Dict[str, Any], template: str = None) -> str:
        """构建分析提示"""
        base_prompt = f"""
你是一个专业的小红书内容分析师，请对以下小红书笔记数据进行深度分析，并提供有价值的洞察和建议。

## 数据概览
- 总笔记数：{data_summary['total_notes']}
- 数据字段：{', '.join(data_summary['columns'])}
- 样本标题：{data_summary['sample_titles']}
- 样本作者：{data_summary['sample_authors']}

## 分析要求
请从以下维度进行专业分析：

### 1. 内容趋势分析
- 热门话题和关键词识别
- 内容类型分布
- 标题特征分析
- 内容风格总结

### 2. 用户行为分析
- 点赞数分布和规律
- 热门作者特征
- 用户偏好分析
- 互动模式总结

### 3. 市场洞察
- 行业趋势判断
- 用户需求分析
- 内容机会识别
- 竞争态势评估

### 4. 策略建议
- 内容创作建议
- 运营策略推荐
- 用户增长建议
- 变现机会分析

### 5. 风险提示
- 潜在风险识别
- 合规建议
- 竞争风险分析

请用中文回答，分析要具体、实用、有数据支撑。如果数据不足，请说明并给出基于经验的建议。
"""
        
        if template:
            # 如果有自定义模板，使用模板
            try:
                with open(template, 'r', encoding='utf-8') as f:
                    template_content = f.read()
                return template_content.format(**data_summary)
            except Exception as e:
                print(f"模板加载失败: {e}")
        
        return base_prompt
    
    def _call_deepseek_api(self, prompt: str) -> str:
        """调用DeepSeek API"""
        try:
            import requests
            
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'model': 'deepseek-chat',
                'messages': [
                    {
                        'role': 'system',
                        'content': '你是一个专业的小红书内容分析师，擅长数据分析和市场洞察。'
                    },
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                'max_tokens': self.config.MAX_TOKENS,
                'temperature': self.config.TEMPERATURE,
                'stream': False
            }
            
            response = requests.post(
                f"{self.api_base}/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                print(f"API调用失败: {response.status_code} - {response.text}")
                return f"API调用失败: {response.status_code}"
                
        except Exception as e:
            print(f"调用DeepSeek API时出错: {e}")
            return f"API调用出错: {str(e)}"
    
    def _mock_ai_analysis(self, data: pd.DataFrame) -> Dict[str, Any]:
        """模拟AI分析（当API不可用时使用）"""
        print("🎭 使用模拟AI分析...")
        
        analysis = {
            "content_trends": {
                "hot_topics": ["美食分享", "生活记录", "购物推荐", "旅行攻略", "美妆教程"],
                "content_types": ["图文笔记", "视频内容", "合集推荐"],
                "title_patterns": ["数字+关键词", "情感化表达", "实用性强"],
                "style_summary": "内容风格偏向实用性和生活化"
            },
            "user_behavior": {
                "engagement_patterns": "用户更倾向于点赞实用性强的内容",
                "author_insights": "头部作者内容质量较高，互动性强",
                "user_preferences": "美食、生活、美妆类内容受欢迎",
                "interaction_summary": "评论和收藏是重要的互动指标"
            },
            "market_insights": {
                "industry_trends": "内容创作向专业化、垂直化发展",
                "user_needs": "用户需要更多实用、真实的内容",
                "opportunities": "细分领域仍有较大发展空间",
                "competition": "内容同质化严重，需要差异化竞争"
            },
            "strategic_recommendations": {
                "content_strategy": [
                    "注重内容质量和原创性",
                    "建立个人品牌和特色",
                    "保持更新频率和互动性",
                    "关注用户反馈和需求"
                ],
                "growth_tips": [
                    "选择合适的细分领域深耕",
                    "与其他创作者合作互动",
                    "利用热点话题增加曝光",
                    "建立粉丝社群"
                ],
                "monetization": [
                    "通过优质内容吸引品牌合作",
                    "开发自有产品或服务",
                    "利用平台变现功能",
                    "建立多元化收入来源"
                ]
            },
            "risk_warnings": {
                "compliance_risks": "注意内容合规性，避免违规",
                "competition_risks": "市场竞争激烈，需要持续创新",
                "platform_risks": "平台政策变化可能影响运营"
            }
        }
        
        return analysis
    
    def save_analysis(self, analysis: Dict[str, Any], filename: str = None) -> str:
        """保存分析结果"""
        if not filename:
            filename = f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        # 确保数据目录存在
        os.makedirs(self.config.DATA_DIR, exist_ok=True)
        filepath = os.path.join(self.config.DATA_DIR, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, ensure_ascii=False, indent=2)
        
        print(f"分析结果已保存到: {filepath}")
        return filepath

    def generate_comprehensive_report(self, data: pd.DataFrame) -> Dict[str, Any]:
        """生成综合分析报告"""
        print("📊 生成综合分析报告...")
        
        # 基础趋势分析
        trends = self.analyze_trends(data)
        
        # AI深度分析
        ai_result = self.analyze_with_ai(data)
        
        # 数据统计
        stats = self._calculate_statistics(data)
        
        # 可视化数据
        chart_data = self._prepare_chart_data(data)
        
        # 生成报告
        report = {
            "summary": {
                "total_notes": len(data),
                "analysis_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "data_source": "小红书爬虫",
                "analysis_version": "1.0.0"
            },
            "trends": trends,
            "ai_analysis": ai_result,
            "statistics": stats,
            "charts": chart_data,
            "recommendations": self._generate_actionable_recommendations(data, trends, ai_result)
        }
        
        return report

    def _calculate_statistics(self, data: pd.DataFrame) -> Dict[str, Any]:
        """计算详细统计数据"""
        stats = {
            "basic_stats": {},
            "engagement_stats": {},
            "author_stats": {},
            "content_stats": {}
        }
        
        # 基础统计
        stats["basic_stats"] = {
            "total_notes": len(data),
            "unique_authors": data['author'].nunique() if 'author' in data.columns else 0,
            "date_range": self._get_date_range(data) if 'publish_time' in data.columns else "未知"
        }
        
        # 互动统计
        if 'likes' in data.columns:
            try:
                likes_data = data['likes'].astype(str).str.extract('(\d+)')[0].astype(float)
                stats["engagement_stats"] = {
                    "avg_likes": likes_data.mean(),
                    "median_likes": likes_data.median(),
                    "max_likes": likes_data.max(),
                    "min_likes": likes_data.min(),
                    "total_likes": likes_data.sum(),
                    "likes_distribution": {
                        "high": len(likes_data[likes_data > likes_data.quantile(0.8)]),
                        "medium": len(likes_data[(likes_data > likes_data.quantile(0.2)) & (likes_data <= likes_data.quantile(0.8))]),
                        "low": len(likes_data[likes_data <= likes_data.quantile(0.2)])
                    }
                }
            except:
                stats["engagement_stats"] = {"error": "无法解析点赞数据"}
        
        # 作者统计
        if 'author' in data.columns:
            author_counts = data['author'].value_counts()
            stats["author_stats"] = {
                "top_authors": author_counts.head(10).to_dict(),
                "author_distribution": {
                    "single_post": len(author_counts[author_counts == 1]),
                    "multiple_posts": len(author_counts[author_counts > 1])
                }
            }
        
        # 内容统计
        if 'title' in data.columns:
            title_lengths = data['title'].str.len()
            stats["content_stats"] = {
                "avg_title_length": title_lengths.mean(),
                "title_length_distribution": {
                    "short": len(title_lengths[title_lengths <= 10]),
                    "medium": len(title_lengths[(title_lengths > 10) & (title_lengths <= 30)]),
                    "long": len(title_lengths[title_lengths > 30])
                }
            }
        
        return stats

    def _get_date_range(self, data: pd.DataFrame) -> str:
        """获取数据的时间范围"""
        try:
            # 尝试解析发布时间
            dates = pd.to_datetime(data['publish_time'], errors='coerce')
            valid_dates = dates.dropna()
            if len(valid_dates) > 0:
                start_date = valid_dates.min().strftime('%Y-%m-%d')
                end_date = valid_dates.max().strftime('%Y-%m-%d')
                return f"{start_date} 至 {end_date}"
        except:
            pass
        return "时间范围未知"

    def _prepare_chart_data(self, data: pd.DataFrame) -> Dict[str, Any]:
        """准备图表数据"""
        chart_data = {}
        
        # 作者分布图
        if 'author' in data.columns:
            author_counts = data['author'].value_counts().head(10)
            chart_data["author_distribution"] = {
                "labels": author_counts.index.tolist(),
                "data": author_counts.values.tolist()
            }
        
        # 点赞数分布图
        if 'likes' in data.columns:
            try:
                likes_data = data['likes'].astype(str).str.extract('(\d+)')[0].astype(float)
                # 创建点赞数区间
                bins = [0, 100, 500, 1000, 5000, float('inf')]
                labels = ['0-100', '101-500', '501-1000', '1001-5000', '5000+']
                likes_binned = pd.cut(likes_data, bins=bins, labels=labels, include_lowest=True)
                likes_dist = likes_binned.value_counts()
                chart_data["likes_distribution"] = {
                    "labels": likes_dist.index.tolist(),
                    "data": likes_dist.values.tolist()
                }
            except:
                pass
        
        # 标题长度分布
        if 'title' in data.columns:
            title_lengths = data['title'].str.len()
            bins = [0, 10, 20, 30, 50, float('inf')]
            labels = ['0-10', '11-20', '21-30', '31-50', '50+']
            length_binned = pd.cut(title_lengths, bins=bins, labels=labels, include_lowest=True)
            length_dist = length_binned.value_counts()
            chart_data["title_length_distribution"] = {
                "labels": length_dist.index.tolist(),
                "data": length_dist.values.tolist()
            }
        
        return chart_data

    def _generate_actionable_recommendations(self, data: pd.DataFrame, trends: Dict, ai_result: Dict) -> Dict[str, Any]:
        """生成可执行的建议"""
        recommendations = {
            "content_strategy": [],
            "growth_tips": [],
            "monetization": [],
            "risk_management": []
        }
        
        # 基于数据的建议
        if trends.get('engagement_analysis', {}).get('avg_likes', 0) > 1000:
            recommendations["content_strategy"].append("内容质量较高，建议保持现有创作风格")
        else:
            recommendations["content_strategy"].append("建议提升内容质量和互动性")
        
        if trends.get('top_authors'):
            recommendations["growth_tips"].append(f"关注头部作者（如{trends['top_authors'][0]['author']}）的创作策略")
        
        if ai_result.get('ai_analysis'):
            # 从AI分析中提取建议
            ai_text = ai_result['ai_analysis']
            if isinstance(ai_text, str):
                if "实用" in ai_text:
                    recommendations["content_strategy"].append("注重内容的实用性")
                if "原创" in ai_text:
                    recommendations["content_strategy"].append("保持内容原创性")
                if "互动" in ai_text:
                    recommendations["growth_tips"].append("加强与用户的互动")
        
        # 通用建议
        recommendations["content_strategy"].extend([
            "定期分析热门话题和关键词",
            "保持内容更新频率",
            "建立个人品牌特色"
        ])
        
        recommendations["growth_tips"].extend([
            "与其他创作者合作互动",
            "利用热点话题增加曝光",
            "建立粉丝社群"
        ])
        
        recommendations["monetization"].extend([
            "通过优质内容吸引品牌合作",
            "开发自有产品或服务",
            "利用平台变现功能"
        ])
        
        recommendations["risk_management"].extend([
            "注意内容合规性",
            "关注平台政策变化",
            "建立多元化收入来源"
        ])
        
        return recommendations

if __name__ == "__main__":
    # 测试分析器
    analyzer = DeepSeekAnalyzer()
    
    # 创建测试数据
    test_data = pd.DataFrame({
        'title': ['美食探店分享', '旅行攻略', '穿搭技巧', '护肤心得', '健身教程'],
        'author': ['美食达人', '旅行博主', '时尚博主', '美妆博主', '健身教练'],
        'likes': ['1.2k', '856', '2.1k', '1.5k', '3.2k'],
        'publish_time': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05']
    })
    
    # 进行趋势分析
    trends = analyzer.analyze_trends(test_data)
    print("趋势分析结果:", json.dumps(trends, ensure_ascii=False, indent=2))
    
    # 进行AI分析
    ai_result = analyzer.analyze_with_ai(test_data)
    print("AI分析结果:", ai_result['ai_analysis']) 