from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import os
import sys
import json
import pandas as pd
from datetime import datetime
import traceback

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config
from crawler.xhs_crawler import XHSCrawler
from crawler.xhs_simple_crawler import XHSSimpleCrawler
from ai_analyzer.deepseek_analyzer import DeepSeekAnalyzer

app = Flask(__name__)
CORS(app)

# 配置
config = Config()
app.config['SECRET_KEY'] = config.FLASK_SECRET_KEY

# 确保必要目录存在
config.ensure_directories()

# API密钥文件路径
API_KEY_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'api_key.json')

# Cookies文件路径
COOKIES_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'xhs_cookies.json')

# 全局变量
crawler = None
analyzer = None

def save_api_key(api_key):
    """保存API密钥到本地文件"""
    try:
        data = {'deepseek_api_key': api_key}
        with open(API_KEY_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"保存API密钥失败: {e}")
        return False

def load_api_key():
    """从本地文件加载API密钥"""
    try:
        if os.path.exists(API_KEY_FILE):
            with open(API_KEY_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('deepseek_api_key', '')
        return ''
    except Exception as e:
        print(f"加载API密钥失败: {e}")
        return ''

def save_cookies(cookies):
    """保存cookies到本地文件"""
    try:
        data = {'xhs_cookies': cookies}
        with open(COOKIES_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"保存cookies失败: {e}")
        return False

def load_cookies():
    """从本地文件加载cookies"""
    try:
        if os.path.exists(COOKIES_FILE):
            with open(COOKIES_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('xhs_cookies', '')
        return ''
    except Exception as e:
        print(f"加载cookies失败: {e}")
        return ''

def get_crawler():
    global crawler
    if crawler is None:
        crawler = XHSCrawler()
    return crawler

def get_simple_crawler():
    """获取简单爬虫实例"""
    return XHSSimpleCrawler()

def get_analyzer():
    global analyzer
    if analyzer is None:
        analyzer = DeepSeekAnalyzer()
    return analyzer

def get_data_files():
    """获取数据文件列表"""
    try:
        data_dir = config.DATA_DIR
        if not os.path.exists(data_dir):
            return []
        
        files = []
        for file in os.listdir(data_dir):
            if file.endswith('.csv'):
                file_path = os.path.join(data_dir, file)
                files.append({
                    'name': file,
                    'path': file_path,
                    'size': os.path.getsize(file_path),
                    'modified': datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
                })
        
        # 按修改时间排序，最新的在前
        files.sort(key=lambda x: x['modified'], reverse=True)
        return files
    except Exception as e:
        print(f"获取数据文件列表失败: {e}")
        return []

def get_analysis_files():
    """获取分析文件列表"""
    try:
        data_dir = config.DATA_DIR
        if not os.path.exists(data_dir):
            return []
        
        files = []
        for file in os.listdir(data_dir):
            if file.endswith('.json'):
                file_path = os.path.join(data_dir, file)
                files.append({
                    'name': file,
                    'path': file_path,
                    'size': os.path.getsize(file_path),
                    'modified': datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
                })
        
        # 按修改时间排序，最新的在前
        files.sort(key=lambda x: x['modified'], reverse=True)
        return files
    except Exception as e:
        print(f"获取分析文件列表失败: {e}")
        return []

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')

@app.route('/api/save-api-key', methods=['POST'])
def save_api_key_route():
    """保存API密钥"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': '请求数据为空'}), 400
        
        api_key = data.get('api_key', '').strip()
        
        if save_api_key(api_key):
            return jsonify({
                'success': True,
                'message': 'API密钥保存成功'
            })
        else:
            return jsonify({'error': 'API密钥保存失败'}), 500
            
    except Exception as e:
        print(f"保存API密钥时出错: {e}")
        return jsonify({'error': f'保存API密钥时出错: {str(e)}'}), 500

@app.route('/api/load-api-key', methods=['GET'])
def load_api_key_route():
    """加载API密钥"""
    try:
        api_key = load_api_key()
        return jsonify({
            'success': True,
            'api_key': api_key
        })
    except Exception as e:
        print(f"加载API密钥时出错: {e}")
        return jsonify({'error': f'加载API密钥时出错: {str(e)}'}), 500

@app.route('/api/save-cookies', methods=['POST'])
def save_cookies_route():
    """保存cookies"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': '请求数据为空'}), 400
        
        cookies = data.get('cookies', '').strip()
        
        if save_cookies(cookies):
            return jsonify({
                'success': True,
                'message': 'cookies保存成功'
            })
        else:
            return jsonify({'error': 'cookies保存失败'}), 500
            
    except Exception as e:
        print(f"保存cookies时出错: {e}")
        return jsonify({'error': f'保存cookies时出错: {str(e)}'}), 500

@app.route('/api/load-cookies', methods=['GET'])
def load_cookies_route():
    """加载cookies"""
    try:
        cookies = load_cookies()
        return jsonify({
            'success': True,
            'cookies': cookies
        })
    except Exception as e:
        print(f"加载cookies时出错: {e}")
        return jsonify({'error': f'加载cookies时出错: {str(e)}'}), 500

@app.route('/api/crawl', methods=['POST'])
def crawl_data():
    """爬取数据API"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': '请求数据为空'}), 400
        
        topic = data.get('topic', '').strip()
        limit = int(data.get('limit', 20))
        cookies = data.get('cookies', '').strip()
        
        # 参数验证
        if not topic:
            return jsonify({'error': '请提供搜索主题'}), 400
        
        if limit <= 0 or limit > 100:
            return jsonify({'error': '获取数量必须在1-100之间'}), 400
        
        print(f"开始爬取: 主题={topic}, 数量={limit}")
        
        # 获取爬虫实例
        crawler = get_crawler()
        
        # 执行爬取
        filepath = crawler.crawl_hot_notes(topic, limit, cookies)
        
        if filepath:
            # 读取爬取的数据用于返回
            try:
                df = pd.read_csv(filepath, encoding='utf-8-sig')
                data_list = df.to_dict('records')
                
                return jsonify({
                    'success': True,
                    'message': f'成功爬取 {len(data_list)} 条笔记',
                    'data': data_list,
                    'filepath': filepath,
                    'filename': os.path.basename(filepath)
                })
            except Exception as e:
                print(f"读取爬取数据失败: {e}")
                return jsonify({
                    'success': True,
                    'message': '爬取完成，但读取数据失败',
                    'filepath': filepath,
                    'filename': os.path.basename(filepath)
                })
        else:
            return jsonify({'error': '爬取失败，未获取到数据'}), 500
            
    except ValueError as e:
        return jsonify({'error': f'参数错误: {str(e)}'}), 400
    except Exception as e:
        print(f"爬取数据时出错: {e}")
        print(traceback.format_exc())
        return jsonify({'error': f'爬取数据时出错: {str(e)}'}), 500

@app.route('/api/analyze', methods=['POST'])
def analyze_data():
    """分析数据API"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': '请求数据为空'}), 400
        
        filename = data.get('file', '').strip()
        analysis_type = data.get('type', 'comprehensive')
        
        if not filename:
            return jsonify({'error': '请选择数据文件'}), 400
        
        # 构建文件路径
        filepath = os.path.join(config.DATA_DIR, filename)
        if not os.path.exists(filepath):
            return jsonify({'error': '文件不存在'}), 404
        
        print(f"开始分析: 文件={filename}, 类型={analysis_type}")
        
        # 获取分析器实例
        analyzer = get_analyzer()
        
        # 加载数据
        df = analyzer.load_data(filepath)
        if df.empty:
            return jsonify({'error': '数据加载失败或数据为空'}), 500
        
        # 根据分析类型执行不同的分析
        if analysis_type == 'comprehensive':
            # 综合分析
            result = analyzer.generate_comprehensive_report(df)
        elif analysis_type == 'trends':
            # 趋势分析
            result = {
                'trends': analyzer.analyze_trends(df),
                'analysis_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        elif analysis_type == 'ai':
            # AI深度分析
            result = analyzer.analyze_with_ai(df)
        else:
            return jsonify({'error': '不支持的分析类型'}), 400
        
        # 保存分析结果
        analysis_filename = f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        analysis_filepath = analyzer.save_analysis(result, analysis_filename)
        
        return jsonify({
            'success': True,
            'message': '分析完成',
            'data': result,
            'analysis_file': analysis_filename
        })
        
    except Exception as e:
        print(f"分析数据时出错: {e}")
        print(traceback.format_exc())
        return jsonify({'error': f'分析数据时出错: {str(e)}'}), 500

@app.route('/api/files')
def list_files():
    """获取文件列表"""
    try:
        data_files = get_data_files()
        analysis_files = get_analysis_files()
        
        return jsonify({
            'success': True,
            'data_files': [f['name'] for f in data_files],
            'analysis_files': [f['name'] for f in analysis_files],
            'data_files_detail': data_files,
            'analysis_files_detail': analysis_files
        })
    except Exception as e:
        print(f"获取文件列表时出错: {e}")
        return jsonify({'error': f'获取文件列表时出错: {str(e)}'}), 500

@app.route('/api/analysis/<filename>')
def get_analysis(filename):
    """获取分析结果"""
    try:
        filepath = os.path.join(config.DATA_DIR, filename)
        if not os.path.exists(filepath):
            return jsonify({'error': '文件不存在'}), 404
        
        with open(filepath, 'r', encoding='utf-8') as f:
            analysis_data = json.load(f)
        
        return jsonify({
            'success': True,
            'data': analysis_data
        })
    except Exception as e:
        print(f"获取分析结果时出错: {e}")
        return jsonify({'error': f'获取分析结果时出错: {str(e)}'}), 500

@app.route('/api/download/<filename>')
def download_file(filename):
    """下载文件"""
    try:
        filepath = os.path.join(config.DATA_DIR, filename)
        if not os.path.exists(filepath):
            return jsonify({'error': '文件不存在'}), 404
        
        return send_file(
            filepath,
            as_attachment=True,
            download_name=filename,
            mimetype='application/octet-stream'
        )
    except Exception as e:
        print(f"下载文件时出错: {e}")
        return jsonify({'error': f'下载文件时出错: {str(e)}'}), 500

@app.route('/api/health')
def health_check():
    """健康检查"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': '接口不存在'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': '服务器内部错误'}), 500

if __name__ == '__main__':
    print("🚀 启动小红书热门博客分析系统...")
    print(f"📁 数据目录: {config.DATA_DIR}")
    print(f"🌐 访问地址: http://{config.FLASK_HOST}:{config.FLASK_PORT}")
    
    app.run(
        host=config.FLASK_HOST,
        port=config.FLASK_PORT,
        debug=config.FLASK_DEBUG
    ) 