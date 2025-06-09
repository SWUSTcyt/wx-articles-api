from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import time

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

@app.get("/health")
def health_check():
    """健康检查端点"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "env_configured": bool(APPID and SECRET),
        "message": "API运行正常"
    }

@app.get("/debug")
def debug_info():
    """调试信息端点"""
    return {
        "env_status": {
            "APPID": "已设置" if APPID else "未设置",
            "APPSecret": "已设置" if SECRET else "未设置",
            "APPID_length": len(APPID) if APPID else 0,
            "APPSecret_length": len(SECRET) if SECRET else 0,
            "APPID_prefix": APPID[:8] + "..." if APPID else None
        },
        "system_info": {
            "platform": os.name,
            "env_count": len(os.environ),
            "current_time": time.time()
        },
        "api_status": "运行中",
        "test": "这是一个测试响应"
    }

@app.get("/articles")
def get_articles(
    offset: int = Query(0, ge=0, description="偏移量，从0开始"),
    count: int = Query(20, ge=1, le=20, description="获取数量，最大20")
):
    """获取微信公众号草稿箱文章列表（临时简化版本）"""
    
    # 返回模拟数据，无论环境变量是否设置
    mock_articles = [
        {
            "title": "测试文章1",
            "url": "https://mp.weixin.qq.com/s/test1",
            "digest": "这是一个测试文章摘要",
            "created": "2024-01-20 10:00",
            "author": "测试作者",
            "thumb_url": "",
            "content": "这是测试内容..."
        },
        {
            "title": "测试文章2", 
            "url": "https://mp.weixin.qq.com/s/test2",
            "digest": "这是另一个测试文章摘要",
            "created": "2024-01-19 15:30",
            "author": "测试作者2",
            "thumb_url": "",
            "content": "这是另一个测试内容..."
        }
    ]
    
    # 分页处理
    total = len(mock_articles)
    articles = mock_articles[offset:offset+count]
    
    env_note = "环境变量已配置，可调用真实API" if APPID and SECRET else "环境变量未配置，返回模拟数据"
    
    return {
        "success": True,
        "data": articles,
        "pagination": {
            "offset": offset,
            "count": len(articles),
            "total": total
        },
        "note": f"当前返回模拟数据。{env_note}",
        "env_configured": bool(APPID and SECRET)
    }

# 简单导出供Vercel使用
handler = app 