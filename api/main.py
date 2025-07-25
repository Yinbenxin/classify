from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from typing import List, Dict, Optional, Union, Any
import sys
import os
from PIL import Image
from io import BytesIO
import json
import tempfile
import pathlib
import logging
import csv
import io

# 添加项目目录到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.classifier.classifier import txtClassifier
from tools.transformer.image import ImageRecognizer
from tools.transformer.audio import AudioRecognizer
from tools.default_labels import unified_security_matrix, get_all_labels
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
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



# 初始化分类器、图像识别器和语音识别器
classifier = txtClassifier()
image_recognizer = ImageRecognizer()
audio_recognizer = AudioRecognizer()

def load_default_labels():
    """从 default_labels.py 加载默认标签"""
    try:
        labels_dict = get_all_labels()
        # 转换为API需要的格式
        return {
            'txt': [labels_dict.get('txt', [])],
            'audio': [labels_dict.get('audio', [])],
            'image': [labels_dict.get('image', [])],
            'csv': [labels_dict.get('csv', [])]
        }
    except Exception as e:
        print(f"加载默认标签失败: {str(e)}")
        return {}
        
default_labels = load_default_labels()

class TxtRequest(BaseModel):
    txt: str

class SecurityLevelRequest(BaseModel):
    category: str  # 类别名称
    security_level: str  # 安全级别：'低风险等级', '中风险等级', '高风险等级'

@app.post("/classify/txt")
async def classify_txt(request: TxtRequest):
    if not request.txt.strip():
        return {"results": []}
    labels = default_labels.get('txt', [])
    if not labels:
        return {"results": []}
    try:
        all_results = []
        for label_group in labels:
            if not label_group:
                all_results.append([])
                continue
            result = classifier.classify(
                sequence=request.txt,
                labels=label_group
            )
            if result['labels'] and result['scores']:
                all_results.append([result['labels'][0], result['scores'][0]])
            else:
                all_results.append([])
        logger.info(f'分类结果：{all_results}')
        return {"results": all_results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/classify/audio")
async def classify_audio(audio: UploadFile = File(...)):
    try:
        label_groups = default_labels.get('audio', [])
        if not label_groups:
            return {"results": []}
        audio_content = await audio.read()
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{audio.filename.split('.')[-1]}") as temp_audio:
            temp_audio.write(audio_content)
            temp_audio_path = temp_audio.name
        try:
            transcription = audio_recognizer.transcribe(temp_audio_path)
            all_results = []
            for label_group in label_groups:
                if not label_group:
                    all_results.append([])
                    continue
                result = classifier.classify(
                    sequence=transcription,
                    labels=label_group
                )
                if result['labels'] and result['scores']:
                    all_results.append([result['labels'][0], result['scores'][0]])
                else:
                    all_results.append([])
            logger.info(f'音频分类结果：{all_results}')
            return {"results": all_results}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            if os.path.exists(temp_audio_path):
                os.remove(temp_audio_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/classify/image")
async def classify_image(image: UploadFile = File(...)):
    try:
        label_groups = default_labels.get('image', [])
        if not label_groups:
            return {"results": []}
        image_content = await image.read()
        img = Image.open(BytesIO(image_content)).convert('RGB')
        all_results = []
        for label_group in label_groups:
            if not label_group:
                all_results.append([])
                continue
            description = image_recognizer.recognize(img)
            # 用图片描述进行文本分类
            result = classifier.classify(
                sequence=description,
                labels=label_group
            )
            if result['labels'] and result['scores']:
                all_results.append([result['labels'][0], result['scores'][0]])
            else:
                all_results.append([])
        logger.info(f'图像分类结果：{all_results}')
        return {"results": all_results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/classify/csv")
async def classify_csv(csv_file: UploadFile = File(...)):
    try:
        label_groups = default_labels.get('csv', default_labels.get('txt', []))
        if not label_groups:
            return {"results": []}
            
        # 读取CSV文件内容
        csv_content = await csv_file.read()
        csv_text = csv_content.decode('utf-8')
        
        # 使用CSV模块解析CSV内容
        csv_reader = csv.reader(io.StringIO(csv_text))
        
        # 提取表头（第一行）
        headers = next(csv_reader, [])
        
        if not headers:
            return {"results": []}
        
        # 将表头合并成一个字符串
        header_text = ", ".join(headers)
        logger.info(f'CSV表头：{header_text}')
        #将表名也合并到header_text
        header_text = f'表名：{csv_file.filename.split(".")[0]}，表头：{header_text}'

        # 使用合并后的表头文本进行分类
        all_results = []
        for label_group in label_groups:
            if not label_group:
                all_results.append([])
                continue
                
            result = classifier.classify(
                sequence=header_text,
                labels=label_group
            )
            
            if result['labels'] and result['scores']:
                all_results.append([result['labels'][0], result['scores'][0]])
            else:
                all_results.append([])
                
        logger.info(f'CSV分类结果：{all_results}')
        return {"results": all_results}
    except Exception as e:
        logger.error(f'CSV分类错误：{str(e)}')
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/security/level")
async def get_security_level(request: SecurityLevelRequest):
    """根据类别和安全级别获取对应的级别值"""
    try:
        # 检查类别是否存在
        if request.category not in unified_security_matrix:
            raise HTTPException(status_code=404, detail=f"未找到类别: {request.category}")
        
        # 检查安全级别是否有效
        if request.security_level not in ["低风险等级", "中风险等级", "高风险等级"]:
            raise HTTPException(status_code=400, detail=f"不支持的安全级别: {request.security_level}")
        
        # 获取对应的级别值
        level_value = unified_security_matrix[request.category][request.security_level]
        
        logger.info(f'安全级别查询结果：类别={request.category}, 级别={request.security_level}, 值={level_value}')
        return {
            "category": request.category,
            "security_level": request.security_level,
            "level_value": level_value
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f'安全级别查询错误：{str(e)}')
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/security/categories")
async def get_categories():
    """获取所有类别"""
    try:
        # 获取所有类别
        categories = list(unified_security_matrix.keys())
        
        return {
            "categories": categories,
            "total_count": len(categories)
        }
        
    except Exception as e:
        logger.error(f'获取类别错误：{str(e)}')
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/security/levels")
async def get_security_levels():
    """获取所有可用的安全级别"""
    return {
        "security_levels": ["低风险等级", "中风险等级", "高风险等级"]
    }
