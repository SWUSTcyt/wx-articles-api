#!/usr/bin/env python3
"""
远程API测试脚本
"""

import requests
import json

def test_remote_api():
    """测试远程API"""
    base_url = "https://wx-api.agiyunting.com"
    
    print("🧪 测试远程API...")
    print(f"📍 API地址: {base_url}")
    
    # 测试端点列表
    endpoints = [
        ("/health", "健康检查"),
        ("/debug", "调试信息"),
        ("/", "根路径"),
        ("/articles?offset=0&count=3", "文章列表")
    ]
    
    for endpoint, name in endpoints:
        print(f"\n{'='*50}")
        print(f"🔍 测试 {name}: {endpoint}")
        
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=30)
            print(f"✅ 状态码: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"📄 响应内容:")
                    print(json.dumps(data, ensure_ascii=False, indent=2)[:500] + "...")
                except json.JSONDecodeError:
                    print(f"📄 响应内容 (非JSON): {response.text[:200]}...")
            else:
                print(f"❌ 错误响应: {response.text[:200]}...")
                
        except requests.exceptions.Timeout:
            print(f"⏰ 请求超时 (30秒)")
        except requests.exceptions.RequestException as e:
            print(f"❌ 网络错误: {e}")
        except Exception as e:
            print(f"❌ 其他错误: {e}")

if __name__ == "__main__":
    test_remote_api() 