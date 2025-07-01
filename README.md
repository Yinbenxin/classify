# 中文零样本文本分类器

这个项目提供了一个基于ModelScope的中文零样本文本分类工具，可以对任意中文文本进行分类，无需额外训练。

## 功能特点

- 零样本分类：无需训练数据，直接对文本进行分类
- 自定义标签：支持自定义任意分类标签
- 命令行接口：提供简洁的命令行接口，方便集成和使用
- 结果导出：支持将分类结果导出为JSON格式
- 错误处理：内置多种错误处理机制，提高稳定性

## 环境要求

- Python 3.8+
- 依赖包：见`requirements.txt`

## 安装

1. 克隆仓库：

```bash
git clone <仓库地址>
cd classify
```

2. 安装依赖：

```bash
pip install -r requirements.txt
```

## 使用方法

### 基本用法

```bash
python classifier/classifier.py
```

这将使用默认文本和标签运行分类器。

### 自定义文本和标签

```bash
python classifier/classifier.py --text "这是一个需要分类的文本" --labels "教育,科技,娱乐,体育"
```

### 保存结果到文件

```bash
python classifier/classifier.py --text "这是一个需要分类的文本" --output "result.json"
```

### 使用自定义模型

```bash
python classifier/classifier.py --model_path "/path/to/your/model"
```

## API使用

您也可以在Python代码中直接使用分类函数：

```python
from classifier.classifier import classify_text

text = "这是一个测试文本"
labels = ["教育", "科技", "娱乐", "体育"]
result = classify_text(text, labels)
print(result)
```

## 故障排除

如果遇到`TypeError: transformers.tokenization_utils.PreTrainedTokenizer._batch_encode_plus() got multiple values for keyword argument 'truncation_strategy'`错误，这是由于transformers库版本兼容性问题导致的。代码中已经包含了自动处理这种情况的逻辑。

## 日志

程序运行日志保存在`classifier/classifier.log`文件中，可以查看详细的运行信息和错误信息。

## 测试

执行单元测试：

```bash
# 运行所有测试
python -m unittest discover api/tests

# 运行指定测试文件
python -m unittest api.tests.test_api
python -m unittest api.tests.test_image
```

## 许可证

MIT