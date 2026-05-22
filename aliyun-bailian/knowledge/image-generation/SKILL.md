# 图像生成（Image Generation）

> 更新时间：2026-04-12
> 来源：https://help.aliyun.com/zh/model-studio/text-to-image

---

## 概述

阿里云百炼提供千问（Qwen-Image）和万相（Wan）两大系列的文生图模型，支持同步和异步调用。

**Base URL（DashScope 原生接口）：**
- 北京：`https://dashscope.aliyuncs.com/api/v1`
- 新加坡：`https://dashscope-intl.aliyuncs.com/api/v1`

---

## 模型矩阵

| 模型 | 特点 | 调用方式 | 分辨率 |
|------|------|----------|--------|
| **wan2.7-image-pro** | 功能最全面，支持组图生成、4096×4096 分辨率，增强五官/色彩/超长文字控制 | 异步+同步 | 最高 4096×4096 |
| **qwen-image-2.0-pro** | 擅长文本渲染，精准生成中英文，适合图表/海报/PPT | 同步（Plus/Flash 也支持异步） | 2K |
| **z-image-turbo** | 速度最快、成本最低，擅长高逼真度人像与产品图 | 同步 | 标准 |

---

## 模型选型决策

```
需要什么？
├── 文字渲染/海报/PPT → qwen-image-2.0-pro
├── 组图生成/最高画质 → wan2.7-image-pro
├── 极致速度/性价比 → z-image-turbo
└── 通用文生图 → wan2.7-image-pro（推荐）
```

---

## 快速开始

### 万相 — 异步调用（推荐）

适用于所有万相模型。

#### Python
```python
import os
import dashscope
from dashscope.aigc.image_generation import ImageGeneration
from dashscope.api_entities.dashscope_response import Message

dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

message = Message(
    role="user",
    content=[{"text": "一间有着精致窗户的花店，漂亮的木质门，摆放着花朵"}]
)

# 提交异步任务
response = ImageGeneration.async_call(
    model="wan2.7-image-pro",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    messages=[message],
    enable_sequential=False,
    n=1,
    size="2K"
)

# 等待任务完成
status = ImageGeneration.wait(task=response, api_key=os.getenv("DASHSCOPE_API_KEY"))
if status.output.task_status == "SUCCEEDED":
    print(status.output.choices[0].message.content[0]["image"])
```

#### curl
```bash
# 步骤1：发起创建任务
curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/image-generation/generation \
-H 'Content-Type: application/json' \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "X-DashScope-Async: enable" \
-d '{
    "model": "wan2.7-image-pro",
    "input": {
        "messages": [{"role": "user", "content": [{"text": "一间有着精致窗户的花店"}]}]
    },
    "parameters": {"size": "2K", "n": 1, "watermark": false, "thinking_mode": true}
}'

# 步骤2：根据 task_id 查询结果
curl -X GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id} \
-H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

### 千问 — 同步调用

#### Python
```python
import os
import dashscope
from dashscope import MultiModalConversation

dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

response = MultiModalConversation.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model="qwen-image-2.0-pro",
    messages=[{"role": "user", "content": [{"text": "冬日北京的都市街景"}]}],
    result_format='message',
    stream=False,
    watermark=False,
    prompt_extend=True,
    negative_prompt="低分辨率，低画质，肢体畸形，画面过饱和，蜡像感",
    size='2048*2048'
)

if response.status_code == 200:
    print(response.output.choices[0].message.content[0]["image"])
```

---

## 关键参数

| 参数 | 说明 | 取值 |
|------|------|------|
| `size` | 图像分辨率 | `"1K"`, `"2K"`, `"2048*2048"` 等 |
| `n` | 生成数量 | 1-4 |
| `watermark` | 是否添加水印 | `true`/`false` |
| `prompt_extend` | 是否扩展提示词 | `true`/`false` |
| `negative_prompt` | 负面提示词 | 文本 |
| `thinking_mode` | 是否开启思考模式（万相） | `true`/`false` |
| `enable_sequential` | 是否启用连续组图生成 | `true`/`false` |

---

## 注意事项

1. **图像链接有效期 24 小时**，请及时下载
2. **万相模型支持异步调用**，wan2.7-image-pro 等也支持同步调用
3. **千问模型均支持同步调用**，qwen-image-plus/Flash 也支持异步
4. **task_id 查询有效期 24 小时**，过期后状态变为 UNKNOWN

---

## 支持的模型

### 千问文生图
- `qwen-image-2.0-pro`
- `qwen-image-plus`
- `qwen-image`

### 万相文生图
- `wan2.7-image-pro`
- `wan2.7-image`
- `wan2.6-image`
- `wan2.6-t2i`
- `z-image-turbo`

### 万相图像生成与编辑
- 支持图生图、图像编辑等功能，详见[万相 API 参考](https://help.aliyun.com/zh/model-studio/wan-image-generation-and-editing-api-reference)
