# Text Classification API Service / 文本分类 API 服务

A zero-shot learning based text classification service implemented with FastAPI.

基于 zero-shot learning 的文本分类服务，使用 FastAPI 实现。

## Installation / 安装依赖

```bash
pip install -r requirements.txt
```

## Start Service / 启动服务

```bash
uvicorn main:app --reload
```

The service will start at http://127.0.0.1:8000

服务将在 http://127.0.0.1:8000 启动

## API Documentation / API 文档

Visit http://127.0.0.1:8000/docs for interactive API documentation

访问 http://127.0.0.1:8000/docs 查看交互式 API 文档

## API Reference / 接口说明

### POST /classify

Classify text into predefined categories / 对文本进行分类

**Request Body / 请求体**：

```json
{
    "text": "The world is so big, I want to see it / 世界那么大，我想去看看",
    "labels": ["travel/旅游", "story/故事", "game/游戏", "military/军事", "technology/科技", "home/家居"],
    "num_results": 3  // Optional, limit number of results / 可选，限制返回结果数量
}
```

**Response Body / 响应体**：

```json
{
    "labels": ["travel/旅游", "story/故事", "game/游戏"],
    "scores": [0.8413, 0.1293, 0.0109]
}
```

### GET /health

Health check endpoint / 健康检查接口

**Response Body / 响应体**：

```json
{
    "status": "healthy"
}
```