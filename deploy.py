#!/usr/bin/env python3
"""
Vercel部署辅助脚本
帮助用户检查和部署项目到Vercel
"""

import os
import subprocess
import json
from pathlib import Path

def check_file_exists():
    """检查必要的文件是否存在"""
    required_files = [
        "api/wx_drafts.py",
        "requirements.txt", 
        "vercel.json",
        "README.md",
        ".gitignore"
    ]
    
    print("🔍 检查项目文件...")
    missing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} (缺失)")
            missing_files.append(file)
    
    return len(missing_files) == 0, missing_files

def check_vercel_cli():
    """检查Vercel CLI是否安装"""
    try:
        result = subprocess.run(["vercel", "--version"], 
                              capture_output=True, text=True, check=True)
        print(f"✅ Vercel CLI已安装: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Vercel CLI未安装")
        return False

def check_env_config():
    """检查环境变量示例文件"""
    if os.path.exists("config.example"):
        print("✅ 环境变量示例文件存在")
        return True
    else:
        print("❌ 环境变量示例文件不存在")
        return False

def display_deployment_instructions():
    """显示部署说明"""
    print("\n" + "="*60)
    print("🚀 Vercel部署说明")
    print("="*60)
    
    print("\n📋 部署前准备:")
    print("1. 确保已安装Node.js和npm")
    print("2. 安装Vercel CLI: npm i -g vercel")
    print("3. 创建.env文件并配置微信公众号信息")
    print("4. 将代码推送到GitHub仓库")
    
    print("\n🌐 部署方法一: 通过GitHub连接")
    print("1. 登录 https://vercel.com")
    print("2. 点击 'New Project'")
    print("3. 导入您的GitHub仓库")
    print("4. 在项目设置中添加环境变量:")
    print("   - APPID: 您的微信公众号AppID")
    print("   - APPSecret: 您的微信公众号AppSecret")
    print("5. 点击部署")
    
    print("\n💻 部署方法二: 使用Vercel CLI")
    print("1. 在项目根目录运行: vercel login")
    print("2. 运行: vercel")
    print("3. 按提示配置项目")
    print("4. 设置环境变量: vercel env add APPID")
    print("5. 设置环境变量: vercel env add APPSecret")
    print("6. 重新部署: vercel --prod")

def create_quick_deploy_script():
    """创建快速部署脚本"""
    script_content = '''#!/bin/bash
# 快速部署脚本 (需要在Linux/Mac或Windows WSL中运行)

echo "🚀 开始部署到Vercel..."

# 检查Vercel CLI
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI未安装，请先运行: npm i -g vercel"
    exit 1
fi

# 登录Vercel
echo "📝 登录Vercel..."
vercel login

# 部署项目
echo "🚀 部署项目..."
vercel

echo "✅ 部署完成！"
echo "💡 如果是首次部署，请在Vercel控制台设置环境变量 APPID 和 APPSecret"
'''
    
    with open("deploy.sh", "w", encoding="utf-8") as f:
        f.write(script_content)
    
    # 在Unix系统上设置执行权限
    try:
        os.chmod("deploy.sh", 0o755)
    except:
        pass
    
    print("✅ 已创建快速部署脚本: deploy.sh")

def main():
    """主函数"""
    print("=" * 60)
    print("🔧 Vercel部署检查工具")
    print("=" * 60)
    
    # 检查文件
    files_ok, missing = check_file_exists()
    if not files_ok:
        print(f"\n❌ 缺少必要文件: {', '.join(missing)}")
        print("请先创建这些文件后再部署")
        return
    
    # 检查环境变量配置
    env_ok = check_env_config()
    
    # 检查Vercel CLI
    cli_ok = check_vercel_cli()
    
    print(f"\n📊 检查结果:")
    print(f"项目文件: {'✅' if files_ok else '❌'}")
    print(f"环境配置: {'✅' if env_ok else '❌'}")
    print(f"Vercel CLI: {'✅' if cli_ok else '❌'}")
    
    if files_ok and env_ok:
        print("\n🎉 项目文件检查通过！")
        
        # 显示部署说明
        display_deployment_instructions()
        
        # 询问是否创建快速部署脚本
        create_script = input("\n❓ 是否创建快速部署脚本？(y/n): ").lower().strip()
        if create_script in ['y', 'yes']:
            create_quick_deploy_script()
        
        if not cli_ok:
            print("\n💡 要使用命令行部署，请先安装Vercel CLI:")
            print("   npm i -g vercel")
    else:
        print("\n❌ 请先解决上述问题后再部署")

if __name__ == "__main__":
    main() 