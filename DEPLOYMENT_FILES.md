# GitHub部署文件清单

## 📋 必须上传的核心文件

以下文件是系统运行所必需的，请确保全部上传到GitHub仓库：

### 1. 核心程序文件
- `tdx_all_news_crawler.py` - 主爬虫程序
- `github_crawler.py` - GitHub Actions专用爬虫
- `tdx_news_live.html` - 前端网站
- `requirements.txt` - Python依赖

### 2. GitHub Actions工作流
- `.github/workflows/news-crawler.yml` - 自动爬虫工作流
- `.github/workflows/deploy-pages.yml` - 网站部署工作流

### 3. 文档文件
- `README.md` - 项目说明
- `DEPLOYMENT_GUIDE.md` - 详细部署指南

## 📁 完整文件清单（可选）

以下文件可以上传以提供完整功能，但不是必需的：

### 测试和调试文件
- `deploy_check.py` - 部署检查脚本
- `advanced_api_test.py` - API测试脚本
- `db_query_tool.py` - 数据库查询工具
- `test_api.py` - API测试

### 历史开发文件（可不上传）
- `*.db` - 数据库文件（GitHub Actions会自动生成）
- `*.csv` - 导出文件（GitHub Actions会自动生成）
- `*.txt` - 测试响应文件
- `__pycache__/` - Python缓存目录
- 其他历史测试文件

## 🚀 最小部署方案

如果只想部署核心功能，只需上传以下文件：

```
tdx-news-crawler/
├── tdx_all_news_crawler.py
├── github_crawler.py
├── tdx_news_live.html
├── requirements.txt
├── .github/workflows/news-crawler.yml
├── .github/workflows/deploy-pages.yml
├── README.md
└── DEPLOYMENT_GUIDE.md
```

## 📝 部署步骤

### 步骤1：创建GitHub仓库
```bash
# 在GitHub上创建新仓库
# 仓库名称：tdx-news-crawler
# 描述：TDX新闻自动爬虫系统
# 选择公开或私有
```

### 步骤2：上传文件
```bash
# 克隆仓库
git clone https://github.com/你的用户名/tdx-news-crawler.git
cd tdx-news-crawler

# 复制核心文件到仓库
cp /path/to/newsonline/tdx_all_news_crawler.py .
cp /path/to/newsonline/github_crawler.py .
cp /path/to/newsonline/tdx_news_live.html .
cp /path/to/newsonline/requirements.txt .
cp -r /path/to/newsonline/.github .

# 提交并推送
git add .
git commit -m "初始提交：TDX新闻爬虫系统"
git push origin main
```

### 步骤3：配置GitHub Pages
1. 进入仓库设置 → Pages
2. 源选择：GitHub Actions
3. 保存设置

### 步骤4：配置Actions权限
1. 进入仓库设置 → Actions → General
2. 在"Workflow permissions"部分：
   - 选择"Read and write permissions"
   - 勾选"Allow GitHub Actions to create and approve pull requests"

### 步骤5：手动触发首次运行
1. 进入仓库 → Actions
2. 点击"TDX News Auto Crawler"工作流
3. 点击"Run workflow"手动触发

## 🔧 文件说明

### tdx_all_news_crawler.py
- 主爬虫程序，包含完整的爬虫逻辑
- 支持API服务模式和数据导出
- 包含数据库操作功能

### github_crawler.py
- GitHub Actions专用爬虫
- 优化了错误处理和日志输出
- 自动导出CSV格式数据

### tdx_news_live.html
- 响应式前端网站
- 支持搜索、筛选、自动刷新
- 适配GitHub Pages环境

### requirements.txt
- Python依赖包列表
- 确保GitHub Actions环境兼容性

## ⚠️ 注意事项

1. **不要上传数据库文件**：GitHub Actions会自动生成
2. **检查文件大小**：避免上传过大文件
3. **注意敏感信息**：不要在代码中硬编码API密钥
4. **测试工作流**：首次部署后手动触发测试

## 📞 故障排除

如果部署失败：
1. 检查GitHub Actions日志
2. 验证requirements.txt依赖
3. 确认文件路径正确
4. 检查GitHub Pages设置

## 🎯 成功标志

部署成功后应该看到：
- ✅ GitHub Actions工作流运行成功
- ✅ 数据库文件自动生成并提交
- ✅ 网站可通过GitHub Pages访问
- ✅ 每15分钟自动更新数据

---

**部署时间**：约10-15分钟  
**首次运行**：需要手动触发  
**持续运行**：7x24小时自动维护