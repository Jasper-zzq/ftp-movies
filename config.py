#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FTP文件服务器配置文件
"""

import os

# 服务器配置
FTP_PORT = 2121  # FTP端口（避免权限问题，使用2121）
DOWNLOADS_PATH = os.path.expanduser("~/Downloads/ftp")  # 用户Downloads/ftp文件夹
MOVIES_PATH = "./movies"  # 备用电影文件夹（如果Downloads不存在）

# 用户配置
ALLOW_ANONYMOUS = True  # 是否允许匿名访问
ADMIN_USERNAME = "a"  # 管理员用户名
ADMIN_PASSWORD = "a"  # 管理员密码

# 网络配置
MAX_CONNECTIONS = 256  # 最大连接数
MAX_CONNECTIONS_PER_IP = 5  # 每个IP最大连接数
PASSIVE_PORTS_START = 60000  # 被动模式端口范围开始
PASSIVE_PORTS_END = 65535  # 被动模式端口范围结束

# 支持的视频格式（用于统计，但不限制文件类型）
SUPPORTED_VIDEO_FORMATS = [
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

# 支持的所有文件类型（不限制）
ALLOW_ALL_FILES = True  # 允许访问所有文件类型
