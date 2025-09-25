import json
import http.server
import socketserver
from urllib.parse import urlparse, parse_qs

class TDXAPIHandler(http.server.SimpleHTTPRequestHandler):
    """同花顺API模拟器"""
    
    def do_POST(self):
        """处理POST请求"""
        if self.path.startswith('/TQLEX'):
            self.handle_tqlex_api()
        else:
            self.send_error(404, "API not found")
    
    def handle_tqlex_api(self):
        """处理TQLEX API请求"""
        try:
            # 解析请求参数
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')
            params = parse_qs(post_data)
            
            # 检查Entry参数
            entry = params.get('Entry', [''])[0]
            
            if entry == 'CWServ.tdxzb_zxts_ywbb':
                # 返回成功的响应数据
                success_response = {
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
                                ],
                                [
                                    2,
                                    5549507,
                                    "蓝特光学(688127):2025年第二次临时股东大会决议公告",
                                    "2025-09-24 17:57:00",
                                    "蓝特光学(688127):2025年第二次临时股东大会决议公告",
                                    "上交所",
                                    20009678,
                                    0,
                                    1
                                ],
                                [
                                    3,
                                    5549506,
                                    "蓝特光学(688127):2025年第二次临时股东大会的法律意见书",
                                    "2025-09-24 17:57:00",
                                    "蓝特光学(688127):2025年第二次临时股东大会的法律意见书",
                                    "上交所",
                                    20009677,
                                    0,
                                    1
                                ]
                            ]
                        }
                    ]
                }
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                response_json = json.dumps(success_response, ensure_ascii=False)
                self.wfile.write(response_json.encode('utf-8'))
                
            else:
                # 参数错误
                error_response = {
                    "ErrorCode": -1002,
                    "ErrorInfo": "请求参数错误"
                }
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps(error_response).encode('utf-8'))
                
        except Exception as e:
            self.send_error(500, f"Server error: {str(e)}")
    
    def do_OPTIONS(self):
        """处理OPTIONS请求（CORS）"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def run_simulator(port=8000):
    """运行API模拟器"""
    print("🚀 启动同花顺API模拟器")
    print(f"📡 服务地址: http://localhost:{port}")
    print("🔧 支持的API:")
    print("   POST /TQLEX?Entry=CWServ.tdxzb_zxts_ywbb")
    print("   Content-Type: application/x-www-form-urlencoded")
    print("📊 返回模拟的股票公告数据")
    print("⏹️ 按 Ctrl+C 停止服务")
    
    with socketserver.TCPServer(("", port), TDXAPIHandler) as httpd:
        print(f"✅ 服务已启动在端口 {port}")
        httpd.serve_forever()

def create_test_client():
    """创建测试客户端"""
    test_client_code = '''import requests
from urllib.parse import urlencode

# 测试本地API模拟器
url = "http://localhost:8000/TQLEX"
payload = {"Entry": "CWServ.tdxzb_zxts_ywbb"}
headers = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
}

try:
    response = requests.post(url, data=urlencode(payload), headers=headers)
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.text}")
except Exception as e:
    print(f"请求失败: {e}")
'''

    with open('test_api_client.py', 'w', encoding='utf-8') as f:
        f.write(test_client_code)
    
    print("✅ 测试客户端已创建: test_api_client.py")

if __name__ == "__main__":
    # 创建测试客户端
    create_test_client()
    
    # 启动模拟器
    try:
        run_simulator()
    except KeyboardInterrupt:
        print("\n🛑 服务已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")