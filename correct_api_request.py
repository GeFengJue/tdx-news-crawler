import requests
import json
from urllib.parse import urlencode

def make_correct_request():
    """使用正确的参数格式发送API请求"""
    
    # 正确的URL和参数
    url = "http://fast1.tdx.com.cn:7615/TQLEX?Entry=CWServ.tdxzb_zxts_ywbb"
    payload = {"Entry": "CWServ.tdxzb_zxts_ywbb"}
    
    # 请求头
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache"
    }
    
    print("发送正确的API请求...")
    print(f"URL: {url}")
    print(f"负载: {payload}")
    print(f"方法: POST")
    
    try:
        # 发送POST请求
        response = requests.post(
            url,
            data=urlencode(payload),
            headers=headers,
            timeout=15
        )
        
        print(f"\n响应状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("请求成功!")
            
            # 解析JSON响应
            try:
                data = response.json()
                print(f"ErrorCode: {data.get('ErrorCode')}")
                print(f"HitCache: {data.get('HitCache')}")
                
                if data.get('ErrorCode') == 0 and 'ResultSets' in data:
                    result_set = data['ResultSets'][0]
                    col_names = result_set['ColName']
                    content = result_set['Content']
                    
                    print(f"\n获取到 {len(content)} 条公告数据:")
                    print(f"列名: {col_names}")
                    
                    # 显示前几条数据
                    for i, item in enumerate(content[:5]):
                        print(f"\n--- 公告 {i+1} ---")
                        for j, value in enumerate(item):
                            print(f"{col_names[j]}: {value}")
                    
                    # 保存完整响应到文件
                    with open('successful_response.json', 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=2, ensure_ascii=False)
                    print(f"\n完整响应已保存到: successful_response.json")
                    
                else:
                    print(f"错误信息: {data.get('ErrorInfo')}")
                    
            except json.JSONDecodeError as e:
                print(f"JSON解析错误: {e}")
                print(f"原始响应: {response.text}")
                
        else:
            print(f"请求失败，状态码: {response.status_code}")
            print(f"响应内容: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"请求发生错误: {e}")
    except Exception as e:
        print(f"其他错误: {e}")

if __name__ == "__main__":
    make_correct_request()