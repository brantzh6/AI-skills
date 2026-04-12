# 向量模型（Embedding）

> 更新时间：2026-04-12
> 来源：https://help.aliyun.com/zh/model-studio/embedding

---

## 概述

向量化模型将文本、图像、视频等数据转换为数值向量，用于语义搜索、推荐、聚类、分类、异常检测等场景。

**Base URL（OpenAI 兼容）：**
- 北京：`https://dashscope.aliyuncs.com/compatible-mode/v1`
- 新加坡：`https://dashscope-intl.aliyuncs.com/compatible-mode/v1`

---

## 模型矩阵

### 文本向量

| 模型 | 向量维度 | 批次大小 | 最大 Token | 单价（每千 Token） | 支持语种 |
|------|----------|----------|------------|-------------------|----------|
| **text-embedding-v4** | 2048/1536/1024(默认)/768/512/256/128/64 | 10 | 8,192 | 0.0005元 | 100+ 语种 |
| **text-embedding-v3** | 1024(默认)/768/512/256/128/64 | — | — | 0.0005元 | 50+ 语种 |
| **text-embedding-v2** | 1536 | 25 | 2,048 | 0.0007元 | 10 语种 |
| **text-embedding-async-v2** | — | — | 100,000 | 0.0007元 | 10 语种 |

### 多模态向量

| 模型 | 向量维度 | 文本限制 | 图片限制 | 视频限制 | 单价 |
|------|----------|----------|----------|----------|------|
| **qwen3-vl-embedding** | 2560(默认)/2048/1536/1024/768/512/256 | 32K Token | ≤5MB | ≤50MB | 图/视: 0.0018元, 文本: 0.0007元 |
| **qwen2.5-vl-embedding** | 2048/1024(默认)/768/512 | — | — | — | — |
| **tongyi-embedding-vision-plus-2026-03-06** | 1152(默认)/1024/512/256/128/64 | 1K Token | ≤10MB, 最多64张 | ≤50MB, H.264/H.265 | 0.0005元 |
| **tongyi-embedding-vision-flash-2026-03-06** | 768(默认)/512/256/128/64 | 同上 | 同上 | 同上 | 0.00015元 |
| **tongyi-embedding-vision-plus** | 1152 | — | ≤3MB, 多图 | ≤50MB | — |
| **tongyi-embedding-vision-flash** | — | — | — | — | 低成本版 |

---

## 快速开始

### 文本向量（OpenAI 兼容）

```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

completion = client.embeddings.create(
    model="text-embedding-v4",
    input="衣服的质量杠杠的"
)

print(completion.model_dump_json())
```

### 多模态独立向量（DashScope）

```python
import dashscope
import json

# 图片向量
image = "https://dashscope.oss-cn-beijing.aliyuncs.com/images/256_1.png"
resp = dashscope.MultiModalEmbedding.call(
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model="tongyi-embedding-vision-plus",
    input=[{'image': image}]
)

print(json.dumps(resp.output, indent=4))
```

### 多模态融合向量

```python
import dashscope

text = "白色运动鞋，轻量透气，适合跑步和日常穿着"
image = "https://dashscope.oss-cn-beijing.aliyuncs.com/images/256_1.png"

# 同一 content 对象中的多模态内容会融合为 1 个向量
input_data = [{"text": text, "image": image}]

resp = dashscope.MultiModalEmbedding.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model="tongyi-embedding-vision-plus-2026-03-06",
    input=input_data,
    dimension=1152
)
```

---

## 向量类型

| 类型 | 说明 | 适用场景 |
|------|------|----------|
| **独立向量** | 为每个输入分别生成独立向量 | 图文标题配对、分类 |
| **融合向量** | 将文本+图片+视频融合为一个向量 | 跨模态检索、文搜图、图搜图 |

### 融合向量的实现方式

| 模型 | 融合方式 |
|------|----------|
| `qwen3-vl-embedding` | 通过 `enable_fusion=True` 参数 |
| `qwen2.5-vl-embedding` | 仅支持融合向量 |
| `tongyi-embedding-vision-plus-2026-03-06` | 将 text+image+video 放在同一个 content 对象中 |

---

## 选型建议

```
需要什么？
├── 纯文本/代码 → text-embedding-v4（推荐，100+ 语种，8192 Token）
├── 大规模批处理 → text-embedding-v4 + Batch API（成本降低 50%）
├── 多模态融合（文搜图等） → qwen3-vl-embedding 或 tongyi-embedding-vision-plus
├── 多模态独立向量 → tongyi-embedding-vision-plus
└── 低成本多模态 → tongyi-embedding-vision-flash-2026-03-06
```

---

## 支持的模型

### 北京地域

**文本向量：** text-embedding-v4、text-embedding-v3、text-embedding-v2、text-embedding-v1、text-embedding-async-v2、text-embedding-async-v1

**多模态向量：** qwen3-vl-embedding、qwen2.5-vl-embedding、tongyi-embedding-vision-plus、tongyi-embedding-vision-flash、tongyi-embedding-vision-plus-2026-03-06、tongyi-embedding-vision-flash-2026-03-06、multimodal-embedding-v1

### 新加坡地域

**文本向量：** text-embedding-v4、text-embedding-v3

**多模态向量：** tongyi-embedding-vision-plus、tongyi-embedding-vision-flash

---

## 免费额度

| 模型 | 免费额度 | 有效期 |
|------|----------|--------|
| text-embedding-v4 | 100 万 Token | 百炼开通后 90 天 |
| text-embedding-v3 | 各 50 万 Token | 同上 |
| text-embedding-async-v2 | 2000 万 Token | 同上 |
| qwen3-vl-embedding | 100 万 Token | 同上 |
