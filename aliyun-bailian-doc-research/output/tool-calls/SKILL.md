# 工具调用（Tool Calls / Function Calling）

> 更新时间：2026-04-12
> 来源：https://help.aliyun.com/zh/model-studio/tool-calls、https://help.aliyun.com/zh/model-studio/function-calling

---

## 概述

工具调用（Function Calling）让大模型能够识别何时需要调用外部函数，并自动生成函数调用的参数。适用于：
- 智能体（Agent）开发
- 外部 API 集成
- 数据库查询
- 实时数据获取

---

## 支持的工具调用方式

### 1. Chat Completions API — 内置工具调用

通过 `tools` 参数注册工具，模型自动决定是否调用。

```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取指定城市的天气信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "城市名称"},
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}
                },
                "required": ["city"]
            }
        }
    }
]

completion = client.chat.completions.create(
    model="qwen-plus",
    messages=[{"role": "user", "content": "杭州明天天气怎么样？"}],
    tools=tools,
    tool_choice="auto"  # 或 "none" / {"type": "function", "function": {"name": "get_weather"}}
)

# 检查模型是否选择了工具调用
if completion.choices[0].message.tool_calls:
    for tool_call in completion.choices[0].message.tool_calls:
        print(f"调用函数: {tool_call.function.name}")
        print(f"参数: {tool_call.function.arguments}")
```

### 2. Assistant API — 智能体工具调用

通过 Assistant API 创建智能体，注册工具后自动处理调用流程。

```python
from dashscope import Assistants, Messages, Runs, Threads
import json

# 定义工具
weather_tool = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "获取指定城市的天气信息",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string"},
            },
            "required": ["city"]
        }
    }
}

# 创建智能体
assistant = Assistants.create(
    model='qwen-plus',
    name='天气助手',
    description='一个能够查询天气的智能体',
    instructions='你是一个天气助手。当用户询问天气时，使用 get_weather 函数查询。',
    tools=[weather_tool]
)

# 创建对话线程
thread = Threads.create()

# 添加用户消息
Messages.create(
    thread_id=thread.id,
    role="user",
    content="杭州明天天气怎么样？"
)

# 运行智能体
run = Runs.create(thread_id=thread.id, assistant_id=assistant.id)
run = Runs.wait(thread_id=thread.id, run_id=run.id)

# 处理函数调用
if run.required_action:
    for tool_call in run.required_action.submit_tool_outputs.tool_calls:
        if tool_call.function.name == "get_weather":
            args = json.loads(tool_call.function.arguments)
            result = get_weather(args["city"])  # 调用你的函数
            
            # 提交结果
            Runs.submit_tool_outputs(
                thread_id=thread.id,
                run_id=run.id,
                tool_outputs=[{"tool_call_id": tool_call.id, "output": result}]
            )
            run = Runs.wait(thread_id=thread.id, run_id=run.id)

# 获取回复
messages = Messages.list(thread_id=thread.id)
for message in messages.data:
    if message.role == "assistant":
        print(f"Assistant: {message.content[0].text.value}")
```

### 3. 联网搜索工具

通过 `tools` 参数启用内置搜索（无需外部函数）。

```python
response = client.responses.create(
    model="qwen3-max-2026-01-23",
    input="杭州天气",
    tools=[
        {"type": "web_search"},       # 联网搜索
        {"type": "web_extractor"},    # 网页抓取
        {"type": "code_interpreter"}  # 代码执行
    ],
    extra_body={"enable_thinking": True}
)
```

---

## 支持的模型

### 工具调用（Function Calling）

| 类别 | 模型 |
|------|------|
| 千问 Max | `qwen3-max`、`qwen-max` |
| 千问 Plus | `qwen3.6-plus`、`qwen3.5-plus`、`qwen-plus` |
| 千问 Flash | `qwen3.5-flash`、`qwen-flash` |
| 千问 Turbo | `qwen-turbo` |
| 第三方 | DeepSeek V3.2、Kimi K2.5、GLM-5、MiniMax M2.5 |

### 联网搜索工具

| 类别 | 模型 |
|------|------|
| 千问 Max | `qwen3-max`（Responses API 支持） |
| 千问 Plus | `qwen3.6-plus`（仅 Responses API）、`qwen3.5-plus`、`qwen-plus` |
| 千问 Flash | `qwen3.5-flash`、`qwen-flash` |
| 第三方 | DeepSeek V3.2、Kimi K2.5、MiniMax M2.1 |

---

## 工具定义格式

### Python 工具 Schema
```python
tool = {
    "type": "function",
    "function": {
        "name": "function_name",
        "description": "函数描述",
        "parameters": {
            "type": "object",
            "properties": {
                "param1": {"type": "string", "description": "参数1描述"},
                "param2": {"type": "integer", "description": "参数2描述"}
            },
            "required": ["param1"]
        }
    }
}
```

### 自动生成 Schema（从 Python 函数）
```python
import inspect

def function_to_schema(func) -> dict:
    type_map = {
        str: "string", int: "integer", float: "number",
        bool: "boolean", list: "array", dict: "object",
        type(None): "null",
    }
    signature = inspect.signature(func)
    parameters = {}
    for param in signature.parameters.values():
        parameters[param.name] = {"type": type_map.get(param.annotation, "string")}
    required = [p.name for p in signature.parameters.values()
                if p.default == inspect._empty]
    return {
        "type": "function",
        "function": {
            "name": func.__name__,
            "description": (func.__doc__ or "").strip(),
            "parameters": {"type": "object", "properties": parameters, "required": required},
        },
    }

# 使用
weather_tool = function_to_schema(get_weather)
```

---

## 最佳实践

1. **工具描述要清晰准确** — 模型依赖 description 决定是否调用
2. **参数类型要明确** — 使用正确的 JSON Schema 类型
3. **tool_choice 控制** — `"auto"` 让模型决定，`"none"` 禁用，`{"type":"function","function":{"name":"xxx"}}` 强制调用
4. **Assistant API 适合复杂智能体** — Chat Completions 适合简单工具调用
5. **处理流式输出时需额外循环** — 提交工具输出后会生成新的 Run 对象
