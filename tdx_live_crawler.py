import requests
import json
import sqlite3
import re
from datetime import datetime

class TDXLiveCrawler:
    def __init__(self):
        self.base_url = "http://fast1.tdx.com.cn:7615"
        self.session = requests.Session()
        
        # 基于您提供的F12数据设置精确的请求头
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
    
    def build_correct_payload(self):
        """构建正确的请求负载 - 基于您提供的F12数据"""
        # 您提供的真实负载格式
        payload = {
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
        return payload
    
    def send_correct_request(self):
        """发送正确的API请求"""
        try:
            print("🔄 发送实时API请求...")
            
            # 构建API URL（基于您提供的F12数据）
            api_url = f"{self.base_url}/TQLEX?Entry=CWServ.tdxzb_zxts_ywbb"
            
            # 构建表单数据（Entry参数）
            form_data = {
                'Entry': 'CWServ.tdxzb_zxts_ywbb'
            }
            
            print(f"🔍 请求URL: {api_url}")
            print(f"🔍 表单数据: {form_data}")
            
            # 发送POST请求
            response = self.session.post(
                api_url,
                data=form_data,
                headers=self.headers,
                timeout=15
            )
            
            print(f"📊 响应状态码: {response.status_code}")
            print(f"📊 响应长度: {len(response.text)}")
            
            if response.status_code == 200:
                # 检查响应内容
                if len(response.text) > 100:  # 有实际内容
                    try:
                        data = response.json()
                        error_code = data.get('ErrorCode')
                        error_info = data.get('ErrorInfo', '')
                        
                        print(f"🔍 错误码: {error_code}")
                        print(f"🔍 错误信息: {error_info}")
                        
                        if error_code == 0:
                            print("✅ API请求成功!")
                            return data
                        else:
                            print(f"❌ API返回错误")
                            # 显示详细错误信息
                            print(f"📄 响应内容: {response.text[:500]}")
                    except json.JSONDecodeError as e:
                        print(f"❌ JSON解析失败: {e}")
                        print(f"📄 响应内容: {response.text[:500]}")
                else:
                    print(f"⚠️ 响应内容过短: {response.text}")
            else:
                print(f"❌ HTTP请求失败")
                
            return None
            
        except Exception as e:
            print(f"❌ 请求过程中发生错误: {e}")
            return None
    
    def try_alternative_methods(self):
        """尝试替代的请求方法"""
        print("\n🔍 尝试替代请求方法...")
        
        alternative_methods = [
            # 方法1: 直接使用JSON负载
            self.try_json_payload,
            # 方法2: 使用不同的参数格式
            self.try_different_params,
            # 方法3: 模拟浏览器完整流程
            self.try_browser_simulation
        ]
        
        for method in alternative_methods:
            result = method()
            if result:
                return result
        
        return None
    
    def try_json_payload(self):
        """尝试JSON格式负载"""
        print("📋 尝试JSON负载...")
        
        try:
            api_url = f"{self.base_url}/TQLEX"
            
            # 构建JSON负载
            json_payload = self.build_correct_payload()
            
            # 修改Content-Type为JSON
            json_headers = self.headers.copy()
            json_headers['Content-Type'] = 'application/json; charset=UTF-8'
            
            response = self.session.post(
                api_url,
                json=json_payload,
                headers=json_headers,
                timeout=15
            )
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if data.get('ErrorCode') == 0:
                        print("✅ JSON负载成功!")
                        return data
                except:
                    pass
                    
        except Exception as e:
            print(f"❌ JSON负载失败: {e}")
        
        return None
    
    def try_different_params(self):
        """尝试不同的参数组合"""
        print("📋 尝试不同参数组合...")
        
        param_combinations = [
            # 组合1: 带时间戳
            {"Entry": "CWServ.tdxzb_zxts_ywbb", "timestamp": str(int(datetime.now().timestamp()))},
            # 组合2: 带随机数
            {"Entry": "CWServ.tdxzb_zxts_ywbb", "random": "123456"},
            # 组合3: 简化参数
            {"Entry": "CWServ.tdxzb_zxts_ywbb"}
        ]
        
        for params in param_combinations:
            try:
                api_url = f"{self.base_url}/TQLEX"
                response = self.session.post(api_url, data=params, headers=self.headers, timeout=10)
                
                if response.status_code == 200 and len(response.text) > 100:
                    try:
                        data = response.json()
                        if data.get('ErrorCode') == 0:
                            print(f"✅ 参数组合成功: {params}")
                            return data
                    except:
                        continue
                        
            except Exception:
                continue
        
        return None
    
    def try_browser_simulation(self):
        """模拟浏览器完整流程"""
        print("📋 模拟浏览器流程...")
        
        try:
            # 1. 访问主页面
            main_url = f"{self.base_url}/site/tdx_zxts/page_main.html?tabsel=0"
            self.session.get(main_url, headers=self.headers)
            
            # 2. 可能需要的其他页面
            script_url = f"{self.base_url}/js/tdx_common.js"
            self.session.get(script_url, headers=self.headers)
            
            # 3. 发送API请求
            api_url = f"{self.base_url}/TQLEX?Entry=CWServ.tdxzb_zxts_ywbb"
            response = self.session.post(api_url, data={'Entry': 'CWServ.tdxzb_zxts_ywbb'}, headers=self.headers, timeout=15)
            
            if response.status_code == 200 and len(response.text) > 100:
                try:
                    data = response.json()
                    if data.get('ErrorCode') == 0:
                        print("✅ 浏览器模拟成功!")
                        return data
                except:
                    pass
                    
        except Exception as e:
            print(f"❌ 浏览器模拟失败: {e}")
        
        return None
    
    def create_database(self):
        """创建数据库"""
        conn = sqlite3.connect('tdx_live_data.db')
        cursor = conn.cursor()
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS live_stock_news (
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
                    INSERT OR IGNORE INTO live_stock_news 
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
        """运行实时爬虫"""
        print("🚀 启动同花顺实时数据爬虫...")
        print(f"⏰ 当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 初始化会话
        if not self.init_session():
            return
        
        # 创建数据库
        conn = self.create_database()
        print("✅ 数据库准备就绪")
        
        # 首先尝试标准请求
        print("\n🎯 尝试标准API请求...")
        live_data = self.send_correct_request()
        
        if not live_data:
            print("\n🔄 标准请求失败，尝试替代方法...")
            live_data = self.try_alternative_methods()
        
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
                for i, row in enumerate(content_data[:3], 1):
                    if len(row) >= 3:
                        title = row[2]
                        short_title = title[:50] + "..." if len(title) > 50 else title
                        print(f"   {i}. {short_title}")
        else:
            print("❌ 未能获取到实时数据")
            print("\n💡 建议:")
            print("   1. 检查网络连接")
            print("   2. 验证API接口是否可用")
            print("   3. 可能需要特定的认证或会话管理")
        
        conn.close()
        print("\n🎉 实时爬虫执行完成!")

def main():
    crawler = TDXLiveCrawler()
    crawler.run()

if __name__ == "__main__":
    main()