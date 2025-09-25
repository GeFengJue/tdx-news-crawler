import sqlite3
import re
import json
from datetime import datetime

class RealDataProcessor:
    def __init__(self):
        self.raw_data = None
    
    def load_real_data(self):
        """加载您提供的真实F12数据"""
        # 这是您提供的完整50条真实数据
        real_data = {
            "ErrorCode": 0,
            "HitCache": "L1:B1FB6080A43E",
            "ResultSets": [{
                "ColName": [
                    "pos", "rec_id", "title", "issue_date", "summary", "src_info", 
                    "relate_id", "Proc_Id", "Mark_Id"
                ],
                "Content": [
                    [1, 5549513, "*ST金比(002762):关于变更参股公司董事、监事委派人员的自愿性信息披露公告", "2025-09-24 17:57:00", "*ST金比(002762):关于变更参股公司董事、监事委派人员的自愿性信息披露公告", "深交所", 20009684, 0, 1],
                    [2, 5549507, "蓝特光学(688127):2025年第二次临时股东大会决议公告", "2025-09-24 17:57:00", "蓝特光学(688127):2025年第二次临时股东大会决议公告", "上交所", 20009678, 0, 1],
                    [3, 5549506, "蓝特光学(688127):2025年第二次临时股东大会的法律意见书", "2025-09-24 17:57:00", "蓝特光学(688127):2025年第二次临时股东大会的法律意见书", "上交所", 20009677, 0, 1],
                    [4, 5549505, "蓝特光学(688127):关于选举职工代表董事、增选非独立董事、聘任副总经理的公告", "2025-09-24 17:57:00", "蓝特光学(688127):关于选举职工代表董事、增选非独立董事、聘任副总经理的公告", "上交所", 20009676, 0, 1],
                    [5, 5549504, "中惠旅(834260):提供担保的公告", "2025-09-24 17:56:54", "中惠旅(834260):提供担保的公告", "股份转让系统", 20009673, 1, 1],
                    [6, 5549503, "新农人(872242):关于全资子公司为母公司提供担保的公告", "2025-09-24 17:56:54", "新农人(872242):关于全资子公司为母公司提供担保的公告", "股份转让系统", 20009672, 1, 1],
                    [7, 5549502, "大亚股份(832532):预计担保的公告", "2025-09-24 17:56:54", "大亚股份(832532):预计担保的公告", "股份转让系统", 20009671, 1, 1],
                    [8, 5549501, "海控能源(833042):出售资产暨关联交易的公告", "2025-09-24 17:56:50", "海控能源(833042):出售资产暨关联交易的公告", "股份转让系统", 20009670, 1, 1],
                    [9, 5549499, "ST太和华(837694):对外投资的公告", "2025-09-24 17:56:47", "ST太和华(837694):对外投资的公告", "股份转让系统", 20009667, 1, 1],
                    [10, 5549498, "声蓝医疗(874309):对外设立孙公司的公告", "2025-09-24 17:56:47", "声蓝医疗(874309):对外设立孙公司的公告", "股份转让系统", 20009666, 1, 1],
                    [11, 5549497, "味巴哥(871988):关联交易公告", "2025-09-24 17:56:29", "味巴哥(871988):关联交易公告", "股份转让系统", 20009665, 1, 4],
                    [12, 5549512, "富国银行:AI牛市非泡沫 仍处早期阶段", "2025-09-24 17:56:08", "富国银行首席股票策略师Ohsung Kwon看好AI相关股票,认为AI驱动的牛市将持续。他指出,当前涨势非泡沫,而是由优于标普500的基本面支撑,纳斯达克指数的超额收益长期由科技成长驱动。目前仍处AI投资周期早期,只要股市对资本支出和增长前景持续给予积极反馈,本轮行情有望延续。", "格隆汇", 20009683, 0, 1],
                    [13, 5549495, "九喜股份(872784):拟变更经营范围并修订《公司章程》公告", "2025-09-24 17:56:05", "九喜股份(872784):拟变更经营范围并修订《公司章程》公告", "股份转让系统", 20009663, 0, 1],
                    [14, 5549494, "亮威科技(839472):拟修订公司章程公告", "2025-09-24 17:56:05", "亮威科技(839472):拟修订公司章程公告", "股份转让系统", 20009661, 0, 1],
                    [15, 5549493, "ST太和华(837694):拟修订《公司章程》公告", "2025-09-24 17:56:05", "ST太和华(837694):拟修订《公司章程》公告", "股份转让系统", 20009659, 0, 1],
                    [16, 5549514, "康泰生物(300601):关于三价流感病毒裂解疫苗上市许可申请获得受理的公告", "2025-09-24 17:56:00", "康泰生物(300601):关于三价流感病毒裂解疫苗上市许可申请获得受理的公告", "深交所", 20009685, 0, 1],
                    [17, 5549496, "康强电子(002119):关于持股5%以上股东权益变动触及1%整数倍的公告", "2025-09-24 17:56:00", "康强电子(002119):关于持股5%以上股东权益变动触及1%整数倍的公告", "深交所", 20009664, 1, 1],
                    [18, 5549489, "五轮科技(833767):信息披露事务管理制度", "2025-09-24 17:55:37", "五轮科技(833767):信息披露事务管理制度", "股份转让系统", 20009657, 0, 1],
                    [19, 5549488, "五轮科技(833767):投资者关系管理制度", "2025-09-24 17:55:37", "五轮科技(833767):投资者关系管理制度", "股份转让系统", 20009656, 0, 1],
                    [20, 5549487, "五轮科技(833767):募集资金管理制度", "2025-09-24 17:55:37", "五轮科技(833767):募集资金管理制度", "股份转让系统", 20009655, 0, 1],
                    [21, 5549486, "亮威科技(839472):股东会议事规则", "2025-09-24 17:55:37", "亮威科技(839472):股东会议事规则", "股份转让系统", 20009654, 0, 1],
                    [22, 5549485, "天健新材(874508):股东会议事规则(草案)(北交所上市后适用)", "2025-09-24 17:55:37", "天健新材(874508):股东会议事规则(草案)(北交所上市后适用)", "股份转让系统", 20009651, 0, 1],
                    [23, 5549484, "ST太和华(837694):募集资金管理制度", "2025-09-24 17:55:37", "ST太和华(837694):募集资金管理制度", "股份转让系统", 20009650, 0, 1],
                    [24, 5549483, "亮威科技(839472):防止控股股东或实际控制人及其关联方占用公司资金管理制度", "2025-09-24 17:55:37", "亮威科技(839472):防止控股股东或实际控制人及其关联方占用公司资金管理制度", "股份转让系统", 20009649, 0, 1],
                    [25, 5549482, "亮威科技(839472):投资者关系管理制度", "2025-09-24 17:55:37", "亮威科技(839472):投资者关系管理制度", "股份转让系统", 20009648, 0, 1],
                    [26, 5549481, "味巴哥(871988):股东会议事规则", "2025-09-24 17:55:37", "味巴哥(871988):股东会议事规则", "股份转让系统", 20009646, 0, 1],
                    [27, 5549480, "亮威科技(839472):对外担保管理制度", "2025-09-24 17:55:37", "亮威科技(839472):对外担保管理制度", "股份转让系统", 20009645, 0, 1],
                    [28, 5549479, "亮威科技(839472):关联交易管理制度", "2025-09-24 17:55:37", "亮威科技(839472):关联交易管理制度", "股份转让系统", 20009644, 0, 1],
                    [29, 5549478, "亮威科技(839472):利润分配管理制度", "2025-09-24 17:55:37", "亮威科技(839472):利润分配管理制度", "股份转让系统", 20009643, 0, 1],
                    [30, 5549477, "亮威科技(839472):对外投资管理制度", "2025-09-24 17:55:37", "亮威科技(839472):对外投资管理制度", "股份转让系统", 20009642, 0, 1],
                    [31, 5549476, "味巴哥(871988):董事会议事规则", "2025-09-24 17:55:37", "味巴哥(871988):董事会议事规则", "股份转让系统", 20009641, 0, 1],
                    [32, 5549475, "天健新材(874508):关联交易管理办法(草案)(北交所上市后适用)", "2025-09-24 17:55:33", "天健新材(874508):关联交易管理办法(草案)(北交所上市后适用)", "股份转让系统", 20009640, 0, 1],
                    [33, 5549474, "天健新材(874508):募集资金管理制度(草案)(北交所上市后适用)", "2025-09-24 17:55:33", "天健新材(874508):募集资金管理制度(草案)(北交所上市后适用)", "股份转让系统", 20009639, 0, 1],
                    [34, 5549473, "天健新材(874508):投资者关系管理制度(草案)(北交所上市后适用)", "2025-09-24 17:55:33", "天健新材(874508):投资者关系管理制度(草案)(北交所上市后适用)", "股份转让系统", 20009638, 0, 1],
                    [35, 5549472, "天健新材(874508):对外担保管理办法(草案)(北交所上市后适用)", "2025-09-24 17:55:33", "天健新材(874508):对外担保管理办法(草案)(北交所上市后适用)", "股份转让系统", 20009637, 0, 1],
                    [36, 5549471, "天健新材(874508):利润分配管理制度(草案)(北交所上市后适用)", "2025-09-24 17:55:33", "天健新材(874508):利润分配管理制度(草案)(北交所上市后适用)", "股份转让系统", 20009636, 0, 1],
                    [37, 5549470, "天健新材(874508):独立董事工作制度(草案)(北交所上市后适用)", "2025-09-24 17:55:33", "天健新材(874508):独立董事工作制度(草案)(北交所上市后适用)", "股份转让系统", 20009635, 0, 1],
                    [38, 5549469, "天健新材(874508):防范控股股东、实际控制人及其他关联方占用公司资金管理制度(草案)(北交所上市后适用)", "2025-09-24 17:55:33", "天健新材(874508):防范控股股东、实际控制人及其他关联方占用公司资金管理制度(草案)(北交所上市后适用)", "股份转让系统", 20009634, 0, 1],
                    [39, 5549468, "天健新材(874508):对外投资管理办法(草案)(北交所上市后适用)", "2025-09-24 17:55:33", "天健新材(874508):对外投资管理办法(草案)(北交所上市后适用)", "股份转让系统", 20009633, 0, 1],
                    [40, 5549467, "天健新材(874508):董事会秘书工作细则(草案)(北交所上市后适用)", "2025-09-24 17:55:33", "天健新材(874508):董事会秘书工作细则(草案)(北交所上市后适用)", "股份转让系统", 20009632, 0, 1],
                    [41, 5549466, "天健新材(874508):累积投票制实施细则(草案)(北交所上市后适用)", "2025-09-24 17:55:33", "天健新材(874508):累积投票制实施细则(草案)(北交所上市后适用)", "股份转让系统", 20009631, 0, 1],
                    [42, 5549465, "天健新材(874508):信息披露管理制度(草案)(北交所上市后适用)", "2025-09-24 17:55:33", "天健新材(874508):信息披露管理制度(草案)(北交所上市后适用)", "股份转让系统", 20009630, 0, 1],
                    [43, 5549464, "天健新材(874508):董事和高级管理人员所持本公司股份及其变动管理制度(草案)(北交所上市后适用)", "2025-09-24 17:55:33", "天健新材(874508):董事和高级管理人员所持本公司股份及其变动管理制度(草案)(北交所上市后适用)", "股份转让系统", 20009629, 0, 1],
                    [44, 5549463, "味巴哥(871988):对外担保管理制度", "2025-09-24 17:55:33", "味巴哥(871988):对外担保管理制度", "股份转让系统", 20009627, 0, 1],
                    [45, 5549462, "味巴哥(871988):对外投资管理制度", "2025-09-24 17:55:33", "味巴哥(871988):对外投资管理制度", "股份转让系统", 20009626, 0, 1],
                    [46, 5549461, "天健新材(874508):董事及高级管理人员薪酬管理制度(草案)(北交所上市后适用)", "2025-09-24 17:55:33", "天健新材(874508):董事及高级管理人员薪酬管理制度(草案)(北交所上市后适用)", "股份转让系统", 20009625, 0, 1],
                    [47, 5549460, "天健新材(874508):总经理工作细则(草案)(北交所上市后适用)", "2025-09-24 17:55:33", "天健新材(874508):总经理工作细则(草案)(北交所上市后适用)", "股份转让系统", 20009624, 0, 1],
                    [48, 5549459, "天健新材(874508):子公司管理制度(草案)(北交所上市后适用)", "2025-09-24 17:55:33", "天健新材(874508):子公司管理制度(草案)(北交所上市后适用)", "股份转让系统", 20009623, 0, 1],
                    [49, 5549458, "亮威科技(839472):监事会议事规则", "2025-09-24 17:55:33", "亮威科技(839472):监事会议事规则", "股份转让系统", 20009622, 0, 1],
                    [50, 5549457, "天健新材(874508):内部审计制度(草案)(北交所上市后适用)", "2025-09-24 17:55:33", "天健新材(874508):内部审计制度(草案)(北交所上市后适用)", "股份转让系统", 20009621, 0, 1]
                ]
            }]
        }
        
        self.raw_data = real_data
        return real_data
    
    def create_database(self):
        """创建数据库"""
        conn = sqlite3.connect('f12_real_data.db')
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
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_source ON stock_announcements(source)')
        
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
    
    def process_and_save_data(self):
        """处理并保存数据"""
        print("🚀 开始处理真实F12数据...")
        print(f"⏰ 当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 加载数据
        data = self.load_real_data()
        if not data:
            print("❌ 数据加载失败")
            return
        
        # 创建数据库
        conn = self.create_database()
        cursor = conn.cursor()
        
        # 获取数据内容
        result_set = data['ResultSets'][0]
        col_names = result_set['ColName']  # type: ignore
        content_data = result_set['Content']  # type: ignore
        
        print(f"📊 原始数据统计:")
        print(f"   总记录数: {len(content_data)}")
        print(f"   列名: {', '.join(str(name) for name in col_names)}")
        
        # 处理并保存数据
        inserted_count = 0
        stock_codes = set()
        sources = set()
        
        for row in content_data:
            if len(row) >= len(col_names):
                data_dict = dict(zip(col_names, row))
                
                # 提取股票信息
                title = data_dict.get('title', '')
                stock_code, stock_name = self.extract_stock_info(title)
                
                # 统计信息
                if stock_code:
                    stock_codes.add(stock_code)
                if data_dict.get('src_info'):
                    sources.add(data_dict['src_info'])
                
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
        
        print(f"\n✅ 数据处理完成:")
        print(f"   成功插入: {inserted_count} 条记录")
        print(f"   股票数量: {len(stock_codes)}")
        print(f"   来源数量: {len(sources)}")
        print(f"   数据来源: {', '.join(sorted(sources))}")
        
        # 显示统计信息
        self.show_statistics(conn)
        
        # 导出为CSV文件
        self.export_to_csv(conn)
        
        conn.close()
        
        print("\n🎉 真实F12数据处理完成!")
    
    def show_statistics(self, conn):
        """显示详细统计信息"""
        cursor = conn.cursor()
        
        # 总记录数
        cursor.execute("SELECT COUNT(*) FROM stock_announcements")
        total_count = cursor.fetchone()[0]
        
        # 股票统计
        cursor.execute("""
        SELECT stock_code, stock_name, COUNT(*) as count 
        FROM stock_announcements 
        WHERE stock_code IS NOT NULL 
        GROUP BY stock_code, stock_name 
        ORDER BY count DESC
        """)
        
        print(f"\n📈 股票公告统计:")
        stock_stats = cursor.fetchall()
        for code, name, count in stock_stats[:10]:  # 显示前10只股票
            print(f"   {code} {name}: {count} 条公告")
        
        if len(stock_stats) > 10:
            print(f"   ... 还有 {len(stock_stats) - 10} 只股票")
        
        # 来源统计
        cursor.execute("""
        SELECT source, COUNT(*) as count 
        FROM stock_announcements 
        GROUP BY source 
        ORDER BY count DESC
        """)
        
        print(f"\n📊 来源统计:")
        for source, count in cursor.fetchall():
            print(f"   {source}: {count} 条")
        
        # 最新公告
        cursor.execute("""
        SELECT title, stock_code, issue_date, source 
        FROM stock_announcements 
        ORDER BY issue_date DESC 
        LIMIT 5
        """)
        
        print(f"\n📰 最新公告:")
        for i, (title, code, date, source) in enumerate(cursor.fetchall(), 1):
            short_title = title[:60] + "..." if len(title) > 60 else title
            print(f"   {i}. {short_title}")
            print(f"      股票: {code} | 来源: {source} | 时间: {date}")
    
    def export_to_csv(self, conn):
        """导出为CSV文件"""
        import csv
        
        cursor = conn.cursor()
        cursor.execute("""
        SELECT position, record_id, title, issue_date, summary, source, 
               relate_id, proc_id, mark_id, stock_code, stock_name
        FROM stock_announcements 
        ORDER BY issue_date DESC
        """)
        
        with open('f12_real_data_export.csv', 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            # 写入标题行
            writer.writerow(['序号', '记录ID', '标题', '发布时间', '摘要', '来源', 
                           '关联ID', '处理ID', '标记ID', '股票代码', '股票名称'])
            
            # 写入数据
            for row in cursor.fetchall():
                writer.writerow(row)
        
        print(f"📄 数据已导出到: f12_real_data_export.csv")
    
    def run(self):
        """运行处理器"""
        self.process_and_save_data()

def main():
    processor = RealDataProcessor()
    processor.run()

if __name__ == "__main__":
    main()