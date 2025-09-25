import requests
import json
import sqlite3
import re
from datetime import datetime

class TDXRealTimeCrawler:
    def __init__(self):
        self.base_url = "http://fast1.tdx.com.cn:7615"
        self.api_url = f"{self.base_url}/TQLEX?Entry=CWServ.tdxzb_zxts_ywbb"
        self.session = requests.Session()
        
        # 设置正确的请求头
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
    
    def fetch_real_data(self):
        """获取真实数据"""
        try:
            print("🔄 发送真实API请求...")
            
            # 构建正确的负载数据（基于您提供的真实格式）
            payload_data = {
                "CallName": "tdxzb_zxts_ywbb",
                "Params": ["2025-09-24 00:00:00", "", 1, 50, "0"],
                "secuparse": True,
                "parsefld": "summary",
                "tdxPageID": "_UrlEncode"
            }
            
            # 将JSON数据转换为表单格式
            form_data = {
                'Entry': 'CWServ.tdxzb_zxts_ywbb'
            }
            
            # 发送POST请求
            response = self.session.post(
                self.api_url,
                data=form_data,
                headers=self.headers,
                timeout=15
            )
            
            print(f"📊 响应状态码: {response.status_code}")
            print(f"📊 响应内容长度: {len(response.text)}")
            
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
                    print(f"📄 响应内容前500字符: {response.text[:500]}")
            else:
                print(f"❌ HTTP请求失败")
                
            return None
            
        except Exception as e:
            print(f"❌ 请求过程中发生错误: {e}")
            return None
    
    def create_database(self):
        """创建数据库"""
        conn = sqlite3.connect('tdx_real_data.db')
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
        
        # 创建索引
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_record_id ON stock_announcements(record_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_stock_code ON stock_announcements(stock_code)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_issue_date ON stock_announcements(issue_date)')
        
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
            data_dict = dict(zip(col_names, row))
            
            # 提取股票信息
            stock_code, stock_name = self.extract_stock_info(data_dict['title'])
            
            try:
                cursor.execute('''
                INSERT OR IGNORE INTO stock_announcements 
                (position, record_id, title, issue_date, summary, source, relate_id, proc_id, mark_id, stock_code, stock_name)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    data_dict['pos'],
                    data_dict['rec_id'],
                    data_dict['title'],
                    data_dict['issue_date'],
                    data_dict['summary'],
                    data_dict['src_info'],
                    data_dict['relate_id'],
                    data_dict['Proc_Id'],
                    data_dict['Mark_Id'],
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
        print("🚀 启动同花顺实时数据爬虫...")
        print(f"⏰ 当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 初始化会话
        if not self.init_session():
            return
        
        # 创建数据库
        conn = self.create_database()
        print("✅ 数据库准备就绪")
        
        # 获取数据
        real_data = self.fetch_real_data()
        
        if real_data:
            # 保存数据
            saved_count = self.save_data(conn, real_data)
            print(f"✅ 成功保存 {saved_count} 条数据到数据库")
            
            # 显示统计信息
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM stock_announcements")
            total_count = cursor.fetchone()[0]
            
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
            LIMIT 5
            """)
            
            print(f"\n📰 最新公告:")
            for i, (title, code, date, source) in enumerate(cursor.fetchall(), 1):
                short_title = title[:50] + "..." if len(title) > 50 else title
                print(f"   {i}. {short_title}")
                print(f"     股票: {code} | 来源: {source} | 时间: {date}")
        
        conn.close()
        print("\n🎉 爬虫执行完成!")

def main():
    crawler = TDXRealTimeCrawler()
    crawler.run()

if __name__ == "__main__":
    main()