#!/bin/bash

echo "🚀 开始部署小红书热门博客分析系统..."

# 检查是否安装了netlify-cli
if ! command -v netlify &> /dev/null; then
    echo "❌ 未安装netlify-cli，正在安装..."
    npm install -g netlify-cli
fi

# 构建项目
echo "📦 构建项目..."
python -m pip install -r requirements.txt

# 创建静态文件
echo "📁 创建静态文件..."
mkdir -p web_app/static
cp web_app/templates/index.html web_app/static/

# 部署到Netlify
echo "🌐 部署到Netlify..."
netlify deploy --prod --dir=web_app/static

echo "✅ 部署完成！" 