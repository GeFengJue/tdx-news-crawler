import sqlite3
import pandas as pd

class SimpleNewsQuery:
    def __init__(self, db_path='news_data.db'):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
    
    def get_total_count(self):
        """获取总记录数"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM news_announcements")
        return cursor.fetchone()[0]
    
    def query_latest_news(self, limit=10):
        """查询最新新闻"""
        query = """
        SELECT 
            rec_id, title, stock_code, stock_name, issue_date, src_info
        FROM news_announcements 
        ORDER BY issue_date DESC 
        LIMIT ?
        """
        df = pd.read_sql_query(query, self.conn, params=[limit])
        return df
    
    def query_by_stock(self, stock_code=None):
        """按股票查询"""
        if stock_code:
            query = """
            SELECT rec_id, title, issue_date, src_info 
            FROM news_announcements 
            WHERE stock_code = ? 
            ORDER BY issue_date DESC
            """
            df = pd.read_sql_query(query, self.conn, params=[stock_code])
            return df
        return pd.DataFrame()
    
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
    
    def show_summary(self):
        """显示数据摘要"""
        total = self.get_total_count()
        source_stats = self.get_source_stats()
        stock_stats = self.get_stock_stats()
        
        print("📊 数据摘要")
        print(f"总记录数: {total}")
        
        print("\n📰 来源分布:")
        for _, row in source_stats.iterrows():
            print(f"  {row['src_info']}: {row['count']} 条")
        
        if not stock_stats.empty:
            print(f"\n📈 股票公告统计:")
            for _, row in stock_stats.iterrows():
                print(f"  {row['stock_name']}({row['stock_code']}): {row['announcement_count']} 条")
    
    def show_latest_news(self, limit=5):
        """显示最新新闻"""
        df = self.query_latest_news(limit)
        if not df.empty:
            print(f"\n📝 最新{len(df)}条新闻:")
            for _, row in df.iterrows():
                print(f"\n🔹 {row['title']}")
                print(f"   代码: {row['stock_code']} | 来源: {row['src_info']} | 时间: {row['issue_date']}")
        else:
            print("❌ 没有新闻数据")
    
    def export_to_csv(self, filename='news_export.csv'):
        """导出数据到CSV"""
        query = "SELECT * FROM news_announcements"
        df = pd.read_sql_query(query, self.conn)
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"✅ 数据已导出到: {filename}")
        return df
    
    def close(self):
        """关闭数据库连接"""
        self.conn.close()

def main():
    """主函数"""
    try:
        query_tool = SimpleNewsQuery()
        print("✅ 数据库连接成功")
        
        # 显示摘要信息
        query_tool.show_summary()
        
        # 显示最新新闻
        query_tool.show_latest_news()
        
        # 导出数据
        query_tool.export_to_csv()
        
        print(f"\n💾 数据库文件: news_data.db")
        print("📄 数据已导出: news_export.csv")
        
    except Exception as e:
        print(f"❌ 错误: {e}")
    finally:
        query_tool.close()

if __name__ == "__main__":
    main()