import os
import time
import json
import requests
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv

# 加载本地 .env（生产环境下在 Vercel Dashboard 配置环境变量，无需 .env）
load_dotenv()

APPID  = os.getenv("APPID")
SECRET = os.getenv("APPSecret")
if not APPID or not SECRET:
    raise RuntimeError("Missing APPID or APPSecret environment variables")

# 进程内简单缓存
_token = {}

def getStableAccessToken(force: bool = False) -> str:
    """获取并缓存稳定的 access_token；提前 5 分钟失效"""
    info = _token.get("wx")
    if info and info["expire_at"] > time.time() and not force:
        return info["token"]

    resp = requests.post(
        "https://api.weixin.qq.com/cgi-bin/stable_token",
        json={
            "grant_type": "client_credential",
            "appid": APPID,
            "secret": SECRET,
            "force_refresh": force
        },
        timeout=10
    ).json()

    if "access_token" not in resp:
        raise RuntimeError(f"WX API error: {resp}")

    _token["wx"] = {
        "token": resp["access_token"],
        "expire_at": time.time() + resp["expires_in"] - 300
    }
    return resp["access_token"]

def _parse_draft(item: dict):
    """拆分草稿列表中的每篇文章，只保留关键字段"""
    ts = time.strftime("%Y-%m-%d %H:%M", time.localtime(item["update_time"]))
    for art in item["content"]["news_item"]:
        yield {
            "updated": ts,
            "title":   art.get("title", ""),
            "url":     art.get("url", ""),
            "digest":  art.get("digest", "")
        }

def list_drafts(offset: int = 0, count: int = 20):
    """拉取一页草稿并返回 (列表, 总数)"""
    ak = getStableAccessToken()
    resp = requests.post(
        f"https://api.weixin.qq.com/cgi-bin/draft/batchget?access_token={ak}",
        json={"offset": offset, "count": count},
        timeout=10
    )
    resp.encoding = "utf-8"
    data = resp.json()
    if "item" not in data:
        raise RuntimeError(f"WX API error: {data}")

    rows = []
    for it in data["item"]:
        rows.extend(_parse_draft(it))
    return rows, data["total_count"]

# ------ FastAPI 应用 & 路由 ------

app = FastAPI(title="微信草稿箱 API")

@app.get("/")
async def get_drafts(offset: int = 0, count: int = 20):
    """
    获取草稿列表
    - offset: 从第几条开始（默认 0）
    - count: 本次拉取数量（默认 20）
    返回 JSON: { items: [...], total_count: N }
    """
    try:
        items, total = list_drafts(offset, count)
        return {"items": items, "total_count": total}
    except Exception as e:
        # 返回 500 并携带错误信息
        raise HTTPException(status_code=500, detail=str(e))
