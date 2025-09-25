import sqlite3
import pandas as pd
from tabulate import tabulate

class NewsQueryTool:
    def __init__(self, db_path='news_data.db'):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
    
    def show_table_structure(self):
        """显示表结构"""
        cursor = self.conn.cursor()
        cursor.execute("PRAGMA table_info(news_announcements)")
        columns = cursor.fetchall()
        
        print("📋 数据表结构:")
        print(tabulate(columns, headers=['CID', 'Name', 'Type', 'NotNull', 'Default', 'PK'], tablefmt='grid'))
    
    def get_total_count(self):
        """获取总记录数"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM news_announcements")
        return cursor.fetchone()[0]
    
    def query_latest_news(self, limit=10):
        """查询最新新闻"""
        query = """
        SELECT 
            rec_id, title, stock_code, stock_name, issue_date, src_info, crawl_time
        FROM news_announcements 
        ORDER BY issue_date DESC 
        LIMIT ?
        """
        df = pd.read_sql_query(query, self.conn, params=[limit])
        return df
    
    def query_by_stock(self, stock_code=None, stock_name=None):
        """按股票查询"""
        if stock_code:
            query = "SELECT * FROM news_announcements WHERE stock_code = ? ORDER BY issue_date DESC"
            df = pd.read_sql_query(query, self.conn, params=[stock_code])
        elif stock_name:
            query = "SELECT * FROM news_announcements WHERE stock_name LIKE ? ORDER BY issue_date DESC"
            df = pd.read_sql_query(query, self.conn, params=[f'%{stock_name}%'])
        else:
            df = pd.DataFrame()
        return df
    
    def query_by_source(self, source):
        """按来源查询"""
        query = "SELECT * FROM news_announcements WHERE src_info = ? ORDER BY issue_date DESC"
        df = pd.read_sql_query(query, self.conn, params=[source])
        return df
    
    def get_source_stats(self):
        """获取来源统计"""
        query = "SELECT src_info, COUNT(*) as count FROM news_announcements GROUP BY src_info ORDER BY count DESC"
        df = pd.read_sql_query(query, self.conn)
        return df
    
    def get_stock_stats(self):
        """获取股票统计"""
        query = """
        SELECT stock_code, stock_name, COUNT(*) as announcement_count 
        FROM news_announcements 
        WHERE stock_code IS NOT NULL
        GROUP BY stock_code, stock_name 
        ORDER BY announcement_count DESC
        """
        df = pd.read_sql_query(query, self.conn)
        return df
    
    def export_to_csv(self, filename='news_export.csv'):
        """导出数据到CSV"""
        query = "SELECT * FROM news_announcements"
        df = pd.read_sql_query(query, self.conn)
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"✅ 数据已导出到: {filename}")
        return df
    
    def show_summary(self):
        """显示数据摘要"""
        total = self.get_total_count()
        source_stats = self.get_source_stats()
        stock_stats = self.get_stock_stats()
        
        print("📊 数据摘要")
        print(f"   总记录数: {total}")
        print(f"\n📰 来源分布:")
        for _, row in source_stats.iterrows():
            print(f"   {row['src_info']}: {row['count']} 条")
        
        if not stock_stats.empty:
            print(f"\n📈 股票公告统计 (前5):")
            for _, row in stock_stats.head().iterrows():
                print(f"   {row['stock_name']}({row['stock_code']}): {row['announcement_count']} 条")
    
    def interactive_query(self):
        """交互式查询界面"""
        while True:
            print("\n" + "="*50)
            print("📋 新闻数据查询工具")
            print("="*50)
            print("1. 查看最新新闻")
            print("2. 按股票代码查询")
            print("3. 按股票名称查询")
            print("4. 按来源查询")
            print("5. 显示数据统计")
            print("6. 导出数据到CSV")
            print("7. 显示表结构")
            print("8. 退出")
            
            choice = input("\n请选择操作 (1-8): ").strip()
            
            if choice == '1':
                limit = input("显示数量 (默认10): ").strip()
                limit = int(limit) if limit.isdigit() else 10
                df = self.query_latest_news(limit)
                if not df.empty:
                    print(tabulate(df, headers='keys', tablefmt='grid', showindex=False))
                else:
                    print("❌ 没有数据")
            
            elif choice == '2':
                code = input("请输入股票代码: ").strip()
                df = self.query_by_stock(stock_code=code)
                if not df.empty:
                    print(tabulate(df[['rec_id', 'title', 'issue_date', 'src_info']], 
                                 headers='keys', tablefmt='grid', showindex=False))
                else:
                    print("❌ 未找到该股票的数据")
            
            elif choice == '3':
                name = input("请输入股票名称: ").strip()
                df = self.query_by_stock(stock_name=name)
                if not df.empty:
                    print(tabulate(df[['rec_id', 'title', 'stock_code', 'issue_date', 'src_info']], 
                                 headers='keys', tablefmt='grid', showindex=False))
                else:
                    print("❌ 未找到该股票的数据")
            
            elif choice == '4':
                sources = self.get_source_stats()['src_info'].tolist()
                print("可用来源:", ", ".join(sources))
                source = input("请输入来源: ").strip()
                df = self.query_by_source(source)
                if not df.empty:
                    print(tabulate(df[['rec_id', 'title', 'stock_code', 'issue_date']], 
                                 headers='keys', tablefmt='grid', showindex=False))
                else:
                    print("❌ 未找到该来源的数据")
            
            elif choice == '5':
                self.show_summary()
            
            elif choice == '6':
                filename = input("导出文件名 (默认: news_export.csv): ").strip() or 'news_export.csv'
                self.export_to_csv(filename)
            
            elif choice == '7':
                self.show_table_structure()
            
            elif choice == '8':
                print("👋 再见!")
                break
            
            else:
                print("❌ 无效选择")

    def close(self):
        """关闭数据库连接"""
        self.conn.close()

def main():
    """主函数"""
    try:
        tool = NewsQueryTool()
        print("✅ 数据库连接成功")
        tool.show_summary()
        tool.interactive_query()
    except Exception as e:
        print(f"❌ 错误: {e}")
    finally:
        tool.close()

if __name__ == "__main__":
    main()