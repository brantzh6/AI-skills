# 深度思考（Deep Thinking）用法

> 来源：https://help.aliyun.com/zh/model-studio/deep-thinking

---

## 概述

深度思考模型在回复前会进行推理过程，输出包含两个部分：
- `reasoning_content` — 思考过程（模型的内部推理）
- `content` — 最终回复内容

---

## 两种思考模式

### 1. 混合思考模式（Hybrid Thinking）

通过 `enable_thinking` 参数控制开关：

| 参数值 | 行为 |
|--------|------|
| `True` | 模型先思考再回复 |
| `False` | 模型直接回复，不思考 |

### 2. 仅思考模式（Thinking Only）

模型始终在回复前进行思考，无法关闭。无需设置 `enable_thinking` 参数。

---

## 支持的模型及默认行为

| 模型系列 | 默认思考 | 模型列表 |
|----------|----------|----------|
| **Qwen3.6** | ✅ 默认开启 | `qwen3.6-plus`、`qwen3.6-plus-2026-04-02` |
| **Qwen3.5-Plus** | ✅ 默认开启 | `qwen3.5-plus`、`qwen3.5-plus-2026-02-15` |
| **Qwen3.5-Flash** | ✅ 默认开启 | `qwen3.5-flash`、`qwen3.5-flash-2026-02-23` |
| **Qwen3-Max** | ❌ 默认关闭 | `qwen3-max`、`qwen3-max-2026-01-23`、`qwen3-max-preview` |
| **Qwen-Plus** | ❌ 默认关闭 | `qwen-plus`、`qwen-plus-latest` 及之后快照 |
| **Qwen-Flash** | ❌ 默认关闭 | `qwen-flash`、`qwen-flash-2025-07-28` 及之后快照 |
| **Qwen-Turbo** | ❌ 默认关闭 | `qwen-turbo`、`qwen-turbo-latest` 及之后快照 |
| **QwQ** | 仅思考 | `qwq-plus`、`qwq-plus-latest`、`qwq-32b` |
| **DeepSeek V3** | ❌ 默认关闭 | `deepseek-v3.2`、`deepseek-v3.1` |
| **DeepSeek R1** | 仅思考 | `deepseek-r1`、`deepseek-r1-0528` |
| **Kimi K2.5** | ❌ 默认关闭 | `kimi-k2.5` |
| **Kimi K2** | 仅思考 | `kimi-k2-thinking` |
| **GLM** | ✅ 默认开启 | `glm-5`、`glm-4.7`、`glm-4.6`、`glm-4.5`、`glm-4.5-air` |

**开源版（默认开启思考）：**
- `qwen3.5-397b-a17b`、`qwen3.5-122b-a10b`、`qwen3.5-27b`、`qwen3.5-35b-a3b`
- `qwen3-235b-a22b`、`qwen3-32b`、`qwen3-30b-a3b`、`qwen3-14b`、`qwen3-8b`

**仅思考版模型：**
- `qwen3-next-80b-a3b-thinking`
- `qwen3-235b-a22b-thinking-2507`
- `qwen3-30b-a3b-thinking-2507`

---

## 调用方式

### OpenAI 兼容（Chat Completions API）

#### Python
```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="qwen-plus",
    messages=[{"role": "user", "content": "你是谁"}],
    # enable_thinking 非 OpenAI 标准参数，需通过 extra_body 传入
    extra_body={"enable_thinking": True},
    # 流式输出
    stream=True,
    stream_options={"include_usage": True},
)

reasoning_content = ""
answer_content = ""
is_answering = False

for chunk in completion:
    if not chunk.choices:
        continue
    delta = chunk.choices[0].delta
    
    # 收集思考内容
    if hasattr(delta, "reasoning_content") and delta.reasoning_content:
        if not is_answering:
            print(delta.reasoning_content, end="", flush=True)
        reasoning_content += delta.reasoning_content
    
    # 收集回复内容
    if hasattr(delta, "content") and delta.content:
        if not is_answering:
            is_answering = True
        print(delta.content, end="", flush=True)
        answer_content += delta.content
```

#### Node.js
```javascript
import OpenAI from "openai";

const openai = new OpenAI({
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: 'https://dashscope.aliyuncs.com/compatible-mode/v1'
});

const stream = await openai.chat.completions.create({
    model: 'qwen-plus',
    messages: [{ role: 'user', content: '你是谁' }],
    stream: true,
    enable_thinking: true  // Node.js 可直接作为顶层参数
});

for await (const chunk of stream) {
    const delta = chunk.choices[0].delta;
    if (delta.reasoning_content) {
        process.stdout.write(delta.reasoning_content);
    }
    if (delta.content) {
        process.stdout.write(delta.content);
    }
}
```

#### curl
```bash
curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen-plus",
    "messages": [{"role": "user", "content": "你是谁"}],
    "stream": true,
    "stream_options": {"include_usage": true},
    "enable_thinking": true
}'
```

### DashScope 原生接口

#### Python
```python
import os
from dashscope import Generation

completion = Generation.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model="qwen-plus",
    messages=[{"role": "user", "content": "你是谁？"}],
    result_format="message",
    enable_thinking=True,
    stream=True,
    incremental_output=True,
)

reasoning_content = ""
answer_content = ""
is_answering = False

for chunk in completion:
    reasoning = chunk.output.choices[0].message.reasoning_content
    content = chunk.output.choices[0].message.content
    
    if reasoning:
        print(reasoning, end="", flush=True)
        reasoning_content += reasoning
    elif content:
        if not is_answering:
            is_answering = True
        print(content, end="", flush=True)
        answer_content += content
```

#### Java
```java
// dashscope SDK >= 2.19.4
GenerationParam param = GenerationParam.builder()
    .apiKey(System.getenv("DASHSCOPE_API_KEY"))
    .model("qwen-plus")
    .enableThinking(true)  // 开启思考
    .incrementalOutput(true)
    .resultFormat("message")
    .messages(Arrays.asList(userMsg))
    .build();
```

---

## 注意事项

1. **流式输出**：深度思考模型多数仅支持流式输出，因为等待回复时间变长
2. **Token 消耗**：思考过程会计入 `completion_tokens`，增加成本
3. **Qwen3.5 系列**：DashScope API 采用多模态接口，调用方式参见[视觉理解文档](https://help.aliyun.com/zh/model-studio/vision)
4. **Responses API**：使用 Responses API 时，深度思考通过 `enable_thinking` 参数控制，思考内容通过 `output` 中的 `reasoning` 字段返回

---

## 适用场景

| 场景 | 推荐策略 | 推荐模型 |
|------|----------|----------|
| 复杂数学题 | 开启思考 | qwen3-max、deepseek-r1 |
| 代码调试 | 开启思考 | qwen3-coder-plus |
| 逻辑推理 | 开启思考 | qwen3.6-plus、glm-5 |
| 日常对话 | 关闭思考 | qwen-plus、qwen-flash |
| 创意写作 | 关闭思考 | qwen-plus |
| 学术研究 | 开启思考（max 策略） | qwen3.5-plus、deepseek-r1 |
