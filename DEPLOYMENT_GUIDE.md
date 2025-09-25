# TDX新闻爬虫系统 - GitHub部署指南

## 📋 系统概述

这是一个完整的新闻爬虫系统，包含以下组件：
- **爬虫程序**：自动抓取同花顺财经新闻
- **数据库**：SQLite存储新闻数据
- **API服务**：Flask API提供数据接口
- **前端网站**：实时显示新闻数据
- **GitHub Actions**：自动化部署和定时任务

## 🚀 部署到GitHub的详细步骤

### 步骤1：准备GitHub仓库

1. **创建新的GitHub仓库**
   - 访问 https://github.com/new
   - 仓库名称：`tdx-news-crawler`（或其他名称）
   - 选择公开或私有仓库
   - 勾选"Add a README file"

2. **克隆仓库到本地**
   ```bash
   git clone https://github.com/你的用户名/tdx-news-crawler.git
   cd tdx-news-crawler
   ```

### 步骤2：上传代码文件

将以下文件复制到仓库根目录：
- `tdx_all_news_crawler.py` - 主爬虫程序
- `github_crawler.py` - GitHub Actions专用爬虫
- `tdx_news_live.html` - 前端网站
- `requirements.txt` - Python依赖
- `.github/workflows/` - GitHub Actions工作流
- `README.md` - 项目说明

### 步骤3：设置GitHub Pages（可选）

1. 进入仓库设置 → Pages
2. 源选择：GitHub Actions
3. 保存设置

### 步骤4：配置GitHub Actions权限

1. 进入仓库设置 → Actions → General
2. 在"Workflow permissions"部分：
   - 选择"Read and write permissions"
   - 勾选"Allow GitHub Actions to create and approve pull requests"

### 步骤5：手动触发首次运行

1. 进入仓库 → Actions
2. 点击"TDX News Auto Crawler"工作流
3. 点击"Run workflow"手动触发

## ⚙️ GitHub Actions工作流说明

### 1. 自动爬虫工作流 (news-crawler.yml)
- **触发条件**：
  - 每15分钟自动运行（cron定时）
  - 代码推送时运行
  - 手动触发运行
- **功能**：
  - 运行爬虫获取最新新闻
  - 更新数据库文件
  - 自动提交数据变更
  - 生成数据文件作为artifact

### 2. 网站部署工作流 (deploy-pages.yml)
- **触发条件**：数据库文件更新时
- **功能**：自动部署网站到GitHub Pages

## 📊 数据文件说明

系统会生成以下数据文件：
- `tdx_all_news.db` - SQLite数据库（包含所有新闻）
- `tdx_all_news_export.csv` - CSV格式导出文件
- `latest_news.json` - 最新新闻的JSON接口

## 🔧 自定义配置

### 修改爬虫频率
编辑 `.github/workflows/news-crawler.yml`：
```yaml
schedule:
  - cron: '*/15 * * * *'  # 每15分钟
  # 可选频率：
  # '*/5 * * * *'   # 每5分钟
  # '0 * * * *'     # 每小时
  # '0 9 * * *'     # 每天9点
```

### 修改爬虫页面数量
编辑 `github_crawler.py`：
```python
# 修改爬取的页数
for page in range(1, 4):  # 当前爬取3页
```

## 🌐 访问网站

部署成功后，可以通过以下方式访问：
- **GitHub Pages地址**：`https://你的用户名.github.io/tdx-news-crawler`
- **原始数据文件**：在仓库的Releases或Actions artifacts中下载

## 🐛 故障排除

### 常见问题1：GitHub Actions运行失败
- 检查requirements.txt中的依赖是否正确
- 查看Actions日志中的具体错误信息
- 确保所有文件路径正确

### 常见问题2：数据库文件不更新
- 检查爬虫是否有网络连接问题
- 确认API端点是否可访问
- 查看爬虫日志输出

### 常见问题3：网站无法访问
- 检查GitHub Pages设置
- 确认index.html文件存在
- 查看部署工作流的日志

## 🔒 安全注意事项

1. **API密钥**：不要在代码中硬编码敏感信息
2. **访问频率**：避免过于频繁的请求
3. **数据存储**：定期清理旧数据避免仓库过大

## 📞 技术支持

如果遇到问题：
1. 查看GitHub Actions的运行日志
2. 检查仓库的Issues页面
3. 提交新的Issue描述问题

## 🎯 下一步优化建议

1. **数据可视化**：添加图表展示新闻趋势
2. **邮件通知**：重要新闻自动邮件提醒
3. **多数据源**：集成更多财经新闻源
4. **移动端适配**：优化手机浏览体验

---

**部署完成后的预期效果**：
- ✅ 每15分钟自动获取最新新闻
- ✅ 数据库文件自动更新并提交到GitHub
- ✅ 网站自动部署到GitHub Pages
- ✅ 可通过网页查看实时新闻数据
- ✅ 支持搜索和筛选功能