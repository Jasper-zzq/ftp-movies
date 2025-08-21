#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FTP电影服务器启动脚本
"""

import os
import sys
import subprocess


def check_dependencies():
    """检查依赖是否安装"""
    try:
        import pyftpdlib

        return True
    except ImportError:
        return False


def install_dependencies():
    """安装依赖"""
    print("📦 正在安装依赖包...")
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
        )
        print("✅ 依赖安装完成!")
        return True
    except subprocess.CalledProcessError:
        print("❌ 依赖安装失败")
        return False


def main():
    """主函数"""
    print("📁 欢迎使用FTP文件服务器!")

    # 检查依赖
    if not check_dependencies():
        print("❌ 缺少依赖包")
        if input("是否自动安装依赖? (y/n): ").lower() == "y":
            if not install_dependencies():
                print("请手动运行: pip install -r requirements.txt")
                return
        else:
            print("请手动安装依赖: pip install -r requirements.txt")
            return

    print("\n🚀 启动FTP服务器...")
    try:
        import ftp_server

        ftp_server.main()
    except KeyboardInterrupt:
        print("\n服务器已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")


if __name__ == "__main__":
    main()
