# 错误码（Error Codes）

> 更新时间：2026-04-12
> 来源：https://help.aliyun.com/zh/model-studio/error-code

---

## 400 — 参数错误（InvalidParameter）

### 思考模式相关

| 错误信息 | 原因 | 解决方案 |
|----------|------|----------|
| `parameter.enable_thinking must be set to false for non-streaming calls` | 非流式输出调用思考模式模型 | 将 `enable_thinking` 设为 `false`，或改用流式输出 |
| `The incremental_output parameter must be "true" when enable_thinking is true` | 开启思考模式时未设置增量输出 | 将 `incremental_output` 设为 `true` |
| `The thinking_budget parameter must be a positive integer and not greater than xxx` | thinking_budget 超出范围 | 设置为 >0 且不超过模型最大思维链长度 |
| `The value of the enable_thinking parameter is restricted to True` | 仅思考模型不允许关闭思考 | 将 `enable_thinking` 设为 `true` |
| `Json mode response is not supported when enable_thinking is true` | 思考模式下不支持结构化输出 | 将 `enable_thinking` 设为 `false` |

### 联网搜索

| 错误信息 | 原因 | 解决方案 |
|----------|------|----------|
| `This model does not support enable_search.` | 模型不支持联网搜索 | 更换支持联网搜索的模型 |
| `Tool names are not allowed to be [search]` | 工具名称设为 search | 工具名称设为 search 之外的值 |

### 输入长度

| 错误信息 | 原因 | 解决方案 |
|----------|------|----------|
| `Range of input length should be [1, xxx]` | 输入内容超过模型上限 | 控制 messages 中的 Token 数在模型范围内 |
| `Range of max_tokens should be [1, xxx]` | max_tokens 超出范围 | 参考模型列表中的"最大输出 Token 数" |

### 参数范围

| 错误信息 | 原因 | 解决方案 |
|----------|------|----------|
| `Temperature should be in [0.0, 2.0)` | temperature 超出范围 | 设置为 0 ~ 2 之间的数字 |
| `Range of top_p should be (0.0, 1.0]` | top_p 超出范围 | 设置为 0 ~ 1 之间的数字 |
| `Presence_penalty should be in [-2.0, 2.0]` | presence_penalty 超出范围 | 设置为 -2.0 ~ 2.0 之间 |
| `Repetition_penalty should be greater than 0.0` | repetition_penalty ≤ 0 | 设置为 > 0 的数字 |
| `Range of n should be [1, 4]` | n 超出范围 | 设置为 1 ~ 4 |
| `Range of seed should be [0, 9223372036854775807]` | seed 超出范围（DashScope 协议） | 设置在规定范围内 |

### 请求格式

| 错误信息 | 原因 | 解决方案 |
|----------|------|----------|
| `messages with role "tool" must be a response to a preceeding message with "tool_calls"` | 工具调用时未添加 Assistant Message | 先将 Assistant Message 添加到 messages 再添加 Tool Message |
| `Required body invalid, please check the request body format.` | 请求体格式错误 | 检查 JSON 格式（逗号、括号等） |
| `input content must be a string.` | 纯文本模型 content 设为非字符串 | 不要将 content 设置为数组类型 |
| `The content field is a required field.` | 未指定 content 参数 | 指定 content 参数 |
| `[] is too short` | messages 为空数组 | 添加 message 后再请求 |
| `Either "prompt" or "messages" must exist` | 未指定 messages 或 prompt | 指定 messages 参数 |
| `Input should be a valid dictionary or instance of GPT3Message` | messages 格式错误 | 检查 JSON 结构 |
| `Value error, contents is neither str nor list of str.` | Embedding 输入格式错误 | 修改为字符串或字符串列表 |

### 结构化输出

| 错误信息 | 原因 | 解决方案 |
|----------|------|----------|
| `'messages' must contain the word 'json' in some form` | 提示词中不含 json 关键词 | 在提示词中加入 "json"（不区分大小写） |
| `Unknown format of response_format` | response_format 格式不正确 | 设置为 `{"type": "json_object"}` |

### 模型相关

| 错误信息 | 原因 | 解决方案 |
|----------|------|----------|
| `Model not exist.` | model 参数不存在或格式不正确 | 检查模型名称（大小写、空格），对照模型列表 |
| `The tool call is not supported.` | 模型不支持 tools 参数 | 更换为支持 Function Calling 的 Qwen 或 DeepSeek 模型 |
| `tool_choice is one of the strings that should be ["none", "auto"]` | tool_choice 参数错误 | 设为 "auto" 或 "none" |
| `The result_format parameter must be "message" when enable_thinking is true` | 思考模式未设置 result_format | 将 result_format 设为 "message" |

### 文件相关

| 错误信息 | 原因 | 解决方案 |
|----------|------|----------|
| `File parsing in progress, please try again later.` | Qwen-Long 文件未完成解析 | 等待解析完成后重试 |
| `File [id:file-fe-xxx] format is not supported.` | 文件格式不支持 | Qwen-Long 仅支持纯文本（TXT/DOCX/PDF/EPUB/MOBI/MD），不支持图片 |
| `File [id:file-fe-xxx] cannot be found.` | 文件已被删除 | 等待模型完成对话后再删除文件 |
| `Too many files provided.` | file-id 数量超限 | 确保 < 100 个 |
| `File [id:file-fe-xxx] exceeds size limit.` | 文件大小超限 | 确保 < 150 MB |
| `File [id:file-fe-xxx] exceeds page limits (15000 pages).` | 页数超限 | 确保 < 15000 页 |
| `File [id:file-fe-xxx] content blank.` | 文件内容为空 | 确保内容不为空 |
| `Total message token length exceed model limit (10000000 tokens).` | 输入超过 10,000,000 Token | 控制 message 长度 |
| `Invalid file [id:file-fe-xxx].` | file-id 无效 | 确认 file-id 是否有效或重新上传 |

### 多模态相关

| 错误信息 | 原因 | 解决方案 |
|----------|------|----------|
| `The provided URL does not appear to be valid.` | URL 或本地路径无效 | URL 需以 `http://`、`https://`、`data:` 开头；本地路径以 `file://` 开头 |
| `Exceeded limit on max bytes per data-uri item : 10485760` | Base64 编码文件 > 10MB | 压缩文件，或改用公网 URL |
| `Failed to download multimodal content.` | 服务端无法下载公网 URL 文件 | 使用同地域 OSS 公网链接，避免内网地址 |
| `Don't have authorization to access the media resource` | OSS 签名 URL 已过期 | 在有效期内访问文件 |
| `Failed to decode the image during the data inspection.` | 图像解码失败 | 确认图像格式和完整性 |
| `The image length and width do not meet the model restrictions.` | 图像尺寸不符合要求 | 宽度和高度 ≥ 10 像素，宽高比 ≤ 200:1 |
| `The video modality input does not meet the requirements` | 图像数量不符合要求 | Qwen3-VL/Qwen2.5-VL：4-512 张；其他：4-80 张 |
| `The video file is too long.` | 视频时长超限 | Qwen2.5-VL：2秒~10分钟；其他：2秒~40秒 |
| `Input should be 'Cherry', 'Serena', 'Ethan' or 'Chelsie'` | voice 参数错误 | 设为四个有效值之一 |
| `The audio is empty` | 音频时间过短 | 增加音频时长 |

### URL 错误

| 错误信息 | 原因 | 解决方案 |
|----------|------|----------|
| `url error, please check url！` | 模型名称与 API 端点不匹配，或 SDK 版本过低 | 多模态模型使用 `MultiModalConversation.call()` 或 `multimodal-generation` 端点；纯文本模型使用 `Generation.call()` 或 `text-generation` 端点；升级 SDK |

---

## 401 — 认证错误

| 错误信息 | 原因 | 解决方案 |
|----------|------|----------|
| `InvalidApiKey` | API Key 无效 | 检查 API Key 是否正确配置 |

---

## 403 — 权限错误

| 错误信息 | 原因 | 解决方案 |
|----------|------|----------|
| `Arrearage` | 账号欠费 | 充值后重试 |

---

## 429 — 限流

| 错误信息 | 原因 | 解决方案 |
|----------|------|----------|
| `Requests rate limit exceeded` | 调用频率触发限流 | 降低调用频率 |
| `Allocated quota exceeded` | Token 消耗触发限流 | 缩短输入或输出长度 |
| `Request rate increased too quickly` | 调用频率激增触发保护 | 采用匀速调度、指数退避策略 |

详见 [限流文档](https://help.aliyun.com/zh/model-studio/rate-limit)

---

## 500/503 — 服务端错误

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| 500 | 内部错误 | 稍后重试 |
| 503 | 服务不可用 | 稍后重试 |
| 504 | 网关超时 | 稍后重试 |

---

## Python 错误处理示例

```python
from openai import OpenAI, APIError, RateLimitError, AuthenticationError

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

try:
    completion = client.chat.completions.create(
        model="qwen-plus",
        messages=[{"role": "user", "content": "你好"}]
    )
except AuthenticationError as e:
    print(f"认证失败: {e.message}")
except RateLimitError as e:
    print(f"频率限制: {e.message}")
except APIError as e:
    print(f"API 错误: {e.message}")
```

---

## 快速排查

推荐使用 [阿里云 AI 助理](https://www.aliyun.com/ai-assistant/)，输入错误信息即可获取解决方案。
