from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
import os
import time
import requests
import json

# 创建FastAPI应用
app = FastAPI(title="微信公众号文章获取API", version="1.0.0")

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 从环境变量读取配置
APPID = os.environ.get("APPID")
SECRET = os.environ.get("APPSecret")

def get_access_token():
    """获取微信API访问令牌"""
    if not APPID or not SECRET:
        raise HTTPException(status_code=500, detail="环境变量 APPID 或 APPSecret 未设置")
    
    url = "https://api.weixin.qq.com/cgi-bin/token"
    params = {"grant_type": "client_credential", "appid": APPID, "secret": SECRET}
    
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if "access_token" not in data:
            raise HTTPException(status_code=500, detail=f"微信API错误: {data}")
        
        return data["access_token"]
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"请求微信API失败: {str(e)}")

def parse_draft_item(item):
    """解析单个草稿项"""
    articles = []
    try:
        content = item.get("content", {})
        create_time = content.get("create_time", item.get("update_time", 0))
        
        # 格式化时间
        if create_time:
            time_str = time.strftime("%Y-%m-%d %H:%M", time.localtime(create_time))
        else:
            time_str = "N/A"
        
        # 解析文章列表
        news_items = content.get("news_item", [])
        for news in news_items:
            article = {
                "title": news.get("title", ""),
                "url": news.get("url", ""),
                "digest": news.get("digest", ""),
                "created": time_str,
                "author": news.get("author", ""),
                "thumb_url": news.get("thumb_url", ""),
                "content": news.get("content", "")[:200] + "..." if news.get("content") else ""
            }
            articles.append(article)
    except Exception as e:
        # 如果解析失败，返回错误信息
        articles.append({
            "title": f"解析错误: {str(e)}",
            "url": "",
            "digest": "",
            "created": "N/A",
            "author": "",
            "thumb_url": "",
            "content": ""
        })
    
    return articles

def get_draft_articles(offset=0, count=20):
    """获取草稿箱文章列表"""
    try:
        # 获取访问令牌
        access_token = get_access_token()
        
        # 调用微信API
        api_url = f"https://api.weixin.qq.com/cgi-bin/draft/batchget?access_token={access_token}"
        payload = {"offset": offset, "count": count}
        
        response = requests.post(api_url, json=payload, timeout=10)
        data = response.json()
        
        if "item" not in data:
            raise HTTPException(status_code=500, detail=f"微信API返回错误: {data}")
        
        # 解析文章数据
        all_articles = []
        for item in data.get("item", []):
            articles = parse_draft_item(item)
            all_articles.extend(articles)
        
        total_count = data.get("total_count", len(all_articles))
        return all_articles, total_count
        
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"网络请求失败: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理数据失败: {str(e)}")

@app.get("/")
def root():
    """根路径，返回API信息"""
    return {
        "message": "微信公众号文章获取API",
        "version": "1.0.0",
        "description": "获取微信公众号草稿箱中的文章列表",
        "status": "running",
        "endpoints": {
            "/articles": "获取草稿箱文章列表",
            "/health": "健康检查",
            "/debug": "调试信息"
        }
    }

@app.get("/debug")
def debug_info():
    """调试信息端点"""
    return {
        "env_status": {
            "APPID": "已设置" if APPID else "未设置",
            "APPSecret": "已设置" if SECRET else "未设置",
            "APPID_length": len(APPID) if APPID else 0,
            "APPSecret_length": len(SECRET) if SECRET else 0
        },
        "system_info": {
            "platform": os.name,
            "env_count": len(os.environ)
        },
        "timestamp": time.time()
    }

@app.get("/health")
def health_check():
    """健康检查端点"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "env_configured": bool(APPID and SECRET)
    }

@app.get("/articles")
def get_articles(
    offset: int = Query(0, ge=0, description="偏移量，从0开始"),
    count: int = Query(20, ge=1, le=20, description="获取数量，最大20")
):
    """获取微信公众号草稿箱文章列表"""
    try:
        articles, total = get_draft_articles(offset, count)
        
        return {
            "success": True,
            "data": articles,
            "pagination": {
                "offset": offset,
                "count": len(articles),
                "total": total
            },
            "note": "返回草稿箱中的文章列表"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"未知错误: {str(e)}")

# 使用Mangum包装FastAPI应用供Vercel使用
handler = Mangum(app) 