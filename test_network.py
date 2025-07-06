#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网络连接测试脚本
用于测试小红书爬虫的网络连通性和环境配置
"""

import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import subprocess
import sys
import os

def test_basic_network():
    """测试基本网络连接"""
    print("=" * 50)
    print("1. 测试基本网络连接")
    print("=" * 50)
    
    # 测试DNS解析
    try:
        import socket
        print("✓ DNS解析测试...")
        socket.gethostbyname("www.xiaohongshu.com")
        print("  DNS解析正常")
    except Exception as e:
        print(f"✗ DNS解析失败: {e}")
    
    # 测试ping
    try:
        print("\n✓ Ping测试...")
        result = subprocess.run(['ping', '-c', '3', 'www.xiaohongshu.com'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("  Ping成功")
        else:
            print("  Ping失败")
    except Exception as e:
        print(f"  Ping测试异常: {e}")

def test_requests():
    """测试requests库的网络连接"""
    print("\n" + "=" * 50)
    print("2. 测试requests库")
    print("=" * 50)
    
    # 测试基本HTTP请求
    test_urls = [
        "https://httpbin.org/get",
        "https://www.baidu.com",
        "https://www.xiaohongshu.com"
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    for url in test_urls:
        try:
            print(f"\n✓ 测试 {url}")
            response = requests.get(url, headers=headers, timeout=10)
            print(f"  状态码: {response.status_code}")
            print(f"  响应时间: {response.elapsed.total_seconds():.2f}秒")
            if response.status_code == 200:
                print("  ✓ 请求成功")
            else:
                print(f"  ⚠ 请求返回非200状态码")
        except requests.exceptions.Timeout:
            print("  ✗ 请求超时")
        except requests.exceptions.ConnectionError:
            print("  ✗ 连接错误")
        except Exception as e:
            print(f"  ✗ 请求失败: {e}")

def test_selenium_environment():
    """测试Selenium环境"""
    print("\n" + "=" * 50)
    print("3. 测试Selenium环境")
    print("=" * 50)
    
    # 检查ChromeDriver
    try:
        print("✓ 检查ChromeDriver...")
        driver_path = ChromeDriverManager().install()
        print(f"  ChromeDriver路径: {driver_path}")
    except Exception as e:
        print(f"✗ ChromeDriver检查失败: {e}")
        return
    
    # 测试Selenium基本功能
    try:
        print("\n✓ 初始化Chrome浏览器...")
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # 无头模式
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        print("  ✓ Chrome浏览器初始化成功")
        
        # 测试访问网页
        print("\n✓ 测试访问百度...")
        driver.get("https://www.baidu.com")
        time.sleep(2)
        
        title = driver.title
        print(f"  页面标题: {title}")
        print("  ✓ 页面访问成功")
        
        # 测试访问小红书
        print("\n✓ 测试访问小红书...")
        driver.get("https://www.xiaohongshu.com")
        time.sleep(3)
        
        title = driver.title
        print(f"  页面标题: {title}")
        print("  ✓ 小红书页面访问成功")
        
        driver.quit()
        print("  ✓ 浏览器正常关闭")
        
    except Exception as e:
        print(f"✗ Selenium测试失败: {e}")
        try:
            driver.quit()
        except:
            pass

def test_proxy_settings():
    """测试代理设置"""
    print("\n" + "=" * 50)
    print("4. 检查代理设置")
    print("=" * 50)
    
    # 检查环境变量中的代理设置
    proxy_vars = ['http_proxy', 'https_proxy', 'HTTP_PROXY', 'HTTPS_PROXY']
    for var in proxy_vars:
        value = os.environ.get(var)
        if value:
            print(f"  {var}: {value}")
        else:
            print(f"  {var}: 未设置")
    
    # 检查系统代理
    try:
        import urllib.request
        opener = urllib.request.build_opener()
        print("\n✓ 测试系统代理...")
        response = opener.open("https://httpbin.org/ip", timeout=10)
        ip_info = response.read().decode()
        print(f"  当前IP信息: {ip_info}")
    except Exception as e:
        print(f"  ✗ 代理测试失败: {e}")

def main():
    """主函数"""
    print("小红书爬虫网络环境测试")
    print("=" * 60)
    
    # 执行各项测试
    test_basic_network()
    test_requests()
    test_selenium_environment()
    test_proxy_settings()
    
    print("\n" + "=" * 60)
    print("测试完成！")
    print("如果看到较多 ✗ 标记，请检查网络连接或考虑使用VPN/代理")

if __name__ == "__main__":
    main()
 