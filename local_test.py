#!/usr/bin/env python3
"""
本地测试脚本
用于测试微信公众号草稿箱文章获取API的功能
"""

import requests
import json
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

def test_local_api():
    """测试本地运行的API"""
    base_url = "http://localhost:8000"
    
    print("🧪 开始测试本地API...")
    
    # 测试根路径
    try:
        response = requests.get(f"{base_url}/")
        print(f"✅ 根路径测试成功: {response.status_code}")
        print(f"📄 响应内容: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
    except Exception as e:
        print(f"❌ 根路径测试失败: {e}")
        return
    
    # 测试健康检查
    try:
        response = requests.get(f"{base_url}/health")
        print(f"✅ 健康检查成功: {response.status_code}")
        print(f"📄 响应内容: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
    except Exception as e:
        print(f"❌ 健康检查失败: {e}")
    
    # 测试获取草稿箱文章列表
    try:
        response = requests.get(f"{base_url}/articles", params={"offset": 0, "count": 5})
        print(f"✅ 草稿箱文章列表测试: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"📄 获取到 {len(data.get('data', []))} 篇草稿文章")
            for i, article in enumerate(data.get('data', [])[:3]):  # 只显示前3篇
                print(f"  {i+1}. {article.get('title', 'N/A')} ({article.get('created', 'N/A')})")
        else:
            print(f"❌ 错误响应: {response.text}")
    except Exception as e:
        print(f"❌ 草稿箱文章列表测试失败: {e}")

def test_remote_api(base_url):
    """测试远程部署的API"""
    print(f"🌐 开始测试远程API: {base_url}")
    
    # 测试根路径
    try:
        response = requests.get(f"{base_url}/")
        print(f"✅ 远程根路径测试成功: {response.status_code}")
    except Exception as e:
        print(f"❌ 远程根路径测试失败: {e}")
        return
    
    # 测试获取草稿箱文章列表
    try:
        response = requests.get(f"{base_url}/articles", params={"offset": 0, "count": 3})
        print(f"✅ 远程草稿箱文章列表测试: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"📄 远程获取到 {len(data.get('data', []))} 篇草稿文章")
        else:
            print(f"❌ 远程错误响应: {response.text}")
    except Exception as e:
        print(f"❌ 远程草稿箱文章列表测试失败: {e}")

def check_env_config():
    """检查环境变量配置"""
    print("🔧 检查环境变量配置...")
    
    appid = os.getenv("APPID")
    secret = os.getenv("APPSecret")
    
    if not appid:
        print("❌ 环境变量 APPID 未设置")
        return False
    
    if not secret:
        print("❌ 环境变量 APPSecret 未设置")
        return False
    
    print(f"✅ APPID: {appid[:8]}...")
    print(f"✅ APPSecret: {secret[:8]}...")
    return True

def main():
    """主函数"""
    print("=" * 50)
    print("🚀 微信公众号草稿箱文章获取API测试工具")
    print("=" * 50)
    
    # 检查环境变量
    if not check_env_config():
        print("\n💡 请先配置环境变量:")
        print("1. 复制 config.example 文件为 .env")
        print("2. 在 .env 文件中填入正确的 APPID 和 APPSecret")
        return
    
    print("\n" + "=" * 30)
    print("选择测试模式:")
    print("1. 测试本地API (需要先运行: uvicorn api.index:app --reload)")
    print("2. 测试远程API (需要提供Vercel部署的URL)")
    print("3. 退出")
    
    choice = input("\n请选择 (1/2/3): ").strip()
    
    if choice == "1":
        test_local_api()
    elif choice == "2":
        url = input("请输入远程API的URL (例如: https://your-project.vercel.app): ").strip()
        if url:
            test_remote_api(url)
        else:
            print("❌ URL不能为空")
    elif choice == "3":
        print("👋 再见!")
    else:
        print("❌ 无效选择")

if __name__ == "__main__":
    main() 