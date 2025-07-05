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
请分析以下小红书笔记数据，并提供深入的洞察和建议：

数据概览：
- 总笔记数：{data_summary['total_notes']}
- 数据字段：{', '.join(data_summary['columns'])}
- 样本标题：{data_summary['sample_titles']}
- 样本作者：{data_summary['sample_authors']}

请从以下角度进行分析：
1. 内容趋势分析
2. 用户偏好分析
3. 热门话题识别
4. 内容质量评估
5. 营销策略建议
6. 未来趋势预测

请提供结构化的分析报告，包含具体的数据洞察和 actionable 的建议。
"""
        
        if template:
            base_prompt += f"\n\n请按照以下模板格式输出：\n{template}"
        
        return base_prompt
    
    def _call_deepseek_api(self, prompt: str) -> str:
        """调用DeepSeek API"""
        try:
            import requests
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 2000
            }
            
            response = requests.post(
                f"{self.api_base}/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                raise Exception(f"API调用失败: {response.status_code}")
                
        except Exception as e:
            raise Exception(f"调用DeepSeek API时出错: {e}")
    
    def _mock_ai_analysis(self, data: pd.DataFrame) -> Dict[str, Any]:
        """模拟AI分析（当API不可用时）"""
        return {
            "ai_analysis": f"""
基于 {len(data)} 条小红书笔记的AI分析报告：

📊 内容趋势分析：
- 当前主题内容呈现多样化趋势
- 用户更倾向于实用性和可操作性的内容
- 视觉化内容（图片、视频）更受欢迎

🎯 用户偏好分析：
- 用户关注内容的质量和实用性
- 互动性强的内容更容易获得关注
- 个性化推荐对用户行为影响显著

🔥 热门话题识别：
- 生活技巧类内容持续热门
- 美食、旅行、时尚是永恒话题
- 新兴话题需要及时跟进

💡 营销策略建议：
- 注重内容质量和原创性
- 增加与用户的互动
- 利用热门话题提高曝光度
- 建立个人品牌形象

🔮 未来趋势预测：
- 短视频内容将继续增长
- 个性化推荐将更加精准
- 社区互动功能将更加重要
            """,
            "data_summary": self._prepare_data_summary(data),
            "analysis_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
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