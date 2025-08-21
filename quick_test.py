#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FTP连接测试脚本
"""

import socket
import subprocess
from ftplib import FTP


def test_ftp_connection():
    """测试FTP连接"""
    print("🔍 FTP连接测试")
    print("=" * 40)

    # 测试端口连通性
    print("1. 测试端口连通性...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex(("192.168.10.10", 2121))
        sock.close()
        if result == 0:
            print("   ✅ 端口2121可以连接")
        else:
            print("   ❌ 端口2121无法连接")
            return False
    except Exception as e:
        print(f"   ❌ 连接测试失败: {e}")
        return False

    # 测试FTP协议
    print("2. 测试FTP协议...")
    try:
        ftp = FTP()
        ftp.connect("192.168.10.10", 2121, timeout=10)
        print("   ✅ FTP协议连接成功")

        # 测试匿名登录
        print("3. 测试匿名登录...")
        ftp.login()
        print("   ✅ 匿名登录成功")

        # 列出文件
        print("4. 列出文件...")
        files = ftp.nlst()
        print(f"   ✅ 发现 {len(files)} 个文件/文件夹")
        if len(files) > 0:
            print("   前5个项目:")
            for i, file in enumerate(files[:5]):
                print(f"     {i+1}. {file}")

        ftp.quit()
        print("\n🎉 FTP服务器工作正常！")
        print("📺 电视机连接信息:")
        print("   🔗 地址: ftp://192.168.10.10:2121")
        print("   👤 用户名: 留空")
        print("   🔑 密码: 留空")
        return True

    except Exception as e:
        print(f"   ❌ FTP测试失败: {e}")
        return False


def check_network():
    """检查网络状态"""
    print("\n🌐 网络状态检查")
    print("=" * 40)

    try:
        # 检查路由
        result = subprocess.run(
            ["route", "-n", "get", "default"], capture_output=True, text=True
        )
        if "192.168.10.1" in result.stdout:
            print("✅ 默认路由指向WiFi网络")
        else:
            print("⚠️ 默认路由可能不是WiFi网络")
    except:
        pass

    # 检查IP地址
    try:
        result = subprocess.run(["ifconfig"], capture_output=True, text=True)
        if "192.168.10.10" in result.stdout:
            print("✅ WiFi IP地址 192.168.10.10 正常")
        else:
            print("❌ 未找到WiFi IP地址")
    except:
        pass


if __name__ == "__main__":
    print("🔧 FTP服务器连接诊断工具")
    print("=" * 50)

    check_network()

    if test_ftp_connection():
        print("\n💡 建议:")
        print("1. 确保电视机连接同一WiFi (192.168.10.x)")
        print("2. 如果还是无法连接，请检查电视机的FTP客户端设置")
        print("3. 某些电视机可能需要输入完整地址: ftp://192.168.10.10:2121")
    else:
        print("\n❌ FTP服务器连接失败")
        print("请检查:")
        print("1. FTP服务器是否正在运行")
        print("2. 防火墙设置")
        print("3. 网络连接")
