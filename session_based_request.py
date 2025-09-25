import requests
import json
from urllib.parse import urlencode
import time

def establish_session_and_request():
    """建立会话并发送API请求"""
    
    # 第一步：访问Referer页面获取有效Cookie
    referer_url = "http://fast1.tdx.com.cn:7615/site/tdx_zxts/page_main.html?tabsel=0"
    api_url = "http://fast1.tdx.com.cn:7615/TQLEX"
    
    session = requests.Session()
    
    # 设置基础头信息
    base_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
    }
    
    print("第一步：访问Referer页面建立会话...")
    print(f"访问: {referer_url}")
    
    try:
        # 访问Referer页面
        response = session.get(referer_url, headers=base_headers, timeout=15)
        print(f"页面访问状态码: {response.status_code}")
        print(f"获取到的Cookie: {dict(session.cookies)}")
        
        # 等待一下让会话建立
        time.sleep(2)
        
        print("\n第二步：发送API请求...")
        
        # API请求头信息
        api_headers = {
            **base_headers,
            "Accept": "*/*",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "http://fast1.tdx.com.cn:7615",
            "Referer": referer_url,
            "X-Requested-With": "XMLHttpRequest"
        }
        
        # API负载
        payload = {"Entry": "CWServ.tdxzb_zxts_ywbb"}
        
        # 发送API请求
        api_response = session.post(
            api_url,
            data=urlencode(payload),
            headers=api_headers,
            timeout=15
        )
        
        print(f"API响应状态码: {api_response.status_code}")
        print(f"API响应头: {dict(api_response.headers)}")
        print(f"响应长度: {len(api_response.text)}")
        
        if api_response.status_code == 200:
            print("✅ API请求成功!")
            
            if api_response.text:
                print(f"响应内容: {api_response.text[:500]}...")
                
                try:
                    data = api_response.json()
                    error_code = data.get('ErrorCode')
                    
                    if error_code == 0:
                        print("🎉 成功获取数据!")
                        print(f"HitCache: {data.get('HitCache')}")
                        
                        if 'ResultSets' in data:
                            result_set = data['ResultSets'][0]
                            content = result_set['Content']
                            col_names = result_set['ColName']
                            
                            print(f"获取到 {len(content)} 条公告数据")
                            
                            # 保存响应
                            with open('session_success_response.json', 'w', encoding='utf-8') as f:
                                json.dump(data, f, indent=2, ensure_ascii=False)
                            print("响应已保存到: session_success_response.json")
                            
                            # 显示前几条数据
                            for i, item in enumerate(content[:3]):
                                print(f"\n公告 {i+1}:")
                                for j, value in enumerate(item[:4]):
                                    print(f"  {col_names[j]}: {value}")
                            
                            return True
                        else:
                            print("响应不包含ResultSets")
                    else:
                        print(f"错误代码: {error_code}")
                        print(f"错误信息: {data.get('ErrorInfo')}")
                        
                except json.JSONDecodeError:
                    print("响应不是JSON格式")
                    print(f"原始响应: {api_response.text}")
            else:
                print("响应内容为空")
                
        else:
            print(f"API请求失败: {api_response.status_code}")
            print(f"错误响应: {api_response.text}")
            
    except Exception as e:
        print(f"请求异常: {e}")
    
    return False

def test_direct_cookie():
    """测试直接使用有效的Cookie"""
    print("\n备用方案：测试直接Cookie访问...")
    
    # 这里需要有效的Cookie值，可能需要从浏览器获取
    # ASPSessionID 和 LST 应该是具体的值，而不是空的
    
    url = "http://fast1.tdx.com.cn:7615/TQLEX"
    
    # 假设的Cookie值（需要从浏览器获取实际值）
    cookies = {
        "ASPSessionID": "实际会话ID",  # 需要替换为实际值
        "LST": "实际LST值"            # 需要替换为实际值
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "http://fast1.tdx.com.cn:7615",
        "Referer": "http://fast1.tdx.com.cn:7615/site/tdx_zxts/page_main.html?tabsel=0",
        "X-Requested-With": "XMLHttpRequest"
    }
    
    payload = {"Entry": "CWServ.tdxzb_zxts_ywbb"}
    
    try:
        response = requests.post(
            url,
            data=urlencode(payload),
            headers=headers,
            cookies=cookies,
            timeout=15
        )
        
        print(f"直接Cookie访问状态码: {response.status_code}")
        if response.text:
            print(f"响应: {response.text[:200]}...")
            
    except Exception as e:
        print(f"直接Cookie访问失败: {e}")

if __name__ == "__main__":
    print("建立会话并发送API请求")
    print("=" * 50)
    
    success = establish_session_and_request()
    
    if not success:
        print("\n❌ 会话建立失败")
        print("可能需要:")
        print("1. 从浏览器获取有效的Cookie值")
        print("2. 检查网络代理设置")
        print("3. 验证服务器可访问性")
        
        # 测试直接Cookie访问（需要有效Cookie值）
        test_direct_cookie()