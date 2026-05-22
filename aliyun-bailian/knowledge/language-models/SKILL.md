# 阿里云百炼 — 语言模型

> 更新时间：2026-05-22
> 来源：[文本生成](https://help.aliyun.com/zh/model-studio/text-generation)、[深度思考](https://help.aliyun.com/zh/model-studio/deep-thinking)、[上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)、[联网搜索](https://help.aliyun.com/zh/model-studio/web-search)

---

## 概述

阿里云百炼（DashScope）提供 OpenAI 兼容的 API 接口，支持千问系列及第三方大语言模型的调用。

**Base URL：**
- 北京（中国内地）：`https://dashscope.aliyuncs.com/compatible-mode/v1`
- 弗吉尼亚（全球）：`https://dashscope-us.aliyuncs.com/compatible-mode/v1`
- 新加坡（国际）：`https://dashscope-intl.aliyuncs.com/compatible-mode/v1`

**API Key：** 各地域不同，需分别获取。

---

## 模型矩阵

| 级别 | 千问旗舰 | 第三方旗舰 | 特点 |
|------|----------|------------|------|
| **Max / 最强效果** | qwen3.7-max | GLM-5.1、Kimi K2.6、DeepSeek V4-Pro | 复杂多步骤任务、深度推理 |
| **Plus / 均衡之选** | qwen3.6-plus | DeepSeek V4、MiniMax M2.7 | 效果/速度/成本平衡 |
| **Flash / 极速低价** | qwen3.6-flash | — | 简单任务、高吞吐 |
| **Coder / 代码专用** | qwen3-coder-plus | — | 代码生成/调试/解释 |
| **Turbo / 轻量级** | qwen-turbo | — | 轻量级任务，默认非思考模式 |

---

## 千问旗舰系列详解

### Qwen3.7-Max — 最新旗舰（2026-05-20 发布）

- **模型名：** `qwen3.7-max`、`qwen3.7-max-2026-05-20`
- **特点：** 当前最强千问模型，适合复杂推理、多步骤任务、深度分析
- **上下文长度：** 1,000,000 Token
- **最大输出：** 64k
- **思考预算：** 256k（思考 token 不计入输出费用）
- **深度思考：** 混合思考模式，默认开启
- **Function Calling：** 支持
- **内置工具：** 支持
- **结构化输出：** 支持
- **批量调用：** 支持（半价）
- **上下文缓存：** 支持
- **价格：** 输入 12元/百万Token，输出 36元/百万Token
- **注意：** 仅支持 bailian provider，不支持 Token Plan 和 Coding Plan

### Qwen3.6-Max-Preview — 上一代最强

- **模型名：** `qwen3.6-max-preview`
- **特点：** Qwen 系列效果最好的模型，适合复杂、多步骤任务
- **推理能力：** 全面超越前代
- **上下文长度：** 262,144 Token
- **深度思考：** 混合思考模式，默认开启
- **注意：** 使用文本生成接口（非多模态接口）
- **价格：** 输入 9元/百万Token，输出 54元/百万Token

### Qwen3.6-Plus — 均衡旗舰（推荐首选）

- **模型名：** `qwen3.6-plus`、`qwen3.6-plus-2026-04-02`
- **特点：** 效果、速度和成本上表现均衡，多数场景的推荐选择
- **上下文长度：** 1,000,000 Token
- **多模态：** 同时支持视觉与文本输入（文+图/视频→文），视觉推理能力飞跃式进步
- **深度思考：** 混合思考模式，默认开启
- **联网搜索：** 仅 Responses API 支持
- **价格：** 输入 2元，输出 12元（思考模式 12元）

### Qwen3.6-Flash — 极速低价

- **模型名：** `qwen3.6-flash`、`qwen3.6-flash-2026-04-16`
- **特点：** 速度最快、成本极低，适合简单任务、高吞吐场景
- **上下文长度：** 1,000,000 Token
- **深度思考：** 混合思考模式，默认开启
- **开源版：** qwen3.6-35b-a3b
- **价格：** 输入 1.2元，输出 7.2元

### Qwen3.5-Plus — 上一代 Plus

- **模型名：** `qwen3.5-plus`、`qwen3.5-plus-2026-04-20`、`qwen3.5-plus-2026-02-15`
- **特点：** 效果/速度/成本均衡
- **深度思考：** 混合思考模式，默认开启
- **联网搜索：** 支持 agent 策略
- **价格：** 输入 0.8元，输出 4.8元

### Qwen3.5-Flash — 上一代 Flash

- **模型名：** `qwen3.5-flash`、`qwen3.5-flash-2026-02-23`
- **特点：** 速度极快、成本极低
- **深度思考：** 混合思考模式，默认开启
- **价格：** 输入 0.2元，输出 2元

### Qwen3-Coder — 代码专用（新增）

- **模型名：** `qwen3-coder-plus`、`qwen3-coder-plus-2025-07-22`、`qwen3-coder-flash`、`qwen3-coder-flash-2025-07-28`
- **特点：** 代码生成、调试、解释，专为开发者设计
- **上下文缓存：** 支持显式缓存
- **Batch 调用：** 支持半价

### Qwen-Turbo — 轻量级

- **模型名：** `qwen-turbo`、`qwen-turbo-latest`、`qwen-turbo-2025-04-28` 及之后的快照版
- **特点：** 轻量级任务，默认非思考模式
- **深度思考：** 混合思考模式，默认不开启

### Qwen3-Max — 上一代 Max

- **模型名：** `qwen3-max`、`qwen3-max-2026-01-23`、`qwen3-max-preview`
- **特点：** 上一代最强推理，适合复杂多步骤任务
- **深度思考：** 混合思考模式，默认不开启
- **缓存：** 支持显式缓存
- **Batch 调用：** 支持半价

### Qwen3-Next — MoE 架构（新增）

- **模型名：** `qwen3-next-80b-a3b-thinking`（仅思考）、`qwen3-next-80b-a3b-instruct`（非思考）
- **特点：** 80B 总参数，每次仅激活 3B 参数，性能媲美 Qwen3-235B
- **架构：** 高稀疏度混合专家（MoE），训练成本下降超 90%

### QwQ — 仅思考模式

- **模型名：** `qwq-plus`、`qwq-plus-latest`、`qwq-plus-2025-03-05`、`qwq-32b`
- **特点：** 基于 Qwen2.5，仅思考模式（无直接回复开关）

---

## 第三方旗舰模型

| 品牌 | 模型 | 特点 | 部署方 |
|------|------|------|-------|
| **DeepSeek** | `deepseek-v4-pro` | 混合思考，默认开启 | 阿里云百炼 |
| **DeepSeek** | `deepseek-v4-flash` | 混合思考，默认开启 | 阿里云百炼 |
| **DeepSeek** | `deepseek-v3.2` | 混合思考，默认不开启 | 阿里云百炼/硅基/快手 |
| **DeepSeek** | `deepseek-r1` | 仅思考模式，深度推理 | 阿里云百炼/快手 |
| **DeepSeek** | `deepseek-r1-0528` | 仅思考模式 | 阿里云百炼/硅基 |
| **Kimi** | `kimi-k2.6` | 混合思考，默认关闭 | 阿里云百炼/月之暗面 |
| **Kimi** | `kimi-k2.5` | 混合思考，默认关闭 | 阿里云百炼/月之暗面 |
| **Kimi** | `kimi-k2-thinking` | 仅思考模式 | 阿里云百炼 |
| **Kimi** | `kimi/kimi-k2.6` | 混合思考，默认开启 | 月之暗面部署 |
| **GLM** | `glm-5.1` | 混合思考，默认开启，支持缓存 | 阿里云百炼 |
| **GLM** | `glm-5` | 混合思考，默认开启 | 阿里云百炼 |
| **GLM** | `glm-4.7`、`glm-4.6` | 混合思考，默认开启 | 阿里云百炼 |
| **MiniMax** | `MiniMax/MiniMax-M2.7` | 混合思考，默认开启 | Token Plan（稀宇科技部署） |
| **MiniMax** | `MiniMax-M2.5` | 仅思考模式 | 阿里云百炼/稀宇 |
| **MiniMax** | `MiniMax-M2.1` | 仅思考模式 | 阿里云百炼/稀宇 |
| **小米** | `xiaomi/mimo-v2.5-pro` | 混合思考，默认开启 | Token Plan |

> ⚠️ **注意**：MiniMax-M2.7 在 Token Plan 下需使用 `MiniMax/MiniMax-M2.7`（带命名空间）

所有第三方模型均通过同一 OpenAI 兼容接口调用，只需更换 model 参数。

---

## 高级特性速查

### 1. 深度思考（Reasoning / Deep Thinking）

通过 `enable_thinking` 参数控制模型是否在回复前进行推理。

| 模式 | 说明 | 适用模型 |
|------|------|----------|
| **混合思考** | 可开关，默认因模型而异 | Qwen3.6-Plus（默认开）、Qwen3.6-Flash（默认开）、GLM-5.1（默认开）、DeepSeek V4（默认开）、Kimi K2.6（默认关） |
| **仅思考** | 始终思考，无法关闭 | QwQ、DeepSeek-R1、Kimi K2 Thinking、Qwen3-Next-thinking |

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

**支持的模型（显式缓存）：**
- 千问 Max/Plus/Flash/Coder/VL
- DeepSeek: deepseek-v3.2
- Kimi: kimi-k2.6、kimi-k2.5
- GLM: glm-5.1

**用法（显式缓存）：**
```python
"content": [{
    "type": "text",
    "text": long_text,
    "cache_control": {"type": "ephemeral"}
}]
```

### 4. 全模态模型（Omni）

| 模型 | 输入 | 输出 | 特点 |
|------|------|------|------|
| **千问Omni** (Qwen3.5-Omni) | 视频、音频、图片、文本 | 文本 + 语音 | 全模态，跨模态复杂任务 |
| **千问Omni-Realtime** | 视频、音频、图片、文本 | 文本 + 语音 | 实时多模态交互 |
| **千问Audio** | 音频 | 文本 | 语音识别/理解 |
| **千问Plus** (Qwen3.6-Plus) | 文本 + 图像/视频 | 文本 | 视觉推理能力飞跃式进步 |

### 5. 角色扮演模型

- `qwen-plus-character` — 千问 Plus 角色扮演版
- `qwen-flash-character`、`qwen-flash-character-2026-02-26` — 千问 Flash 角色扮演版

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

---

## 更新日志

### 2026-05-22
- **新增 Qwen3.7-Max**（qwen3.7-max，混合思考默认开启，1M上下文，256K思考预算，最强旗舰）
- 新增 Qwen3.7-Max 快照版（qwen3.7-max-2026-05-20）
- 修正 MiniMax-M2.7：Token Plan 下使用 `MiniMax/MiniMax-M2.7`（带命名空间），混合思考默认开启
- 新增小米 mimo-v2.5-pro（Token Plan，混合思考默认开启，1M上下文）
- 确认思考模式矩阵：qwen3.6-plus/flash 默认开启，kimi-k2.6 默认关闭
- 模型矩阵表更新：Max 级别升级为 qwen3.7-max

### 2026-04-27
- 新增 DeepSeek V4（deepseek-v4-pro/flash，混合思考默认开启）
- 新增 GLM-5.1（混合思考默认开启，支持上下文缓存）
- 新增 Kimi K2.6（混合思考默认关闭）
- 新增 MiniMax M2.7（稀宇科技部署，仅思考模式）
- 新增 Qwen3-Coder（qwen3-coder-plus/flash，代码专用）
- 新增 Qwen-Turbo（轻量级，默认非思考模式）
- 新增 Qwen3-Next MoE 架构（80B参数，3B激活）
- 新增角色扮演模型（qwen-plus-character、qwen-flash-character）
- 新增 Qwen3.6-Flash 快照版（qwen3.6-flash-2026-04-16）
- 新增 Qwen3.5-Plus 快照版（qwen3.5-plus-2026-04-20）
- 联网搜索新增 qwen3.5-omni、qwen3.5-omni-realtime 支持
- DeepThinking 文档中 Qwen3.6-Flash 默认开启思考模式

### 2026-04-12
- Qwen3.6-Max-Preview、Qwen3.6-Plus/Flash、千问 Omni/Omni-Realtime 首次记录