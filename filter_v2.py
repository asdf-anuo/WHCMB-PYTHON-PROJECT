# -*- coding: utf-8 -*-
"""武汉城市留言板数据筛选 v2 —— 老旧小区改造主题（精准优化版）
核心原则：必须明确出现"老旧/旧改/改造"类信号，或具体改造动作词，
不再仅凭"物业费/业委会/违建/充电桩"等所有小区都有的日常治理词召回。
"""
import openpyxl, os, sys

DST_DIR = r'D:\leich\MPA-Study\论文写作汇总\数据-筛选后'
SRC_DIR = r'D:\leich\MPA-Study\论文写作汇总\数据-原始全量'

YEAR_FILES = {
    2017: ['wuhan_comments_2017全年.xlsx'],
    2018: ['wuhan_comments_2018全年.xlsx'],
    2019: ['wuhan_comments_2019全年.xlsx'],
    2020: ['wuhan_comments_2020全年.xlsx'],
    2021: ['wuhan_comments_2021全年.xlsx'],
    2022: ['wuhan_comments_2022全年.xlsx'],
    2023: ['wuhan_comments_2023上半年.xlsx', 'wuhan_comments_2023下半年.xlsx'],
    2024: ['wuhan_comments_2024上半年.xlsx', 'wuhan_comments_2024下半年.xlsx'],
    2025: ['wuhan_comments_2025上半年.xlsx', 'wuhan_comments_2025下半年.xlsx'],
    2026: ['wuhan_comments_2026上半年.xlsx'],
}

OUT_HEADER = ['content', 'subject', 'dateline_str', 'crawl_time']

# ============================================================
# 第一层：改造语境锚定词（必须命中其一，锁定"老旧小区改造"议题）
# ============================================================
# 1A. 明确"老旧/旧"目的小区词
old_target = [
    '老旧小区', '老小区', '旧小区', '老旧社区', '旧社区', '老旧住宅', '旧住宅区',
    '老旧楼院', '老居民楼', '老房子', '老宿舍', '老旧楼栋', '老旧房屋',
    '年久失修', '建成年代久', '房龄老', '老旧街区',
]
# 1B. 政策/改造术语词（直接锁定改造议题）
policy_term = [
    '旧改', '旧区改造', '旧城改造', '小区改造', '社区改造', '老旧小区改造',
    '城镇老旧小区', '老旧小区更新', '微改造', '微更新', '综合改造', '综合整治',
    '应改尽改', '纳入改造', '列入改造', '申报改造', '改造范围', '改造项目',
    '改造工程', '改造施工', '改造方案', '改造提升', '改造内容', '改造计划',
    '五改四好', '存量提质',
]

# ============================================================
# 第二层：改造动作词（明确改造行为，与场所词组合）
# 注意："整治/提升/完善/升级/更新"等词太宽泛，不作为独立改造动作词，
# 仅在路径1（含老旧/旧信号）下作为辅助信号。
# ============================================================
renovation_action = [
    '改造', '翻新', '翻修', '整修', '修缮', '改建', '微改造', '微更新',
    '加装', '增设', '增建', '重建', '更换', '替换', '铺设', '改造升级',
    '纳入改造', '列入改造', '申报改造', '启动改造', '推进改造',
]

# 路径3专用：更严格的改造动作词（排除单独"改造"，避免召回日常物业改造行为）
strict_renovation = [
    '翻新', '翻修', '整修', '修缮', '微改造', '微更新',
    '加装电梯', '装电梯', '电梯加装', '电梯安装',
    '纳入改造', '列入改造', '申报改造', '启动改造', '推进改造',
    '改造升级', '雨污分流', '管网改造', '管道改造',
    '外墙翻新', '防水处理', '屋面改造', '路面硬化',
]

# ============================================================
# 第三层：场所词（居住区语境）
# ============================================================
place = [
    '小区', '社区', '居民区', '住宅区', '楼院', '院落', '家属院', '宿舍区',
    '居民楼', '住宅楼', '楼栋', '楼栋',
]

# ============================================================
# 第四层：改造内容词（具体改造对象，需配合改造动作词或老旧信号）
# ============================================================
# 基础类改造内容（水电气路等）
content_basic = [
    '水改', '电改', '气改', '雨污分流', '化粪池', '管网改造', '管道改造',
    '外墙', '墙皮', '瓷砖', '防水', '保温', '隔热', '屋面', '屋顶', '房顶',
    '飞线', '危房', '漏水', '渗水', '渗漏', '管道老化', '下水道', '排水管',
    '路面', '道路', '地坪', '硬化', '坑洼', '破损',
]
# 完善类改造内容（电梯停车等）
content_improve = [
    '加装电梯', '装电梯', '电梯加装', '电梯安装', '适老化', '无障碍', '扶手', '坡道',
    '充电桩', '充电设施', '消防通道', '消防设施', '楼道灯', '感应灯', '声控灯',
    '门禁', '道闸', '围栏', '围墙', '封闭管理', '监控', '摄像头', '安防',
    '停车位', '车位', '停车', '停车难',
]
# 提升类改造内容（服务品质等）
content_enhance = [
    '物业', '物业费', '物业公司', '业委会', '业主委员会', '业主大会',
    '绿化', '景观', '绿地', '花园', '毁绿', '黄土裸露',
    '活动中心', '活动室', '公共空间', '健身器材', '健身设施',
    '垃圾分类', '垃圾房', '智慧', '智能化', '人脸识别',
    '维修资金', '维修基金', '大修基金', '长效', '管护', '维护',
]

# ============================================================
# 第五层：排除词（命中即剔除）
# ============================================================
exclude = [
    # 非老旧小区改造政策范畴
    '棚改', '棚户区', '城中村', '村改居', '农村危房', '农房', '农村改造',
    '新建小区', '商品房', '新楼盘', '新小区', '新房', '交房', '交付',
    '写字楼', '商铺', '商场', '办公楼', '厂房',
    '市政道路', '主干道', '城市道路', '公路', '高架', '地铁施工', '轨道交通',
    '拆除重建', '整体拆除', '推倒重建', '还建', '拆迁', '征收',
    # 非改造类常见误召
    '变电站', '高压线', '基站', '辐射',
    '营业执照', '经营场所', '住改商', '改变用途',
    '被盗', '盗窃', '抢劫',
    '快递', '外卖', '快递员',
    '养狗', '养鸡', '宠物', '犬',
    '广场舞', '跳舞',
    '装修', '家装', '自家装修', '室内装修',
    '群租', '群租房',
    '占道经营', '摆摊', '占道摆摊',
    '渣土车', '水泥车', '泥头车',
    '油烟', '油污', '餐饮', '餐馆', '饭店',
    '麻将', '棋牌',
    # 纯物业费/车位费纠纷（非改造）
    '物业费涨价', '物业费上涨', '物业费打折', '物业费质价不符', '车位管理费',
    '车位售价', '车位权属', '车位销售', '停车费',
    # 纯商业/消费纠纷
    '虚假宣传', '诱导消费', '拒不退款', '退款',
    # 纯市政/公共空间（非小区改造）
    '公园', '公交站', '公交车站', '候车座椅', '人行道', '盲道',
    '洒水车', '方言', '闯红灯', '学位', '学校', '幼儿园',
    '桥下空间', '桥下',
]


def hit_any(text, words):
    for w in words:
        if w in text:
            return True
    return False


def is_relevant(text):
    """判断一条留言是否与老旧小区改造相关"""
    # 先排除
    if hit_any(text, exclude):
        return False

    # 路径1：明确命中"老旧/旧"目的小区词 + (改造动作 OR 改造内容 OR 任何设施问题)
    if hit_any(text, old_target):
        if hit_any(text, renovation_action) or hit_any(text, content_basic) or \
           hit_any(text, content_improve) or hit_any(text, content_enhance):
            return True

    # 路径2：命中政策/改造术语词（直接锁定改造议题，需在小区语境）
    if hit_any(text, policy_term) and hit_any(text, place):
        return True

    # 路径3：场所词 + 明确老旧小区改造动作词 + 改造内容词（三者同时命中）
    # 仅用明确改造动作词，避免"改造"单独召回日常物业行为
    if hit_any(text, place) and hit_any(text, strict_renovation) and \
       (hit_any(text, content_basic) or hit_any(text, content_improve) or hit_any(text, content_enhance)):
        return True

    return False


def main():
    if len(sys.argv) < 2:
        print('用法: python filter_v2.py <年份> [年份2 ...]')
        sys.exit(1)
    years = [int(y) for y in sys.argv[1:]]
    for year in years:
        files = YEAR_FILES.get(year)
        if not files:
            print(f'[{year}] 未配置源文件，跳过')
            continue
        dst = os.path.join(DST_DIR, f'{year}.xlsx')
        print(f'\n========== 处理 {year} 年 ==========')
        process_one(year, files, dst)


def process_one(year, files, DST):
    kept = []
    stats = {'total': 0, 'final': 0}

    for fname in files:
        src = os.path.join(SRC_DIR, fname)
        print(f'  读取: {fname}')
        wb = openpyxl.load_workbook(src, read_only=True)
        ws = wb.active
        rows_iter = ws.iter_rows(min_row=1, values_only=True)
        header = next(rows_iter)
        h = [str(c) for c in header]
        try:
            ci = h.index('content')
            si = h.index('subject')
            di = h.index('dateline_str')
            ti = h.index('crawl_time')
        except ValueError as e:
            print(f'    表头异常: {header}, 跳过该文件')
            wb.close()
            continue
        if h != ['content', 'subject', 'dateline_str', 'crawl_time']:
            print(f'    列顺序自适应: content={ci}, subject={si}, dateline_str={di}, crawl_time={ti}')

        for row in rows_iter:
            stats['total'] += 1
            content = str(row[ci]) if row[ci] is not None else ''
            subject = str(row[si]) if row[si] is not None else ''
            text = subject + ' ' + content

            if is_relevant(text):
                stats['final'] += 1
                kept.append((content, subject,
                             str(row[di]) if row[di] is not None else '',
                             str(row[ti]) if row[ti] is not None else ''))
        wb.close()

    os.makedirs(DST_DIR, exist_ok=True)
    wb2 = openpyxl.Workbook()
    ws2 = wb2.active
    ws2.title = 'Sheet1'
    ws2.append(OUT_HEADER)
    for r in kept:
        ws2.append(list(r))
    try:
        wb2.save(DST)
        out_path = DST
    except PermissionError:
        out_path = DST.replace('.xlsx', '_v2.xlsx')
        wb2.save(out_path)
        print(f'[{year}] 注意: {DST} 被占用，已保存到 {out_path}')

    print(f'[{year}] 总留言数        : {stats["total"]}')
    print(f'[{year}] 最终有效留言    : {stats["final"]}')
    print(f'[{year}] 有效占比        : {stats["final"]/stats["total"]*100:.2f}%')
    print(f'[{year}] 输出文件        : {out_path}')
    print(f'OUTPUT={os.path.abspath(out_path)}')


if __name__ == '__main__':
    main()
