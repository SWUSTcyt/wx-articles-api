#!/usr/bin/env python3
"""
本地API测试脚本
"""

import requests
import json
import time

def test_local_api():
    """测试本地API"""
    print("🧪 等待本地服务器启动...")
    time.sleep(3)
    
    base_url = "http://localhost:8000"
    print(f"📍 测试地址: {base_url}")
    
    endpoints = [
        ("/", "根路径"),
        ("/health", "健康检查"),
        ("/debug", "调试信息"),
        ("/articles?offset=0&count=2", "文章列表")
    ]
    
    for endpoint, name in endpoints:
        print(f"\n{'='*50}")
        print(f"🔍 测试 {name}: {endpoint}")
        
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=10)
            print(f"✅ 状态码: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"📄 响应内容:")
                    print(json.dumps(data, ensure_ascii=False, indent=2)[:300] + "...")
                except json.JSONDecodeError:
                    print(f"📄 响应内容 (非JSON): {response.text[:200]}...")
            else:
                print(f"❌ 错误响应: {response.text[:200]}...")
                
        except requests.exceptions.ConnectionError:
            print(f"❌ 连接失败: 服务器可能未启动")
        except requests.exceptions.Timeout:
            print(f"⏰ 请求超时")
        except Exception as e:
            print(f"❌ 其他错误: {e}")

if __name__ == "__main__":
    test_local_api() 