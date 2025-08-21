#!/bin/bash
# FTP文件服务器启动脚本

echo "📁 FTP文件服务器启动脚本"
echo "=========================="

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "📥 检查依赖..."
pip install -r requirements.txt > /dev/null 2>&1

# 启动服务器
echo "🚀 启动FTP服务器..."
echo "正在共享你的Downloads文件夹..."
echo "按 Ctrl+C 停止服务器"
echo ""
python3 ftp_server.py 