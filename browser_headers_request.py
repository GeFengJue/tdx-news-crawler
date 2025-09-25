import requests
import json
from urllib.parse import urlencode

def make_request_with_browser_headers():
    """使用完整的浏览器头信息发送请求"""
    
    url = "http://fast1.tdx.com.cn:7615/TQLEX"
    
    # 基于提供的请求头信息
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": "ASPSessionID=; LST=00",
        "Host": "fast1.tdx.com.cn:7615",
        "Origin": "http://fast1.tdx.com.cn:7615",
        "Referer": "http://fast1.tdx.com.cn:7615/site/tdx_zxts/page_main.html?tabsel=0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0",
        "X-Requested-With": "XMLHttpRequest"
    }
    
    # 负载数据
    payload = {"Entry": "CWServ.tdxzb_zxts_ywbb"}
    
    print("使用完整浏览器头信息发送请求...")
    print(f"URL: {url}")
    print(f"Headers: {json.dumps(headers, indent=2, ensure_ascii=False)}")
    print(f"Payload: {payload}")
    
    try:
        response = requests.post(
            url,
            data=urlencode(payload),
            headers=headers,
            timeout=15
        )
        
        print(f"\n响应状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        print(f"响应长度: {len(response.text)}")
        
        if response.status_code == 200:
            print("✅ 请求成功!")
            
            if response.text:
                print(f"响应内容: {response.text[:500]}...")
                
                # 尝试解析JSON
                try:
                    data = response.json()
                    print(f"ErrorCode: {data.get('ErrorCode')}")
                    
                    if data.get('ErrorCode') == 0:
                        print("🎉 成功获取数据!")
                        print(f"HitCache: {data.get('HitCache')}")
                        
                        if 'ResultSets' in data:
                            result_set = data['ResultSets'][0]
                            content = result_set['Content']
                            col_names = result_set['ColName']
                            
                            print(f"获取到 {len(content)} 条公告数据")
                            print(f"列名: {col_names}")
                            
                            # 保存响应
                            with open('browser_success_response.json', 'w', encoding='utf-8') as f:
                                json.dump(data, f, indent=2, ensure_ascii=False)
                            print("响应已保存到: browser_success_response.json")
                            
                            # 显示前几条数据
                            for i, item in enumerate(content[:3]):
                                print(f"\n公告 {i+1}:")
                                for j, value in enumerate(item[:4]):
                                    print(f"  {col_names[j]}: {value}")
                            
                            return True
                        else:
                            print("响应不包含ResultSets")
                    else:
                        print(f"错误信息: {data.get('ErrorInfo')}")
                        
                except json.JSONDecodeError:
                    print("响应不是JSON格式")
                    print(f"原始响应: {response.text}")
            else:
                print("响应内容为空")
                
        else:
            print(f"HTTP错误: {response.status_code}")
            print(f"错误响应: {response.text}")
            
    except Exception as e:
        print(f"请求异常: {e}")
    
    return False

if __name__ == "__main__":
    success = make_request_with_browser_headers()
    if not success:
        print("\n❌ 请求仍然失败")
        print("可能需要:")
        print("1. 有效的会话Cookie")
        print("2. 先访问Referer页面建立会话")
        print("3. 其他认证信息")