#!/bin/bash
# FTP文件服务器停止脚本

echo "📁 FTP文件服务器停止脚本"
echo "=========================="

# 查找FTP服务器进程
PID=$(pgrep -f "python3.*ftp_server.py" || echo "")

if [ -z "$PID" ]; then
    echo "❌ 未发现正在运行的FTP服务器"
    exit 0
fi

echo "🔍 发现FTP服务器进程 (PID: $PID)"
echo "🛑 正在停止服务器..."

# 发送终止信号
kill $PID

# 检查进程是否已终止
sleep 2
if ps -p $PID > /dev/null; then
    echo "⚠️ 服务器未能正常终止，尝试强制终止..."
    kill -9 $PID
    sleep 1
fi

# 再次检查
if ps -p $PID > /dev/null; then
    echo "❌ 无法终止服务器进程，请手动终止: sudo kill -9 $PID"
else
    echo "✅ FTP服务器已成功停止"
fi

# 显示日志最后几行
if [ -f "logs/ftp_server.log" ]; then
    echo ""
    echo "📋 服务器最后日志内容:"
    tail -n 10 logs/ftp_server.log
fi 