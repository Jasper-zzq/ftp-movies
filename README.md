# 📁 本地局域网 FTP 文件服务器

一个专为电视机设计的简单 FTP 服务器，用于在局域网内访问你的 Downloads 文件夹中的所有文件。

## 🚀 快速开始

### 1. 安装依赖

```bash
# 创建虚拟环境（推荐）
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 运行服务器

```bash
python ftp_server.py
```

### 3. 电视机连接

1. 打开电视机的文件管理器或媒体播放器
2. 选择网络/FTP 连接
3. 输入服务器地址（程序启动时会显示）
4. 端口：2121
5. 匿名登录或使用 admin/admin123

## 📁 文件夹结构

```
ftp-movie-server/
├── ftp_server.py      # 主服务器文件
├── config.py          # 配置文件
├── start.py          # 交互式启动脚本
├── run.sh            # 一键启动脚本
├── requirements.txt   # 依赖包
├── movies/           # 备用文件夹
└── README.md         # 说明文档
```

## 📂 支持的文件夹

默认情况下，服务器会自动共享你的 `~/Downloads` 文件夹中的所有文件：

- **优先级 1**: `~/Downloads` (用户下载文件夹)
- **优先级 2**: `./movies` (项目内的 movies 文件夹)
- **优先级 3**: `./files` (自动创建的 files 文件夹)

## ⚙️ 配置选项

编辑 `config.py` 文件来自定义设置：

- `FTP_PORT`: FTP 端口（默认 2121，避免权限问题）
- `DOWNLOADS_PATH`: Downloads 文件夹路径
- `ALLOW_ANONYMOUS`: 是否允许匿名访问
- `ADMIN_USERNAME/PASSWORD`: 管理员账户
- `ALLOW_ALL_FILES`: 允许访问所有文件类型

## 🎯 功能特性

- ✅ **自动共享 Downloads 文件夹** - 无需手动复制文件
- ✅ **支持所有文件类型** - 视频、图片、文档、音频等
- ✅ **智能文件统计** - 按类型显示文件数量
- ✅ **匿名访问** - 电视机可直接连接
- ✅ **管理员权限** - 支持上传和删除文件
- ✅ **被动模式传输** - 适合电视机连接
- ✅ **多设备同时连接**
- ✅ **实时连接状态显示**

## 📺 支持的设备

- 智能电视（支持 FTP 的型号）
- 电视盒子
- 手机/平板（FTP 客户端）
- 电脑（文件管理器）
- 媒体播放器

## 📋 支持的文件类型

### 🎬 视频文件

MP4, MKV, AVI, MOV, WMV, FLV, M4V, 3GP, WEBM, MPG, MPEG, RMVB

### 🖼️ 图片文件

JPG, JPEG, PNG, GIF, BMP, TIFF, WEBP, SVG

### 📄 文档文件

PDF, DOC, DOCX, TXT, RTF, ODT, XLS, XLSX, PPT, PPTX

### 🎵 音频文件

MP3, WAV, FLAC, AAC, OGG, WMA, M4A

### 📦 压缩文件

ZIP, RAR, 7Z, TAR, GZ, BZ2, XZ

### 📋 其他文件

支持任何文件类型！

## 🔧 故障排除

### 权限问题

默认使用端口 2121，避免权限问题。

### 连接问题

- 确保防火墙允许 FTP 端口
- 确保电视机和电脑在同一局域网
- 检查 IP 地址是否正确

### 文件访问问题

- 确保 Downloads 文件夹存在
- 检查文件权限
- 尝试管理员账户登录

## 📝 使用提示

1. **文件访问**: 服务器自动共享 Downloads 文件夹
2. **网络**: 确保所有设备连接同一 WiFi
3. **格式**: 支持所有文件类型，无限制
4. **下载**: 直接下载文件到 Downloads 即可通过 FTP 访问

## 🛡️ 安全说明

此 FTP 服务器仅适用于家庭局域网环境，请勿暴露到公网。
# ftp-movies
