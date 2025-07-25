import os
import logging
import numpy as np
from typing import Union, Optional
import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
model_path = "/etc/model/whisper-model"

class AudioRecognizer:
    def __init__(self, model_path: str = model_path):
        """初始化语音识别器
        
        Args:
            model_path: Whisper模型的本地路径
        """
        self.model_path = model_path
        logger.info(f'正在初始化语音识别器，使用模型：{model_path}')
        
        try:
            if os.path.exists(model_path):
                logger.info(f'发现本地模型：{model_path}')
                # 加载本地模型
                device = "cuda:0" if torch.cuda.is_available() else "cpu"
                torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
                
                model = AutoModelForSpeechSeq2Seq.from_pretrained(
                    model_path, torch_dtype=torch_dtype, low_cpu_mem_usage=True
                )
                model.to(device)
                
                processor = AutoProcessor.from_pretrained(model_path)
                
                # 清除模型的 forced_decoder_ids 配置
                model.generation_config.forced_decoder_ids = None
                
                self.pipe = pipeline(
                    "automatic-speech-recognition",
                    model=model,
                    tokenizer=processor.tokenizer,
                    feature_extractor=processor.feature_extractor,
                    max_new_tokens=128,
                    chunk_length_s=30,
                    batch_size=16,
                    return_timestamps=False,
                    torch_dtype=torch_dtype,
                    device=device,
                    generate_kwargs={"language": "chinese"}
                )
            else:
                logger.info(f'本地模型不存在，从网络加载：openai/whisper-small')
                # 从网络加载模型
                device = "cuda:0" if torch.cuda.is_available() else "cpu"
                torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
                
                model = AutoModelForSpeechSeq2Seq.from_pretrained(
                    "openai/whisper-small", torch_dtype=torch_dtype, low_cpu_mem_usage=True
                )
                model.to(device)
                
                processor = AutoProcessor.from_pretrained("openai/whisper-small")
                
                # 清除模型的 forced_decoder_ids 配置
                model.generation_config.forced_decoder_ids = None
                
                self.pipe = pipeline(
                    "automatic-speech-recognition",
                    model=model,
                    tokenizer=processor.tokenizer,
                    feature_extractor=processor.feature_extractor,
                    max_new_tokens=128,
                    chunk_length_s=30,
                    batch_size=16,
                    return_timestamps=False,
                    torch_dtype=torch_dtype,
                    device=device,
                    generate_kwargs={"language": "chinese"}
                )
                
                # 保存到本地
                os.makedirs(model_path, exist_ok=True)
                model.save_pretrained(model_path)
                processor.save_pretrained(model_path)
                logger.info(f'模型已保存到本地：{model_path}')
                
            logger.info('语音识别器初始化成功')
        except Exception as e:
            logger.error(f'语音识别器初始化失败：{str(e)}')
            raise
    
    def transcribe(self, audio_file: str) -> str:
        """将语音转换为文本
        
        Args:
            audio_file: 音频文件路径
            
        Returns:
            转录的文本
        """
        try:
            if not os.path.exists(audio_file):
                raise FileNotFoundError(f'音频文件不存在：{audio_file}')
                
            logger.info(f'开始转录音频：{audio_file}')
            result = self.pipe(audio_file)
            transcription = result["text"]
            
            logger.info(f'音频转录完成：{transcription}')
            return transcription
        except Exception as e:
            logger.error(f'音频转录失败：{str(e)}')
            raise

if __name__ == '__main__':
    # 测试代码
    recognizer = AudioRecognizer()
    
    # 测试本地音频文件（如果有的话）
    audio_file = '/var/folders/fg/cdwfcq7j0xx97fpzvv3yydcr0000gn/T/tmp4usko48q.wav'
    print('\n音频转录结果：')
    print(recognizer.transcribe(audio_file))