# -*- coding: utf-8 -*-
"""武汉城市留言板数据筛选 —— 老旧小区改造主题（通用版，支持多源合并+列顺序自适应）"""
import openpyxl, os, sys

DST_DIR = r'D:\leich\MPA-Study\论文写作汇总\数据-筛选后'
SRC_DIR = r'D:\leich\MPA-Study\论文写作汇总\数据-原始全量'

# 各年对应的源文件列表（支持上下半年合并）
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

# 统一输出列顺序
OUT_HEADER = ['content', 'subject', 'dateline_str', 'crawl_time']

# ===== 组合A：核心锚定词（含"老旧/旧"或政策术语，高精度）=====
anchor_A = [
    '老旧小区', '老小区', '旧小区', '老旧社区', '旧社区', '老旧住宅', '旧住宅区',
    '老旧楼院', '老居民楼', '老房子', '老宿舍', '旧改', '旧区改造', '旧城改造',
    '小区改造', '社区改造', '老旧小区改造', '城镇老旧小区', '老旧小区更新',
    '微改造', '微更新', '综合改造', '综合整治',
]

# ===== 明确含"老/旧"目的小区词（组合C主路径）=====
anchor_old = [
    '老旧小区', '老小区', '旧小区', '老旧社区', '旧社区', '老旧住宅', '旧住宅区',
    '老旧楼院', '老居民楼', '老房子', '老宿舍', '老旧', '年久失修',
]

# ===== 改造动作词（明确改造行为）=====
action = [
    '改造', '翻新', '修缮', '整治', '更新', '翻修', '整修', '改建', '提升', '完善', '升级',
    '纳入改造', '列入计划', '申报改造', '应改尽改',
]

# ===== 施工类词（需配合"老旧/旧"词使用，不单独召回）=====
action_construct = [
    '施工', '开工', '进场', '动工', '拆除', '拆违',
]

# ===== 组合B：场所泛称词（扩展召回）=====
place_B = [
    '小区', '社区', '居民区', '住宅区', '楼院', '院落', '家属院', '宿舍区',
    '居民楼', '住宅楼', '楼栋',
]

# ===== 组合B-强：强改造内容词（单独即可召回，物理设施/改造直接相关）=====
content_B_strong = [
    # 基础类-强
    '水改', '电改', '气改', '雨污分流', '化粪池', '管道老化', '管道破裂',
    '外墙', '墙皮', '瓷砖', '空鼓', '屋顶', '屋面', '防水', '保温', '隔热',
    '飞线', '危房', '老旧', '年久失修', '老化', '破损严重',
    # 完善类-强
    '加装电梯', '装电梯', '电梯加装', '适老化', '无障碍', '扶手',
    '充电桩', '消防通道', '楼道灯', '感应灯', '声控灯',
    '门禁', '道闸', '围栏', '围墙', '封闭管理', '监控', '摄像头',
    # 提升类-强
    '物业费', '物业公司', '业委会', '业主委员会', '业主大会',
    '毁绿', '黄土裸露', '健身器材', '垃圾分类', '垃圾房',
    '智慧', '智能化', '人脸识别', '智能门禁',
    '维修资金', '维修基金', '大修基金', '长效', '后续管理', '改后管理', '管理机制',
    # 过程-强
    '违建', '违章建筑', '私搭乱建', '拆违', '占绿', '圈地',
    '偷工减料', '返工', '围挡', '坠物',
    '微改造', '微更新', '综合整治', '应改尽改', '纳入改造', '旧改',
]

# ===== 组合B-弱：弱改造内容词（需额外改造信号词才召回）=====
content_B_weak = [
    '供水', '自来水', '水管', '水压', '停水', '二次供水', '水箱',
    '供电', '电线', '电网', '电表', '停电', '线路',
    '供气', '天然气', '燃气', '煤气', '通气', '装气',
    '道路', '路面', '坑洼', '塌陷', '硬化',
    '排水', '下水道', '下水管', '管网', '排水管', '积水', '排污',
    '漏水', '渗水', '渗漏', '脱落', '裂缝', '房顶', '顶楼', '地基', '沉降',
    '电梯', '电梯费', '电梯故障',
    '停车', '停车位', '车位', '停车难', '乱停', '占道停车',
    '充电', '电动车充电',
    '消防', '消防栓', '灭火器',
    '照明', '路灯', '亮化', '灯不亮',
    '安防',
    '信报箱', '快递柜',
    '物业', '绿化', '花园', '景观', '绿地', '花草', '树木',
    '活动中心', '活动室', '社区用房', '公共空间', '休闲广场', '健身广场',
    '健身', '图书室', '老年活动室',
    '垃圾', '垃圾桶', '垃圾清运', '保洁', '清扫',
    '社区服务', '便民服务', '养老', '托育', '助餐', '食堂', '日间照料',
    '扰民', '噪音', '噪声', '粉尘', '灰尘',
    '出资', '分摊', '财政补助',
    '进度', '工期', '延期', '拖延', '停工', '烂尾', '竣工',
    '方案', '公示', '征求意见', '听证',
    '维护', '管护', '保养', '规约',
    '参与', '表决', '投票', '签字', '协商', '座谈',
]

# ===== 弱词的额外改造信号（弱词命中时，文本还需含以下任一词才召回）====
renovation_signal = [
    '改造', '翻新', '修缮', '整治', '更新', '提升', '完善', '升级',
    '施工', '开工', '进场', '动工', '拆除',
    '老旧', '旧', '老小区', '年久', '老化', '破损', '失修',
    '纳入', '申报', '列入', '计划', '方案', '规划',
    '维修', '翻修', '整修', '改建', '加装',
]

# ===== 排除词（命中即剔除，非老旧小区改造语境）=====
exclude = [
    '棚改', '棚户区', '城中村', '村改居', '农村危房', '农房', '农村改造',
    '新建小区', '商品房', '新楼盘', '新小区', '新房', '交房',
    '写字楼', '商铺', '商场', '办公楼', '厂房',
    '市政道路', '主干道', '城市道路', '公路', '高架', '地铁施工',
    '拆除重建', '整体拆除', '推倒重建', '还建', '拆迁', '征收',
    # 非改造类常见误召
    '变电站', '高压线', '基站', '辐射',
    '营业执照', '经营场所', '住改商', '改变用途',
    '被盗', '盗窃', '偷', '抢劫',
    '物业费涨价', '物业费上涨',
    '快递', '外卖', '快递员',
    '养狗', '养鸡', '宠物', '犬',
    '广场舞', '跳舞',
    '装修', '家装', '自家装修', '室内装修',
    '群租', '群租房',
    '占道经营', '摆摊', '占道摆摊',
    '渣土车', '水泥车', '泥头车',
    '油烟', '油污', '餐饮', '餐馆', '饭店',
    '麻将', '棋牌',
    '跳广场舞', '广场舞噪音',
]


def hit_any(text, words):
    for w in words:
        if w in text:
            return True
    return False


def main():
    if len(sys.argv) < 2:
        print('用法: python filter_year.py <年份> [年份2 ...]')
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
    stats = {'total': 0, 'A': 0, 'B': 0, 'A_or_B': 0, 'excluded': 0, 'final': 0}

    for fname in files:
        src = os.path.join(SRC_DIR, fname)
        print(f'  读取: {fname}')
        wb = openpyxl.load_workbook(src, read_only=True)
        ws = wb.active
        rows_iter = ws.iter_rows(min_row=1, values_only=True)
        header = next(rows_iter)
        # 根据表头自适应列顺序
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

            hitA = hit_any(text, anchor_A) and hit_any(text, action)
            hitB = hit_any(text, place_B) and hit_any(text, content_B_strong)
            hitC = hit_any(text, anchor_old) and (
                hit_any(text, content_B_strong) or hit_any(text, content_B_weak) or hit_any(text, action_construct)
            )
            hitB = hitB or hitC

            if hitA:
                stats['A'] += 1
            if hitB:
                stats['B'] += 1

            if hitA or hitB:
                stats['A_or_B'] += 1
                if hit_any(text, exclude):
                    stats['excluded'] += 1
                else:
                    stats['final'] += 1
                    # 统一列顺序输出
                    kept.append((content, subject, str(row[di]) if row[di] is not None else '', str(row[ti]) if row[ti] is not None else ''))
        wb.close()

    os.makedirs(DST_DIR, exist_ok=True)
    wb2 = openpyxl.Workbook()
    ws2 = wb2.active
    ws2.title = 'Sheet1'
    ws2.append(OUT_HEADER)
    for r in kept:
        ws2.append(list(r))
    wb2.save(DST)

    print(f'[{year}] 总留言数        : {stats["total"]}')
    print(f'[{year}] 组合A命中       : {stats["A"]}')
    print(f'[{year}] 组合B命中       : {stats["B"]}')
    print(f'[{year}] 合并去重(A∪B)   : {stats["A_or_B"]}')
    print(f'[{year}] 命中排除词剔除  : {stats["excluded"]}')
    print(f'[{year}] 最终有效留言    : {stats["final"]}')
    print(f'[{year}] 有效占比        : {stats["final"]/stats["total"]*100:.2f}%')
    print(f'[{year}] 输出文件        : {DST}')
    print(f'OUTPUT={os.path.abspath(DST)}')


if __name__ == '__main__':
    main()
