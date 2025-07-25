# 中文零样本分类分级服务

这个项目提供了一个基于深度学习的中文零样本分类服务，支持多模态数据分类和安全级别评估功能。

## 功能特点

- **零样本分类**：无需训练数据，直接进行分类
- **多模态支持**：支持文本、音频、图像、CSV文件分类
- **安全级别评估**：提供统一的安全风险等级评估体系
- **RESTful API**：提供标准的HTTP接口
- **自定义标签**：支持自定义任意分类标签
- **中文语音识别**：基于Whisper模型的中文音频转录
- **错误处理**：内置多种错误处理机制，提高稳定性

## 环境要求

- Python 3.8+
- 依赖包：见`requirements.txt`

## 项目结构

```
├── api/                    # API服务
│   ├── main.py            # FastAPI应用主文件
│   └── tests/             # 测试用例
│       ├── test_txt.py    # 文本分类测试
│       ├── test_audio.py  # 音频分类测试
│       ├── test_image.py  # 图像分类测试
│       ├── test_csv.py    # CSV分类测试
│       └── test_security.py # 安全级别测试
├── tools/                 # 工具模块
│   ├── classifier/        # 文本分类器
│   │   └── classifier.py  # 零样本分类实现
│   ├── transformer/       # 多模态处理器
│   │   ├── audio.py       # 音频识别器
│   │   └── image.py       # 图像识别器
│   └── default_labels.py  # 默认标签和安全矩阵
├── model/                 # 模型管理
│   └── download.py        # 模型下载脚本
├── audio/                 # 测试音频文件
└── requirements.txt       # 依赖包列表
```

## 安装

1. 克隆仓库：

```bash
git clone https://github.com/Yinbenxin/classify.git
cd classify
```

2. 安装依赖：

```bash
pip install -r requirements.txt
brew install ffmpeg
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

服务启动后，可以访问 http://localhost:8000/docs 查看完整的API文档。

## API接口

### 1. 文本分类

**接口**: `POST /classify/txt`

```bash
curl -X POST "http://localhost:8000/classify/txt" \
     -H "Content-Type: application/json" \
     -d '{"txt":"今天天气很好，适合出去旅游"}'
```

**响应示例**:
```json
{
  "results": [
    ["信息查询", 0.85],
    ["生活服务", 0.92]
  ]
}
```

### 2. 音频分类

**接口**: `POST /classify/audio`

```bash
curl -X POST "http://localhost:8000/classify/audio" \
     -F "audio=@/path/to/audio.wav"
```

**功能**: 自动将音频转录为中文文本，然后进行分类

### 3. 图像分类

**接口**: `POST /classify/image`

```bash
curl -X POST "http://localhost:8000/classify/image" \
     -F "image=@/path/to/image.jpg"
```

**功能**: 识别图像内容并生成描述，然后进行分类

### 4. CSV文件分类

**接口**: `POST /classify/csv`

```bash
curl -X POST "http://localhost:8000/classify/csv" \
     -F "csv_file=@/path/to/data.csv"
```

**功能**: 分析CSV文件的表头和文件名，进行数据类型分类

### 5. 安全级别查询

**接口**: `POST /security/level`

```bash
curl -X POST "http://localhost:8000/security/level" \
     -H "Content-Type: application/json" \
     -d '{"category":"个人基本信息","security_level":"低风险等级"}'
```

**响应示例**:
```json
{
  "category": "个人基本信息",
  "security_level": "低风险等级",
  "level_value": 2
}
```

### 6. 获取所有类别

**接口**: `GET /security/categories`

```bash
curl "http://localhost:8000/security/categories"
```

### 7. 获取安全级别列表

**接口**: `GET /security/levels`

```bash
curl "http://localhost:8000/security/levels"
```

## 测试

执行单元测试：

```bash
# 运行所有测试
python -m unittest discover api/tests

# 运行指定测试文件
python -m unittest api.tests.test_txt        # 文本分类测试
python -m unittest api.tests.test_audio      # 音频分类测试
python -m unittest api.tests.test_image      # 图像分类测试
python -m unittest api.tests.test_csv        # CSV分类测试
python -m unittest api.tests.test_security   # 安全级别测试
```

## 安全级别体系

项目内置了统一的安全风险等级评估体系，包含以下风险等级：

- **低风险等级**: 对个人隐私影响较小的数据
- **中风险等级**: 对个人隐私有一定影响的数据
- **高风险等级**: 对个人隐私影响较大的敏感数据

支持的数据类别包括：
- 个人基本信息
- 个人财产信息
- 个人行为信息
- 网络身份标识信息
- 个人生物识别信息
- 个人健康生理信息
- 个人教育工作信息
- 车辆信息
- 环境变量
- 出行服务数据
- 等等...

## 模型说明

- **文本分类**: 使用零样本学习模型进行中文文本分类
- **音频识别**: 基于Whisper模型进行中文语音转录
- **图像识别**: 使用多模态模型进行图像内容识别
- **安全评估**: 基于预定义的安全风险矩阵进行评级

## 故障排除

1. **模型下载失败**: 请检查网络连接并重试，确保可以访问Hugging Face模型库
2. **API服务无法启动**: 请确保端口8000未被占用，检查依赖包是否正确安装
3. **音频转录失败**: 确保音频文件格式正确（支持wav、mp3等格式），检查Whisper模型是否正确加载
4. **分类结果不准确**: 可以尝试调整或增加标签，确保输入文本质量
5. **依赖包安装失败**: 建议使用conda环境或虚拟环境，避免包冲突

## 性能优化

- 首次运行时会下载模型文件，请耐心等待
- 建议使用GPU加速（如果可用）
- 对于大批量处理，可以考虑批量API调用
- 音频文件建议控制在合理大小以提高处理速度

## 许可证

MIT