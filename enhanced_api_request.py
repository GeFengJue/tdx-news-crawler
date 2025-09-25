import requests
import json
import time
from urllib.parse import urlencode

def make_api_request(url, payload, headers, retries=3, delay=2):
    """发送API请求并处理重试"""
    for attempt in range(retries):
        try:
            print(f"尝试第 {attempt + 1} 次请求...")
            response = requests.post(
                url,
                data=urlencode(payload),
                headers=headers,
                timeout=15
            )
            return response
        except requests.exceptions.Timeout:
            print(f"请求超时，{delay}秒后重试...")
            time.sleep(delay)
        except requests.exceptions.RequestException as e:
            print(f"请求错误: {e}")
            if attempt == retries - 1:
                raise e
            time.sleep(delay)
    return None

# 目标API配置
url = "http://fast1.tdx.com.cn:7615/TQLEX"

# 尝试不同的请求头配置
header_configs = [
    {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    },
    {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
]

# 主要负载参数
main_payload = {"Entry": "CWServ.tdxzb_zxts_ywbb"}

print("开始API请求测试...")

for header_idx, headers in enumerate(header_configs):
    print(f"\n=== 测试第 {header_idx + 1} 种请求头配置 ===")
    print(f"请求头: {headers}")
    
    response = make_api_request(url, main_payload, headers)
    
    if response:
        print(f"状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        print(f"响应内容长度: {len(response.text)}")
        
        # 保存响应到文件
        filename = f"response_header_{header_idx + 1}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"URL: {url}\n")
            f.write(f"Payload: {main_payload}\n")
            f.write(f"Headers: {headers}\n")
            f.write(f"Status: {response.status_code}\n")
            f.write(f"Response: {response.text}\n")
        print(f"响应已保存到: {filename}")
        
        # 显示部分响应内容
        if response.text:
            print("响应内容(前500字符):")
            print(response.text[:500])
    else:
        print("所有重试尝试都失败了")

print("\n测试完成！")