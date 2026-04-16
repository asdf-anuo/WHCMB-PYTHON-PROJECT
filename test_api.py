# -*- coding: utf-8 -*-
import requests

# 测试配置
url = "https://api1-liuyan.cjn.cn/messageboard/api/essearch/querySearchMapByPage"

# 从 config 复制 Cookie
cookie = "Hm_lvt_703a2e4b7c1acee6e7f0cf6d71017dee=1772936205; JSESSIONID=2a702f87-12ec-49c5-ae95-30dee8f544b7; rememberMe=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"  # 粘贴你的 Cookie

headers = {
    "Cookie": cookie,
    "accept": "application/json, text/plain, */*",
    "content-type": "application/x-www-form-urlencoded",
    "origin": "https://liuyan.cjn.cn",
    "referer": "https://liuyan.cjn.cn/",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36"
}

# 测试请求参数
data = {
    "pageNum": "1",
    "pageSize": "100",
    "tid": "",
    "queryCode": "",
    "fid": "",
    "startTime": "",
    "endTime": "",
    "nickName": "",
    "keywords": ""
}

print("正在测试 API...")
print(f"请求参数: {data}")
print("=" * 50)

try:
    response = requests.post(url, headers=headers, data=data, timeout=30)
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {response.text[:500]}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n响应码: {result.get('code')}")
        print(f"响应消息: {result.get('msg')}")
        
        if result.get('data'):
            rows = result['data'].get('rows', [])
            print(f"获取到数据条数: {len(rows)}")
            
            if rows:
                print("\n第一条数据示例:")
                source = rows[0].get('source', {})
                print(f"标题: {source.get('subject', '')[:50]}")
                print(f"内容: {source.get('content', '')[:100]}")
    else:
        print(f"请求失败: {response.status_code}")
        
except Exception as e:
    print(f"请求异常: {e}")