import requests
import json
import sqlite3
import re
from datetime import datetime

class TDXExactRequest:
    def __init__(self):
        self.base_url = "http://fast1.tdx.com.cn:7615"
        self.session = requests.Session()
        
        # 设置精确的请求头（基于您提供的F12数据）
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'http://fast1.tdx.com.cn:7615',
            'Referer': 'http://fast1.tdx.com.cn:7615/site/tdx_zxts/page_main.html?tabsel=0',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
        }
    
    def init_session(self):
        """初始化会话"""
        try:
            print("🔄 初始化会话...")
            main_url = f"{self.base_url}/site/tdx_zxts/page_main.html?tabsel=0"
            response = self.session.get(main_url, headers=self.headers, timeout=10)
            print(f"✅ 会话初始化成功，状态码: {response.status_code}")
            return True
        except Exception as e:
            print(f"❌ 会话初始化失败: {e}")
            return False
    
    def send_exact_request(self):
        """发送精确的API请求 - 基于您提供的真实F12数据"""
        try:
            print("🔄 发送精确API请求...")
            
            # API URL
            api_url = f"{self.base_url}/TQLEX?Entry=CWServ.tdxzb_zxts_ywbb"
            
            # 构建精确的负载数据（基于您提供的F12数据）
            # 您提供的负载格式：{"CallName":"tdxzb_zxts_ywbb","Params":["2025-09-24 00:00:00","",1,50,"0"],"secuparse":true,"parsefld":"summary","tdxPageID":"_UrlEncode"}
            payload_data = {
                "CallName": "tdxzb_zxts_ywbb",
                "Params": [
                    datetime.now().strftime("%Y-%m-%d 00:00:00"),  # 当前日期
                    "",  # 空字符串
                    1,   # 页码
                    50,  # 每页数量
                    "0"  # 其他参数
                ],
                "secuparse": True,
                "parsefld": "summary",
                "tdxPageID": "_UrlEncode"
            }
            
            # 将JSON数据转换为字符串
            json_payload = json.dumps(payload_data, ensure_ascii=False)
            
            print(f"🔍 请求URL: {api_url}")
            print(f"🔍 JSON负载: {json_payload}")
            
            # 发送POST请求 - 使用data参数发送JSON字符串
            response = self.session.post(
                api_url,
                data=json_payload,  # 直接发送JSON字符串
                headers=self.headers,
                timeout=15
            )
            
            print(f"📊 响应状态码: {response.status_code}")
            print(f"📊 响应长度: {len(response.text)}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    error_code = data.get('ErrorCode')
                    error_info = data.get('ErrorInfo', '')
                    
                    print(f"🔍 错误码: {error_code}")
                    print(f"🔍 错误信息: {error_info}")
                    
                    if error_code == 0:
                        print("✅ API请求成功!")
                        result_sets = data.get('ResultSets', [])
                        if result_sets:
                            content = result_sets[0].get('Content', [])
                            print(f"📈 获取到 {len(content)} 条数据")
                            return data
                        else:
                            print("⚠️ 无结果数据")
                    else:
                        print(f"❌ API返回错误")
                        
                except json.JSONDecodeError as e:
                    print(f"❌ JSON解析失败: {e}")
                    print(f"📄 响应内容: {response.text[:500]}")
            else:
                print(f"❌ HTTP请求失败")
                
            return None
            
        except Exception as e:
            print(f"❌ 请求过程中发生错误: {e}")
            return None
    
    def try_form_data_request(self):
        """尝试表单数据格式请求"""
        print("\n🔄 尝试表单数据格式...")
        
        try:
            api_url = f"{self.base_url}/TQLEX?Entry=CWServ.tdxzb_zxts_ywbb"
            
            # 构建表单数据
            form_data = {
                'Entry': 'CWServ.tdxzb_zxts_ywbb',
                'CallName': 'tdxzb_zxts_ywbb',
                'Params': '["2025-09-24 00:00:00","",1,50,"0"]',
                'secuparse': 'true',
                'parsefld': 'summary',
                'tdxPageID': '_UrlEncode'
            }
            
            response = self.session.post(
                api_url,
                data=form_data,
                headers=self.headers,
                timeout=15
            )
            
            print(f"📊 响应状态码: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if data.get('ErrorCode') == 0:
                        print("✅ 表单数据请求成功!")
                        return data
                except:
                    pass
                    
        except Exception as e:
            print(f"❌ 表单数据请求失败: {e}")
        
        return None
    
    def create_database(self):
        """创建数据库"""
        conn = sqlite3.connect('tdx_exact_data.db')
        cursor = conn.cursor()
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS stock_news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            position INTEGER,
            record_id INTEGER UNIQUE,
            title TEXT,
            issue_date TEXT,
            summary TEXT,
            source TEXT,
            relate_id INTEGER,
            proc_id INTEGER,
            mark_id INTEGER,
            stock_code TEXT,
            stock_name TEXT,
            crawl_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        conn.commit()
        return conn
    
    def extract_stock_info(self, title):
        """从标题中提取股票代码和名称"""
        pattern = r'([^\(]+)\((\d{6})\)'
        match = re.search(pattern, title)
        if match:
            stock_name = match.group(1).strip()
            stock_code = match.group(2)
            return stock_code, stock_name
        return None, None
    
    def save_data(self, conn, data):
        """保存数据到数据库"""
        if not data or 'ResultSets' not in data or len(data['ResultSets']) == 0:
            print("❌ 无效的数据格式")
            return 0
        
        cursor = conn.cursor()
        result_set = data['ResultSets'][0]
        col_names = result_set['ColName']
        content_data = result_set['Content']
        
        inserted_count = 0
        for row in content_data:
            if len(row) >= len(col_names):
                data_dict = dict(zip(col_names, row))
                
                # 提取股票信息
                title = data_dict.get('title', '')
                stock_code, stock_name = self.extract_stock_info(title)
                
                try:
                    cursor.execute('''
                    INSERT OR IGNORE INTO stock_news 
                    (position, record_id, title, issue_date, summary, source, relate_id, proc_id, mark_id, stock_code, stock_name)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        data_dict.get('pos', 0),
                        data_dict.get('rec_id', 0),
                        title,
                        data_dict.get('issue_date', ''),
                        data_dict.get('summary', ''),
                        data_dict.get('src_info', ''),
                        data_dict.get('relate_id', 0),
                        data_dict.get('Proc_Id', 0),
                        data_dict.get('Mark_Id', 0),
                        stock_code,
                        stock_name
                    ))
                    
                    if cursor.rowcount > 0:
                        inserted_count += 1
                    
                except Exception as e:
                    print(f"❌ 插入数据失败: {e}")
        
        conn.commit()
        return inserted_count
    
    def run(self):
        """运行爬虫"""
        print("🚀 启动同花顺精确请求爬虫...")
        print(f"⏰ 当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 初始化会话
        if not self.init_session():
            return
        
        # 创建数据库
        conn = self.create_database()
        print("✅ 数据库准备就绪")
        
        # 首先尝试精确JSON请求
        print("\n🎯 尝试精确JSON请求...")
        live_data = self.send_exact_request()
        
        if not live_data:
            print("\n🔄 JSON请求失败，尝试表单数据格式...")
            live_data = self.try_form_data_request()
        
        if live_data:
            # 保存数据
            saved_count = self.save_data(conn, live_data)
            print(f"✅ 成功保存 {saved_count} 条实时数据")
            
            # 显示统计信息
            result_set = live_data['ResultSets'][0]
            content_data = result_set['Content']
            
            print(f"\n📊 实时数据统计:")
            print(f"   获取记录数: {len(content_data)}")
            
            # 显示最新数据
            if content_data:
                print(f"\n📰 最新公告:")
                for i, row in enumerate(content_data[:5], 1):
                    if len(row) >= 3:
                        title = row[2]
                        short_title = title[:60] + "..." if len(title) > 60 else title
                        print(f"   {i}. {short_title}")
        else:
            print("❌ 未能获取到实时数据")
            print("\n💡 可能的原因:")
            print("   1. API需要特定的会话认证")
            print("   2. 需要特定的Cookie或Token")
            print("   3. 服务器限制或IP被封")
            print("   4. 请求格式需要进一步调整")
        
        conn.close()
        print("\n🎉 爬虫执行完成!")

def main():
    crawler = TDXExactRequest()
    crawler.run()

if __name__ == "__main__":
    main()