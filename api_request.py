import requests
import json
from urllib.parse import urlencode

# 目标API配置
url = "http://fast1.tdx.com.cn:7615/TQLEX"

# 尝试不同的参数格式
payload_formats = [
    {"Entry": "CWServ.tdxzb_zxts_ywbb"},
    {"entry": "CWServ.tdxzb_zxts_ywbb"},
    {"Entry": "CWServ.tdxzb_zxts_ywbb", "other": "param"},
    {"function": "CWServ.tdxzb_zxts_ywbb"}
]

# 请求头
headers = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json",
    "Accept-Encoding": "gzip, deflate"
}

for i, payload in enumerate(payload_formats):
    print(f"\n=== 尝试第 {i+1} 种参数格式 ===")
    print(f"请求参数: {payload}")
    
    try:
        # 发送POST请求
        response = requests.post(
            url,
            data=urlencode(payload),
            headers=headers,
            timeout=15
        )
        
        # 检查响应状态
        if response.status_code == 200:
            print("请求成功!")
            print(f"状态码: {response.status_code}")
            print(f"响应内容长度: {len(response.text)}")
            print(f"响应内容: {response.text[:200]}...")  # 只显示前200字符
            
            # 尝试解析JSON响应
            try:
                data = response.json()
                print("\n解析后的JSON数据:")
                print(json.dumps(data, indent=2, ensure_ascii=False))
            except json.JSONDecodeError:
                print("\n响应不是有效的JSON格式")
                
        else:
            print(f"请求失败! 状态码: {response.status_code}")
            print(f"响应内容: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"请求发生错误: {e}")
    except Exception as e:
        print(f"其他错误: {e}")