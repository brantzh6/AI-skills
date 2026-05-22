# 上下文缓存（Context Cache）

> 来源：https://help.aliyun.com/zh/model-studio/context-cache

---

## 概述

上下文缓存技术缓存请求的公共前缀，减少推理时的重复计算。适用于：
- 对同一长文档的多次提问
- 持续多轮对话
- 固定 System Prompt + 不同 User 输入

---

## 两种工作模式

| 特性 | 显式缓存（Explicit） | 隐式缓存（Implicit） |
|------|---------------------|---------------------|
| **是否需要配置** | 需要手动添加 `cache_control` 标记 | 自动，无需配置 |
| **创建成本** | 输入 Token 单价的 **125%** | 输入 Token 单价的 **100%** |
| **命中成本** | 输入 Token 单价的 **10%** | 输入 Token 单价的 **20%** |
| **最小 Token** | 1024 | 256 |
| **有效期** | 5 分钟（命中后重置） | 不确定，系统定期清理 |
| **命中率** | 确定性命中 | 不确定 |
| **能否关闭** | 可选开启 | 无法关闭 |

**两者互斥**：单个请求只能应用一种模式。

---

## 显式缓存 — 用法

### 原理

在 `messages` 的 `content` 中添加 `"cache_control": {"type": "ephemeral"}` 标记。

- **未命中**：系统创建新缓存块，有效期 5 分钟
- **命中**：选取最长匹配前缀，重置有效期为 5 分钟

### Python（OpenAI 兼容）

```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# 长文本内容（需 > 1024 Token）
long_text_content = "<Your Code Here>" * 400

def get_completion(user_input):
    messages = [
        {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": long_text_content,
                    "cache_control": {"type": "ephemeral"}  # 缓存标记
                }
            ],
        },
        {"role": "user", "content": user_input},
    ]
    return client.chat.completions.create(
        model="qwen3-coder-plus",  # 需使用支持显式缓存的模型
        messages=messages,
    )

# 第一次请求：创建缓存
first = get_completion("这段代码的内容是什么")
print(f"创建缓存 Token: {first.usage.prompt_tokens_details.cache_creation_input_tokens}")
print(f"命中缓存 Token: {first.usage.prompt_tokens_details.cached_tokens}")
# 输出: 创建=1605, 命中=0

# 第二次请求：命中缓存
second = get_completion("这段代码怎么优化")
print(f"创建缓存 Token: {second.usage.prompt_tokens_details.cache_creation_input_tokens}")
print(f"命中缓存 Token: {second.usage.prompt_tokens_details.cached_tokens}")
# 输出: 创建=0, 命中=1605
```

### 多缓存标记（精细控制）

单次请求最多支持 **4 个缓存标记**。

适用于提示词由多个稳定/变化频率不同的部分组成：

```python
messages = [
    {
        "role": "system",
        "content": [
            {"type": "text", "text": system_prompt, "cache_control": {"type": "ephemeral"}},
        ],
    },
    {
        "role": "user",
        "content": [
            {"type": "text", "text": knowledge_base, "cache_control": {"type": "ephemeral"}},
            {"type": "text", "text": conversation_history},  # 不缓存，变化太快
            {"type": "text", "text": current_question},      # 不缓存，每次不同
        ],
    },
]
```

**典型场景：智能客服**
- 系统人设（稳定）→ 缓存
- 外部知识（半稳定）→ 缓存
- 对话历史（动态增长）→ 不缓存
- 当前问题（每次不同）→ 不缓存

---

## 显式缓存 — 计费规则

| 操作 | 计费 | 查看参数 |
|------|------|----------|
| 创建缓存 | 标准输入单价 × 125% | `cache_creation_input_tokens` |
| 命中缓存 | 标准输入单价 × 10% | `cached_tokens` |
| 其他 Token | 标准单价 | — |

**增量创建计费：** 若新缓存包含已有缓存作为前缀，仅对新增部分按 125% 计费。

示例：已有 1200 Token 的缓存 A，新请求需缓存 1500 Token 的 AB：
- 前 1200 Token（命中 A）：按 10% 计费
- 新增 300 Token（创建 B）：按 125% 计费

---

## 显式缓存 — 缓存限制

1. **最小长度**：1024 Token
2. **匹配策略**：从后向前前缀匹配，检查最近 20 个 content 块
3. **有效期**：5 分钟（`ephemeral`）
4. **单次最多**：4 个缓存标记
5. **支持的消息类型**：System、User、Assistant、Tool
6. **支持的工具描述**：若请求包含 `tools` 参数，也会缓存工具描述

---

## 支持的模型

### 中国内地

| 类别 | 模型 |
|------|------|
| 千问 Max | `qwen3-max` |
| 千问 Plus | `qwen3.6-plus`、`qwen3.5-plus`、`qwen-plus` |
| 千问 Flash | `qwen3.5-flash`、`qwen-flash` |
| 千问 Coder | `qwen3-coder-plus`、`qwen3-coder-flash` |
| 千问 VL | `qwen3-vl-plus`、`qwen3-vl-flash` |
| DeepSeek | `deepseek-v3.2` |
| Kimi | `kimi-k2.5` |

### 全球

| 类别 | 模型 |
|------|------|
| 千问 Max | `qwen3-max` |
| 千问 Plus | `qwen3.6-plus`、`qwen3.5-plus`、`qwen-plus` |
| 千问 Flash | `qwen3.5-flash`、`qwen-flash` |
| 千问 Coder | `qwen3-coder-plus`、`qwen3-coder-flash` |
| 千问 VL | `qwen3-vl-plus` |

### 国际（新加坡）

| 类别 | 模型 |
|------|------|
| 千问 Max | `qwen3-max` |
| 千问 Plus | `qwen3.6-plus`、`qwen3.5-plus`、`qwen-plus` |
| 千问 Flash | `qwen3.5-flash`、`qwen-flash` |
| 千问 Coder | `qwen3-coder-plus`、`qwen3-coder-flash` |
| 千问 VL | `qwen3-vl-plus`、`qwen3-vl-flash` |
| DeepSeek | `deepseek-v3.2` |

---

## 隐式缓存

### 说明

- 自动模式，无需配置，无法关闭
- 系统自动识别请求内容的公共前缀并缓存
- 命中率不确定，系统定期清理
- 命中部分按标准输入单价的 **20%** 计费

### 支持的模型（中国内地）

| 类别 | 模型 |
|------|------|
| 千问 Max | `qwen3-max`、`qwen3-max-preview`、`qwen-max` |
| 千问 Plus | `qwen-plus` |
| 千问 Flash | `qwen-flash` |
| 千问 Turbo | `qwen-turbo` |
| 千问 Coder | `qwen3-coder-plus`、`qwen3-coder-flash` |
| DeepSeek | `deepseek-v3.2`、`deepseek-v3.1`、`deepseek-v3`、`deepseek-r1` |
| Kimi | `kimi-k2.5`、`kimi-k2-thinking`、`Moonshot-Kimi-K2-Instruct` |
| GLM | `glm-5`、`glm-4.7`、`glm-4.6` |
| MiniMax | `MiniMax-M2.5`、`MiniMax-M2.1` |
| 千问 VL | `qwen3-vl-plus`、`qwen3-vl-flash`、`qwen-vl-max`、`qwen-vl-plus` |

---

## 使用建议

### 何时使用显式缓存

- 对同一长文档（代码库、书籍、报告）的多次提问
- 固定 System Prompt + 不同 User 输入
- 持续多轮对话（每轮命中前一轮缓存）
- 需要确定性缓存命中率的场景

### 何时使用隐式缓存

- 通用场景，不想手动配置
- 请求之间有天然公共前缀
- 对命中率要求不高

### 最佳实践

```
推荐：固定前缀（System + 文档）用显式缓存，变化部分（User 输入）不缓存
避免：缓存内容 < 1024 Token（不会命中）
避免：cache_control 标记间超过 20 个 content 块（无法匹配）
```
