import requests
import json
import sqlite3
import re
from datetime import datetime, timedelta
import time
from flask import Flask, jsonify, request
from flask_cors import CORS

class TDXAllNewsCrawler:
    def __init__(self):
        self.base_url = "http://fast1.tdx.com.cn:7615"
        self.session = requests.Session()
        
        # 设置精确的请求头
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
    
    def fetch_page_data(self, page=1, page_size=50):
        """获取指定页面的数据"""
        try:
            # 使用当前日期作为查询条件（基于您提供的成功格式）
            current_date = datetime.now().strftime("%Y-%m-%d 00:00:00")
            
            api_url = f"{self.base_url}/TQLEX?Entry=CWServ.tdxzb_zxts_ywbb"
            
            # 构建负载数据（使用您提供的成功参数格式）
            payload_data = {
                "CallName": "tdxzb_zxts_ywbb",
                "Params": [
                    current_date,  # 当前日期
                    "",           # 空字符串
                    page,         # 页码
                    page_size,    # 每页数量
                    "0"           # 其他参数
                ],
                "secuparse": True,
                "parsefld": "summary",
                "tdxPageID": "_UrlEncode"
            }
            
            json_payload = json.dumps(payload_data, ensure_ascii=False)
            
            print(f"📄 获取第{page}页数据...")
            
            response = self.session.post(
                api_url,
                data=json_payload,
                headers=self.headers,
                timeout=15
            )
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if data.get('ErrorCode') == 0:
                        result_sets = data.get('ResultSets', [])
                        if result_sets:
                            content = result_sets[0].get('Content', [])
                            print(f"✅ 第{page}页获取到 {len(content)} 条数据")
                            return data
                        else:
                            print(f"⚠️ 第{page}页无数据")
                    else:
                        print(f"❌ 第{page}页API错误: {data.get('ErrorInfo')}")
                except json.JSONDecodeError:
                    print(f"❌ 第{page}页JSON解析失败")
            else:
                print(f"❌ 第{page}页HTTP错误: {response.status_code}")
                
        except Exception as e:
            print(f"❌ 第{page}页请求失败: {e}")
        
        return None
    
    def fetch_all_news(self, max_pages=10, page_size=50):
        """获取所有新闻数据"""
        print("🔄 开始获取所有新闻数据...")
        
        all_data = []
        total_records = 0
        
        for page in range(1, max_pages + 1):
            page_data = self.fetch_page_data(page, page_size)
            if page_data:
                result_sets = page_data.get('ResultSets', [])
                if result_sets:
                    content = result_sets[0].get('Content', [])
                    if len(content) > 0:
                        all_data.append(page_data)
                        total_records += len(content)
                        print(f"📊 累计获取: {total_records} 条记录")
                        
                        # 如果当前页数据不足一页，说明没有更多数据了
                        if len(content) < page_size:
                            print("📄 已获取所有可用数据")
                            break
                    else:
                        print("📄 无更多数据，停止获取")
                        break
                else:
                    print("📄 无结果集，停止获取")
                    break
            else:
                print("❌ 获取数据失败，停止获取")
                break
            
            # 添加延迟避免请求过快
            time.sleep(1)
        
        print(f"🎉 获取完成，共 {len(all_data)} 页，{total_records} 条记录")
        return all_data
    
    def create_database(self, db_name='tdx_all_news.db'):
        """创建数据库"""
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS all_stock_news (
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
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_record_id ON all_stock_news(record_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_stock_code ON all_stock_news(stock_code)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_issue_date ON all_stock_news(issue_date)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_source ON all_stock_news(source)')
        
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
    
    def save_all_data(self, conn, all_data):
        """保存所有数据到数据库"""
        if not all_data:
            print("❌ 无数据可保存")
            return 0
        
        cursor = conn.cursor()
        total_inserted = 0
        
        for page_data in all_data:
            if 'ResultSets' not in page_data or len(page_data['ResultSets']) == 0:
                continue
                
            result_set = page_data['ResultSets'][0]
            col_names = result_set['ColName']
            content_data = result_set['Content']
            
            page_inserted = 0
            for row in content_data:
                if len(row) >= len(col_names):
                    data_dict = dict(zip(col_names, row))
                    
                    # 提取股票信息
                    title = data_dict.get('title', '')
                    stock_code, stock_name = self.extract_stock_info(title)
                    
                    try:
                        cursor.execute('''
                        INSERT OR IGNORE INTO all_stock_news 
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
                            page_inserted += 1
                            total_inserted += 1
                        
                    except Exception as e:
                        print(f"❌ 插入数据失败: {e}")
            
            print(f"💾 第{all_data.index(page_data) + 1}页保存: {page_inserted} 条记录")
        
        conn.commit()
        return total_inserted
    
    def display_top_news(self, conn, limit=50):
        """显示前N条新闻"""
        cursor = conn.cursor()
        
        print(f"\n🔥 前{limit}条最新公告:")
        print("=" * 80)
        
        cursor.execute('''
        SELECT title, stock_code, stock_name, issue_date, source, summary
        FROM all_stock_news 
        ORDER BY issue_date DESC 
        LIMIT ?
        ''', (limit,))
        
        news_list = cursor.fetchall()
        
        for i, (title, code, name, date, source, summary) in enumerate(news_list, 1):
            print(f"{i:2d}. {title}")
            if code:
                print(f"    股票: {code} {name}")
            else:
                print(f"    新闻类型")
            print(f"    时间: {date} | 来源: {source}")
            if summary and len(summary) > 100:
                short_summary = summary[:100] + "..."
                print(f"    摘要: {short_summary}")
            print("-" * 80)
        
        return news_list
    
    def show_statistics(self, conn):
        """显示详细统计信息"""
        cursor = conn.cursor()
        
        # 总记录数
        cursor.execute("SELECT COUNT(*) FROM all_stock_news")
        total_count = cursor.fetchone()[0]
        
        # 股票统计
        cursor.execute("SELECT COUNT(DISTINCT stock_code) FROM all_stock_news WHERE stock_code IS NOT NULL")
        stock_count = cursor.fetchone()[0]
        
        # 来源统计
        cursor.execute("SELECT source, COUNT(*) FROM all_stock_news GROUP BY source ORDER BY COUNT(*) DESC")
        sources = cursor.fetchall()
        
        # 日期范围
        cursor.execute("SELECT MIN(issue_date), MAX(issue_date) FROM all_stock_news")
        min_date, max_date = cursor.fetchone()
        
        print(f"\n📊 数据库统计:")
        print(f"   总记录数: {total_count}")
        print(f"   股票数量: {stock_count}")
        print(f"   时间范围: {min_date} 到 {max_date}")
        
        print(f"\n📰 来源分布:")
        for source, count in sources:
            percentage = (count / total_count) * 100
            print(f"   {source}: {count} 条 ({percentage:.1f}%)")
        
        # 热门股票
        cursor.execute('''
        SELECT stock_code, stock_name, COUNT(*) as count 
        FROM all_stock_news 
        WHERE stock_code IS NOT NULL 
        GROUP BY stock_code, stock_name 
        ORDER BY count DESC 
        LIMIT 10
        ''')
        
        print(f"\n🏆 热门股票公告排行:")
        for code, name, count in cursor.fetchall():
            print(f"   {code} {name}: {count} 条公告")
    
    def run(self):
        """运行爬虫"""
        print("🚀 启动同花顺全量新闻爬虫...")
        print(f"⏰ 当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 初始化会话
        if not self.init_session():
            return
        
        # 创建数据库
        conn = self.create_database('tdx_all_news.db')
        print("✅ 数据库准备就绪")
        
        # 获取所有新闻数据
        all_data = self.fetch_all_news(max_pages=5, page_size=50)  # 获取5页，每页50条
        
        if all_data:
            # 保存数据
            saved_count = self.save_all_data(conn, all_data)
            print(f"✅ 成功保存 {saved_count} 条数据到数据库")
            
            # 显示统计信息
            self.show_statistics(conn)
            
            # 显示前50条新闻
            self.display_top_news(conn, 50)
            
            # 导出为CSV
            self.export_to_csv(conn)
        else:
            print("❌ 未能获取到数据")
        
        conn.close()
        print("\n🎉 全量新闻爬取完成!")
    
    def export_to_csv(self, conn):
        """导出为CSV文件"""
        import csv
        
        cursor = conn.cursor()
        cursor.execute('''
        SELECT position, record_id, title, issue_date, summary, source, 
               stock_code, stock_name, relate_id, proc_id, mark_id
        FROM all_stock_news 
        ORDER BY issue_date DESC
        ''')
        
        with open('tdx_all_news_export.csv', 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            # 写入标题行
            writer.writerow(['序号', '记录ID', '标题', '发布时间', '摘要', '来源', 
                           '股票代码', '股票名称', '关联ID', '处理ID', '标记ID'])
            
            # 写入数据
            for row in cursor.fetchall():
                writer.writerow(row)
        
        print(f"📄 数据已导出到: tdx_all_news_export.csv")

class TDXNewsAPI:
    def __init__(self, db_name='tdx_all_news.db'):
        self.db_name = db_name
        self.app = Flask(__name__)
        CORS(self.app)  # 启用CORS支持
        self.setup_routes()
    
    def get_db_connection(self):
        """获取数据库连接"""
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        return conn
    
    def setup_routes(self):
        """设置API路由"""
        
        @self.app.route('/api/news', methods=['GET'])
        def get_all_news():
            """获取所有新闻"""
            page = request.args.get('page', 1, type=int)
            limit = request.args.get('limit', 50, type=int)
            offset = (page - 1) * limit
            
            conn = self.get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT COUNT(*) FROM all_stock_news')
            total = cursor.fetchone()[0]
            
            cursor.execute('''
            SELECT * FROM all_stock_news 
            ORDER BY issue_date DESC 
            LIMIT ? OFFSET ?
            ''', (limit, offset))
            
            news_list = [dict(row) for row in cursor.fetchall()]
            conn.close()
            
            return jsonify({
                'success': True,
                'total': total,
                'page': page,
                'limit': limit,
                'data': news_list
            })
        
        @self.app.route('/api/news/<int:news_id>', methods=['GET'])
        def get_news_by_id(news_id):
            """根据ID获取新闻详情"""
            conn = self.get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM all_stock_news WHERE id = ?', (news_id,))
            news = cursor.fetchone()
            conn.close()
            
            if news:
                return jsonify({
                    'success': True,
                    'data': dict(news)
                })
            else:
                return jsonify({
                    'success': False,
                    'message': '新闻不存在'
                }), 404
        
        @self.app.route('/api/news/search', methods=['GET'])
        def search_news():
            """搜索新闻"""
            keyword = request.args.get('q', '')
            page = request.args.get('page', 1, type=int)
            limit = request.args.get('limit', 50, type=int)
            offset = (page - 1) * limit
            
            if not keyword:
                return jsonify({
                    'success': False,
                    'message': '请输入搜索关键词'
                }), 400
            
            conn = self.get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
            SELECT COUNT(*) FROM all_stock_news 
            WHERE title LIKE ? OR summary LIKE ?
            ''', (f'%{keyword}%', f'%{keyword}%'))
            total = cursor.fetchone()[0]
            
            cursor.execute('''
            SELECT * FROM all_stock_news 
            WHERE title LIKE ? OR summary LIKE ?
            ORDER BY issue_date DESC 
            LIMIT ? OFFSET ?
            ''', (f'%{keyword}%', f'%{keyword}%', limit, offset))
            
            news_list = [dict(row) for row in cursor.fetchall()]
            conn.close()
            
            return jsonify({
                'success': True,
                'total': total,
                'page': page,
                'limit': limit,
                'keyword': keyword,
                'data': news_list
            })
        
        @self.app.route('/api/news/stocks', methods=['GET'])
        def get_stock_news():
            """获取股票相关新闻"""
            stock_code = request.args.get('code', '')
            page = request.args.get('page', 1, type=int)
            limit = request.args.get('limit', 50, type=int)
            offset = (page - 1) * limit
            
            if not stock_code:
                return jsonify({
                    'success': False,
                    'message': '请输入股票代码'
                }), 400
            
            conn = self.get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT COUNT(*) FROM all_stock_news WHERE stock_code = ?', (stock_code,))
            total = cursor.fetchone()[0]
            
            cursor.execute('''
            SELECT * FROM all_stock_news 
            WHERE stock_code = ?
            ORDER BY issue_date DESC 
            LIMIT ? OFFSET ?
            ''', (stock_code, limit, offset))
            
            news_list = [dict(row) for row in cursor.fetchall()]
            conn.close()
            
            return jsonify({
                'success': True,
                'total': total,
                'page': page,
                'limit': limit,
                'stock_code': stock_code,
                'data': news_list
            })
        
        @self.app.route('/api/news/sources', methods=['GET'])
        def get_sources():
            """获取新闻来源统计"""
            conn = self.get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
            SELECT source, COUNT(*) as count 
            FROM all_stock_news 
            GROUP BY source 
            ORDER BY count DESC
            ''')
            
            sources = [{'source': row[0], 'count': row[1]} for row in cursor.fetchall()]
            conn.close()
            
            return jsonify({
                'success': True,
                'data': sources
            })
        
        @self.app.route('/api/news/statistics', methods=['GET'])
        def get_statistics():
            """获取统计信息"""
            conn = self.get_db_connection()
            cursor = conn.cursor()
            
            # 总记录数
            cursor.execute("SELECT COUNT(*) FROM all_stock_news")
            total_count = cursor.fetchone()[0]
            
            # 股票数量
            cursor.execute("SELECT COUNT(DISTINCT stock_code) FROM all_stock_news WHERE stock_code IS NOT NULL")
            stock_count = cursor.fetchone()[0]
            
            # 日期范围
            cursor.execute("SELECT MIN(issue_date), MAX(issue_date) FROM all_stock_news")
            min_date, max_date = cursor.fetchone()
            
            # 热门股票
            cursor.execute('''
            SELECT stock_code, stock_name, COUNT(*) as count 
            FROM all_stock_news 
            WHERE stock_code IS NOT NULL 
            GROUP BY stock_code, stock_name 
            ORDER BY count DESC 
            LIMIT 10
            ''')
            
            hot_stocks = [{'code': row[0], 'name': row[1], 'count': row[2]} for row in cursor.fetchall()]
            
            conn.close()
            
            return jsonify({
                'success': True,
                'data': {
                    'total_count': total_count,
                    'stock_count': stock_count,
                    'date_range': {
                        'min': min_date,
                        'max': max_date
                    },
                    'hot_stocks': hot_stocks
                }
            })
        
        @self.app.route('/api/health', methods=['GET'])
        def health_check():
            """健康检查"""
            return jsonify({
                'success': True,
                'message': 'API服务运行正常',
                'timestamp': datetime.now().isoformat()
            })
    
    def run_api(self, host='127.0.0.1', port=5000, debug=False):
        """启动API服务"""
        print(f"🚀 启动新闻API服务: http://{host}:{port}")
        print("📋 可用接口:")
        print("   GET /api/news - 获取所有新闻")
        print("   GET /api/news/<id> - 根据ID获取新闻详情")
        print("   GET /api/news/search?q=<keyword> - 搜索新闻")
        print("   GET /api/news/stocks?code=<stock_code> - 获取股票相关新闻")
        print("   GET /api/news/sources - 获取新闻来源统计")
        print("   GET /api/news/statistics - 获取统计信息")
        print("   GET /api/health - 健康检查")
        
        self.app.run(host=host, port=port, debug=debug)

import threading
import schedule
import time

def auto_crawl_job():
    """自动爬虫任务"""
    print(f"🔄 [{datetime.now().strftime('%H:%M:%S')}] 开始自动爬取新闻数据...")
    crawler = TDXAllNewsCrawler()
    
    # 初始化会话
    if not crawler.init_session():
        print("❌ 会话初始化失败")
        return
    
    # 创建数据库连接
    conn = crawler.create_database('tdx_all_news.db')
    
    # 获取新闻数据（只获取最新的一页数据，避免重复）
    page_data = crawler.fetch_page_data(page=1, page_size=50)
    
    if page_data:
        # 保存数据
        saved_count = crawler.save_all_data(conn, [page_data])
        print(f"✅ 自动爬取完成，新增 {saved_count} 条数据")
        
        # 显示最新统计
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM all_stock_news')
        total_count = cursor.fetchone()[0]
        cursor.execute('SELECT MAX(issue_date) FROM all_stock_news')
        latest_date = cursor.fetchone()[0]
        print(f"📊 数据库总计: {total_count} 条记录，最新时间: {latest_date}")
    else:
        print("❌ 自动爬取失败")
    
    conn.close()

def run_auto_crawler():
    """运行自动爬虫调度器"""
    print("🤖 启动自动爬虫调度器...")
    print("⏰ 爬虫将每分钟自动运行一次")
    
    # 立即执行一次
    auto_crawl_job()
    
    # 设置每分钟执行一次
    schedule.every(1).minutes.do(auto_crawl_job)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

def main():
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == 'api':
            # 启动API服务
            api = TDXNewsAPI()
            api.run_api()
        elif sys.argv[1] == 'auto':
            # 启动自动爬虫
            run_auto_crawler()
        elif sys.argv[1] == 'crawl':
            # 单次爬虫运行
            crawler = TDXAllNewsCrawler()
            crawler.run()
        else:
            print("用法:")
            print("  python tdx_all_news_crawler.py api     - 启动API服务")
            print("  python tdx_all_news_crawler.py auto    - 启动自动爬虫")
            print("  python tdx_all_news_crawler.py crawl   - 单次爬虫运行")
    else:
        # 默认运行单次爬虫
        crawler = TDXAllNewsCrawler()
        crawler.run()

if __name__ == "__main__":
    main()