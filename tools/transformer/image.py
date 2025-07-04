import os
import logging
import requests
from PIL import Image
from typing import Optional, Union
from transformers import BlipProcessor, BlipForConditionalGeneration

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
model_path ="/etc/model/blip-model"

class ImageRecognizer:
    def __init__(self, model_path: str = model_path):
        """初始化图像识别器
        
        Args:
            model_path: BLIP模型的本地路径
        """
        self.model_path = model_path
        logger.info(f'正在初始化图像识别器，使用模型：{model_path}')
        
        try:
            if not os.path.exists(model_path):
                raise ValueError(f'模型路径不存在：{model_path}')
                
            self.processor = BlipProcessor.from_pretrained(model_path)
            self.model = BlipForConditionalGeneration.from_pretrained(model_path)
            logger.info('图像识别器初始化成功')
        except Exception as e:
            logger.error(f'图像识别器初始化失败：{str(e)}')
            raise
    
    def load_image(self, image_source: Union[str, Image.Image]) -> Image.Image:
        """加载图像
        
        Args:
            image_source: 图像来源，可以是图像URL、本地文件路径或PIL Image对象
            
        Returns:
            PIL Image对象
        """
        try:
            if isinstance(image_source, Image.Image):
                return image_source
            
            if isinstance(image_source, str):
                if image_source.startswith('http'):
                    # 从URL加载图像
                    response = requests.get(image_source, stream=True)
                    response.raise_for_status()
                    return Image.open(response.raw).convert('RGB')
                else:
                    # 从本地文件加载图像
                    if not os.path.exists(image_source):
                        raise FileNotFoundError(f'图像文件不存在：{image_source}')
                    return Image.open(image_source).convert('RGB')
            
            raise ValueError('不支持的图像来源类型')
        except Exception as e:
            logger.error(f'图像加载失败：{str(e)}')
            raise
    
    def recognize(self, image_source: Union[str, Image.Image], max_length: Optional[int] = None) -> str:
        """识别图像内容
        
        Args:
            image_source: 图像来源，可以是图像URL、本地文件路径或PIL Image对象
            max_length: 生成描述的最大长度
            
        Returns:
            图像描述文本
        """
        try:
            # 加载并处理图像
            raw_image = self.load_image(image_source)
            inputs = self.processor(raw_image, return_tensors="pt")
            
            # 生成描述
            generation_kwargs = {}
            if max_length is not None:
                generation_kwargs['max_length'] = max_length
                
            out = self.model.generate(**inputs, **generation_kwargs)
            description = self.processor.decode(out[0], skip_special_tokens=True)
            
            logger.info(f'图像识别完成：{description}')
            return description
        except Exception as e:
            logger.error(f'图像识别失败：{str(e)}')
            raise

if __name__ == '__main__':
    # 测试代码
    recognizer = ImageRecognizer()
    
    # 测试URL图像
    img_url = 'https://img2.baidu.com/it/u=2048195462,703560066&fm=253&fmt=auto&app=138&f=JPEG'
    print('\nURL图像识别结果：')
    description = recognizer.recognize(img_url)
    print(description)
    
    # 测试本地图像（如果有的话）
    # local_image = 'path/to/your/local/image.jpg'
    # print('\n本地图像识别结果：')
    # print(recognizer.recognize(local_image))
