#!/usr/bin/env python3
"""
GitHub Actions专用的新闻爬虫脚本
每15分钟自动运行，更新新闻数据库
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from tdx_all_news_crawler import TDXAllNewsCrawler
import sqlite3
import pandas as pd
from datetime import datetime

def main():
    print("🚀 GitHub Actions新闻爬虫启动")
    print(f"⏰ 当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # 初始化爬虫
        crawler = TDXAllNewsCrawler()
        
        # 初始化会话
        if not crawler.init_session():
            print("❌ 会话初始化失败")
            return 1
        
        # 创建数据库连接
        conn = crawler.create_database('tdx_all_news.db')
        
        # 获取新闻数据（获取前3页，每页50条）
        all_data = []
        for page in range(1, 4):
            page_data = crawler.fetch_page_data(page, 50)
            if page_data:
                all_data.append(page_data)
                print(f"✅ 第{page}页获取成功")
            else:
                print(f"❌ 第{page}页获取失败")
                break
        
        if all_data:
            # 保存数据到数据库
            saved_count = crawler.save_all_data(conn, all_data)
            print(f"✅ 成功保存 {saved_count} 条数据到数据库")
            
            # 导出为CSV文件
            export_to_csv(conn)
            
            # 导出为JSON文件供网站使用
            export_to_json(conn)
            
            # 显示统计信息
            show_statistics(conn)
        else:
            print("❌ 未能获取到任何数据")
        
        conn.close()
        print("\n🎉 GitHub Actions爬虫任务完成!")
        return 0
        
    except Exception as e:
        print(f"❌ 爬虫执行失败: {e}")
        return 1

def export_to_csv(conn):
    """导出数据库为CSV文件"""
    try:
        cursor = conn.cursor()
        cursor.execute('''
        SELECT position, record_id, title, issue_date, summary, source, 
               stock_code, stock_name, relate_id, proc_id, mark_id
        FROM all_stock_news 
        ORDER BY issue_date DESC
        ''')
        
        # 获取列名
        columns = [description[0] for description in cursor.description]
        data = cursor.fetchall()
        
        # 创建DataFrame并导出
        df = pd.DataFrame(data, columns=columns)
        df.to_csv('tdx_all_news_export.csv', index=False, encoding='utf-8-sig')
        print(f"📄 数据已导出到CSV文件，共 {len(df)} 条记录")
        
    except Exception as e:
        print(f"❌ CSV导出失败: {e}")

def export_to_json(conn):
    """导出数据库为JSON文件供网站使用"""
    try:
        cursor = conn.cursor()
        cursor.execute('''
        SELECT record_id, title, issue_date, summary, source, mark_id
        FROM all_stock_news 
        ORDER BY issue_date DESC
        LIMIT 200
        ''')
        
        data = cursor.fetchall()
        
        # 转换为网站需要的格式
        news_list = []
        for record in data:
            news_list.append({
                'id': record[0],
                'title': record[1],
                'date': record[2],
                'time': record[2].split(' ')[1] if record[2] and ' ' in record[2] else '--:--:--',
                'content': record[3] or record[1],
                'source': record[4] or '未知来源',
                'highlight': record[5] == 1
            })
        
        # 生成JSON文件
        import json
        json_data = {
            'success': True,
            'data': news_list,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'count': len(news_list)
        }
        
        with open('latest_news.json', 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        
        print(f"📄 数据已导出到JSON文件，共 {len(news_list)} 条记录")
        
    except Exception as e:
        print(f"❌ JSON导出失败: {e}")

def show_statistics(conn):
    """显示统计信息"""
    try:
        cursor = conn.cursor()
        
        # 总记录数
        cursor.execute("SELECT COUNT(*) FROM all_stock_news")
        total_count = cursor.fetchone()[0]
        
        # 最新记录时间
        cursor.execute("SELECT MAX(issue_date) FROM all_stock_news")
        latest_date = cursor.fetchone()[0]
        
        # 来源统计
        cursor.execute("SELECT source, COUNT(*) FROM all_stock_news GROUP BY source ORDER BY COUNT(*) DESC LIMIT 5")
        top_sources = cursor.fetchall()
        
        print(f"\n📊 数据库统计:")
        print(f"   总记录数: {total_count}")
        print(f"   最新记录: {latest_date}")
        print(f"   主要来源:")
        for source, count in top_sources:
            percentage = (count / total_count) * 100 if total_count > 0 else 0
            print(f"     {source}: {count} 条 ({percentage:.1f}%)")
            
    except Exception as e:
        print(f"❌ 统计信息获取失败: {e}")

if __name__ == "__main__":
    sys.exit(main())