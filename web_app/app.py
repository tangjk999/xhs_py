from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import os
import sys
import json
import pandas as pd
from datetime import datetime

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config
from crawler.xhs_crawler import XHSCrawler
from ai_analyzer.deepseek_analyzer import DeepSeekAnalyzer

app = Flask(__name__)
CORS(app)

# 配置
config = Config()
app.config['SECRET_KEY'] = config.FLASK_SECRET_KEY

# 全局变量
crawler = None
analyzer = None

def get_crawler():
    global crawler
    if crawler is None:
        crawler = XHSCrawler()
    return crawler

def get_analyzer():
    global analyzer
    if analyzer is None:
        analyzer = DeepSeekAnalyzer()
    return analyzer

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')

@app.route('/api/crawl', methods=['POST'])
def crawl_data():
    """爬取数据API"""
    try:
        data = request.get_json()
        topic = data.get('topic', '')
        limit = int(data.get('limit', 20))
        
        if not topic:
            return jsonify({'error': '请提供搜索主题'}), 400
        
        crawler = get_crawler()
        filepath = crawler.crawl_hot_notes(topic, limit)
        
        if filepath:
            return jsonify({
                'success': True,
                'message': f'成功爬取 {limit} 条笔记',
                'filepath': filepath
            })
        else:
            return jsonify({'error': '爬取失败，请检查网络连接或重试'}), 500
            
    except Exception as e:
        return jsonify({'error': f'爬取过程中出错: {str(e)}'}), 500

@app.route('/api/analyze', methods=['POST'])
def analyze_data():
    """分析数据API"""
    try:
        data = request.get_json()
        csv_file = data.get('csv_file', '')
        
        if not csv_file or not os.path.exists(csv_file):
            return jsonify({'error': 'CSV文件不存在'}), 400
        
        analyzer = get_analyzer()
        
        # 加载数据
        df = analyzer.load_data(csv_file)
        if df.empty:
            return jsonify({'error': '数据加载失败'}), 500
        
        # 进行趋势分析
        trends = analyzer.analyze_trends(df)
        
        # 进行AI分析
        ai_result = analyzer.analyze_with_ai(df)
        
        # 合并分析结果
        analysis_result = {
            'trends': trends,
            'ai_analysis': ai_result,
            'analysis_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'data_file': csv_file
        }
        
        # 保存分析结果
        analysis_file = analyzer.save_analysis(analysis_result)
        
        return jsonify({
            'success': True,
            'message': '分析完成',
            'analysis': analysis_result,
            'analysis_file': analysis_file
        })
        
    except Exception as e:
        return jsonify({'error': f'分析过程中出错: {str(e)}'}), 500

@app.route('/api/files')
def list_files():
    """列出数据文件"""
    try:
        data_dir = config.DATA_DIR
        if not os.path.exists(data_dir):
            return jsonify({'files': []})
        
        files = []
        for filename in os.listdir(data_dir):
            if filename.endswith('.csv'):
                filepath = os.path.join(data_dir, filename)
                stat = os.stat(filepath)
                files.append({
                    'name': filename,
                    'path': filepath,
                    'size': stat.st_size,
                    'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                })
        
        # 按修改时间排序
        files.sort(key=lambda x: x['modified'], reverse=True)
        
        return jsonify({'files': files})
        
    except Exception as e:
        return jsonify({'error': f'获取文件列表失败: {str(e)}'}), 500

@app.route('/api/analysis/<filename>')
def get_analysis(filename):
    """获取分析结果"""
    try:
        filepath = os.path.join(config.DATA_DIR, filename)
        if not os.path.exists(filepath):
            return jsonify({'error': '分析文件不存在'}), 404
        
        with open(filepath, 'r', encoding='utf-8') as f:
            analysis_data = json.load(f)
        
        return jsonify(analysis_data)
        
    except Exception as e:
        return jsonify({'error': f'读取分析文件失败: {str(e)}'}), 500

@app.route('/api/download/<filename>')
def download_file(filename):
    """下载文件"""
    try:
        filepath = os.path.join(config.DATA_DIR, filename)
        if not os.path.exists(filepath):
            return jsonify({'error': '文件不存在'}), 404
        
        return send_file(filepath, as_attachment=True)
        
    except Exception as e:
        return jsonify({'error': f'下载文件失败: {str(e)}'}), 500

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
    return jsonify({'error': '页面不存在'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': '服务器内部错误'}), 500

if __name__ == '__main__':
    # 确保必要的目录存在
    os.makedirs(config.DATA_DIR, exist_ok=True)
    os.makedirs(config.TEMPLATES_DIR, exist_ok=True)
    os.makedirs(config.STATIC_DIR, exist_ok=True)
    
    print(f"启动Web应用...")
    print(f"数据目录: {config.DATA_DIR}")
    print(f"模板目录: {config.TEMPLATES_DIR}")
    print(f"静态文件目录: {config.STATIC_DIR}")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=config.FLASK_DEBUG
    ) 