import requests
import json
import time
from urllib.parse import urlencode

def test_api_variations():
    """测试API的不同变体"""
    base_url = "http://fast1.tdx.com.cn:7615/TQLEX"
    
    # 测试配置
    test_cases = [
        {
            "name": "基本POST请求",
            "method": "POST",
            "params": {"Entry": "CWServ.tdxzb_zxts_ywbb"},
            "data": {"Entry": "CWServ.tdxzb_zxts_ywbb"},
            "headers": {
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
        },
        {
            "name": "GET请求带参数",
            "method": "GET",
            "params": {"Entry": "CWServ.tdxzb_zxts_ywbb"},
            "data": None,
            "headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
        },
        {
            "name": "带Referer头的POST",
            "method": "POST",
            "params": {"Entry": "CWServ.tdxzb_zxts_ywbb"},
            "data": {"Entry": "CWServ.tdxzb_zxts_ywbb"},
            "headers": {
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Referer": "http://fast1.tdx.com.cn:7615/",
                "Origin": "http://fast1.tdx.com.cn:7615"
            }
        }
    ]
    
    for test_case in test_cases:
        print(f"\n=== {test_case['name']} ===")
        print(f"方法: {test_case['method']}")
        print(f"参数: {test_case['params']}")
        print(f"头信息: {test_case['headers']}")
        
        try:
            if test_case['method'] == 'POST':
                response = requests.post(
                    base_url,
                    params=test_case['params'],
                    data=urlencode(test_case['data']) if test_case['data'] else None,
                    headers=test_case['headers'],
                    timeout=10
                )
            else:
                response = requests.get(
                    base_url,
                    params=test_case['params'],
                    headers=test_case['headers'],
                    timeout=10
                )
            
            print(f"状态码: {response.status_code}")
            print(f"响应长度: {len(response.text)}")
            print(f"响应头: {dict(response.headers)}")
            
            if response.text:
                print("响应内容(前200字符):")
                print(response.text[:200])
                
                # 保存详细响应
                filename = f"response_{test_case['name'].replace(' ', '_')}.txt"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(f"测试用例: {test_case['name']}\n")
                    f.write(f"URL: {response.url}\n")
                    f.write(f"状态码: {response.status_code}\n")
                    f.write(f"响应头: {dict(response.headers)}\n")
                    f.write(f"响应内容:\n{response.text}\n")
                print(f"详细响应已保存到: {filename}")
                
        except Exception as e:
            print(f"请求失败: {e}")
        
        time.sleep(1)  # 短暂延迟

if __name__ == "__main__":
    print("开始API诊断测试...")
    test_api_variations()
    print("\n诊断测试完成！")