#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
本地局域网FTP文件服务器
支持电视机直连访问Downloads文件夹中的所有文件
"""

import os
import sys
import socket
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

# 导入配置
try:
    from config import *
except ImportError:
    # 如果没有配置文件，使用默认配置
    FTP_PORT = 2121
    DOWNLOADS_PATH = os.path.expanduser("~/Downloads/ftp")
    MOVIES_PATH = "./movies"
    ALLOW_ANONYMOUS = True
    ADMIN_USERNAME = "admin"
    ADMIN_PASSWORD = "admin123"
    MAX_CONNECTIONS = 256
    MAX_CONNECTIONS_PER_IP = 5
    PASSIVE_PORTS_START = 60000
    PASSIVE_PORTS_END = 65535
    ALLOW_ALL_FILES = True


class FileFTPHandler(FTPHandler):
    """自定义FTP处理器，专门优化文件传输"""

    def on_connect(self):
        """客户端连接时的处理"""
        print(f"📺 新的客户端连接: {self.remote_ip}:{self.remote_port}")

    def on_disconnect(self):
        """客户端断开连接时的处理"""
        print(f"🔌 客户端断开连接: {self.remote_ip}:{self.remote_port}")

    def on_login(self, username):
        """用户登录时的处理"""
        print(f"👤 用户登录: {username} 来自 {self.remote_ip}")

    def on_file_sent(self, file):
        """文件发送完成时的处理"""
        print(f"📤 文件发送完成: {file}")

    def on_file_received(self, file):
        """文件接收完成时的处理"""
        print(f"📥 文件接收完成: {file}")


def get_local_ip():
    """获取本机IP地址，优先返回局域网IP"""
    import subprocess

    try:
        # 方法1: 优先获取192.168.x.x网段的IP（标准家庭WiFi网段）
        result = subprocess.run(["ifconfig"], capture_output=True, text=True)
        lines = result.stdout.split("\n")

        wifi_ips = []
        other_ips = []

        for line in lines:
            if (
                "inet " in line
                and "127.0.0.1" not in line
                and "inet 169.254" not in line
            ):
                parts = line.strip().split()
                for part in parts:
                    if (
                        part.startswith("192.168.")
                        or part.startswith("10.")
                        or part.startswith("172.")
                    ):
                        if "192.168." in part:
                            wifi_ips.append(part)
                        else:
                            other_ips.append(part)

        # 优先返回WiFi网段的IP
        if wifi_ips:
            print(f"🌐 检测到WiFi网络IP: {wifi_ips[0]}")
            return wifi_ips[0]
        elif other_ips:
            print(f"🌐 检测到局域网IP: {other_ips[0]}")
            return other_ips[0]
    except Exception as e:
        print(f"⚠️ 无法通过ifconfig获取IP: {e}")

    try:
        # 方法2: 备用方法
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            print(f"🌐 备用方法获取IP: {ip}")
            return ip
    except Exception as e:
        print(f"⚠️ 备用方法也失败: {e}")
        return "127.0.0.1"


def count_files_by_type(directory):
    """统计文件夹中各种类型文件的数量"""
    if not os.path.exists(directory):
        return {}

    file_stats = {
        "total": 0,
        "videos": 0,
        "images": 0,
        "documents": 0,
        "music": 0,
        "archives": 0,
        "others": 0,
    }

    try:
        video_extensions = [
            ".mp4",
            ".mkv",
            ".avi",
            ".mov",
            ".wmv",
            ".flv",
            ".m4v",
            ".3gp",
            ".webm",
            ".mpg",
            ".mpeg",
            ".rmvb",
        ]
        image_extensions = [
            ".jpg",
            ".jpeg",
            ".png",
            ".gif",
            ".bmp",
            ".tiff",
            ".webp",
            ".svg",
        ]
        document_extensions = [
            ".pdf",
            ".doc",
            ".docx",
            ".txt",
            ".rtf",
            ".odt",
            ".xls",
            ".xlsx",
            ".ppt",
            ".pptx",
        ]
        music_extensions = [".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a"]
        archive_extensions = [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz"]

        for root, dirs, files in os.walk(directory):
            for file in files:
                file_lower = file.lower()
                file_stats["total"] += 1

                if any(file_lower.endswith(ext) for ext in video_extensions):
                    file_stats["videos"] += 1
                elif any(file_lower.endswith(ext) for ext in image_extensions):
                    file_stats["images"] += 1
                elif any(file_lower.endswith(ext) for ext in document_extensions):
                    file_stats["documents"] += 1
                elif any(file_lower.endswith(ext) for ext in music_extensions):
                    file_stats["music"] += 1
                elif any(file_lower.endswith(ext) for ext in archive_extensions):
                    file_stats["archives"] += 1
                else:
                    file_stats["others"] += 1
    except Exception:
        pass

    return file_stats


def determine_share_path():
    """确定要共享的文件夹路径"""
    # 优先使用Downloads文件夹
    if hasattr(sys.modules[__name__], "DOWNLOADS_PATH") and os.path.exists(
        DOWNLOADS_PATH
    ):
        return DOWNLOADS_PATH

    # 如果Downloads不存在，使用movies文件夹
    if hasattr(sys.modules[__name__], "MOVIES_PATH"):
        return MOVIES_PATH

    # 默认使用当前目录下的files文件夹
    return "./files"


def setup_ftp_server():
    """设置FTP服务器"""

    # 确定共享路径
    share_path = determine_share_path()

    # 创建共享文件夹（如果不存在）
    if not os.path.exists(share_path):
        os.makedirs(share_path)
        print(f"📁 创建共享文件夹: {os.path.abspath(share_path)}")

    # 统计文件
    file_stats = count_files_by_type(share_path)
    print(f"📊 文件统计 (共享路径: {os.path.abspath(share_path)}):")
    print(f"  📁 总文件数: {file_stats['total']}")
    if file_stats["total"] > 0:
        print(f"  🎬 视频文件: {file_stats['videos']}")
        print(f"  🖼️  图片文件: {file_stats['images']}")
        print(f"  📄 文档文件: {file_stats['documents']}")
        print(f"  🎵 音频文件: {file_stats['music']}")
        print(f"  📦 压缩文件: {file_stats['archives']}")
        print(f"  📋 其他文件: {file_stats['others']}")
    else:
        print("  📂 文件夹为空，请添加文件")

    # 创建授权器
    authorizer = DummyAuthorizer()

    if ALLOW_ANONYMOUS:
        # 允许匿名用户（只读权限）
        authorizer.add_anonymous(share_path, perm="elr")
        print("🔓 已启用匿名访问（只读权限）")

    # 添加管理员用户（读写权限）
    authorizer.add_user(ADMIN_USERNAME, ADMIN_PASSWORD, share_path, perm="elradfmw")
    print(f"👑 管理员账户: {ADMIN_USERNAME}/{ADMIN_PASSWORD} （读写权限）")

    # 创建FTP处理器
    handler = FileFTPHandler
    handler.authorizer = authorizer

    # 设置传输模式为被动模式（适合电视机连接）
    handler.passive_ports = range(PASSIVE_PORTS_START, PASSIVE_PORTS_END)

    # 设置最大连接数
    handler.max_cons = MAX_CONNECTIONS
    handler.max_cons_per_ip = MAX_CONNECTIONS_PER_IP

    # 获取WiFi网络IP地址
    wifi_ip = get_local_ip()

    # 创建FTP服务器，绑定到特定IP地址
    print(f"🌐 绑定FTP服务器到: {wifi_ip}:{FTP_PORT}")
    server = FTPServer((wifi_ip, FTP_PORT), handler)

    return server, share_path, wifi_ip


def main():
    """主函数"""
    print("📁 本地局域网FTP文件服务器启动中...")
    print("=" * 50)

    try:
        # 设置FTP服务器
        server, share_path, local_ip = setup_ftp_server()

        # 获取本机IP
        # local_ip = get_local_ip() # This line is now redundant as local_ip is passed from setup_ftp_server

        print("\n✅ FTP服务器配置完成!")
        print(f"📍 服务器地址: {local_ip}:{FTP_PORT}")
        print(f"📂 共享文件夹: {os.path.abspath(share_path)}")
        print("\n连接信息:")
        print(f"  🔗 FTP地址: ftp://{local_ip}:{FTP_PORT}")
        if ALLOW_ANONYMOUS:
            print(f"  👤 匿名登录: 用户名留空，密码留空")
        print(f"  👑 管理员登录: {ADMIN_USERNAME} / {ADMIN_PASSWORD}")
        print("\n📺 电视机连接步骤:")
        print(f"  1. 打开电视机的文件管理器或媒体播放器")
        print(f"  2. 选择网络/FTP连接")
        print(f"  3. 输入服务器地址: {local_ip}")
        print(f"  4. 端口: {FTP_PORT}")
        if ALLOW_ANONYMOUS:
            print(f"  5. 匿名登录或使用 {ADMIN_USERNAME}/{ADMIN_PASSWORD}")
        else:
            print(f"  5. 使用账户 {ADMIN_USERNAME}/{ADMIN_PASSWORD}")
        print("\n💡 提示:")
        print(f"  • 当前共享: {share_path}")
        print("  • 支持所有文件类型")
        print("  • 按 Ctrl+C 停止服务器")
        print("  • 可编辑 config.py 自定义设置")
        print("=" * 50)
        print(f"🚀 FTP服务器正在运行在 {local_ip}:{FTP_PORT}")

        # 启动服务器
        server.serve_forever()

    except PermissionError:
        print(f"❌ 权限错误: 无法绑定端口 {FTP_PORT}")
        print("请以管理员身份运行或使用其他端口")
        print("提示: 可以编辑 config.py 修改端口")
        sys.exit(1)
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ 端口 {FTP_PORT} 已被占用")
            print("请检查是否有其他FTP服务器运行")
            print("或编辑 config.py 使用其他端口")
        else:
            print(f"❌ 网络错误: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n🛑 服务器已停止")
        sys.exit(0)
    except Exception as e:
        print(f"❌ 未知错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
