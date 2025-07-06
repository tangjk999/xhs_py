#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从国内镜像源下载ChromeDriver
"""

import requests
import os
import zipfile
import subprocess
import sys
import json

def get_chrome_version():
    """获取Chrome浏览器版本"""
    try:
        result = subprocess.run(['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            version_str = result.stdout.strip()
            import re
            match = re.search(r'(\d+)\.(\d+)\.(\d+)\.(\d+)', version_str)
            if match:
                return f"{match.group(1)}.{match.group(2)}.{match.group(3)}.{match.group(4)}"
    except Exception as e:
        print(f"获取Chrome版本失败: {e}")
    return None

def download_chromedriver():
    """从国内镜像源下载ChromeDriver"""
    chrome_version = get_chrome_version()
    if not chrome_version:
        print("无法获取Chrome版本")
        return False
    
    print(f"Chrome版本: {chrome_version}")
    
    # 尝试使用webdriver-manager配置国内镜像源
    try:
        from webdriver_manager.chrome import ChromeDriverManager
        from webdriver_manager.core.os_manager import ChromeType
        
        # 设置环境变量使用国内镜像
        os.environ['GH_TOKEN'] = ''
        os.environ['WDM_LOCAL'] = '1'
        os.environ['WDM_SSL_VERIFY'] = '0'
        
        # 尝试下载
        driver_path = ChromeDriverManager().install()
        print(f"ChromeDriver下载成功: {driver_path}")
        return True
    except Exception as e:
        print(f"webdriver-manager下载失败: {e}")
    
    # 如果webdriver-manager失败，尝试手动下载
    # 国内镜像源列表
    mirrors = [
        f"https://cdn.npmmirror.com/binaries/chromedriver/{chrome_version}/chromedriver_mac64.zip",
        f"https://registry.npmmirror.com/-/binary/chromedriver/{chrome_version}/chromedriver_mac64.zip",
        f"https://npm.taobao.org/mirrors/chromedriver/{chrome_version}/chromedriver_mac64.zip",
        f"https://npm.taobao.org/mirrors/chromedriver/{chrome_version}/chromedriver_mac_arm64.zip",
    ]
    
    # 检查系统架构
    import platform
    if platform.machine() == 'arm64':
        # ARM架构，尝试ARM版本
        mirrors = [
            f"https://cdn.npmmirror.com/binaries/chromedriver/{chrome_version}/chromedriver_mac_arm64.zip",
            f"https://registry.npmmirror.com/-/binary/chromedriver/{chrome_version}/chromedriver_mac_arm64.zip",
            f"https://npm.taobao.org/mirrors/chromedriver/{chrome_version}/chromedriver_mac_arm64.zip",
        ] + mirrors
    
    for mirror in mirrors:
        try:
            print(f"尝试从镜像源下载: {mirror}")
            response = requests.get(mirror, timeout=30, verify=False)
            if response.status_code == 200:
                # 保存文件
                filename = f"chromedriver_{chrome_version}.zip"
                with open(filename, 'wb') as f:
                    f.write(response.content)
                
                print(f"下载成功: {filename}")
                
                # 解压文件
                with zipfile.ZipFile(filename, 'r') as zip_ref:
                    zip_ref.extractall('.')
                
                # 设置执行权限
                os.chmod('chromedriver', 0o755)
                print("ChromeDriver安装完成")
                
                # 清理zip文件
                os.remove(filename)
                return True
            else:
                print(f"下载失败，状态码: {response.status_code}")
        except Exception as e:
            print(f"从镜像源下载失败: {e}")
            continue
    
    print("所有镜像源都失败了")
    return False

if __name__ == "__main__":
    success = download_chromedriver()
    if success:
        print("ChromeDriver下载并安装成功！")
    else:
        print("ChromeDriver下载失败！") 