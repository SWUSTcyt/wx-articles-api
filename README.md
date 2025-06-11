# 微信公众号文章获取 API (Vercel FastAPI 部署)

## 一、项目结构

```
微信公众号文章获取/
├── api/
│   └── index.py           # FastAPI 主应用，所有API入口
├── test_api2.ipynb        # Jupyter Notebook 示例（本地开发用，已被 .gitignore 忽略）
├── requirements.txt       # Python 依赖
├── Pipfile                # Python 环境配置（可选）
├── vercel.json            # Vercel 路由配置
├── .gitignore             # Git 忽略文件
```

> **注意：** `test_api2.ipynb` 仅用于本地开发和调试，已在 `.gitignore` 中配置，**不会上传到 GitHub**。

## 二、核心代码说明

### 1. FastAPI 主应用（api/index.py）
- 直接导出 `app` 变量，Vercel 自动识别为 ASGI 应用。
- 提供 `/` 路由用于获取微信公众号草稿箱文章列表。
- 支持 offset/count 分页参数。
- 依赖环境变量 `APPID` 和 `APPSecret`，本地可用 `.env` 文件，线上用 Vercel 环境变量。

### 2. 依赖配置
- `requirements.txt` 只需：
  ```
  fastapi==0.104.1
  requests
  python-dotenv
  ```
- `Pipfile` 便于本地开发和 Vercel 自动检测。

### 3. 路由配置（vercel.json）
- 所有请求都路由到 `api/index.py`，由 FastAPI 应用分发。
  ```json
  {
    "routes": [
      { "src": "/(.*)", "dest": "api/index.py" }
    ]
  }
  ```

## 三、部署流程

### 1. GitHub 部署
1. 初始化 Git 仓库并推送到 GitHub：
   ```bash
   git init
   git add .
   git commit -m "init: wechat article api"
   git remote add origin https://github.com/your-username/your-repo.git
   git push -u origin main
   ```
2. 在 Vercel 选择 Import Project，关联 GitHub 仓库。
3. 设置环境变量 `APPID` 和 `APPSecret`。

### 2. Vercel CLI 部署
1. 安装 Vercel CLI：
   ```bash
   npm install -g vercel
   ```
2. 登录 Vercel：
   ```bash
   vercel login
   ```
3. 部署：
   ```bash
   vercel
   ```
4. 设置环境变量（可在 Vercel 控制台设置）。

### 3. 本地开发
1. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
2. 本地运行：
   ```bash
   uvicorn api.index:app --reload
   ```
3. 访问 `http://localhost:8000/` 测试 API。

## 四、注意事项与问题处理

### 1. 环境变量
- 本地开发用 `.env` 文件，线上用 Vercel 环境变量。
- 缺少 `APPID` 或 `APPSecret` 会启动报错。

### 2. 依赖问题
- 只需 `fastapi`、`requests`、`python-dotenv`。
- 避免多余依赖，确保 requirements.txt 格式正确。

### 3. 路由与入口
- 只保留 `api/index.py` 作为主入口，vercel.json 路由所有请求到此文件。
- 不需要 handler、Mangum、builds 配置。

### 4. 常见错误与解决
- **ModuleNotFoundError: No module named 'fastapi'**
  - 检查 requirements.txt 是否包含 fastapi
- **issubclass() arg 1 must be a class**
  - 不要定义 handler = Mangum(app)，直接导出 app
- **Vercel 构建警告**
  - 删除 vercel.json 中的 builds 配置，只保留 routes
- **环境变量未生效**
  - 本地用 .env，线上在 Vercel 控制台设置

### 5. 其他建议
- 只保留 test_api2.ipynb 作为 Notebook 示例，其余测试脚本可删除
- `.gitignore` 已包含 test_api2.ipynb、.env、__pycache__、.vercel 等

---

本项目结构极简，适合 Vercel Serverless 部署，支持微信公众号草稿箱文章的 API 获取。遇到问题请优先检查依赖、环境变量和 vercel.json 配置。 