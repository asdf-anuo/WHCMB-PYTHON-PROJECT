# -*- coding: utf-8 -*-
"""
配置文件 - 武汉城市留言板爬虫
修改此文件中的配置即可适配不同的爬虫项目
"""

# ========== 基础配置 ==========
# API接口地址
BASE_URL = "https://api1-liuyan.cjn.cn/messageboard/api/essearch/querySearchMapByPage"

# 文件保存配置
BASE_FILE_NAME = "wuhan_comments_"  # 文件名前缀
FILE_EXTENSION = "xlsx"             # 文件扩展名

# ========== 爬取模式配置 ==========
# 是否爬取全量数据（True=不加关键词，爬取所有数据；False=使用关键词列表）
CRAWL_ALL_DATA = True

# 全量爬取时的关键词占位符（接口要求keywords不能为空，传空字符串即可获取所有数据）
ALL_DATA_KEYWORD = ""

# 关键词列表文件（当 CRAWL_ALL_DATA = False 时生效）
KEYWORDS_FILE = "keywords.txt"


# 日期范围
#  2017年 共 60731 条
#  2017-04-28 1493308800
#  2017-12-31 1514735999

#  2018年 共 134078 条
#  2018-01-01 1514736000
#  2018-12-31 1546271999

#  2019年 共 156220 条
#  2019-01-01 1546272000
#  2019-12-31 1577807999

#  2020年 共 147037 条
#  2020-01-01 1577808000
#  2020-12-31 1609430399
 
#  2021年 共 193158 条
#  2021-01-01 1609430400
#  2021-12-31 1640966399

#  2022年 共 226622 条
#  2022-01-01 1640966400
#  2022-12-31 1672502399

#  2023年 共 253879 条
#  2023-01-01 1672502400
#  2023-12-31 1704038399

#  2024年 共 176443 条
#  2024-01-01 1704038400
#  2024-12-31 1735660799

#  2025年 共 67931 条
#  2025-01-01 1735660800
#  2025-12-31 1767196799

#  2026年 共 17800 条
#  2026-01-01 1767196800
#  2026-03-31 1774972799

# ========== 爬取参数 ==========
# 开始时间和结束时间（Unix时间戳，单位秒）
START_DATE = "1735660800"
END_DATE = "1767196799"
# 每页数据量（建议10-100）
PAGE_SIZE = 100
# 最大翻页数（根据数据量调整）
MAX_PAGES = 1000

# ========== 请求延迟配置 ==========
# 请求间隔时间（秒），随机范围 [MIN_DELAY, MAX_DELAY]
MIN_DELAY = 2
MAX_DELAY = 5

# 关键词之间的等待时间（秒）
KEYWORD_DELAY = 3

# ========== Cookie配置 ==========
# 直接在这里配置Cookie，或从文件读取
# 如果留空，则从 COOKIE_FILE 读取
COOKIE_STRING = "Hm_lvt_703a2e4b7c1acee6e7f0cf6d71017dee=1772936205; JSESSIONID=2a702f87-12ec-49c5-ae95-30dee8f544b7; rememberMe=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"

# Cookie文件路径（如果 COOKIE_STRING 为空，则从此文件读取）
COOKIE_FILE = "cookie.txt"

# ========== HTTP请求头配置 ==========
HEADERS = {
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,af;q=0.6",
    "cache-control": "no-cache",
    "connection": "keep-alive",
    "content-type": "application/x-www-form-urlencoded",
    "host": "api1-liuyan.cjn.cn",
    "origin": "https://liuyan.cjn.cn",
    "referer": "https://liuyan.cjn.cn/",
    "sec-ch-ua": '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Windows",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36"
}

# ========== 需要保留的字段列表 ==========
# 只保留这些字段，其他字段将被过滤掉
KEEP_FIELDS = [
    "anonymousState",
    "ansCheckState",
    "attachment",
    "availableTime",
    "checkNum",
    "commentsNum",
    "content",
    "dateline",
    "dateline_str",  # 转换后的时间字符串
    "domainId",
    "favNum",
    "fdFailCount",
    "fidsNum",
    "handleState",
    "handleTogetherHandleTime",
    "handletogetherLastAnswerTime",
    "hasSecAnswer",
    "isOpenComment",
    "isReply",
    "isReplyStr",
    "isShowComment",
    "lastupdate",
    "leaderAnswer",
    "lybh",
    "markState",
    "nickName",
    "overt",
    "params",
    "processState",
    "queryCode",
    "queryCodeList",
    "recommend",
    "reportState",
    "satisfaction",
    "score",
    "sfnm",
    "sfnmStr",
    "smrxDataId",
    "smrxGetReplyed",
    "source",
    "subject",
    "threadState",
    "tid",
    "timelyAnswered",
    "togetherNum",
    "traceState",
    "typeId",
    "userId",
    "viewsNum",
    "keyword",      # 添加搜索关键词
    "crawl_time"    # 添加爬取时间
]

# ========== 调试配置 ==========
# 是否打印详细日志
VERBOSE = True