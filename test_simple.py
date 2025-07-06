#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单网络测试脚本
"""

import requests
import time

def test_network():
    """测试网络连接"""
    print("测试网络连接...")
    
    # 测试基本连接
    try:
        response = requests.get("https://www.baidu.com", timeout=10)
        print(f"✓ 百度连接成功: {response.status_code}")
    except Exception as e:
        print(f"✗ 百度连接失败: {e}")
    
    # 测试小红书
    try:
        response = requests.get("https://www.xiaohongshu.com", timeout=10)
        print(f"✓ 小红书连接成功: {response.status_code}")
    except Exception as e:
        print(f"✗ 小红书连接失败: {e}")
    
    # 测试ChromeDriver下载地址
    try:
        response = requests.get("https://storage.googleapis.com/chrome-for-testing-public/", timeout=10)
        print(f"✓ ChromeDriver下载地址可访问: {response.status_code}")
    except Exception as e:
        print(f"✗ ChromeDriver下载地址不可访问: {e}")

if __name__ == "__main__":
    test_network() 