#!/bin/bash
# FTP文件服务器启动脚本 - 使用nohup在后台运行

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

# 检查日志目录
if [ ! -d "logs" ]; then
    echo "📂 创建日志目录..."
    mkdir -p logs
fi

# 检查是否已经运行
PID=$(pgrep -f "python3.*ftp_server.py" || echo "")
if [ ! -z "$PID" ]; then
    echo "⚠️ FTP服务器已经在运行中 (PID: $PID)"
    echo "如需重启，请先运行: kill $PID"
    exit 1
fi

# 启动服务器（使用nohup在后台运行）
echo "🚀 启动FTP服务器在后台运行..."
echo "正在共享你的Downloads文件夹..."
echo "日志将保存在 logs/ftp_server.log"
echo ""

# 使用nohup在后台运行，即使终端关闭也能继续运行
nohup python3 ftp_server.py > logs/ftp_server.log 2>&1 &

# 获取进程ID
NEW_PID=$!
echo "✅ FTP服务器已在后台启动 (PID: $NEW_PID)"
echo "查看日志: tail -f logs/ftp_server.log"
echo "停止服务: kill $NEW_PID" 