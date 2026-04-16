# 武汉城市留言板爬虫

## 项目简介
本项目用于爬取武汉城市留言板（https://liuyan.cjn.cn/）的留言数据，支持关键词搜索、日期范围筛选、字段筛选等功能。

## 功能特性
- 支持多关键词爬取 (也可以全量爬取)
- 支持日期范围筛选（时间戳格式）
- 自动清理文本中的多余空格
- 时间戳自动转换为可读格式
- 随机延迟，模拟人类操作
- 自动保存进度，防止数据丢失
- 可配置的字段筛选，只保留需要的字段

## 环境要求
- Python 3.6 或更高版本
- Windows / macOS / Linux

## 安装步骤

### 1. 安装 Python 确保已安装 Python 3.6+，检查版本：
python3 --version

### 2. 在项目目录下运行以下命令安装依赖：
python3 -m pip install --upgrade pip
python3 -m pip install pandas requests openpyxl

# 如果下载速度慢，可使用国内镜像源：
python3 -m pip install pandas requests openpyxl -i https://pypi.tuna.tsinghua.edu.cn/simple/

### 3. 获取 Cookie
打开浏览器，访问 https://liuyan.cjn.cn/
按 F12 打开开发者工具
刷新页面，在 Network 标签中找到任意请求
在 Request Headers 中找到 Cookie 字段，复制其值
打开 config.py 文件，找到 COOKIE_STRING 配置项，粘贴 Cookie 值

### 4. 配置关键词
编辑 keywords.txt 文件，每行一个关键词

### 5. 修改配置文件（可选）
如需调整爬取参数，编辑 config.py：
START_DATE / END_DATE：日期范围
PAGE_SIZE：每页数据量
MAX_PAGES：最大翻页数
MIN_DELAY / MAX_DELAY：请求间隔时间（秒）
KEEP_FIELDS：需要保留的字段列表

### 6.运行项目 
在项目目录下执行：
python3 start.py

### 7.输出结果
运行成功后，会在当前目录生成 Excel 文件，文件名格式：wuhan_comments_YYYYMMDDHHMMSS.xlsx

### 常见问题
Q1: ModuleNotFoundError: No module named 'pandas'
A: 未安装依赖包，请执行安装命令：
python3 -m pip install pandas requests openpyxl

Q2: Cookie 失效
A: Cookie 有效期有限，需要重新登录网页获取新的 Cookie，更新 config.py 中的 COOKIE_STRING。

Q3: 请求返回错误
A: 可能是请求频率过高，可以适当增加 MIN_DELAY 和 MAX_DELAY 的值。

Q4: 数据量太大怎么办
A: 可以调整 MAX_PAGES 减少翻页数量，或调整 KEYWORDS 减少关键词。


### 文件说明
mpa-python-project/
├── config.py          # 配置文件（Cookie、参数等）
├── eur.py             # 主爬虫程序
├── start.py           # 启动文件
├── keywords.txt       # 关键词列表
├── cookie.txt         # Cookie 文件（可选，可配置在 config.py 中）
└── readme.md          # 说明文档


### 注意事项

    请合理设置请求间隔，避免对目标网站造成压力

    Cookie 包含个人登录信息，请勿分享给他人

    爬取的数据仅限个人研究使用，请遵守相关法律法规