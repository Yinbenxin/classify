# 中文零样本分类服务

这个项目提供了一个基于深度学习的中文零样本分类服务，支持文本分类和图像识别功能。

## 功能特点

- 零样本分类：无需训练数据，直接进行分类
- 多模态支持：同时支持文本分类和图像识别
- RESTful API：提供标准的HTTP接口
- 自定义标签：支持自定义任意分类标签
- 错误处理：内置多种错误处理机制，提高稳定性

## 环境要求

- Python 3.8+
- 依赖包：见`requirements.txt`

## 项目结构

```
├── api/          # API服务
│   ├── main.py   # FastAPI应用
│   └── tests/    # 测试用例
├── tools/        # 工具模块
│   ├── classifier/    # 文本分类器
│   └── transformer/   # 图像识别器
└── model/       # 模型管理
    └── download.py    # 模型下载脚本
```

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

3. 下载模型：

```bash
python model/download.py
```

## API服务

启动服务：

```bash
uvicorn api.main:app --reload
```

### 文本分类

```bash
curl -X POST "http://localhost:8000/classify" \
     -H "Content-Type: application/json" \
     -d '{"txt":"这是一个测试文本","labels":["教育","科技","娱乐"]}'
```

### 图像识别

```bash
curl -X POST "http://localhost:8000/classify/image" \
     -F "image=@/path/to/image.jpg" \
     -F "labels=[\"猫\",\"狗\",\"鸟\"]" \
     -F "num_results=3"
```

## 测试

执行单元测试：

```bash
# 运行所有测试
python -m unittest discover api/tests

# 运行指定测试文件
python -m unittest api.tests.test_api
python -m unittest api.tests.test_image
```

## 故障排除

1. 如果遇到模型下载失败，请检查网络连接并重试
2. 如果API服务无法启动，请确保端口8000未被占用
3. 如果分类结果不准确，可以尝试调整或增加标签

## 许可证

MIT