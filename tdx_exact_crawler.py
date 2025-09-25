import requests
import json
import sqlite3
import re
from datetime import datetime
from urllib.parse import urlencode

class TDXExactCrawler:
    def __init__(self):
        self.base_url = "http://fast1.tdx.com.cn:7615"
        self.api_url = f"{self.base_url}/TQLEX"
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
            'Cookie': 'ASPSessionID=; LST=00'
        }
    
    def init_session(self):
        """初始化会话"""
        try:
            print("🔄 初始化会话...")
            main_url = f"{self.base_url}/site/tdx_zxts/page_main.html?tabsel=0"
            response = self.session.get(main_url, headers=self.headers, timeout=10)
            
            # 更新Cookie
            if 'Set-Cookie' in response.headers:
                self.headers['Cookie'] = response.headers['Set-Cookie']
            
            print(f"✅ 会话初始化成功，状态码: {response.status_code}")
            return True
        except Exception as e:
            print(f"❌ 会话初始化失败: {e}")
            return False
    
    def fetch_real_data(self):
        """获取真实数据 - 基于您提供的F12捕获数据"""
        try:
            print("🔄 发送精确API请求...")
            
            # 基于您提供的真实F12数据构建负载
            # 您提供的负载格式：{"CallName":"tdxzb_zxts_ywbb","Params":["2025-09-24 00:00:00","",1,50,"0"],"secuparse":true,"parsefld":"summary","tdxPageID":"_UrlEncode"}
            
            # 构建完整的请求参数
            request_params = {
                "CallName": "tdxzb_zxts_ywbb",
                "Params": ["2025-09-24 00:00:00", "", 1, 50, "0"],
                "secuparse": True,
                "parsefld": "summary",
                "tdxPageID": "_UrlEncode"
            }
            
            # 将JSON参数转换为字符串
            json_params = json.dumps(request_params, ensure_ascii=False)
            
            # 构建表单数据（基于您提供的F12数据）
            form_data = {
                'Entry': 'CWServ.tdxzb_zxts_ywbb'
            }
            
            # 完整的URL（包含Entry参数）
            full_url = f"{self.api_url}?Entry=CWServ.tdxzb_zxts_ywbb"
            
            print(f"🔍 请求URL: {full_url}")
            print(f"🔍 请求参数: {json_params}")
            
            # 发送POST请求
            response = self.session.post(
                full_url,
                data=form_data,  # 只发送Entry参数
                headers=self.headers,
                timeout=15
            )
            
            print(f"📊 响应状态码: {response.status_code}")
            print(f"📊 响应内容长度: {len(response.text)}")
            
            if response.status_code == 200:
                try:
                    # 尝试解析JSON响应
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
                            
                            # 显示前几条数据预览
                            if content:
                                print("\n📰 数据预览:")
                                for i, row in enumerate(content[:3], 1):
                                    if len(row) >= 3:
                                        print(f"   {i}. {row[2]}")  # 标题
                            
                            return data
                        else:
                            print("⚠️ 无结果数据")
                    else:
                        print(f"❌ API返回错误")
                        
                except json.JSONDecodeError as e:
                    print(f"❌ JSON解析失败: {e}")
                    print(f"📄 响应内容: {response.text[:500]}")
            else:
                print(f"❌ HTTP请求失败，状态码: {response.status_code}")
                print(f"📄 响应内容: {response.text[:200]}")
                
            return None
            
        except Exception as e:
            print(f"❌ 请求过程中发生错误: {e}")
            return None
    
    def test_different_formats(self):
        """测试不同的请求格式"""
        print("\n🔍 测试不同请求格式...")
        
        test_cases = [
            # 测试用例1: 基本Entry参数
            {"Entry": "CWServ.tdxzb_zxts_ywbb"},
            
            # 测试用例2: 带JSON参数
            {"Entry": "CWServ.tdxzb_zxts_ywbb", "data": json.dumps({
                "CallName": "tdxzb_zxts_ywbb",
                "Params": ["2025-09-24 00:00:00", "", 1, 50, "0"]
            })},
            
            # 测试用例3: 仅JSON参数
            {"CallName": "tdxzb_zxts_ywbb", "Params": '["2025-09-24 00:00:00","",1,50,"0"]'},
        ]
        
        for i, form_data in enumerate(test_cases, 1):
            print(f"\n📋 测试格式 {i}:")
            print(f"   参数: {form_data}")
            
            try:
                response = self.session.post(
                    self.api_url,
                    data=form_data,
                    headers=self.headers,
                    timeout=10
                )
                
                print(f"   状态码: {response.status_code}")
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        error_code = data.get('ErrorCode')
                        print(f"   错误码: {error_code}")
                        
                        if error_code == 0:
                            print("   ✅ 成功!")
                            return form_data, data
                    except:
                        print(f"   响应: {response.text[:100]}")
                
            except Exception as e:
                print(f"   请求失败: {e}")
        
        return None, None
    
    def create_database(self):
        """创建数据库"""
        conn = sqlite3.connect('tdx_exact_data.db')
        cursor = conn.cursor()
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS stock_announcements (
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
                    INSERT OR IGNORE INTO stock_announcements 
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
        print("🚀 启动同花顺精确数据爬虫...")
        print(f"⏰ 当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 初始化会话
        if not self.init_session():
            return
        
        # 创建数据库
        conn = self.create_database()
        print("✅ 数据库准备就绪")
        
        # 首先尝试精确请求
        print("\n🎯 尝试精确请求格式...")
        real_data = self.fetch_real_data()
        
        if not real_data:
            print("\n🔍 精确请求失败，尝试不同格式...")
            successful_format, real_data = self.test_different_formats()
            
            if successful_format:
                print(f"✅ 找到成功格式: {successful_format}")
        
        if real_data:
            # 保存数据
            saved_count = self.save_data(conn, real_data)
            print(f"✅ 成功保存 {saved_count} 条数据到数据库")
            
            # 显示统计信息
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM stock_announcements")
            total_count = cursor.fetchone()[0]
            
            if total_count > 0:
                cursor.execute("SELECT COUNT(DISTINCT stock_code) FROM stock_announcements WHERE stock_code IS NOT NULL")
                stock_count = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(DISTINCT source) FROM stock_announcements")
                source_count = cursor.fetchone()[0]
                
                print(f"\n📊 数据库统计:")
                print(f"   总记录数: {total_count}")
                print(f"   股票数量: {stock_count}")
                print(f"   来源数量: {source_count}")
                
                # 显示最新数据
                cursor.execute("""
                SELECT title, stock_code, issue_date, source 
                FROM stock_announcements 
                ORDER BY issue_date DESC 
                LIMIT 3
                """)
                
                print(f"\n📰 最新公告:")
                for i, (title, code, date, source) in enumerate(cursor.fetchall(), 1):
                    short_title = title[:60] + "..." if len(title) > 60 else title
                    print(f"   {i}. {short_title}")
                    print(f"      股票: {code} | 来源: {source} | 时间: {date}")
            else:
                print("⚠️ 数据库中没有保存任何数据")
        else:
            print("❌ 未能获取到有效数据")
        
        conn.close()
        print("\n🎉 爬虫执行完成!")

def main():
    crawler = TDXExactCrawler()
    crawler.run()

if __name__ == "__main__":
    main()