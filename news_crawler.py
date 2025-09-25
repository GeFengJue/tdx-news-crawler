import requests
import json
import sqlite3
from urllib.parse import urlencode
import time
from datetime import datetime

class NewsCrawler:
    def __init__(self, db_path='news_data.db'):
        self.db_path = db_path
        self.api_url = "http://localhost:8000/TQLEX"  # 使用本地模拟器
        self.headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
    def setup_database(self):
        """创建数据库和表结构"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 创建新闻表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS news_announcements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pos INTEGER,
                rec_id INTEGER UNIQUE,
                title TEXT,
                issue_date TEXT,
                summary TEXT,
                src_info TEXT,
                relate_id INTEGER,
                proc_id INTEGER,
                mark_id INTEGER,
                crawl_time TEXT,
                stock_code TEXT,
                stock_name TEXT
            )
        ''')
        
        # 创建索引
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_rec_id ON news_announcements(rec_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_issue_date ON news_announcements(issue_date)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_stock_code ON news_announcements(stock_code)')
        
        conn.commit()
        conn.close()
        print("✅ 数据库初始化完成")
    
    def extract_stock_info(self, title):
        """从标题中提取股票代码和名称"""
        import re
        
        # 匹配模式: 股票名称(代码):公告标题
        pattern = r'(.+?)\((\d{6})\):'
        match = re.search(pattern, title)
        
        if match:
            stock_name = match.group(1).strip()
            stock_code = match.group(2)
            return stock_code, stock_name
        return None, None
    
    def fetch_news_data(self):
        """从API获取新闻数据"""
        payload = {"Entry": "CWServ.tdxzb_zxts_ywbb"}
        
        try:
            response = requests.post(
                self.api_url,
                data=urlencode(payload),
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('ErrorCode') == 0 and 'ResultSets' in data:
                    return data['ResultSets'][0]  # 返回第一个结果集
                else:
                    print(f"API错误: {data.get('ErrorInfo')}")
            else:
                print(f"HTTP错误: {response.status_code}")
                
        except Exception as e:
            print(f"请求失败: {e}")
        
        return None
    
    def save_to_database(self, result_set):
        """保存数据到数据库"""
        if not result_set:
            print("❌ 没有数据可保存")
            return False
        
        col_names = result_set['ColName']
        content = result_set['Content']
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        success_count = 0
        duplicate_count = 0
        error_count = 0
        
        for item in content:
            try:
                # 构建数据字典
                data_dict = dict(zip(col_names, item))
                
                # 提取股票信息
                stock_code, stock_name = self.extract_stock_info(data_dict['title'])
                
                # 检查是否已存在
                cursor.execute('SELECT id FROM news_announcements WHERE rec_id = ?', (data_dict['rec_id'],))
                if cursor.fetchone():
                    duplicate_count += 1
                    continue
                
                # 插入数据
                cursor.execute('''
                    INSERT INTO news_announcements 
                    (pos, rec_id, title, issue_date, summary, src_info, relate_id, proc_id, mark_id, crawl_time, stock_code, stock_name)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    stock_code,
                    stock_name
                ))
                
                success_count += 1
                
            except Exception as e:
                print(f"保存数据失败: {e}")
                error_count += 1
        
        conn.commit()
        conn.close()
        
        print(f"✅ 数据保存完成: 成功 {success_count} 条, 重复 {duplicate_count} 条, 错误 {error_count} 条")
        return success_count > 0
    
    def get_statistics(self):
        """获取数据库统计信息"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 总记录数
        cursor.execute('SELECT COUNT(*) FROM news_announcements')
        total_count = cursor.fetchone()[0]
        
        # 按来源统计
        cursor.execute('SELECT src_info, COUNT(*) FROM news_announcements GROUP BY src_info')
        src_stats = cursor.fetchall()
        
        # 最新公告时间
        cursor.execute('SELECT MAX(issue_date) FROM news_announcements')
        latest_date = cursor.fetchone()[0]
        
        conn.close()
        
        print(f"📊 数据库统计:")
        print(f"   总记录数: {total_count}")
        print(f"   最新公告: {latest_date}")
        print(f"   来源分布:")
        for src, count in src_stats:
            print(f"     {src}: {count} 条")
    
    def crawl(self):
        """执行完整的爬取流程"""
        print("🚀 开始爬取新闻数据...")
        print(f"📡 API地址: {self.api_url}")
        print(f"💾 数据库: {self.db_path}")
        
        # 初始化数据库
        self.setup_database()
        
        # 获取数据
        print("\n📥 从API获取数据...")
        result_set = self.fetch_news_data()
        
        if result_set:
            print(f"📊 获取到 {len(result_set['Content'])} 条公告数据")
            
            # 保存数据
            print("\n💾 保存数据到数据库...")
            self.save_to_database(result_set)
            
            # 显示统计信息
            print("\n📈 数据统计:")
            self.get_statistics()
            
            print("\n🎉 爬取任务完成!")
        else:
            print("❌ 数据获取失败")

def main():
    """主函数"""
    crawler = NewsCrawler()
    crawler.crawl()

if __name__ == "__main__":
    main()1