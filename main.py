#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小红书热门博客分析系统
主程序入口
"""

import os
import sys
import argparse
from datetime import datetime

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import Config
from crawler.xhs_crawler import XHSCrawler
from ai_analyzer.deepseek_analyzer import DeepSeekAnalyzer
from web_app.app import app

def print_banner():
    """打印项目横幅"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║    小红书热门博客分析系统 v1.0.0                              ║
    ║                                                              ║
    ║    🕷️  智能爬取  |  🤖 AI分析  |  📊 可视化展示              ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def crawl_mode(args):
    """爬取模式"""
    print("🕷️ 启动爬取模式...")
    
    crawler = XHSCrawler()
    result = crawler.crawl_hot_notes(args.topic, args.limit)
    
    if result:
        print(f"✅ 爬取完成！数据已保存到: {result}")
        
        if args.analyze:
            print("🤖 开始AI分析...")
            analyzer = DeepSeekAnalyzer()
            
            # 加载数据
            df = analyzer.load_data(result)
            if not df.empty:
                # 进行趋势分析
                trends = analyzer.analyze_trends(df)
                print("📊 趋势分析完成")
                
                # 进行AI分析
                ai_result = analyzer.analyze_with_ai(df)
                print("🤖 AI分析完成")
                
                # 保存分析结果
                analysis_file = analyzer.save_analysis({
                    'trends': trends,
                    'ai_analysis': ai_result,
                    'analysis_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'data_file': result
                })
                
                print(f"📄 分析结果已保存到: {analysis_file}")
                
                # 打印简要结果
                print("\n📊 简要分析结果:")
                print(f"   总笔记数: {trends.get('total_notes', 0)}")
                if trends.get('engagement_analysis', {}).get('avg_likes'):
                    print(f"   平均点赞: {trends['engagement_analysis']['avg_likes']:.1f}")
                print(f"   热门作者数: {len(trends.get('top_authors', []))}")
                print(f"   热门话题数: {len(trends.get('popular_topics', []))}")
            else:
                print("❌ 数据加载失败")
    else:
        print("❌ 爬取失败")

def analyze_mode(args):
    """分析模式"""
    print("🤖 启动分析模式...")
    
    if not os.path.exists(args.file):
        print(f"❌ 文件不存在: {args.file}")
        return
    
    analyzer = DeepSeekAnalyzer()
    
    # 加载数据
    df = analyzer.load_data(args.file)
    if df.empty:
        print("❌ 数据加载失败")
        return
    
    print(f"📊 成功加载 {len(df)} 条数据")
    
    # 进行趋势分析
    print("📈 进行趋势分析...")
    trends = analyzer.analyze_trends(df)
    
    # 进行AI分析
    print("🤖 进行AI分析...")
    ai_result = analyzer.analyze_with_ai(df)
    
    # 保存分析结果
    analysis_result = {
        'trends': trends,
        'ai_analysis': ai_result,
        'analysis_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'data_file': args.file
    }
    
    analysis_file = analyzer.save_analysis(analysis_result)
    print(f"📄 分析结果已保存到: {analysis_file}")
    
    # 打印详细结果
    print("\n📊 详细分析结果:")
    print("=" * 50)
    
    # 核心指标
    print(f"📈 核心指标:")
    print(f"   总笔记数: {trends.get('total_notes', 0)}")
    
    engagement = trends.get('engagement_analysis', {})
    if engagement and not engagement.get('error'):
        print(f"   平均点赞: {engagement.get('avg_likes', 0):.1f}")
        print(f"   最高点赞: {engagement.get('max_likes', 0):.1f}")
        print(f"   最低点赞: {engagement.get('min_likes', 0):.1f}")
    
    # 热门作者
    top_authors = trends.get('top_authors', [])
    if top_authors:
        print(f"\n👥 热门作者 TOP5:")
        for i, author in enumerate(top_authors[:5], 1):
            print(f"   {i}. {author['author']} ({author['count']} 篇)")
    
    # 热门话题
    popular_topics = trends.get('popular_topics', [])
    if popular_topics:
        print(f"\n🔥 热门话题 TOP10:")
        for i, topic in enumerate(popular_topics[:10], 1):
            print(f"   {i}. {topic['keyword']} ({topic['frequency']} 次)")
    
    # 建议
    recommendations = trends.get('recommendations', [])
    if recommendations:
        print(f"\n💡 策略建议:")
        for rec in recommendations:
            print(f"   • {rec}")
    
    # AI分析摘要
    if ai_result and ai_result.get('ai_analysis'):
        print(f"\n🤖 AI分析摘要:")
        ai_text = ai_result['ai_analysis']
        # 只显示前500个字符
        if len(ai_text) > 500:
            ai_text = ai_text[:500] + "..."
        print(f"   {ai_text}")

def web_mode(args):
    """Web模式"""
    print("🌐 启动Web应用...")
    print(f"   访问地址: http://localhost:{args.port}")
    print(f"   数据目录: {Config().DATA_DIR}")
    print(f"   按 Ctrl+C 停止服务")
    
    try:
        app.run(
            host='0.0.0.0',
            port=args.port,
            debug=args.debug
        )
    except KeyboardInterrupt:
        print("\n👋 服务已停止")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='小红书热门博客分析系统',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python main.py crawl -t "美食" -l 20 -a          # 爬取美食主题并分析
  python main.py analyze -f data/xhs_美食_20240101.csv  # 分析指定文件
  python main.py web -p 5000                      # 启动Web服务
        """
    )
    
    subparsers = parser.add_subparsers(dest='mode', help='运行模式')
    
    # 爬取模式
    crawl_parser = subparsers.add_parser('crawl', help='爬取数据')
    crawl_parser.add_argument('-t', '--topic', required=True, help='搜索主题')
    crawl_parser.add_argument('-l', '--limit', type=int, default=20, help='获取数量 (默认: 20)')
    crawl_parser.add_argument('-a', '--analyze', action='store_true', help='爬取后立即分析')
    
    # 分析模式
    analyze_parser = subparsers.add_parser('analyze', help='分析数据')
    analyze_parser.add_argument('-f', '--file', required=True, help='CSV文件路径')
    
    # Web模式
    web_parser = subparsers.add_parser('web', help='启动Web应用')
    web_parser.add_argument('-p', '--port', type=int, default=5000, help='端口号 (默认: 5000)')
    web_parser.add_argument('-d', '--debug', action='store_true', help='调试模式')
    
    args = parser.parse_args()
    
    if not args.mode:
        parser.print_help()
        return
    
    # 打印横幅
    print_banner()
    
    # 确保必要的目录存在
    config = Config()
    os.makedirs(config.DATA_DIR, exist_ok=True)
    os.makedirs(config.TEMPLATES_DIR, exist_ok=True)
    os.makedirs(config.STATIC_DIR, exist_ok=True)
    
    # 根据模式执行相应功能
    if args.mode == 'crawl':
        crawl_mode(args)
    elif args.mode == 'analyze':
        analyze_mode(args)
    elif args.mode == 'web':
        web_mode(args)

if __name__ == '__main__':
    main() 