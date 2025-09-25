import requests
import json
import sqlite3
import time
from urllib.parse import urlencode

def get_real_session():
    """获取真实的会话Cookie"""
    session = requests.Session()
    
    # 首先访问主页面获取有效Cookie
    main_url = "http://fast1.tdx.com.cn:7615/site/tdx_zxts/page_main.html?tabsel=0"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
    }
    
    try:
        print("🔄 正在访问主页面获取会话Cookie...")
        response = session.get(main_url, headers=headers, timeout=10)
        print(f"✅ 主页面访问状态: {response.status_code}")
        print(f"🍪 获取到的Cookie: {session.cookies.get_dict()}")
        
        return session
        
    except Exception as e:
        print(f"❌ 获取会话失败: {e}")
        return None

def try_real_api(session):
    """尝试使用真实会话访问API"""
    api_url = "http://fast1.tdx.com.cn:7615/TQLEX?Entry=CWServ.tdxzb_zxts_ywbb"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'http://fast1.tdx.com.cn:7615',
        'Referer': 'http://fast1.tdx.com.cn:7615/site/tdx_zxts/page_main.html?tabsel=0',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
    }
    
    # 尝试不同的参数格式
    payloads = [
        {'Entry': 'CWServ.tdxzb_zxts_ywbb'},
        {'entry': 'CWServ.tdxzb_zxts_ywbb'},
        {'method': 'CWServ.tdxzb_zxts_ywbb'},
        {'action': 'CWServ.tdxzb_zxts_ywbb'},
        {'func': 'CWServ.tdxzb_zxts_ywbb'},
        # 空参数
        {},
    ]
    
    for i, payload in enumerate(payloads):
        try:
            print(f"\n🔄 尝试第 {i+1} 种参数格式: {payload}")
            
            response = session.post(api_url, data=payload, headers=headers, timeout=15)
            
            print(f"📊 响应状态: {response.status_code}")
            print(f"📝 响应头: {dict(response.headers)}")
            
            if response.status_code == 200:
                try:
                    result = response.json()
                    print(f"✅ API响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
                    
                    if result.get('ErrorCode') == 0:
                        print("🎉 成功获取真实数据!")
                        return result
                    else:
                        print(f"⚠️ API错误: {result.get('ErrorCode')}")
                        
                except json.JSONDecodeError:
                    print(f"📄 响应内容: {response.text[:200]}...")
            
            time.sleep(1)
            
        except Exception as e:
            print(f"❌ 请求失败: {e}")
    
    return None

def main():
    print("🚀 开始尝试获取真实API数据...")
    
    # 获取真实会话
    session = get_real_session()
    if not session:
        print("❌ 无法建立会话，请检查网络连接")
        return
    
    # 尝试访问真实API
    real_data = try_real_api(session)
    
    if real_data:
        print("\n🎯 成功获取到真实API数据!")
        # 这里可以添加数据保存逻辑
    else:
        print("\n💥 所有尝试都失败了，可能需要:")
        print("1. 有效的用户认证")
        print("2. 特定的时间参数")  
        print("3. IP白名单权限")
        print("4. 商业API密钥")

if __name__ == "__main__":
    main()