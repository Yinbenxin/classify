import os
from transformers import pipeline

# 检查并创建模型保存目录
MODEL_DIR = '/tmp/model'
if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)

# 下载分类模型
classifier_model = "MoritzLaurer/mDeBERTa-v3-base-mnli-xnli"
print(f"正在下载分类模型：{classifier_model}")
classifier_pipe = pipeline("zero-shot-classification", model=classifier_model)
classifier_pipe.save_pretrained(os.path.join(MODEL_DIR, 'nlp_structbert_zero-shot-classification_chinese-base'))

# 下载图像识别模型
image_model = "Salesforce/blip-image-captioning-base"
print(f"正在下载图像识别模型：{image_model}")
image_pipe = pipeline("image-to-text", model=image_model)
image_pipe.save_pretrained(os.path.join(MODEL_DIR, 'blip-model'))