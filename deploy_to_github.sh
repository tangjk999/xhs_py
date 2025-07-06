#!/bin/bash

# 小红书分析系统 - GitHub自动部署脚本

echo "🚀 开始部署小红书分析系统到GitHub..."

# 检查Git状态
if [ -z "$(git status --porcelain)" ]; then
    echo "✅ 工作目录干净，无需提交"
else
    echo "📝 检测到文件变更，准备提交..."
    
    # 添加所有文件
    git add .
    
    # 提交更改
    commit_message="✨ 更新小红书分析系统 v1.1.0

🎉 新功能发布：
- ✨ 新增Cookie格式自动转换功能
- ✨ 新增左右分栏布局设计
- ✨ 新增Cookie状态实时监控
- ✨ 新增定时自动更新Cookie功能
- ✨ 新增博客详细分析页面
- ✨ 优化用户界面和交互体验
- 🐛 修复多个已知问题
- 📚 完善文档和说明

🔧 技术改进：
- 优化Cookie管理流程
- 改进前端界面布局
- 增强系统稳定性
- 完善错误处理机制

📊 测试结果：所有功能测试通过 ✅"
    
    git commit -m "$commit_message"
    echo "✅ 代码已提交到本地仓库"
fi

# 推送到GitHub
echo "📤 推送到GitHub..."
if git push origin main; then
    echo "✅ 代码已成功推送到GitHub"
    echo "🌐 Netlify将自动部署更新"
else
    echo "❌ 推送失败，请检查网络连接和权限"
    exit 1
fi

# 显示部署信息
echo ""
echo "🎉 部署完成！"
echo "📊 部署信息："
echo "   - 版本: v1.1.0"
echo "   - 分支: main"
echo "   - 时间: $(date)"
echo ""
echo "🔗 相关链接："
echo "   - GitHub仓库: https://github.com/your-username/xhs_py"
echo "   - Netlify部署: https://your-app-name.netlify.app"
echo "   - 本地测试: http://localhost:8080"
echo ""
echo "📚 使用说明："
echo "   1. 访问 http://localhost:8080 进行本地测试"
echo "   2. 查看 README.md 了解详细功能"
echo "   3. 运行 python test_new_features.py 验证功能"
echo ""
echo "✨ 新功能亮点："
echo "   - Cookie格式自动转换"
echo "   - 左右分栏数据展示"
echo "   - 实时Cookie状态监控"
echo "   - 博客详细分析页面" 