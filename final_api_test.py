import requests
import json
from urllib.parse import urlencode

def test_api_with_session():
    """使用会话和正确的参数格式测试API"""
    
    # 创建会话以保持cookie
    session = requests.Session()
    
    # 基础URL
    base_url = "http://fast1.tdx.com.cn:7615/TQLEX"
    
    # 尝试不同的参数组合
    test_cases = [
        {
            "name": "URL参数+表单数据",
            "params": {"Entry": "CWServ.tdxzb_zxts_ywbb"},
            "data": {"Entry": "CWServ.tdxzb_zxts_ywbb"}
        },
        {
            "name": "仅URL参数",
            "params": {"Entry": "CWServ.tdxzb_zxts_ywbb"},
            "data": None
        },
        {
            "name": "仅表单数据",
            "params": None,
            "data": {"Entry": "CWServ.tdxzb_zxts_ywbb"}
        },
        {
            "name": "带额外参数",
            "params": {"Entry": "CWServ.tdxzb_zxts_ywbb", "type": "ywbb"},
            "data": {"Entry": "CWServ.tdxzb_zxts_ywbb", "type": "ywbb"}
        }
    ]
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache"
    }
    
    for test_case in test_cases:
        print(f"\n=== 测试: {test_case['name']} ===")
        print(f"URL参数: {test_case['params']}")
        print(f"表单数据: {test_case['data']}")
        
        try:
            response = session.post(
                base_url,
                params=test_case['params'],
                data=urlencode(test_case['data']) if test_case['data'] else None,
                headers=headers,
                timeout=15
            )
            
            print(f"状态码: {response.status_code}")
            print(f"响应长度: {len(response.text)}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    error_code = data.get('ErrorCode')
                    
                    if error_code == 0:
                        print("✅ 请求成功!")
                        print(f"HitCache: {data.get('HitCache')}")
                        
                        if 'ResultSets' in data:
                            result_set = data['ResultSets'][0]
                            col_names = result_set['ColName']
                            content = result_set['Content']
                            
                            print(f"获取到 {len(content)} 条公告数据")
                            print(f"列名: {col_names}")
                            
                            # 显示前3条数据
                            for i, item in enumerate(content[:3]):
                                print(f"\n公告 {i+1}:")
                                for j, value in enumerate(item[:3]):  # 只显示前3个字段
                                    print(f"  {col_names[j]}: {value}")
                            
                            # 保存成功响应
                            filename = f"success_response_{test_case['name']}.json"
                            with open(filename, 'w', encoding='utf-8') as f:
                                json.dump(data, f, indent=2, ensure_ascii=False)
                            print(f"完整响应已保存到: {filename}")
                            return True
                            
                    else:
                        print(f"❌ 错误代码: {error_code}")
                        print(f"错误信息: {data.get('ErrorInfo')}")
                        
                except json.JSONDecodeError:
                    print("响应不是有效的JSON格式")
                    print(f"原始响应: {response.text[:200]}...")
                    
            else:
                print(f"HTTP错误: {response.status_code}")
                print(f"响应: {response.text}")
                
        except Exception as e:
            print(f"请求失败: {e}")
    
    return False

if __name__ == "__main__":
    print("开始最终API测试...")
    success = test_api_with_session()
    
    if success:
        print("\n🎉 API请求成功完成!")
    else:
        print("\n❌ 所有测试用例都失败了，可能需要检查API文档或网络连接")