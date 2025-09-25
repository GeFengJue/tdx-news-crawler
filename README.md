# TDX新闻爬虫系统

一个自动化的财经新闻爬虫系统，实时抓取同花顺要闻直播数据，并提供Web界面展示。

## ✨ 功能特性

- 🔄 **自动爬虫**：每15分钟自动获取最新新闻
- 💾 **数据存储**：SQLite数据库存储历史数据
- 🌐 **Web界面**：响应式设计，支持搜索筛选
- 📊 **数据导出**：支持CSV格式数据导出
- ⚡ **实时更新**：自动刷新保持数据最新
- 🚀 **云端部署**：GitHub Actions自动化运行

## 📁 项目结构

```
tdx-news-crawler/
├── .github/workflows/          # GitHub Actions工作流
│   ├── news-crawler.yml        # 自动爬虫工作流
│   └── deploy-pages.yml        # 网站部署工作流
├── tdx_all_news_crawler.py     # 主爬虫程序
├── github_crawler.py           # GitHub Actions专用爬虫
├── tdx_news_live.html          # 前端网站
├── requirements.txt            # Python依赖
├── tdx_all_news.db             # 新闻数据库（自动生成）
├── tdx_all_news_export.csv     # 数据导出文件（自动生成）
└── README.md                   # 项目说明
```

## 🛠️ 快速开始

### 本地运行

1. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

2. **运行爬虫**
   ```bash
   python tdx_all_news_crawler.py
   ```

3. **启动API服务**
   ```bash
   python tdx_all_news_crawler.py api
   ```

4. **打开网站**
   访问 `tdx_news_live.html` 查看新闻

### 云端部署

详细部署指南请查看 [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

## 📊 数据示例

系统爬取的数据包括：
- 新闻标题和摘要
- 发布时间和来源
- 相关股票代码和名称
- 重要程度标记

## 🔧 技术栈

- **后端**：Python + Flask + SQLite
- **前端**：HTML + CSS + JavaScript
- **部署**：GitHub Actions + GitHub Pages
- **爬虫**：Requests + 自定义会话管理

## 📈 自动化流程

1. **定时爬取**：GitHub Actions每15分钟运行爬虫
2. **数据更新**：自动提交数据库变更到仓库
3. **网站部署**：数据更新后自动部署网站
4. **持续运行**：7x24小时不间断服务

## 🌐 访问方式

部署成功后可通过以下方式访问：
- **GitHub Pages**：`https://用户名.github.io/tdx-news-crawler`
- **原始数据**：在仓库Actions中下载数据库文件

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进项目！

## 📄 许可证

本项目仅供学习和研究使用。

---

**最新状态**：🟢 系统运行正常  
**最后更新**：2025-09-25  
**数据量**：800+ 条新闻记录