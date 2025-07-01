from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import sys
import os

# 添加classifier目录到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from classifier.classifier import TextClassifier

app = FastAPI(
    title="文本分类API",
    description="基于zero-shot learning的文本分类服务",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# 添加全局异常处理
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return {
        "error": str(exc),
        "type": type(exc).__name__,
        "path": request.url.path
    }

# 添加健康检查
@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {"status": "healthy"}

class ClassificationRequest(BaseModel):
    text: str
    labels: List[str]
    num_results: Optional[int] = None

class ClassificationResponse(BaseModel):
    labels: List[str]
    scores: List[float]

# 初始化分类器
classifier = TextClassifier()

@app.post("/classify", response_model=ClassificationResponse)
async def classify_text(request: ClassificationRequest):
    """
    对文本进行分类
    
    Args:
        request: 包含文本和标签的请求体
        
    Returns:
        包含分类结果的响应体
    """
    # 检查输入是否为空
    if not request.text.strip() or not request.labels:
        return ClassificationResponse(labels=[], scores=[])
        
    try:
        result = classifier.classify(
            sequence=request.text,
            labels=request.labels,
            num=request.num_results
        )
        return ClassificationResponse(
            labels=result['labels'],
            scores=result['scores']
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))