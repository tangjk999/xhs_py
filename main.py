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
    
    # 参数验证
    if not args.topic:
        print("❌ 错误: 请提供搜索主题")
        return
    
    if args.limit <= 0 or args.limit > 100:
        print("❌ 错误: 获取数量必须在1-100之间")
        return
    
    print(f"📊 爬取参数:")
    print(f"   主题: {args.topic}")
    print(f"   数量: {args.limit}")
    print(f"   输出文件: {args.output if args.output else '自动生成'}")
    
    # 执行爬取
    try:
        crawler = XHSCrawler()
        result = crawler.crawl_hot_notes(args.topic, args.limit, args.cookies)
        
        if result:
            print(f"✅ 爬取完成！数据已保存到: {result}")
            
            if args.analyze:
                print("🤖 开始AI分析...")
                analyzer = DeepSeekAnalyzer()
                
                # 加载数据
                df = analyzer.load_data(result)
                if not df.empty:
                    # 进行综合分析
                    report = analyzer.generate_comprehensive_report(df)
                    print("📊 综合分析完成")
                    
                    # 保存分析结果
                    analysis_file = analyzer.save_analysis(report)
                    print(f"📄 分析结果已保存到: {analysis_file}")
                    
                    # 打印简要结果
                    print("\n📊 简要分析结果:")
                    summary = report.get('summary', {})
                    print(f"   总笔记数: {summary.get('total_notes', 0)}")
                    
                    stats = report.get('statistics', {})
                    engagement = stats.get('engagement_stats', {})
                    if engagement and not engagement.get('error'):
                        print(f"   平均点赞: {engagement.get('avg_likes', 0):.1f}")
                        print(f"   最高点赞: {engagement.get('max_likes', 0):.1f}")
                    
                    basic_stats = stats.get('basic_stats', {})
                    print(f"   作者数量: {basic_stats.get('unique_authors', 0)}")
                    
                    # 显示热门作者
                    trends = report.get('trends', {})
                    top_authors = trends.get('top_authors', [])
                    if top_authors:
                        print(f"   热门作者: {top_authors[0]['author']} ({top_authors[0]['count']}篇)")
                    
                    # 显示热门话题
                    popular_topics = trends.get('popular_topics', [])
                    if popular_topics:
                        print(f"   热门话题: {popular_topics[0]['keyword']} ({popular_topics[0]['frequency']}次)")
                else:
                    print("❌ 数据加载失败")
        else:
            print("❌ 爬取失败")
            
    except Exception as e:
        print(f"❌ 爬取过程中出错: {e}")
        import traceback
        traceback.print_exc()

def analyze_mode(args):
    """分析模式"""
    print("🤖 启动分析模式...")
    
    # 参数验证
    if not os.path.exists(args.file):
        print(f"❌ 错误: 文件不存在: {args.file}")
        return
    
    print(f"📊 分析参数:")
    print(f"   数据文件: {args.file}")
    print(f"   分析类型: {args.type}")
    print(f"   输出文件: {args.output if args.output else '自动生成'}")
    
    try:
        analyzer = DeepSeekAnalyzer()
        
        # 加载数据
        df = analyzer.load_data(args.file)
        if df.empty:
            print("❌ 数据加载失败")
            return
        
        print(f"📊 成功加载 {len(df)} 条数据")
        
        # 根据分析类型执行不同的分析
        if args.type == 'comprehensive':
            print("📈 进行综合分析...")
            result = analyzer.generate_comprehensive_report(df)
        elif args.type == 'trends':
            print("📈 进行趋势分析...")
            result = {
                'trends': analyzer.analyze_trends(df),
                'analysis_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'data_file': args.file
            }
        elif args.type == 'ai':
            print("🤖 进行AI深度分析...")
            result = analyzer.analyze_with_ai(df)
        else:
            print(f"❌ 不支持的分析类型: {args.type}")
            return
        
        # 保存分析结果
        if args.output:
            analysis_file = analyzer.save_analysis(result, args.output)
        else:
            analysis_file = analyzer.save_analysis(result)
        
        print(f"📄 分析结果已保存到: {analysis_file}")
        
        # 打印详细结果
        print("\n📊 详细分析结果:")
        print("=" * 50)
        
        if args.type == 'comprehensive':
            # 核心指标
            summary = result.get('summary', {})
            print(f"📈 核心指标:")
            print(f"   总笔记数: {summary.get('total_notes', 0)}")
            print(f"   分析时间: {summary.get('analysis_time', '未知')}")
            
            stats = result.get('statistics', {})
            engagement = stats.get('engagement_stats', {})
            if engagement and not engagement.get('error'):
                print(f"   平均点赞: {engagement.get('avg_likes', 0):.1f}")
                print(f"   最高点赞: {engagement.get('max_likes', 0):.1f}")
                print(f"   最低点赞: {engagement.get('min_likes', 0):.1f}")
                print(f"   总点赞数: {engagement.get('total_likes', 0):.1f}")
            
            basic_stats = stats.get('basic_stats', {})
            print(f"   作者数量: {basic_stats.get('unique_authors', 0)}")
            print(f"   时间范围: {basic_stats.get('date_range', '未知')}")
            
            # 热门作者
            trends = result.get('trends', {})
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
            recommendations = result.get('recommendations', {})
            if recommendations:
                print(f"\n💡 策略建议:")
                for category, tips in recommendations.items():
                    if tips:
                        print(f"   {category}:")
                        for tip in tips[:3]:  # 只显示前3条
                            print(f"     • {tip}")
        
        elif args.type == 'trends':
            # 趋势分析结果
            trends = result.get('trends', {})
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
        
        elif args.type == 'ai':
            # AI分析结果
            ai_result = result.get('ai_analysis', {})
            if ai_result:
                print(f"\n🤖 AI分析摘要:")
                ai_text = ai_result
                if isinstance(ai_text, str):
                    # 只显示前500个字符
                    if len(ai_text) > 500:
                        ai_text = ai_text[:500] + "..."
                    print(f"   {ai_text}")
            
    except Exception as e:
        print(f"❌ 分析过程中出错: {e}")
        import traceback
        traceback.print_exc()

def web_mode(args):
    """Web模式"""
    print("🌐 启动Web应用...")
    print(f"   访问地址: http://{config.FLASK_HOST}:{config.FLASK_PORT}")
    print(f"   数据目录: {config.DATA_DIR}")
    print(f"   调试模式: {'开启' if config.FLASK_DEBUG else '关闭'}")
    print(f"   按 Ctrl+C 停止服务")
    print("=" * 50)
    
    try:
        app.run(
            host=config.FLASK_HOST,
            port=config.FLASK_PORT,
            debug=config.FLASK_DEBUG
        )
    except KeyboardInterrupt:
        print("\n👋 服务已停止")
    except Exception as e:
        print(f"❌ Web服务启动失败: {e}")

def list_files_mode(args):
    """文件列表模式"""
    print("📁 文件列表模式...")
    
    try:
        data_dir = config.DATA_DIR
        if not os.path.exists(data_dir):
            print(f"❌ 数据目录不存在: {data_dir}")
            return
        
        print(f"📂 数据目录: {data_dir}")
        print("=" * 50)
        
        # 列出CSV文件
        csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
        if csv_files:
            print("📊 数据文件:")
            for file in sorted(csv_files):
                file_path = os.path.join(data_dir, file)
                size = os.path.getsize(file_path)
                modified = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
                print(f"   📄 {file} ({size} bytes, {modified})")
        else:
            print("   📄 暂无数据文件")
        
        # 列出JSON文件
        json_files = [f for f in os.listdir(data_dir) if f.endswith('.json')]
        if json_files:
            print("\n📋 分析文件:")
            for file in sorted(json_files):
                file_path = os.path.join(data_dir, file)
                size = os.path.getsize(file_path)
                modified = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
                print(f"   📄 {file} ({size} bytes, {modified})")
        else:
            print("   📄 暂无分析文件")
            
    except Exception as e:
        print(f"❌ 获取文件列表失败: {e}")

def main():
    """主函数"""
    # 创建配置实例
    config = Config()
    
    parser = argparse.ArgumentParser(
        description='小红书热门博客分析系统',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python main.py crawl -t "美食" -l 20                    # 爬取美食主题20条笔记
  python main.py crawl -t "旅行" -l 50 -a                 # 爬取并分析旅行主题
  python main.py analyze -f data/xhs_美食_20241201.csv    # 分析指定文件
  python main.py analyze -f data/xhs_美食_20241201.csv -t comprehensive  # 综合分析
  python main.py web                                      # 启动Web应用
  python main.py list                                     # 列出所有文件
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # 爬取命令
    crawl_parser = subparsers.add_parser('crawl', help='爬取数据')
    crawl_parser.add_argument('-t', '--topic', required=True, help='搜索主题')
    crawl_parser.add_argument('-l', '--limit', type=int, default=20, help='获取数量 (默认: 20)')
    crawl_parser.add_argument('-c', '--cookies', help='cookies字符串')
    crawl_parser.add_argument('-o', '--output', help='输出文件名')
    crawl_parser.add_argument('-a', '--analyze', action='store_true', help='爬取后自动分析')
    
    # 分析命令
    analyze_parser = subparsers.add_parser('analyze', help='分析数据')
    analyze_parser.add_argument('-f', '--file', required=True, help='数据文件路径')
    analyze_parser.add_argument('-t', '--type', choices=['comprehensive', 'trends', 'ai'], 
                               default='comprehensive', help='分析类型 (默认: comprehensive)')
    analyze_parser.add_argument('-o', '--output', help='输出文件名')
    
    # Web命令
    web_parser = subparsers.add_parser('web', help='启动Web应用')
    
    # 文件列表命令
    list_parser = subparsers.add_parser('list', help='列出文件')
    
    args = parser.parse_args()
    
    if not args.command:
        print_banner()
        parser.print_help()
        return
    
    # 确保必要目录存在
    config.ensure_directories()
    
    # 根据命令执行相应功能
    if args.command == 'crawl':
        crawl_mode(args)
    elif args.command == 'analyze':
        analyze_mode(args)
    elif args.command == 'web':
        web_mode(args)
    elif args.command == 'list':
        list_files_mode(args)

if __name__ == '__main__':
    main() 