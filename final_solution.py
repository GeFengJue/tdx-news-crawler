import requests
import json
import time

def create_successful_request():
    """基于成功响应数据创建正确的请求"""
    
    # 基于您提供的成功响应数据，API应该返回类似结构
    url = "http://fast1.tdx.com.cn:7615/TQLEX"
    
    # 尝试基于成功响应的模式构建请求
    # 成功响应包含: HitCache, ErrorCode: 0, ResultSets
    
    # 可能的正确参数格式
    test_scenarios = [
        # 场景1: 简单的GET请求
        {
            "method": "GET",
            "params": {"Entry": "CWServ.tdxzb_zxts_ywbb"},
            "headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
                "X-Requested-With": "XMLHttpRequest"
            }
        },
        
        # 场景2: 带会话的GET请求
        {
            "method": "GET", 
            "params": {
                "Entry": "CWServ.tdxzb_zxts_ywbb",
                "_": int(time.time() * 1000)  # 时间戳
            },
            "headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "application/json",
                "Referer": "http://fast1.tdx.com.cn:7615/",
                "Origin": "http://fast1.tdx.com.cn:7615"
            }
        },
        
        # 场景3: 模拟浏览器完整会话
        {
            "method": "GET",
            "params": {
                "Entry": "CWServ.tdxzb_zxts_ywbb",
                "cache": str(int(time.time())),
                "format": "json"
            },
            "headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Accept": "application/json, text/plain, */*",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Connection": "keep-alive",
                "Cache-Control": "no-cache",
                "Pragma": "no-cache"
            }
        }
    ]
    
    session = requests.Session()
    
    print("尝试基于成功响应模式的请求...")
    
    for i, scenario in enumerate(test_scenarios):
        print(f"\n=== 场景 {i+1}: {scenario['method']}请求 ===")
        print(f"参数: {scenario['params']}")
        
        try:
            if scenario['method'] == 'GET':
                response = session.get(
                    url,
                    params=scenario['params'],
                    headers=scenario['headers'],
                    timeout=15
                )
            else:
                response = session.post(
                    url,
                    params=scenario['params'],
                    headers=scenario['headers'],
                    timeout=15
                )
            
            print(f"状态码: {response.status_code}")
            print(f"响应长度: {len(response.text)}")
            print(f"响应头: {dict(response.headers)}")
            
            if response.status_code == 200:
                # 分析响应内容
                if response.text:
                    print(f"响应内容预览: {response.text[:200]}...")
                    
                    # 检查是否是成功的JSON响应
                    if response.text.strip().startswith('{'):
                        try:
                            data = response.json()
                            
                            if 'ErrorCode' in data:
                                error_code = data.get('ErrorCode')
                                if error_code == 0:
                                    print("🎉 成功获取数据!")
                                    print(f"HitCache: {data.get('HitCache')}")
                                    
                                    if 'ResultSets' in data:
                                        result_set = data['ResultSets'][0]
                                        content = result_set['Content']
                                        col_names = result_set['ColName']
                                        
                                        print(f"获取到 {len(content)} 条公告数据")
                                        print(f"列名: {col_names}")
                                        
                                        # 保存成功响应
                                        with open('successful_api_response.json', 'w', encoding='utf-8') as f:
                                            json.dump(data, f, indent=2, ensure_ascii=False)
                                        print("响应已保存到: successful_api_response.json")
                                        
                                        # 显示前几条数据
                                        for j, item in enumerate(content[:3]):
                                            print(f"\n公告 {j+1}:")
                                            for k, value in enumerate(item[:4]):
                                                print(f"  {col_names[k]}: {value}")
                                        
                                        return True
                                    else:
                                        print(f"错误代码: {error_code}")
                                        print(f"错误信息: {data.get('ErrorInfo')}")
                                else:
                                    print(f"API错误: {data.get('ErrorInfo')}")
                            else:
                                print("响应不包含ErrorCode字段")
                                print(f"完整响应: {json.dumps(data, indent=2, ensure_ascii=False)}")
                                
                        except json.JSONDecodeError:
                            print("响应不是有效的JSON格式")
                            print(f"原始响应: {response.text}")
                    else:
                        print("响应不是JSON格式")
            else:
                print(f"HTTP错误: {response.status_code}")
                print(f"错误响应: {response.text}")
                
        except Exception as e:
            print(f"请求异常: {e}")
        
        time.sleep(1)
    
    return False

def create_mock_success_response():
    """创建模拟的成功响应文件"""
    print("\n=== 创建模拟成功响应 ===")
    
    # 基于您提供的成功响应数据创建模拟文件
    mock_data = {
        "HitCache": "L1:B1FB6080A43E",
        "ErrorCode": 0,
        "ResultSets": [
            {
                "ColName": [
                    "pos",
                    "rec_id", 
                    "title",
                    "issue_date",
                    "summary",
                    "src_info",
                    "relate_id",
                    "Proc_Id",
                    "Mark_Id"
                ],
                "Content": [
                    [
                        1,
                        5549513,
                        "*ST金比(002762):关于变更参股公司董事、监事委派人员的自愿性信息披露公告",
                        "2025-09-24 17:57:00",
                        "*ST金比(002762):关于变更参股公司董事、监事委派人员的自愿性信息披露公告",
                        "深交所",
                        20009684,
                        0,
                        1
                    ]
                ]
            }
        ]
    }
    
    with open('mock_success_response.json', 'w', encoding='utf-8') as f:
        json.dump(mock_data, f, indent=2, ensure_ascii=False)
    
    print("模拟成功响应已创建: mock_success_response.json")
    print("这可以用于开发和测试目的")

if __name__ == "__main__":
    print("最终API请求解决方案")
    print("=" * 50)
    
    # 尝试真实请求
    success = create_successful_request()
    
    if not success:
        print("\n❌ 无法连接到真实API")
        print("可能的原因:")
        print("1. API需要特定的认证或会话管理")
        print("2. 服务器端有访问限制")
        print("3. 参数格式需要更精确的配置")
        
        # 创建模拟响应用于开发
        create_mock_success_response()
        
        print("\n💡 建议:")
        print("1. 检查API文档获取正确的认证方式")
        print("2. 使用浏览器开发者工具捕获完整的请求头")
        print("3. 验证是否需要先访问其他页面建立会话")