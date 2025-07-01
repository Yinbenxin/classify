import logging
import os
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
# path = "MoritzLaurer/mDeBERTa-v3-base-mnli-xnli"
path = "/Users/yinbenxin/model/nlp_structbert_zero-shot-classification_chinese-base"

class TextClassifier:
    def __init__(self, model_path: str=path):
        """初始化分类器
        
        Args:
            model_path: 模型路径或名称
        """
 
        logger.info(f'正在初始化分类器，使用模型：{model_path}')
        try:
            # 检查本地模型
            if os.path.exists(model_path):
                logger.info(f'发现本地模型：{model_path}')
                model = AutoModelForSequenceClassification.from_pretrained(model_path)
                tokenizer = AutoTokenizer.from_pretrained(model_path)
                self.classifier = pipeline(
                    'zero-shot-classification',
                    model=model,
                    tokenizer=tokenizer
                )
            else:
                logger.info(f'本地模型不存在，从网络加载：{model_path}')
                model = AutoModelForSequenceClassification.from_pretrained(model_path)
                tokenizer = AutoTokenizer.from_pretrained(model_path)
                # 保存到本地
                # model.save_pretrained(model_path)
                # tokenizer.save_pretrained(model_path)
                # logger.info(f'模型已保存到本地：{model_path}')
                self.classifier = pipeline(
                    'zero-shot-classification',
                    model=model,
                    tokenizer=tokenizer
                )
            logger.info('分类器初始化成功')
        except Exception as e:
            logger.error(f'分类器初始化失败：{str(e)}')
            raise
    
    def classify(self, sequence: str, labels: list, num: int = None) -> dict:
        """对文本进行零样本分类
        
        Args:
            sequence: 待分类的文本
            labels: 标签列表
            num: 返回的标签数量，默认返回所有
            
        Returns:
            dict: 包含分类结果的字典
        """
        if not sequence or not labels:
            logger.warning('输入的文本或标签为空')
            return {}
        
        logger.info(f'开始分类，文本：{sequence[:50]}，标签：{labels}')
        
        try:
            result = self.classifier(sequence, candidate_labels=labels)
            
            if num is not None:
                result['labels'] = result['labels'][:num]
                result['scores'] = result['scores'][:num]
                logger.info(f'返回前 {num} 个结果')
            
            logger.info('分类完成')
            return result
        except Exception as e:
            logger.error(f'分类过程出错：{str(e)}')
            raise

if __name__ == '__main__':
    # 测试代码

    classifier = TextClassifier()
    
    test_sequence = '世界那么大，我想去看看'
    test_labels = ['旅游', '故事', '游戏', '军事', '科技', '家居']
    
    result = classifier.classify(test_sequence, test_labels)
    print('\n分类结果:')
    for label, score in zip(result['labels'], result['scores']):
        print(f'{label}: {score:.2%}')