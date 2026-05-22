# 视觉理解（Vision）

> 更新时间：2026-04-12
> 来源：https://help.aliyun.com/zh/model-studio/vision

---

## 概述

Qwen3.6 和 Qwen3-VL 系列支持视觉理解，包括图像问答、创意写作、文字识别、多学科题目解答、视觉编程、物体定位（2D/3D）、文档解析、视频理解等。

**Base URL（OpenAI 兼容）：**
- 北京：`https://dashscope.aliyuncs.com/compatible-mode/v1`
- 新加坡：`https://dashscope-intl.aliyuncs.com/compatible-mode/v1`

**SDK 版本要求：** DashScope Python SDK >= 1.24.6，Java SDK >= 2.21.10

---

## 模型矩阵

### Qwen3.6 系列（最新一代）

| 模型 | 特点 |
|------|------|
| **qwen3.6-plus** | 最新一代，视觉理解显著增强（万物识别、OCR、物体定位） |

### Qwen3.5 系列

| 模型 | 特点 |
|------|------|
| **qwen3.5-plus** | 性能最强的视觉理解模型 |
| **qwen3.5-flash** | 速度更快，成本更低 |
| 开源版 | qwen3.5-397b-a17b、qwen3.5-122b-a10b、qwen3.5-27b、qwen3.5-35b-a3b |

### Qwen3-VL 系列

| 模型 | 特点 |
|------|------|
| **qwen3-vl-plus** | Qwen3-VL 系列性能最强 |
| **qwen3-vl-flash** | 速度更快，成本更低 |

### Qwen2.5-VL 系列

| 模型 | 特点 |
|------|------|
| **qwen-vl-max** | Qwen2.5-VL 系列效果最佳 |
| **qwen-vl-plus** | 速度更快，效果与成本平衡 |

---

## 模型特性对比

| 特性 | Qwen3.6/3.5 | Qwen3-VL | Qwen2.5-VL |
|------|-------------|----------|------------|
| 深度思考 | ✅ 支持 | ✅ 支持 | ❌ |
| 工具调用 | ✅ 支持 | ✅ 支持 | ❌ |
| 上下文缓存 | 仅显式缓存 | 稳定版支持 | 稳定版支持 |
| 识别语言 | 33 种 | 33 种 | 11 种 |

---

## 核心能力

### 1. 图像问答
描述图像内容或分类打标，如识别人物、地点、动植物等。

### 2. 创意写作
根据图片或视频生成文字描述，适用于故事创作、文案、短视频脚本。

### 3. 文字识别与信息抽取（OCR）
识别图像中的文字、公式或抽取票据、证件、表单中的信息，支持格式化输出。

### 4. 多学科题目解答
解答图像中的数学、物理、化学等问题。

### 5. 视觉编程
通过图像或视频生成代码，可用于将设计图、网站截图生成 HTML/CSS/JS。

### 6. 物体定位
- **2D 定位**：返回 Box（边界框）或 Point（中心点）坐标
- **3D 定位**（Qwen3-VL 新增）：返回 3D 边界框和位姿

### 7. 文档解析
将扫描件/图片PDF解析为 QwenVL HTML 或 QwenVL Markdown 格式，精准识别文本、图像、表格等元素。

### 8. 视频理解
分析视频内容，事件定位、时间戳提取、关键时间段摘要等。

---

## 快速开始

### OpenAI 兼容（Python）

```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="qwen3.6-plus",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"
                    },
                },
                {"type": "text", "text": "图中描绘的是什么景象?"},
            ],
        },
    ],
)
print(completion.choices[0].message.content)
```

### DashScope（Python）

```python
import os
import dashscope

dashscope.base_http_api_url = "https://dashscope.aliyuncs.com/api/v1"

messages = [
    {
        "role": "user",
        "content": [
            {"image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"},
            {"text": "图中描绘的是什么景象?"}
        ]
    }
]

response = dashscope.MultiModalConversation.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model="qwen3.6-plus",
    messages=messages
)
print(response.output.choices[0].message.content[0]["text"])
```

### curl（OpenAI 兼容）

```bash
curl 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions' \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json' \
-d '{
    "model": "qwen3.6-plus",
    "messages": [
        {
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"}},
                {"type": "text", "text": "图中描绘的是什么景象?"}
            ]
        }
    ]
}'
```

---

## 传入本地文件

### 通过 DashScope SDK
支持传入本地文件路径（`file://` 开头）或 Base64 编码。

### 通过 OpenAI 兼容接口
- 支持公网 URL（`http://`、`https://` 开头）
- 支持 Base64 编码（`data:image/jpeg;base64,...` 格式）
- 不支持本地文件路径

### 文件规格限制

| 类型 | 大小限制 | 推荐方式 |
|------|----------|----------|
| 图像 < 7MB | 本地路径 / Base64 / 公网URL | 任意 |
| 图像 7MB ~ 10MB | 本地路径 | DashScope SDK |
| 视频 < 7MB | 本地路径 / Base64 / 公网URL | 任意 |
| 视频 7MB ~ 100MB | 公网 URL | 推荐使用阿里云 OSS |
| 视频 > 100MB | 公网 URL | Qwen3-VL、qwen-vl-max 支持 ≤2GB |

**重要：**
- 使用 OSS 生成公网 URL 时，**请勿使用内网地址**
- Base64 编码会增大数据体积，原始文件应 < 7MB
- 推荐使用阿里云 OSS 同地域存储，避免跨地域访问超时

---

## 开启/关闭思考模式

- **qwen3.6、qwen3.5、qwen3-vl-plus、qwen3-vl-flash**：混合思考模型，通过 `enable_thinking` 控制
  - `true`：开启思考（默认开启 qwen3.6/3.5）
  - `false`：关闭思考（qwen3-vl 默认关闭）
- **带 thinking 后缀的模型**（如 `qwen3-vl-235b-a22b-thinking`）：仅思考模型，无法关闭

```python
extra_body={
    'enable_thinking': True,
    "thinking_budget": 81920  # 限制思考过程的最大 Token 数
}
```

---

## 图像限制

| 限制 | 要求 |
|------|------|
| 最小尺寸 | 宽度和高度均不小于 10 像素 |
| 最大宽高比 | 不超过 200:1 或 1:200 |
| 最大文件 | Base64 编码后 ≤ 10MB |
| 支持格式 | JPEG、PNG、WebP、BMP 等 |

---

## 视频限制

| 模型系列 | 时长限制 | 图像数量（以图代视频） |
|----------|----------|----------------------|
| Qwen2.5-VL | 2秒 ~ 10分钟 | 4 ~ 512 张 |
| 其他 VL/Omni | 2秒 ~ 40秒 | 4 ~ 512 张 |

---

## 注意事项

1. **非 Agent 工具调用场景**：建议不设置 System Message，将角色设定通过 User Message 传入
2. **优先使用流式输出**：开启思考模式时，避免长文本导致超时
3. **图像尺寸**：宽度和高度均 ≥ 10 像素，宽高比 ≤ 200:1
4. **详见**：[图像与视频理解文档](https://help.aliyun.com/zh/model-studio/vision)
