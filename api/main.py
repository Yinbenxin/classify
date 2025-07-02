from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from typing import List, Dict, Optional
import sys
import os
from PIL import Image
from io import BytesIO
import json

# 添加项目目录到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.classifier.classifier import TextClassifier
from tools.transformer.image import ImageRecognizer

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

class ImageClassificationRequest(BaseModel):
    labels: List[str]
    num_results: Optional[int] = None

class ClassificationResponse(BaseModel):
    labels: List[str]
    scores: List[float]

# 初始化分类器和图像识别器
classifier = TextClassifier()
image_recognizer = ImageRecognizer()

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

@app.post("/classify/image", response_model=ClassificationResponse)
async def classify_image(
    image: UploadFile = File(...),
    labels: str = Form(None),
    num_results: Optional[int] = Form(None)
):
    """
    对图像进行分类：先将图像转换为描述文本，再对文本进行分类
    
    Args:
        image: 上传的图像文件
        request: 包含标签和其他参数的请求体
        
    Returns:
        包含分类结果的响应体
    """
    try:
        # 解析标签
        label_list = json.loads(labels) if labels else []
        if not label_list:
            return ClassificationResponse(labels=[], scores=[])
            
        # 读取并转换图像
        image_content = await image.read()
        pil_image = Image.open(BytesIO(image_content)).convert('RGB')
        
        # 使用图像识别器生成描述
        description = image_recognizer.recognize(pil_image)
        
        # 对描述文本进行分类
        result = classifier.classify(
            sequence=description,
            labels=label_list,
            num=num_results
        )
        
        return ClassificationResponse(
            labels=result['labels'],
            scores=result['scores']
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))