#!/usr/bin/env python3
"""
部署前检查脚本
验证所有必要的文件和配置是否正确
"""

import os
import sys

def check_files():
    """检查必要的文件是否存在"""
    required_files = [
        'tdx_all_news_crawler.py',
        'github_crawler.py',
        'tdx_news_live.html',
        'requirements.txt',
        '.github/workflows/news-crawler.yml',
        '.github/workflows/deploy-pages.yml',
        'README.md',
        'DEPLOYMENT_GUIDE.md'
    ]
    
    print("🔍 检查必要文件...")
    missing_files = []
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - 文件缺失")
            missing_files.append(file_path)
    
    return missing_files

def check_requirements():
    """检查requirements.txt内容"""
    print("\n🔍 检查依赖配置...")
    
    try:
        with open('requirements.txt', 'r', encoding='utf-8') as f:
            content = f.read()
        
        required_packages = [
            'requests>=2.28.0',
            'flask>=2.2.0',
            'flask-cors>=4.0.0',
            'schedule>=1.2.0',
            'pandas>=1.5.0'
        ]
        
        for package in required_packages:
            if package.split('>=')[0] in content:
                print(f"✅ {package}")
            else:
                print(f"⚠️  {package} - 可能缺失")
                
    except Exception as e:
        print(f"❌ 无法读取requirements.txt: {e}")

def check_workflows():
    """检查GitHub Actions工作流配置"""
    print("\n🔍 检查工作流配置...")
    
    workflow_files = [
        '.github/workflows/news-crawler.yml',
        '.github/workflows/deploy-pages.yml'
    ]
    
    for workflow_file in workflow_files:
        if os.path.exists(workflow_file):
            print(f"✅ {workflow_file}")
            # 检查基本语法
            try:
                with open(workflow_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                if 'runs-on: ubuntu-latest' in content:
                    print(f"   ✅ 使用ubuntu-latest运行器")
                else:
                    print(f"   ⚠️  运行器配置可能需要检查")
            except Exception as e:
                print(f"   ❌ 读取失败: {e}")
        else:
            print(f"❌ {workflow_file} - 工作流文件缺失")

def generate_deployment_list():
    """生成部署文件清单"""
    print("\n📋 部署文件清单:")
    
    deployment_files = []
    
    # 遍历当前目录
    for root, dirs, files in os.walk('.'):
        # 跳过.git目录
        if '.git' in root:
            continue
            
        for file in files:
            file_path = os.path.join(root, file)
            # 跳过隐藏文件和特定目录
            if not file.startswith('.') and not file.endswith('.db'):
                deployment_files.append(file_path)
    
    # 排序并显示
    deployment_files.sort()
    for file_path in deployment_files:
        print(f"   {file_path}")
    
    return deployment_files

def main():
    print("🚀 TDX新闻爬虫系统 - 部署前检查")
    print("=" * 50)
    
    # 检查文件
    missing_files = check_files()
    
    # 检查依赖
    check_requirements()
    
    # 检查工作流
    check_workflows()
    
    # 生成部署清单
    deployment_files = generate_deployment_list()
    
    print("\n" + "=" * 50)
    
    if missing_files:
        print(f"❌ 发现 {len(missing_files)} 个缺失文件")
        print("请先解决上述问题再部署")
        return 1
    else:
        print("✅ 所有检查通过！")
        print("\n📝 部署步骤:")
        print("1. 创建GitHub仓库")
        print("2. 上传上述清单中的所有文件")
        print("3. 启用GitHub Pages")
        print("4. 配置Actions权限")
        print("5. 手动触发首次运行")
        print("\n详细指南请参考 DEPLOYMENT_GUIDE.md")
        return 0

if __name__ == "__main__":
    sys.exit(main())