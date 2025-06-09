#!/usr/bin/env python3
"""
部署辅助脚本
帮助检查项目配置和部署状态
"""

import os
import json
import requests
from pathlib import Path

def check_required_files():
    """检查必需的文件是否存在"""
    print("📁 检查项目文件...")
    
    required_files = [
        "api/index.py",
        "requirements.txt",
        ".gitignore",
        "README.md"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
            print(f"❌ 缺少文件: {file_path}")
        else:
            print(f"✅ 文件存在: {file_path}")
    
    return len(missing_files) == 0

def check_env_config():
    """检查环境变量配置示例"""
    print("\n🔧 检查环境配置...")
    
    if os.path.exists("config.example"):
        print("✅ 环境配置示例文件存在")
        with open("config.example", "r") as f:
            content = f.read()
            if "APPID" in content and "APPSecret" in content:
                print("✅ 环境变量模板正确")
            else:
                print("❌ 环境变量模板不完整")
                return False
    else:
        print("❌ 缺少环境配置示例文件")
        return False
    
    # 检查是否有本地环境文件
    if os.path.exists(".env"):
        print("✅ 本地环境配置文件存在")
    else:
        print("⚠️  本地环境配置文件不存在（部署时需要在Vercel中配置）")
    
    return True

def check_dependencies():
    """检查依赖文件"""
    print("\n📦 检查依赖配置...")
    
    if not os.path.exists("requirements.txt"):
        print("❌ 缺少 requirements.txt 文件")
        return False
    
    with open("requirements.txt", "r") as f:
        deps = f.read().strip().split("\n")
        required_deps = ["fastapi", "uvicorn", "requests", "python-dotenv"]
        
        for dep in required_deps:
            found = any(dep in line for line in deps)
            if found:
                print(f"✅ 依赖存在: {dep}")
            else:
                print(f"❌ 缺少依赖: {dep}")
                return False
    
    return True

def check_api_structure():
    """检查API文件结构"""
    print("\n🔍 检查API结构...")
    
    api_file = "api/index.py"
    if not os.path.exists(api_file):
        print(f"❌ API文件不存在: {api_file}")
        return False
    
    with open(api_file, "r", encoding="utf-8") as f:
        content = f.read()
        
        checks = [
            ("FastAPI导入", "from fastapi import FastAPI"),
            ("应用实例", "app = FastAPI"),
            ("草稿箱路由", "@app.get(\"/articles\")"),
            ("健康检查路由", "@app.get(\"/health\")"),
            ("根路径路由", "@app.get(\"/\")")
        ]
        
        for name, pattern in checks:
            if pattern in content:
                print(f"✅ {name}: 存在")
            else:
                print(f"❌ {name}: 缺失")
                return False
    
    return True

def test_local_import():
    """测试本地导入"""
    print("\n🧪 测试API模块导入...")
    
    try:
        # 添加当前目录到Python路径
        import sys
        sys.path.insert(0, ".")
        
        # 尝试导入API模块
        from api.index import app
        print("✅ API模块导入成功")
        
        # 检查应用类型
        from fastapi import FastAPI
        if isinstance(app, FastAPI):
            print("✅ FastAPI应用实例正确")
        else:
            print("❌ 应用实例类型错误")
            return False
            
        return True
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 其他错误: {e}")
        return False

def check_deployment_readiness():
    """检查部署就绪状态"""
    print("\n" + "=" * 50)
    print("🚀 检查Vercel部署就绪状态")
    print("=" * 50)
    
    checks = [
        ("必需文件", check_required_files),
        ("环境配置", check_env_config),
        ("依赖配置", check_dependencies),
        ("API结构", check_api_structure),
        ("模块导入", test_local_import)
    ]
    
    all_passed = True
    for name, check_func in checks:
        result = check_func()
        if not result:
            all_passed = False
            print(f"\n❌ {name} 检查失败")
        else:
            print(f"\n✅ {name} 检查通过")
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 项目已准备好部署到Vercel!")
        print("\n📝 部署步骤:")
        print("1. 确保代码已推送到GitHub")
        print("2. 在Vercel中连接GitHub仓库")
        print("3. 配置环境变量 APPID 和 APPSecret")
        print("4. 点击部署")
    else:
        print("❌ 项目部署前需要修复上述问题")
    
    return all_passed

def check_remote_deployment(url):
    """检查远程部署状态"""
    print(f"\n🌐 检查远程部署: {url}")
    
    endpoints = [
        ("/", "根路径"),
        ("/health", "健康检查"),
        ("/articles", "草稿箱文章列表")
    ]
    
    for endpoint, name in endpoints:
        try:
            response = requests.get(f"{url}{endpoint}", timeout=10)
            print(f"✅ {name} ({endpoint}): {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"❌ {name} ({endpoint}): {e}")

def main():
    """主函数"""
    print("🛠️  微信公众号草稿箱文章获取API - 部署检查工具")
    print("=" * 60)
    
    print("选择操作:")
    print("1. 检查部署就绪状态")
    print("2. 检查远程部署状态")
    print("3. 退出")
    
    choice = input("\n请选择 (1/2/3): ").strip()
    
    if choice == "1":
        check_deployment_readiness()
    elif choice == "2":
        url = input("请输入部署的URL (例如: https://your-project.vercel.app): ").strip()
        if url:
            check_remote_deployment(url)
        else:
            print("❌ URL不能为空")
    elif choice == "3":
        print("👋 再见!")
    else:
        print("❌ 无效选择")

if __name__ == "__main__":
    main() 