#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小红书热门博客分析系统 - 快速启动脚本
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 8):
        print("❌ 错误: 需要Python 3.8或更高版本")
        print(f"当前版本: {sys.version}")
        return False
    print(f"✅ Python版本检查通过: {sys.version}")
    return True

def check_dependencies():
    """检查依赖包"""
    required_packages = [
        'flask', 'pandas', 'selenium', 'requests', 
        'beautifulsoup4', 'python-dotenv'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ 缺少依赖包: {', '.join(missing_packages)}")
        print("请运行: pip install -r requirements.txt")
        return False
    
    print("✅ 依赖包检查通过")
    return True

def setup_environment():
    """设置环境"""
    # 创建必要目录
    directories = ['data', 'logs', 'static', 'templates']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"📁 创建目录: {directory}")
    
    # 检查.env文件
    if not Path('.env').exists():
        if Path('env_example.txt').exists():
            print("📝 创建.env文件...")
            with open('env_example.txt', 'r', encoding='utf-8') as f:
                content = f.read()
            with open('.env', 'w', encoding='utf-8') as f:
                f.write(content)
            print("✅ .env文件已创建，请编辑配置")
        else:
            print("⚠️ 未找到.env文件，请手动创建")
    
    print("✅ 环境设置完成")

def show_menu():
    """显示菜单"""
    print("\n" + "="*50)
    print("小红书热门博客分析系统")
    print("="*50)
    print("1. 启动Web应用")
    print("2. 爬取数据")
    print("3. 分析数据")
    print("4. 查看文件")
    print("5. 安装依赖")
    print("6. 退出")
    print("="*50)

def run_web_app():
    """启动Web应用"""
    print("🌐 启动Web应用...")
    try:
        subprocess.run([sys.executable, 'main.py', 'web'], check=True)
    except KeyboardInterrupt:
        print("\n👋 Web应用已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")

def run_crawl():
    """运行爬取"""
    topic = input("请输入搜索主题: ").strip()
    if not topic:
        print("❌ 主题不能为空")
        return
    
    limit = input("请输入获取数量 (默认20): ").strip()
    if not limit:
        limit = "20"
    
    try:
        limit = int(limit)
        if limit <= 0 or limit > 100:
            print("❌ 数量必须在1-100之间")
            return
    except ValueError:
        print("❌ 数量必须是数字")
        return
    
    print(f"🕷️ 开始爬取: {topic}, 数量: {limit}")
    try:
        subprocess.run([sys.executable, 'main.py', 'crawl', '-t', topic, '-l', str(limit)], check=True)
    except Exception as e:
        print(f"❌ 爬取失败: {e}")

def run_analyze():
    """运行分析"""
    # 列出可用的数据文件
    data_dir = Path('data')
    if not data_dir.exists():
        print("❌ 数据目录不存在")
        return
    
    csv_files = list(data_dir.glob('*.csv'))
    if not csv_files:
        print("❌ 没有找到数据文件，请先爬取数据")
        return
    
    print("📊 可用的数据文件:")
    for i, file in enumerate(csv_files, 1):
        print(f"  {i}. {file.name}")
    
    try:
        choice = int(input("请选择文件编号: ")) - 1
        if choice < 0 or choice >= len(csv_files):
            print("❌ 无效的选择")
            return
        
        selected_file = csv_files[choice]
        print(f"🤖 开始分析: {selected_file.name}")
        subprocess.run([sys.executable, 'main.py', 'analyze', '-f', str(selected_file)], check=True)
    except ValueError:
        print("❌ 请输入有效的数字")
    except Exception as e:
        print(f"❌ 分析失败: {e}")

def run_list():
    """查看文件"""
    try:
        subprocess.run([sys.executable, 'main.py', 'list'], check=True)
    except Exception as e:
        print(f"❌ 查看文件失败: {e}")

def install_dependencies():
    """安装依赖"""
    print("📦 安装依赖包...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], check=True)
        print("✅ 依赖安装完成")
    except Exception as e:
        print(f"❌ 安装失败: {e}")

def main():
    """主函数"""
    print("🚀 小红书热门博客分析系统启动器")
    
    # 检查环境
    if not check_python_version():
        return
    
    if not check_dependencies():
        print("\n是否现在安装依赖? (y/n): ", end="")
        if input().lower() == 'y':
            install_dependencies()
        else:
            return
    
    # 设置环境
    setup_environment()
    
    # 主循环
    while True:
        show_menu()
        choice = input("请选择操作 (1-6): ").strip()
        
        if choice == '1':
            run_web_app()
        elif choice == '2':
            run_crawl()
        elif choice == '3':
            run_analyze()
        elif choice == '4':
            run_list()
        elif choice == '5':
            install_dependencies()
        elif choice == '6':
            print("👋 再见!")
            break
        else:
            print("❌ 无效的选择，请重试")
        
        input("\n按回车键继续...")

if __name__ == '__main__':
    main() 