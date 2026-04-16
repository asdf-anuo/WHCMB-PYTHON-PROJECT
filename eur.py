# -*- coding: utf-8 -*-
import json
import pandas as pd
import requests
import os
from datetime import datetime
import time
import random
import config  # 导入配置文件

# 基础配置从 config 读取
base_url = config.BASE_URL
base_file_name = config.BASE_FILE_NAME
file_extension = config.FILE_EXTENSION


def generate_timestamp_filename(base_name, file_extension):
    """生成带时间戳的文件名"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{base_name}{timestamp}.{file_extension}"
    return filename


def clean_text(text):
    """清理文本中的多余空格和换行"""
    if not text or not isinstance(text, str):
        return text
    # 去除首尾空格
    text = text.strip()
    # 将多个连续空格替换为单个空格
    text = ' '.join(text.split())
    return text


def convert_timestamp(timestamp):
    """将时间戳转换为日期时间字符串"""
    if not timestamp:
        return ""
    try:
        # 假设 timestamp 是秒级时间戳
        dt = datetime.fromtimestamp(int(timestamp))
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except (ValueError, TypeError):
        return str(timestamp)


def filter_fields(source_data):
    """只保留需要的字段"""
    filtered_data = {}
    for field in config.KEEP_FIELDS:
        if field in source_data:
            filtered_data[field] = source_data[field]
        elif field == "dateline_str":
            # 特殊处理：转换时间戳
            filtered_data[field] = convert_timestamp(source_data.get("dateline"))
        else:
            filtered_data[field] = ""
    return filtered_data


class WuhanCommentsCrawler:
    
    def __init__(self):
        """初始化爬虫，创建已处理ID集合"""
        self.processed_ids = set()  # 用于去重的ID集合
        self.total_duplicates = 0   # 统计重复数量
    
    def read_keywords(self):
        """读取关键词列表（根据配置决定是否使用全量爬取）"""
        # 如果开启全量爬取，返回一个包含空字符串的列表
        if config.CRAWL_ALL_DATA:
            if config.VERBOSE:
                print("全量爬取模式：不限制关键词，爬取所有数据")
            return [config.ALL_DATA_KEYWORD]
        
        # 否则从文件读取关键词
        file_path = config.KEYWORDS_FILE
        keywords = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    # 跳过空行和注释行
                    if line and not line.startswith('#'):
                        keywords.append(line)
            if config.VERBOSE:
                print(f"成功读取 {len(keywords)} 个关键词")
            return keywords
        except FileNotFoundError:
            print(f"未找到关键词文件 {file_path}，使用默认关键词")
            return ["老旧小区改造"]
        except Exception as e:
            print(f"读取关键词文件失败: {e}")
            return ["老旧小区改造"]
    
    def read_cookie(self):
        """读取Cookie配置"""
        # 优先使用 config 中配置的 Cookie 字符串
        if config.COOKIE_STRING:
            if config.VERBOSE:
                print(f"成功读取Cookie (长度: {len(config.COOKIE_STRING)})")
            return config.COOKIE_STRING
        
        # 否则从文件读取
        try:
            with open(config.COOKIE_FILE, 'r', encoding='utf-8') as f:
                cookie_content = f.read().strip()
            if config.VERBOSE:
                print(f"成功读取Cookie (长度: {len(cookie_content)})")
            return cookie_content
        except Exception as e:
            print(f"读取Cookie文件失败: {e}")
            return ""
    
    def build_form_data(self, keyword, page, page_size=None, start_date=None, end_date=None):
        """构建表单数据（application/x-www-form-urlencoded格式）"""
        if page_size is None:
            page_size = config.PAGE_SIZE
        if start_date is None:
            start_date = config.START_DATE
        if end_date is None:
            end_date = config.END_DATE
            
        form_data = {
            "pageNum": str(page),
            "pageSize": str(page_size),
            "tid": "",
            "queryCode": "",
            "fid": "",
            "startTime": start_date,
            "endTime": end_date,
            "nickName": "",
            "keywords": keyword  # 空字符串表示不限制关键词
        }
        return form_data
    
    def send_request(self, keyword, page, cookie_value, page_size=None):
        """发送POST请求获取数据（表单格式）"""
        url = base_url
        
        # 使用 config 中的 headers
        headers = config.HEADERS.copy()
        headers["Cookie"] = cookie_value
        
        # 构建表单数据
        form_data = self.build_form_data(keyword, page, page_size)
        
        try:
            # 使用 data 参数发送表单数据
            response = requests.post(
                url=url,
                headers=headers,
                data=form_data,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                if config.VERBOSE:
                    print(f"    请求失败，状态码: {response.status_code}")
                    print(f"    响应内容: {response.text[:200]}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"    HTTP请求异常: {e}")
            return None
    
    def deduplicate_data(self, data_list):
        """
        对数据进行去重
        返回去重后的数据列表和新增加的数量
        """
        unique_data = []
        new_count = 0
        
        for item in data_list:
            # 使用 tid 作为唯一标识
            tid = item.get('tid', '')
            if tid:
                if tid not in self.processed_ids:
                    self.processed_ids.add(tid)
                    unique_data.append(item)
                    new_count += 1
                else:
                    self.total_duplicates += 1
            else:
                # 如果没有 tid，仍然保留（但这种情况很少）
                unique_data.append(item)
        
        if config.VERBOSE and self.total_duplicates > 0:
            print(f"    去重: 本次新增 {new_count} 条，累计去重 {self.total_duplicates} 条")
        
        return unique_data
    
    def process_response_data(self, response_data, keyword, page):
        """处理响应数据，提取rows数组并添加元数据"""
        if not response_data:
            return []
        
        # 检查响应状态
        if response_data.get('code') != 0:
            if config.VERBOSE:
                print(f"    接口返回错误: {response_data.get('msg', '未知错误')}")
            return []
        
        # 提取数据 - 武汉留言板的数据在 data.rows 中
        data = response_data.get('data', {})
        rows = data.get('rows', [])
        
        if not rows:
            return []
        
        processed_data = []
        for item in rows:
            # 提取 source 中的实际数据
            source = item.get('source', item)
            
            # 清理 content 字段中的多余空格
            if 'content' in source:
                source['content'] = clean_text(source['content'])
            
            # 添加元数据
            source['keyword'] = keyword
            source['crawl_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # 只保留需要的字段
            filtered_source = filter_fields(source)
            processed_data.append(filtered_source)
        
        return processed_data
    
    def append_to_excel_append_mode(self, data_list, filename):
        """追加模式保存数据（用于分批爬取，已包含去重）"""
        if not data_list:
            return
        
        # 先对数据进行去重
        unique_data = self.deduplicate_data(data_list)
        
        if not unique_data:
            if config.VERBOSE:
                print("    本批次数据全部重复，跳过保存")
            return
        
        df_new = pd.DataFrame(unique_data)
        df_new = df_new.astype(str)
        
        if os.path.exists(filename):
            try:
                df_existing = pd.read_excel(filename, engine='openpyxl')
                df_combined = pd.concat([df_existing, df_new], ignore_index=True)
                df_combined.to_excel(filename, index=False, engine='openpyxl')
                if config.VERBOSE:
                    print(f"已追加 {len(df_new)} 条新数据到Excel文件")
            except Exception as e:
                print(f"读取现有Excel文件失败，创建新文件: {e}")
                df_new.to_excel(filename, index=False, engine='openpyxl')
        else:
            df_new.to_excel(filename, index=False, engine='openpyxl')
            if config.VERBOSE:
                print(f"创建Excel文件并写入 {len(df_new)} 条新数据")
    
    def load_existing_ids(self, filename):
        """从已有Excel文件中加载已处理的ID，用于断点续爬"""
        if not os.path.exists(filename):
            return
        
        try:
            df_existing = pd.read_excel(filename, engine='openpyxl')
            if 'tid' in df_existing.columns:
                existing_ids = df_existing['tid'].dropna().astype(str).tolist()
                self.processed_ids.update(existing_ids)
                if config.VERBOSE:
                    print(f"从已有文件加载 {len(existing_ids)} 条已处理记录")
        except Exception as e:
            print(f"读取已有Excel文件失败: {e}")
    
    def run_crawler(self):
        """主运行函数"""
        print("=" * 60)
        print("武汉城市留言板爬虫开始运行")
        if config.CRAWL_ALL_DATA:
            print("模式: 全量爬取（不限制关键词）")
        else:
            print("模式: 关键词爬取")
        print(f"时间范围: {config.START_DATE} 至 {config.END_DATE}")
        print(f"每页数量: {config.PAGE_SIZE}")
        print(f"最大页数: {config.MAX_PAGES}")
        print("=" * 60)
        
        # 1. 读取关键词
        keywords = self.read_keywords()
        if not keywords:
            print("没有找到关键词，程序退出")
            return
        
        # 2. 读取Cookie
        cookie_value = self.read_cookie()
        if not cookie_value:
            print("Cookie读取失败，程序退出")
            print("请确保 config.py 中配置了 COOKIE_STRING 或 cookie.txt 文件存在且包含有效的Cookie")
            return
        
        # 3. 生成文件名
        global final_filename
        final_filename = generate_timestamp_filename(base_file_name, file_extension)
        
        # 4. 加载已有的ID（如果文件已存在）
        self.load_existing_ids(final_filename)
        
        # 5. 配置爬取参数
        all_data = []
        total_new_records = 0
        
        # 6. 循环处理每个关键词
        for idx, keyword in enumerate(keywords):
            print(f"\n{'='*40}")
            if config.CRAWL_ALL_DATA:
                print(f"全量爬取阶段 [{idx+1}/{len(keywords)}]")
            else:
                print(f"关键词 [{idx+1}/{len(keywords)}]: {keyword}")
            print(f"{'='*40}")
            
            consecutive_empty = 0  # 连续空页计数
            
            for page in range(1, config.MAX_PAGES + 1):
                print(f"  正在爬取第 {page} 页...", end=" ")
                
                # 发送请求
                response_data = self.send_request(keyword, page, cookie_value)
                
                if not response_data:
                    print("请求失败")
                    consecutive_empty += 1
                    if consecutive_empty >= 2:
                        print("    连续2次请求失败，停止翻页")
                        break
                    continue
                
                # 处理响应数据
                processed_data = self.process_response_data(response_data, keyword, page)
                
                if not processed_data:
                    print("本页无数据")
                    consecutive_empty += 1
                    if consecutive_empty >= 2:
                        print("    连续2页无数据，停止翻页")
                        break
                    continue
                
                consecutive_empty = 0  # 重置空页计数
                
                # 添加到待保存列表
                all_data.extend(processed_data)
                print(f"获取 {len(processed_data)} 条，累计待保存 {len(all_data)} 条")
                
                # 每500条保存一次
                if len(all_data) >= 500:
                    self.append_to_excel_append_mode(all_data, final_filename)
                    total_new_records += len(all_data) - (len(all_data) - len([d for d in all_data if d.get('tid') not in self.processed_ids]))
                    all_data = []  # 清空已保存的数据
                
                # 随机延迟
                delay = random.uniform(config.MIN_DELAY, config.MAX_DELAY)
                time.sleep(delay)
            
            # 关键词之间增加延迟
            if idx < len(keywords) - 1:
                if config.CRAWL_ALL_DATA:
                    print(f"\n全量爬取阶段完成，等待{config.KEYWORD_DELAY}秒后继续...")
                else:
                    print(f"\n关键词 [{keyword}] 完成，等待{config.KEYWORD_DELAY}秒后继续...")
                time.sleep(config.KEYWORD_DELAY)
        
        # 7. 保存剩余数据
        if all_data:
            self.append_to_excel_append_mode(all_data, final_filename)
        
        # 8. 显示最终结果
        print("\n" + "=" * 60)
        print("爬虫运行完成！")
        print(f"数据已保存到: {final_filename}")
        
        # 显示统计信息
        try:
            if os.path.exists(final_filename):
                df = pd.read_excel(final_filename, engine='openpyxl')
                print(f"\n统计信息:")
                print(f"  - Excel文件总行数: {len(df)}")
                print(f"  - 去重统计: 共去重 {self.total_duplicates} 条重复数据")
                print(f"  - 有效数据: {len(df)} 条")
                print(f"  - Excel文件列数: {len(df.columns)}")
                print(f"  - 主要字段: {list(df.columns[:10])}")
                
                # 按关键词统计（仅当有关键词数据时显示）
                if 'keyword' in df.columns and not config.CRAWL_ALL_DATA:
                    print(f"\n各关键词数据量统计:")
                    keyword_counts = df['keyword'].value_counts().head(10)
                    for kw, count in keyword_counts.items():
                        if kw:  # 只显示非空关键词
                            print(f"    - {kw}: {count} 条")
        except Exception as e:
            print(f"读取结果文件失败: {e}")
        
        print("=" * 60)


# 为了保持与原有 start.py 的兼容性
ProjectDataCrawler = WuhanCommentsCrawler