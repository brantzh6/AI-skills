# 阿里云百炼 — 语言模型

> 更新时间：2026-04-12
> 来源：[文本生成](https://help.aliyun.com/zh/model-studio/text-generation)、[深度思考](https://help.aliyun.com/zh/model-studio/deep-thinking)、[上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)、[联网搜索](https://help.aliyun.com/zh/model-studio/web-search)

---

## 概述

阿里云百炼（DashScope）提供 OpenAI 兼容的 API 接口，支持千问系列及第三方大语言模型的调用。

**Base URL：**
- 北京（中国内地）：`https://dashscope.aliyuncs.com/compatible-mode/v1`
- 新加坡（国际）：`https://dashscope-intl.aliyuncs.com/compatible-mode/v1`

**API Key：** 各地域不同，需分别获取。

---

## 模型矩阵

| 级别 | 千问旗舰 | 第三方旗舰 | 特点 |
|------|----------|------------|------|
| **Max / 最强效果** | qwen3-max、qwen3.6-plus | GLM-5、Kimi K2.5 | 复杂多步骤任务、深度推理 |
| **Plus / 均衡之选** | qwen3.5-plus、qwen-plus | DeepSeek V3.2、MiniMax M2.5 | 效果/速度/成本平衡 |
| **Flash / 极速低价** | qwen3.5-flash、qwen-flash | — | 简单任务、高吞吐 |
| **专用** | qwen3-coder-plus（代码） | — | 代码生成/调试 |

---

## 千问旗舰系列详解

### Qwen3.6-Plus — 最新旗舰

- **模型名：** `qwen3.6-plus`、`qwen3.6-plus-2026-04-02`
- **特点：** 语言理解、逻辑推理、代码生成、智能体任务、图像理解、视频理解、GUI 全面卓越
- **文本能力：** 媲美 Qwen3-Max
- **多模态：** 同时支持视觉与文本输入（文+图/视频→文）
- **搜索：** 仅 Responses API 支持联网搜索
- **深度思考：** 混合思考模式，默认开启

### Qwen3.5-Plus — 推荐首选

- **模型名：** `qwen3.5-plus`、`qwen3.5-plus-2026-02-15`
- **特点：** 效果/速度/成本均衡，多数场景推荐
- **搜索：** 支持 agent 策略
- **深度思考：** 混合思考模式，默认开启
- **开源版：** qwen3.5-397b-a17b、qwen3.5-122b-a10b、qwen3.5-27b、qwen3.5-35b-a3b

### Qwen3-Max — 最强推理

- **模型名：** `qwen3-max`、`qwen3-max-2026-01-23`、`qwen3-max-preview`
- **特点：** 千问3系列效果最好，适合复杂多步骤任务
- **搜索：** 支持 agent/agent_max 策略（思考模式下）
- **深度思考：** 混合思考模式，默认不开启
- **缓存：** 支持显式缓存

### Qwen3.5-Flash / Qwen-Flash — 极速

- **模型名：** `qwen3.5-flash`、`qwen3.5-flash-2026-02-23`、`qwen-flash`、`qwen-flash-2025-07-28`
- **特点：** 速度最快、成本极低
- **搜索：** 支持
- **深度思考：** 混合思考模式，默认开启

### Qwen3-Coder — 代码专用

- **模型名：** `qwen3-coder-plus`、`qwen3-coder-flash`
- **特点：** 代码生成、调试、解释
- **缓存：** 支持显式缓存

### QwQ — 仅思考模式

- **模型名：** `qwq-plus`、`qwq-32b`
- **特点：** 基于 Qwen2.5，仅思考模式（无直接回复开关）

---

## 第三方旗舰模型

| 品牌 | 模型 | 特点 |
|------|------|------|
| **DeepSeek** | `deepseek-v3.2` | 混合思考，默认不开启 |
| **DeepSeek** | `deepseek-r1` | 仅思考模式，深度推理 |
| **Kimi** | `kimi-k2.5` | 混合思考，默认关闭 |
| **Kimi** | `kimi-k2-thinking` | 仅思考模式 |
| **GLM** | `glm-5` | 混合思考，默认开启 |
| **MiniMax** | `MiniMax-M2.5` | 高速推理 |

所有第三方模型均通过同一 OpenAI 兼容接口调用，只需更换 model 参数。

---

## 高级特性速查

### 1. 深度思考（Reasoning / Deep Thinking）

通过 `enable_thinking` 参数控制模型是否在回复前进行推理。

| 模式 | 说明 | 适用模型 |
|------|------|----------|
| **混合思考** | 可开关，默认因模型而异 | Qwen3.6-Plus、Qwen3.5-Plus、DeepSeek V3.2、GLM-5 |
| **仅思考** | 始终思考，无法关闭 | QwQ、DeepSeek-R1、Kimi K2 Thinking |

**用法（OpenAI 兼容）：**
```python
extra_body={"enable_thinking": True}
```

**返回字段：**
- `reasoning_content` — 完整思考过程
- `content` — 最终回复内容

### 2. 联网搜索（Web Search）

通过 `enable_search` 参数启用网页抓取。

| 策略 | 说明 | 适用场景 |
|------|------|----------|
| `turbo` | 兼顾速度与效果（默认） | 日常查询 |
| `max` | 更全面的搜索策略 | 高精度、多源验证 |
| `agent` | 多轮检索与整合 | 研究/报告 |
| `agent_max` | agent + 网页抓取 | 最详尽搜索 |

**用法（OpenAI 兼容）：**
```python
extra_body={
    "enable_search": True,
    "search_options": {
        "search_strategy": "max"
    }
}
```

### 3. 上下文缓存（Context Cache）

缓存公共前缀，减少重复计算的 Token 成本。

| 模式 | 创建成本 | 命中成本 | 最小 Token | 有效期 |
|------|----------|----------|------------|--------|
| **显式缓存** | 125% | 10% | 1024 | 5分钟 |
| **隐式缓存** | 100% | 20% | 256 | 系统自动管理 |

**用法（显式缓存）：**
```python
"content": [{
    "type": "text",
    "text": long_text,
    "cache_control": {"type": "ephemeral"}
}]
```

**查看缓存命中：**
```python
response.usage.prompt_tokens_details.cache_creation_input_tokens
response.usage.prompt_tokens_details.cached_tokens
```

### 4. 多模态输入

千问 Plus（Qwen3.6-Plus）同时支持文本+图像/视频输入，视觉推理能力相比 VL 系列有飞跃式进步。

### 5. 全模态（Omni）

千问 Omni 支持视频、音频、图片、文本多种输入，生成文本和语音输出。

---

## 快速开始

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
        {"role": "system", "content": "你是一个有帮助的助手。"},
        {"role": "user", "content": "你好"},
    ],
)
print(completion.choices[0].message.content)
```

---

## 详细文档

- [模型选型指南](docs/models.md) — 完整模型列表、特性对比
- [深度思考用法](docs/deep-thinking.md) — enable_thinking、思考模式、流式输出
- [上下文缓存](docs/context-cache.md) — 显式/隐式缓存、多缓存标记
- [联网搜索](docs/web-search.md) — 搜索策略、强制搜索、搜索来源
