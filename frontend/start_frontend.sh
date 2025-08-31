#!/bin/bash

# LearnPilot 前端启动脚本

echo "🚀 启动 LearnPilot 前端开发服务器..."
echo "=================================="

# 检查 Node.js
if ! command -v node &> /dev/null; then
    echo "❌ 错误: 未找到 Node.js，请先安装 Node.js"
    echo "   下载地址: https://nodejs.org/"
    exit 1
fi

# 显示 Node.js 版本
node_version=$(node -v)
echo "📦 Node.js 版本: $node_version"

# 检查 npm
if ! command -v npm &> /dev/null; then
    echo "❌ 错误: 未找到 npm"
    exit 1
fi

# 检查是否在正确的目录
if [ ! -f "package.json" ]; then
    echo "❌ 错误: 请在 frontend 目录中运行此脚本"
    exit 1
fi

# 检查环境变量文件
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        echo "📝 创建环境配置文件..."
        cp .env.example .env
        echo "✅ 已复制 .env.example 到 .env"
        echo "💡 如需修改配置，请编辑 .env 文件"
    else
        echo "⚠️  警告: 未找到环境配置文件"
    fi
fi

# 检查依赖
if [ ! -d "node_modules" ]; then
    echo "📦 安装依赖包..."
    npm install
    
    if [ $? -ne 0 ]; then
        echo "❌ 依赖安装失败，请检查网络连接"
        exit 1
    fi
    echo "✅ 依赖安装完成"
else
    echo "✅ 依赖已安装"
fi

# 显示项目信息
echo ""
echo "🎯 项目信息:"
echo "   名称: LearnPilot Frontend"
echo "   端口: http://localhost:3000"
echo "   API:  http://localhost:8000/api"
echo ""

# 启动开发服务器
echo "🌟 启动开发服务器..."
echo "   按 Ctrl+C 停止服务器"
echo "=================================="
echo ""

npm run dev