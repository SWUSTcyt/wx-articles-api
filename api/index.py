from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os, time, requests, json

load_dotenv()
app = FastAPI(title="微信公众号文章获取API", version="1.0.0")

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

APPID = os.getenv("APPID")
SECRET = os.getenv("APPSecret")

def get_access_token():
    """获取微信API访问令牌"""
    if not APPID or not SECRET:
        raise HTTPException(status_code=500, detail="环境变量 APPID 或 APPSecret 未设置")
    
    url = "https://api.weixin.qq.com/cgi-bin/token"
    params = {"grant_type": "client_credential", "appid": APPID, "secret": SECRET}
    try:
        r = requests.get(url, params=params, timeout=10).json()
        if "access_token" not in r:
            raise RuntimeError(f"微信API错误 → {r}")
        return r["access_token"]
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"请求微信API失败: {str(e)}")

def _parse_draft(item):
    """解析单个草稿项"""
    meta = item.get("content") or {}
    ts = meta.get("create_time") or item.get("update_time")
    ts_fmt = (
        time.strftime("%Y-%m-%d %H:%M", time.localtime(ts))
        if ts else "N/A"
    )
    for news in meta.get("news_item", []):
        yield {
            "title": news.get("title", ""),
            "url": news.get("url", ""),
            "digest": news.get("digest", ""),
            "created": ts_fmt,
            "author": news.get("author", ""),
            "thumb_url": news.get("thumb_url", ""),
            "content": news.get("content", "")[:200] + "..." if news.get("content", "") else ""  # 只返回前200个字符的内容预览
        }

def list_drafts(offset=0, count=20):
    """获取草稿箱文章列表"""
    try:
        ak = get_access_token()
        resp = requests.post(
            f"https://api.weixin.qq.com/cgi-bin/draft/batchget?access_token={ak}",
            json={"offset": offset, "count": count},
            timeout=10
        )
        resp.encoding = "utf-8"  # 防止中文乱码
        data = resp.json()
        
        if "item" not in data:
            raise RuntimeError(f"微信API错误 → {data}")

        articles = []
        for item in data["item"]:
            articles.extend(_parse_draft(item))
        return articles, data.get("total_count", 0)
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"获取草稿列表失败: {str(e)}")

@app.get("/")
def root():
    """根路径，返回API信息"""
    return {
        "message": "微信公众号文章获取API",
        "version": "1.0.0",
        "description": "获取微信公众号草稿箱中的文章列表",
        "endpoints": {
            "/articles": "获取草稿箱文章列表",
            "/health": "健康检查",
            "/debug": "调试信息"
        }
    }

@app.get("/debug")
def debug_info():
    """调试信息端点，检查环境变量状态"""
    return {
        "env_check": {
            "APPID": "已设置" if APPID else "未设置",
            "APPSecret": "已设置" if SECRET else "未设置",
            "APPID_length": len(APPID) if APPID else 0,
            "APPSecret_length": len(SECRET) if SECRET else 0
        },
        "system_info": {
            "platform": os.name,
            "env_vars_count": len(os.environ)
        }
    }

@app.get("/articles")
def get_articles(
    offset: int = Query(0, ge=0, description="偏移量，从0开始"),
    count: int = Query(20, ge=1, le=20, description="获取数量，最大20")
):
    """
    获取微信公众号草稿箱文章列表
    
    - **offset**: 偏移量，从0开始
    - **count**: 获取数量，最大20
    """
    try:
        articles, total = list_drafts(offset, count)
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    """健康检查端点"""
    return {"status": "healthy", "timestamp": time.time()}

# 确保兼容Vercel部署
handler = app
app_handler = app 