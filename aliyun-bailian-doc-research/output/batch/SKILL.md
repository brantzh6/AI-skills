# Batch 批量调用

> 更新时间：2026-04-12
> 来源：https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/

---

## 概述

百炼提供与 OpenAI 兼容的 Batch File API，以文件方式批量提交任务，系统异步执行。**费用仅为实时调用的 50%**。适用于数据分析、模型评测等对时效性要求不高的场景。

---

## 支持的模型

### 中国内地

**文本生成模型：**
- 千问 Max：qwen3-max、qwen-max、qwen-max-latest
- 千问 Plus：qwen3.6-plus、qwen3.5-plus、qwen-plus、qwen-plus-latest
- 千问 Flash：qwen3.5-flash、qwen-flash
- 千问 Turbo：qwen-turbo、qwen-turbo-latest
- 千问 Long：qwen-long、qwen-long-latest
- QwQ：qwq-plus
- 第三方：deepseek-r1、deepseek-v3.2、deepseek-v3

**多模态模型：**
- 图像与视频理解：qwen3.6-plus、qwen3.5-plus、qwen3.5-flash、qwen3-vl-plus、qwen3-vl-flash、qwen-vl-max、qwen-vl-plus
- 文字提取：qwen-vl-ocr、qwen-vl-ocr-latest
- 全模态：qwen-omni-turbo

**文本向量模型：**
- text-embedding-v1、v2、v3、v4

### 国际（新加坡）

- qwen-max、qwen-plus、qwen-turbo

---

## 快速开始

### 测试模型

可使用 `batch-test-model` 进行全链路测试。该模型跳过推理过程，直接返回固定响应，用于验证 API 调用链路和数据格式。

**测试模型限制：**
- 文件大小 ≤ 1 MB，行数 ≤ 100 行
- 最大并行任务数 2 个
- 不产生模型推理费用

### 第 1 步：准备输入文件

JSONL 格式，每行一个请求：

```jsonl
{"custom_id":"1","method":"POST","url":"/v1/chat/completions","body":{"model":"qwen-plus","messages":[{"role":"system","content":"You are a helpful assistant."},{"role":"user","content":"你好"}]}}
{"custom_id":"2","method":"POST","url":"/v1/chat/completions","body":{"model":"qwen-plus","messages":[{"role":"system","content":"You are a helpful assistant."},{"role":"user","content":"What is 2+2?"}]}}
```

**多模态模型**支持文件 URL 和 Base64 编码：

```jsonl
{"custom_id":"image-url","method":"POST","url":"/v1/chat/completions","body":{"model":"qwen-vl-plus","messages":[{"role":"user","content":[{"type":"image_url","image_url":{"url":"https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg"}},{"type":"text","text":"请描述这张图片"}]}]}}
```

### 第 2 步：运行代码

```python
import os
from pathlib import Path
from openai import OpenAI
import time

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

# Step 1: 上传 JSONL 文件
file_object = client.files.create(file=Path("input.jsonl"), purpose="batch")
input_file_id = file_object.id
print(f"文件上传成功: {input_file_id}")

# Step 2: 创建 Batch 任务
# endpoint 参数需与输入文件中的 url 字段一致
batch = client.batches.create(
    input_file_id=input_file_id,
    endpoint="/v1/chat/completions",
    completion_window="24h"
)
batch_id = batch.id
print(f"Batch 任务创建: {batch_id}")

# Step 3: 轮询任务状态
while batch.status not in ["completed", "failed", "expired", "cancelled"]:
    time.sleep(10)
    batch = client.batches.retrieve(batch_id)
    print(f"状态: {batch.status}")

# Step 4: 下载结果
if batch.output_file_id:
    content = client.files.content(batch.output_file_id)
    content.write_to_file("result.jsonl")
    print(f"成功结果已保存至 result.jsonl")

if batch.error_file_id:
    error_content = client.files.content(batch.error_file_id)
    error_content.write_to_file("error.jsonl")
    print(f"错误信息已保存至 error.jsonl")
```

---

## 关键参数

| 参数 | 说明 | 取值 |
|------|------|------|
| `input_file_id` | 上传的输入文件 ID | `file-xxx` |
| `endpoint` | API 端点 | `/v1/chat/completions`、`/v1/embeddings`、`/v1/chat/ds-test`（测试模型） |
| `completion_window` | 最长等待时间 | `24h` |

---

## 注意事项

1. **Batch 场景下**，qwen3.6-plus、qwen3.5-plus、qwen3.5-flash 单次请求最大支持 **256K 输入 Token**
2. 部分模型开启思考模式后会产生思考 tokens，增加成本
3. qwen3.6-plus 和 qwen3.5 系列默认开启思考模式，建议显式设置 `enable_thinking`
4. 任务完成后输出文件和错误文件有效期 24 小时
5. 详见 [Batch 接口文档](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)
