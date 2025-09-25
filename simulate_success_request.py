import requests
import json
from urllib.parse import urlencode
import time

def simulate_browser_request():
    """模拟浏览器行为，包含完整的时间戳和会话信息"""
    
    # 基础配置
    url = "http://fast1.tdx.com.cn:7615/TQLEX"
    
    # 基于成功响应模式构建参数
    # 可能需要时间戳或其他隐藏参数
    current_timestamp = int(time.time() * 1000)
    
    # 尝试不同的参数组合
    param_combinations = [
        # 基本参数
        {"Entry": "CWServ.tdxzb_zxts_ywbb"},
        
        # 带时间戳
        {"Entry": "CWServ.tdxzb_zxts_ywbb", "_": current_timestamp},
        
        # 带缓存标识
        {"Entry": "CWServ.tdxzb_zxts_ywbb", "cache": "true"},
        
        # 带分页参数
        {"Entry": "CWServ.tdxzb_zxts_ywbb", "page": "1", "limit": "50"},
        
        # 带日期范围
        {"Entry": "CWServ.tdxzb_zxts_ywbb", "start_date": "2025-09-24", "end_date": "2025-09-24"}
    ]
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "http://fast1.tdx.com.cn:7615",
        "Referer": "http://fast1.tdx.com.cn:7615/",
        "Connection": "keep-alive",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache"
    }
    
    session = requests.Session()
    
    print("模拟浏览器请求...")
    print(f"当前时间戳: {current_timestamp}")
    
    for i, params in enumerate(param_combinations):
        print(f"\n--- 测试组合 {i+1} ---")
        print(f"参数: {params}")
        
        try:
            # 先尝试GET请求
            print("尝试GET请求...")
            get_response = session.get(url, params=params, headers=headers, timeout=10)
            print(f"GET状态码: {get_response.status_code}")
            if get_response.text:
                print(f"GET响应: {get_response.text[:100]}...")
            
            # 然后尝试POST请求
            print("尝试POST请求...")
            post_response = session.post(
                url,
                params=params,
                data=urlencode(params),
                headers=headers,
                timeout=10
            )
            
            print(f"POST状态码: {post_response.status_code}")
            print(f"响应长度: {len(post_response.text)}")
            
            if post_response.status_code == 200:
                try:
                    data = post_response.json()
                    error_code = data.get('ErrorCode')
                    
                    if error_code == 0:
                        print("🎉 请求成功!")
                        print(f"HitCache: {data.get('HitCache')}")
                        
                        if 'ResultSets' in data:
                            result_set = data['ResultSets'][0]
                            content = result_set['Content']
                            print(f"获取到 {len(content)} 条数据")
                            
                            # 保存成功响应
                            filename = f"success_{i+1}.json"
                            with open(filename, 'w', encoding='utf-8') as f:
                                json.dump(data, f, indent=2, ensure_ascii=False)
                            print(f"响应已保存: {filename}")
                            
                            # 显示一些数据
                            for j, item in enumerate(content[:2]):
                                print(f"\n数据 {j+1}:")
                                for k, value in enumerate(item[:4]):
                                    col_name = result_set['ColName'][k]
                                    print(f"  {col_name}: {value}")
                            
                            return True
                        else:
                            print(f"错误代码: {error_code}")
                            print(f"错误信息: {data.get('ErrorInfo')}")
                    else:
                        print(f"错误代码: {error_code}")
                        print(f"错误信息: {data.get('ErrorInfo')}")
                        
                except json.JSONDecodeError:
                    print("响应不是JSON格式")
                    print(f"原始响应: {post_response.text[:200]}...")
            else:
                print(f"HTTP错误: {post_response.status_code}")
                
        except Exception as e:
            print(f"请求失败: {e}")
        
        time.sleep(1)  # 请求间延迟
    
    return False

if __name__ == "__main__":
    success = simulate_browser_request()
    if not success:
        print("\n❌ 所有尝试都失败了")
        print("可能需要:")
        print("1. 检查API文档获取正确的参数格式")
        print("2. 验证网络连接和服务器状态")
        print("3. 检查是否需要特定的认证或会话")