import requests
import json
import socket
from urllib.parse import urlencode

def network_diagnosis():
    """网络连接诊断"""
    
    hostname = "fast1.tdx.com.cn"
    port = 7615
    
    print("=== 网络连接诊断 ===")
    
    # 1. DNS解析测试
    try:
        ip_address = socket.gethostbyname(hostname)
        print(f"✅ DNS解析成功: {hostname} -> {ip_address}")
    except socket.gaierror:
        print(f"❌ DNS解析失败: {hostname}")
        return False
    
    # 2. 端口连接测试
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((ip_address, port))
        sock.close()
        
        if result == 0:
            print(f"✅ 端口连接成功: {ip_address}:{port}")
        else:
            print(f"❌ 端口连接失败: {ip_address}:{port} (错误代码: {result})")
            return False
    except Exception as e:
        print(f"❌ 端口连接异常: {e}")
        return False
    
    # 3. HTTP请求测试
    url = f"http://{hostname}:{port}/TQLEX"
    
    # 测试不同的Content-Type
    content_types = [
        "application/x-www-form-urlencoded; charset=UTF-8",
        "application/x-www-form-urlencoded", 
        "text/plain; charset=UTF-8",
        "application/json"
    ]
    
    print("\n=== HTTP请求测试 ===")
    
    for content_type in content_types:
        print(f"\n测试 Content-Type: {content_type}")
        
        headers = {
            "Content-Type": content_type,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "*/*"
        }
        
        payload = {"Entry": "CWServ.tdxzb_zxts_ywbb"}
        
        try:
            # 尝试GET
            get_response = requests.get(url, params=payload, headers=headers, timeout=10)
            print(f"GET状态: {get_response.status_code}, 长度: {len(get_response.text)}")
            
            # 尝试POST  
            post_response = requests.post(
                url, 
                data=urlencode(payload),
                headers=headers,
                timeout=10
            )
            print(f"POST状态: {post_response.status_code}, 长度: {len(post_response.text)}")
            
            if post_response.status_code == 200 and post_response.text:
                print(f"响应内容: {post_response.text[:100]}...")
                
                # 如果是JSON，解析错误信息
                if post_response.text.startswith('{'):
                    try:
                        data = post_response.json()
                        if 'ErrorCode' in data:
                            print(f"错误代码: {data.get('ErrorCode')}")
                            print(f"错误信息: {data.get('ErrorInfo')}")
                    except:
                        pass
                        
        except requests.exceptions.RequestException as e:
            print(f"请求异常: {e}")
    
    return True

def test_proxy_settings():
    """测试代理设置"""
    print("\n=== 代理设置测试 ===")
    
    # 检查系统代理
    try:
        import urllib.request
        proxy_handler = urllib.request.ProxyHandler()
        opener = urllib.request.build_opener(proxy_handler)
        urllib.request.install_opener(opener)
        
        # 测试连接
        test_url = "http://httpbin.org/ip"
        response = urllib.request.urlopen(test_url, timeout=10)
        print(f"系统代理测试: 成功连接到 {test_url}")
        
    except Exception as e:
        print(f"系统代理可能有问题: {e}")

if __name__ == "__main__":
    print("开始网络诊断...")
    
    # 测试网络连接
    network_ok = network_diagnosis()
    
    if network_ok:
        print("\n✅ 网络连接正常")
        print("问题可能在于:")
        print("1. API需要特定的认证或会话")
        print("2. 参数格式需要调整") 
        print("3. 服务器端限制或验证")
    else:
        print("\n❌ 网络连接存在问题")
        print("请检查:")
        print("1. 网络连接和防火墙设置")
        print("2. DNS解析")
        print("3. 代理设置")
    
    # 测试代理设置
    test_proxy_settings()