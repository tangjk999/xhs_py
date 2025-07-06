#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
提取小红书页面中的JavaScript数据
"""

import re
import json
import sys

def extract_js_data(html_content):
    """从HTML内容中提取JavaScript数据"""
    
    # 查找JavaScript数据 - 使用更简单的方法
    start_marker = 'window.__INITIAL_STATE__='
    end_marker = ';</script>'
    
    start_pos = html_content.find(start_marker)
    if start_pos == -1:
        print("未找到 __INITIAL_STATE__ 标记")
        return None
    
    # 从开始标记后开始
    data_start = start_pos + len(start_marker)
    
    # 查找结束位置
    end_pos = html_content.find(end_marker, data_start)
    if end_pos == -1:
        print("未找到结束标记")
        return None
    
    # 提取JSON字符串
    json_str = html_content[data_start:end_pos]
    print(f"提取的JSON字符串长度: {len(json_str)}")
    print(f"JSON字符串前100字符: {json_str[:100]}")
    
    try:
        js_data = json.loads(json_str)
        return js_data
    except json.JSONDecodeError as e:
        print(f"JSON解析失败: {e}")
        print(f"JSON字符串前500字符: {json_str[:500]}")
        return None

def search_notes_data(js_data, keyword):
    """在JavaScript数据中搜索笔记信息"""
    
    def search_recursive(data, path=""):
        if isinstance(data, dict):
            for key, value in data.items():
                current_path = f"{path}.{key}" if path else key
                
                # 检查是否是笔记数据
                if key in ['notes', 'items', 'feeds', 'data'] and isinstance(value, list):
                    print(f"找到数据数组: {current_path}, 长度: {len(value)}")
                    if len(value) > 0:
                        print(f"第一个元素: {value[0]}")
                    return value
                
                # 递归搜索
                result = search_recursive(value, current_path)
                if result:
                    return result
                    
        elif isinstance(data, list) and len(data) > 0:
            # 检查列表中的第一个元素是否是笔记
            first_item = data[0]
            if isinstance(first_item, dict):
                if any(key in first_item for key in ['title', 'desc', 'content', 'note_id', 'id']):
                    print(f"找到笔记列表，长度: {len(data)}")
                    return data
    
    return search_recursive(js_data)

def main():
    if len(sys.argv) != 2:
        print("用法: python extract_js_data.py <html_file>")
        sys.exit(1)
    
    html_file = sys.argv[1]
    
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        print(f"读取HTML文件: {html_file}")
        print(f"文件大小: {len(html_content)} 字符")
        
        # 提取JavaScript数据
        js_data = extract_js_data(html_content)
        
        if js_data:
            print("成功提取JavaScript数据")
            
            # 搜索笔记数据
            notes_data = search_notes_data(js_data, "美食")
            
            if notes_data:
                print(f"找到 {len(notes_data)} 条笔记数据")
                for i, note in enumerate(notes_data[:5]):  # 只显示前5条
                    print(f"\n笔记 {i+1}:")
                    print(json.dumps(note, ensure_ascii=False, indent=2))
            else:
                print("未找到笔记数据")
                
                # 保存完整的JavaScript数据用于调试
                with open('js_data_debug.json', 'w', encoding='utf-8') as f:
                    json.dump(js_data, f, ensure_ascii=False, indent=2)
                print("已保存完整JavaScript数据到 js_data_debug.json")
        else:
            print("未找到JavaScript数据")
            
    except Exception as e:
        print(f"错误: {e}")

if __name__ == "__main__":
    main() 