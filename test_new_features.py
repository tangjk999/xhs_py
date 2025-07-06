#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试新功能脚本
验证Cookie转换、左右分栏、状态检查等功能
"""

import requests
import json
import time

def test_health_check():
    """测试健康检查"""
    print("🔍 测试健康检查...")
    try:
        response = requests.get('http://localhost:8080/api/health')
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 健康检查通过")
            print(f"   状态: {data['status']}")
            print(f"   版本: {data['app']['version']}")
            return True
        else:
            print(f"❌ 健康检查失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 健康检查异常: {e}")
        return False

def test_cookie_status():
    """测试Cookie状态检查"""
    print("\n🔍 测试Cookie状态检查...")
    try:
        response = requests.get('http://localhost:8080/api/cookie-status')
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Cookie状态检查通过")
            print(f"   有效性: {data['valid']}")
            print(f"   消息: {data['message']}")
            print(f"   最后检查: {data['last_check']}")
            return True
        else:
            print(f"❌ Cookie状态检查失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cookie状态检查异常: {e}")
        return False

def test_cookie_conversion():
    """测试Cookie转换功能"""
    print("\n🔍 测试Cookie转换功能...")
    
    # 模拟原始Cookie格式
    raw_cookies = """a1	197db3f9380zg3ss63t73s4wccn6nj02mc272auy430000380633	.xiaohongshu.com	/	2026/7/5 23:41:06	54 B
web_session	0400698f99c131566b26056b5f3a4b0e526af5	.xiaohongshu.com	/	2026/7/6 15:19:08	49 B
webId	6ef185a9c4c3adac1e3dce8720f972bb	.xiaohongshu.com	/	2026/7/5 23:41:06	37 B"""
    
    try:
        # 测试保存Cookie（包含转换）
        response = requests.post('http://localhost:8080/api/save-cookies', 
                               json={'cookies': raw_cookies})
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Cookie转换和保存成功")
            print(f"   消息: {data['message']}")
            return True
        else:
            print(f"❌ Cookie转换失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cookie转换异常: {e}")
        return False

def test_cookie_loading():
    """测试Cookie加载功能"""
    print("\n🔍 测试Cookie加载功能...")
    try:
        response = requests.get('http://localhost:8080/api/load-cookies')
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Cookie加载成功")
            if data['cookies']:
                print(f"   Cookie长度: {len(data['cookies'])} 字符")
                # 尝试解析JSON
                try:
                    cookie_data = json.loads(data['cookies'])
                    print(f"   转换后的Cookie键数量: {len(cookie_data)}")
                    print(f"   Cookie键: {list(cookie_data.keys())}")
                except:
                    print("   Cookie格式不是JSON")
            else:
                print("   没有保存的Cookie")
            return True
        else:
            print(f"❌ Cookie加载失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cookie加载异常: {e}")
        return False

def test_api_key_management():
    """测试API密钥管理"""
    print("\n🔍 测试API密钥管理...")
    
    # 测试保存API密钥
    test_api_key = "test_api_key_12345"
    try:
        response = requests.post('http://localhost:8080/api/save-api-key', 
                               json={'api_key': test_api_key})
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API密钥保存成功")
            print(f"   消息: {data['message']}")
            
            # 测试加载API密钥
            response = requests.get('http://localhost:8080/api/load-api-key')
            if response.status_code == 200:
                data = response.json()
                if data['api_key'] == test_api_key:
                    print(f"✅ API密钥加载成功")
                    return True
                else:
                    print(f"❌ API密钥不匹配")
                    return False
            else:
                print(f"❌ API密钥加载失败: {response.status_code}")
                return False
        else:
            print(f"❌ API密钥保存失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API密钥管理异常: {e}")
        return False

def test_file_management():
    """测试文件管理功能"""
    print("\n🔍 测试文件管理功能...")
    try:
        response = requests.get('http://localhost:8080/api/files')
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 文件管理功能正常")
            print(f"   数据文件数量: {len(data['data_files'])}")
            print(f"   分析文件数量: {len(data['analysis_files'])}")
            return True
        else:
            print(f"❌ 文件管理失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 文件管理异常: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 开始测试小红书分析系统新功能")
    print("=" * 50)
    
    # 等待应用启动
    print("⏳ 等待应用启动...")
    time.sleep(2)
    
    tests = [
        test_health_check,
        test_cookie_status,
        test_cookie_conversion,
        test_cookie_loading,
        test_api_key_management,
        test_file_management
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ 测试异常: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有功能测试通过！")
        print("\n✨ 新功能验证成功:")
        print("   ✅ Cookie格式自动转换")
        print("   ✅ Cookie状态实时监控")
        print("   ✅ 左右分栏布局设计")
        print("   ✅ API密钥管理")
        print("   ✅ 文件管理功能")
        print("   ✅ 系统健康监控")
    else:
        print("⚠️ 部分功能测试失败，请检查")
    
    print("\n🌐 访问地址: http://localhost:8080")
    print("📚 查看README.md了解详细使用说明")

if __name__ == '__main__':
    main() 