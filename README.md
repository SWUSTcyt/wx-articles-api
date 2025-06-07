# 微信公众号文章获取API

这是一个基于FastAPI的微信公众号文章获取服务，可以部署到Vercel平台，提供HTTP API接口来获取微信公众号草稿箱中的文章列表。

## 项目特点

- 🚀 基于FastAPI框架，高性能异步API
- 🌐 支持Vercel一键部署
- 📱 获取微信公众号草稿箱文章列表
- 🔧 支持分页查询
- 📋 完整的API文档（Swagger）
- 🔒 环境变量安全配置

## 重要说明

本API获取的是**草稿箱中的文章**，而不是已发布的文章。这是因为：
- 草稿箱API可以获取所有文章，包括保存但未发布的内容
- 已发布文章API只能获取通过群发功能发布的文章，不包括其他方式发布的内容
- 大多数公众号文章在发布前都会保存在草稿箱中

## 项目结构

```
微信公众号文章获取/
├── api/
│   └── wx_drafts.py          # FastAPI应用主文件
├── requirements.txt          # Python依赖
├── vercel.json              # Vercel部署配置
├── config.example           # 环境变量示例
├── .gitignore               # Git忽略文件
├── local_test.py            # 本地测试脚本
├── deploy.py                # 部署辅助脚本
└── README.md                # 项目说明文档
```

## 快速开始

### 1. 环境准备

确保您有：
- 微信公众号开发者账号
- 微信公众号的AppID和AppSecret

### 2. 环境变量配置

复制 `config.example` 文件为 `.env`，并填入您的微信公众号信息：

```bash
cp config.example .env
```

编辑 `.env` 文件：
```env
APPID=your_wechat_appid
APPSecret=your_wechat_app_secret
```

### 3. 本地开发

安装依赖：
```bash
pip install -r requirements.txt
```

运行开发服务器：
```bash
uvicorn api.wx_drafts:app --reload
```

访问 `http://localhost:8000` 查看API文档。

## Vercel部署

### 方法一：通过Git连接

1. 将代码推送到GitHub仓库
2. 在Vercel中导入GitHub仓库
3. 在Vercel项目设置中添加环境变量：
   - `APPID`: 您的微信公众号AppID
   - `APPSecret`: 您的微信公众号AppSecret
4. 部署完成

### 方法二：使用Vercel CLI

1. 安装Vercel CLI：
```bash
npm i -g vercel
```

2. 登录并部署：
```bash
vercel login
vercel --env APPID=your_appid --env APPSecret=your_secret
```

## API接口

### 基础信息
- **基础URL**: `https://your-project.vercel.app`
- **响应格式**: JSON
- **数据来源**: 微信公众号草稿箱

### 接口列表

#### 1. 获取API信息
```http
GET /
```

#### 2. 获取草稿箱文章列表
```http
GET /articles?offset=0&count=20
```

**参数说明：**
- `offset`: 偏移量，从0开始（可选，默认0）
- `count`: 获取数量，最大20（可选，默认20）

**响应示例：**
```json
{
  "success": true,
  "data": [
    {
      "title": "文章标题",
      "url": "https://mp.weixin.qq.com/s/...",
      "digest": "文章摘要",
      "created": "2024-01-01 12:00",
      "author": "作者名称",
      "thumb_url": "封面图片URL",
      "content": "文章内容预览..."
    }
  ],
  "pagination": {
    "offset": 0,
    "count": 1,
    "total": 10
  },
  "note": "返回草稿箱中的文章列表"
}
```

#### 3. 健康检查
```http
GET /health
```

## 使用示例

### JavaScript/Node.js
```javascript
// 获取草稿箱文章列表
const response = await fetch('https://your-project.vercel.app/articles?offset=0&count=10');
const data = await response.json();
console.log(data.data); // 文章列表
```

### Python
```python
import requests

# 获取草稿箱文章列表
response = requests.get('https://your-project.vercel.app/articles', params={
    'offset': 0,
    'count': 10
})
articles = response.json()['data']
print(articles)
```

### cURL
```bash
# 获取草稿箱文章列表
curl "https://your-project.vercel.app/articles?offset=0&count=10"
```

## 错误处理

API会返回标准的HTTP状态码：

- `200`: 请求成功
- `400`: 请求参数错误
- `500`: 服务器内部错误

错误响应格式：
```json
{
  "detail": "错误信息描述"
}
```

## 注意事项

1. **数据来源**: 本API获取的是草稿箱中的文章，包括已发布和未发布的内容
2. **访问限制**: 微信API有调用频率限制，请合理控制请求频率
3. **环境变量**: 确保在生产环境中正确设置APPID和APPSecret
4. **安全性**: 不要在客户端代码中暴露AppSecret
5. **缓存**: 建议在客户端实现适当的缓存策略

## 开发说明

### 主要功能模块

- `get_access_token()`: 获取微信API访问令牌
- `list_drafts()`: 获取草稿箱文章列表
- `_parse_draft()`: 解析单个草稿数据

### 依赖说明

- `fastapi`: Web框架
- `uvicorn`: ASGI服务器
- `requests`: HTTP客户端
- `python-dotenv`: 环境变量管理
- `python-multipart`: 表单数据处理

## 故障排除

### 常见问题

1. **环境变量未设置**
   - 错误：`请设置环境变量 APPID 和 APPSecret`
   - 解决：检查环境变量是否正确设置

2. **微信API调用失败**
   - 错误：`微信API错误`
   - 解决：检查AppID和AppSecret是否正确，网络是否正常

3. **部署失败**
   - 检查`vercel.json`配置是否正确
   - 确认Python版本兼容性

4. **获取不到文章**
   - 确保草稿箱中有文章
   - 检查API权限是否正确

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request来改进这个项目。

## 联系方式

如有问题，请创建Issue或联系项目维护者。 