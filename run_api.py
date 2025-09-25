#!/usr/bin/env python3
"""
同花顺新闻API启动脚本
"""

from tdx_all_news_crawler import TDXNewsAPI

def main():
    """启动API服务"""
    print("=" * 60)
    print("📰 同花顺新闻API服务")
    print("=" * 60)
    
    # 创建API实例
    api = TDXNewsAPI('tdx_all_news.db')
    
    # 启动API服务
    api.run_api(host='0.0.0.0', port=5000, debug=True)

if __name__ == "__main__":
    main()