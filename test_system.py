#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
系统测试脚本
用于验证小红书热门博客分析系统的各个模块功能
"""

import os
import sys
import json
import pandas as pd
from datetime import datetime

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import Config
from crawler.xhs_crawler import XHSCrawler
from ai_analyzer.deepseek_analyzer import DeepSeekAnalyzer

def test_config():
    """测试配置模块"""
    print("🔧 测试配置模块...")
    try:
        config = Config()
        print(f"   ✅ 配置加载成功")
        print(f"   📁 数据目录: {config.DATA_DIR}")
        print(f"   🌐 API基础URL: {config.DEEPSEEK_API_BASE}")
        return True
    except Exception as e:
        print(f"   ❌ 配置加载失败: {e}")
        return False

def test_crawler():
    """测试爬虫模块"""
    print("\n🕷️ 测试爬虫模块...")
    try:
        crawler = XHSCrawler()
        print("   ✅ 爬虫初始化成功")
        
        # 创建测试数据
        test_data = [
            {
                'title': '美食探店分享',
                'author': '美食达人',
                'likes': '1.2k',
                'link': 'https://example.com/1',
                'publish_time': '2024-01-01',
                'crawl_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            },
            {
                'title': '旅行攻略',
                'author': '旅行博主',
                'likes': '856',
                'link': 'https://example.com/2',
                'publish_time': '2024-01-02',
                'crawl_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            },
            {
                'title': '穿搭技巧',
                'author': '时尚博主',
                'likes': '2.1k',
                'link': 'https://example.com/3',
                'publish_time': '2024-01-03',
                'crawl_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        ]
        
        # 保存测试数据
        filepath = crawler.save_to_csv(test_data, 'test_data.csv')
        print(f"   ✅ 测试数据保存成功: {filepath}")
        
        return True, filepath
    except Exception as e:
        print(f"   ❌ 爬虫测试失败: {e}")
        return False, None

def test_analyzer():
    """测试分析器模块"""
    print("\n🤖 测试分析器模块...")
    try:
        analyzer = DeepSeekAnalyzer()
        print("   ✅ 分析器初始化成功")
        
        # 创建测试数据
        test_df = pd.DataFrame({
            'title': ['美食探店分享', '旅行攻略', '穿搭技巧', '护肤心得', '健身教程'],
            'author': ['美食达人', '旅行博主', '时尚博主', '美妆博主', '健身教练'],
            'likes': ['1.2k', '856', '2.1k', '1.5k', '3.2k'],
            'publish_time': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05']
        })
        
        # 测试趋势分析
        trends = analyzer.analyze_trends(test_df)
        print("   ✅ 趋势分析完成")
        print(f"   📊 总笔记数: {trends.get('total_notes', 0)}")
        print(f"   👥 热门作者数: {len(trends.get('top_authors', []))}")
        print(f"   🔥 热门话题数: {len(trends.get('popular_topics', []))}")
        
        # 测试AI分析
        ai_result = analyzer.analyze_with_ai(test_df)
        print("   ✅ AI分析完成")
        
        # 保存分析结果
        analysis_result = {
            'trends': trends,
            'ai_analysis': ai_result,
            'analysis_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'test_mode': True
        }
        
        analysis_file = analyzer.save_analysis(analysis_result, 'test_analysis.json')
        print(f"   📄 分析结果保存成功: {analysis_file}")
        
        return True
    except Exception as e:
        print(f"   ❌ 分析器测试失败: {e}")
        return False

def test_web_app():
    """测试Web应用模块"""
    print("\n🌐 测试Web应用模块...")
    try:
        from web_app.app import app
        print("   ✅ Web应用导入成功")
        
        # 测试应用配置
        with app.test_client() as client:
            # 测试健康检查
            response = client.get('/api/health')
            if response.status_code == 200:
                print("   ✅ 健康检查API正常")
            else:
                print(f"   ❌ 健康检查API失败: {response.status_code}")
                return False
            
            # 测试文件列表API
            response = client.get('/api/files')
            if response.status_code == 200:
                print("   ✅ 文件列表API正常")
            else:
                print(f"   ❌ 文件列表API失败: {response.status_code}")
                return False
        
        return True
    except Exception as e:
        print(f"   ❌ Web应用测试失败: {e}")
        return False

def test_data_flow():
    """测试完整数据流"""
    print("\n🔄 测试完整数据流...")
    try:
        # 1. 创建测试数据
        test_data = [
            {
                'title': '美食探店分享',
                'author': '美食达人',
                'likes': '1.2k',
                'link': 'https://example.com/1',
                'publish_time': '2024-01-01',
                'crawl_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            },
            {
                'title': '旅行攻略',
                'author': '旅行博主',
                'likes': '856',
                'link': 'https://example.com/2',
                'publish_time': '2024-01-02',
                'crawl_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        ]
        
        # 2. 保存数据
        crawler = XHSCrawler()
        csv_file = crawler.save_to_csv(test_data, 'flow_test.csv')
        print("   ✅ 步骤1: 数据保存完成")
        
        # 3. 加载数据
        analyzer = DeepSeekAnalyzer()
        df = analyzer.load_data(csv_file)
        print(f"   ✅ 步骤2: 数据加载完成 ({len(df)} 条记录)")
        
        # 4. 分析数据
        trends = analyzer.analyze_trends(df)
        ai_result = analyzer.analyze_with_ai(df)
        print("   ✅ 步骤3: 数据分析完成")
        
        # 5. 保存分析结果
        analysis_result = {
            'trends': trends,
            'ai_analysis': ai_result,
            'analysis_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'data_file': csv_file
        }
        
        analysis_file = analyzer.save_analysis(analysis_result, 'flow_test_analysis.json')
        print("   ✅ 步骤4: 分析结果保存完成")
        
        # 6. 验证结果
        if os.path.exists(csv_file) and os.path.exists(analysis_file):
            print("   ✅ 步骤5: 文件验证通过")
            return True
        else:
            print("   ❌ 步骤5: 文件验证失败")
            return False
            
    except Exception as e:
        print(f"   ❌ 数据流测试失败: {e}")
        return False

def cleanup_test_files():
    """清理测试文件"""
    print("\n🧹 清理测试文件...")
    test_files = [
        'test_data.csv',
        'test_analysis.json',
        'flow_test.csv',
        'flow_test_analysis.json'
    ]
    
    config = Config()
    for filename in test_files:
        filepath = os.path.join(config.DATA_DIR, filename)
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
                print(f"   🗑️ 删除: {filename}")
            except Exception as e:
                print(f"   ❌ 删除失败 {filename}: {e}")

def main():
    """主测试函数"""
    print("🧪 小红书热门博客分析系统 - 功能测试")
    print("=" * 50)
    
    # 确保数据目录存在
    config = Config()
    os.makedirs(config.DATA_DIR, exist_ok=True)
    
    # 测试结果统计
    test_results = []
    
    # 1. 测试配置模块
    test_results.append(("配置模块", test_config()))
    
    # 2. 测试爬虫模块
    crawler_success, csv_file = test_crawler()
    test_results.append(("爬虫模块", crawler_success))
    
    # 3. 测试分析器模块
    test_results.append(("分析器模块", test_analyzer()))
    
    # 4. 测试Web应用模块
    test_results.append(("Web应用模块", test_web_app()))
    
    # 5. 测试完整数据流
    test_results.append(("完整数据流", test_data_flow()))
    
    # 输出测试结果
    print("\n📊 测试结果汇总:")
    print("=" * 50)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"   {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 总体结果: {passed}/{total} 个测试通过")
    
    if passed == total:
        print("🎉 所有测试通过！系统运行正常。")
    else:
        print("⚠️ 部分测试失败，请检查相关模块。")
    
    # 清理测试文件
    cleanup_test_files()
    
    print("\n✨ 测试完成！")

if __name__ == '__main__':
    main() 