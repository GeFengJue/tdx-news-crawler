import requests
import json
import time

def test_json_payload():
    """测试JSON格式的负载"""
    url = "http://fast1.tdx.com.cn:7615/TQLEX"
    
    # 尝试不同的JSON负载格式
    json_payloads = [
        {
            "Entry": "CWServ.tdxzb_zxts_ywbb",
            "params": {"stock_code": "002762", "date": "2025-09-24"}
        },
        {
            "function": "CWServ.tdxzb_zxts_ywbb",
            "data": {"code": "002762", "type": "announcement"}
        },
        {
            "method": "getAnnouncements",
            "symbol": "002762",
            "start_date": "2025-09-24",
            "end_date": "2025-09-24"
        }
    ]
    
    headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json"
    }
    
    for i, payload in enumerate(json_payloads):
        print(f"\n=== 测试JSON负载格式 {i+1} ===")
        print(f"负载: {json.dumps(payload, ensure_ascii=False)}")
        
        try:
            response = requests.post(
                url,
                json=payload,
                headers=headers,
                timeout=10
            )
            
            print(f"状态码: {response.status_code}")
            print(f"响应: {response.text}")
            
            # 保存响应
            filename = f"json_response_{i+1}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"负载: {json.dumps(payload, ensure_ascii=False, indent=2)}\n")
                f.write(f"状态码: {response.status_code}\n")
                f.write(f"响应: {response.text}\n")
                
        except Exception as e:
            print(f"请求失败: {e}")

def test_form_data_with_additional_params():
    """测试带额外参数的表单数据"""
    url = "http://fast1.tdx.com.cn:7615/TQLEX"
    
    form_data_variations = [
        {"Entry": "CWServ.tdxzb_zxts_ywbb", "symbol": "002762", "date": "2025-09-24"},
        {"Entry": "CWServ.tdxzb_zxts_ywbb", "code": "002762", "type": "ywbb"},
        {"Entry": "CWServ.tdxzb_zxts_ywbb", "stock": "002762", "start_date": "2025-09-24"}
    ]
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    for i, data in enumerate(form_data_variations):
        print(f"\n=== 测试表单数据格式 {i+1} ===")
        print(f"数据: {data}")
        
        try:
            response = requests.post(
                url,
                data=data,
                headers=headers,
                timeout=10
            )
            
            print(f"状态码: {response.status_code}")
            print(f"响应: {response.text}")
            
            # 保存响应
            filename = f"form_response_{i+1}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"数据: {data}\n")
                f.write(f"状态码: {response.status_code}\n")
                f.write(f"响应: {response.text}\n")
                
        except Exception as e:
            print(f"请求失败: {e}")

if __name__ == "__main__":
    print("开始高级API测试...")
    print("1. 测试JSON负载格式")
    test_json_payload()
    
    print("\n2. 测试表单数据格式")
    test_form_data_with_additional_params()
    
    print("\n测试完成！")