# 语音合成（TTS）

> 更新时间：2026-04-12
> 来源：https://help.aliyun.com/zh/model-studio/qwen-tts

---

## 概述

千问 TTS 支持流式输出、多语言/方言、丰富音色、声音复刻与声音设计、指令控制。

**Base URL（DashScope 原生接口）：**
- 北京：`https://dashscope.aliyuncs.com/api/v1`
- 新加坡：`https://dashscope-intl.aliyuncs.com/api/v1`

**SDK 版本要求：** DashScope Python SDK >= 1.24.6，Java SDK >= 2.21.9

---

## 核心功能

- 流式输出，边合成边播放
- 多语言覆盖（含中文方言）
- 丰富系统音色
- 声音复刻（基于音频样本）与声音设计（基于文本描述）
- 指令控制：通过自然语言指令控制语音表现力

---

## 支持的模型

### 中国内地

| 模型 | 版本 | 特点 |
|------|------|------|
| **qwen3-tts-instruct-flash** | 稳定版：`qwen3-tts-instruct-flash`（等同 2026-01-26） | 支持指令控制 |
| **qwen3-tts-vd** | `qwen3-tts-vd-2026-01-26` | 声音设计，无需音频样本 |
| **qwen3-tts-vc** | `qwen3-tts-vc-2026-01-22` | 声音复刻，基于音频样本 |
| **qwen3-tts-flash** | 稳定版：`qwen3-tts-flash`（等同 2025-11-27） | 按字符计费 |
| **qwen-tts** | 稳定版：`qwen-tts`（等同 2025-04-10） | 通用 |

### 国际（新加坡）

- qwen3-tts-instruct-flash、qwen3-tts-vd-2026-01-26、qwen3-tts-vc-2026-01-22、qwen3-tts-flash

---

## 模型选型

| 场景 | 推荐模型 | 理由 |
|------|----------|------|
| 品牌声音/音色设计（从零开始） | `qwen3-tts-vd-2026-01-26` | 无需音频，通过文本描述创建音色 |
| 品牌声音/音色复刻（有音频） | `qwen3-tts-vc-2026-01-22` | 基于真实音频复刻音色 |
| 有声书/广播剧/游戏配音 | `qwen3-tts-instruct-flash` | 支持指令控制，精确控制音调/语速/情感 |
| 移动端通知播报 | `qwen3-tts-flash` | 按字符计费，短文本高频调用 |
| 在线教育课件 | `qwen3-tts-flash` | 多语种与方言 |

---

## 系统音色

| 音色 | 风格 |
|------|------|
| Cherry | 女声 |
| Serena | 女声 |
| Ethan | 男声 |
| Chelsie | 女声 |

---

## 快速开始

### Python（非流式）

```python
import os
import dashscope

dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

response = dashscope.MultiModalConversation.call(
    model="qwen3-tts-flash",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    text="你好啊，我是千问",
    voice="Cherry",
    language_type="Chinese",
    stream=False
)
# response.output.audio.url 包含音频下载链接（有效期24小时）
```

### Python（流式输出）

```python
import pyaudio
import numpy as np
import base64

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=24000, output=True)

response = dashscope.MultiModalConversation.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model="qwen3-tts-flash",
    text="你好啊，我是千问",
    voice="Cherry",
    language_type="Chinese",
    stream=True
)

for chunk in response:
    if chunk.output and chunk.output.audio and chunk.output.audio.data:
        wav_bytes = base64.b64decode(chunk.output.audio.data)
        audio_np = np.frombuffer(wav_bytes, dtype=np.int16)
        stream.write(audio_np.tobytes())

stream.stop_stream()
stream.close()
p.terminate()
```

### curl

```bash
curl -X POST 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json' \
-d '{
    "model": "qwen3-tts-flash",
    "input": {
        "text": "你好啊，我是千问",
        "voice": "Cherry",
        "language_type": "Chinese"
    }
}'
```

---

## 指令控制（Instruct）

仅 `qwen3-tts-instruct-flash` 支持：

```python
response = dashscope.MultiModalConversation.call(
    model="qwen3-tts-instruct-flash",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    text="这款T恤真的超级好看！",
    voice="Cherry",
    language_type="Chinese",
    instructions='语速较快，带有明显的上扬语调，适合介绍时尚产品。',
    optimize_instructions=True,
    stream=False
)
```

---

## 关键参数

| 参数 | 说明 | 取值 |
|------|------|------|
| `text` | 待合成文本 | 字符串 |
| `voice` | 音色 | `Cherry`, `Serena`, `Ethan`, `Chelsie` |
| `language_type` | 语种 | `Chinese`, `English`, `Japanese` 等 |
| `instructions` | 指令控制（instruct 模型） | 自然语言描述 |
| `optimize_instructions` | 自动优化指令 | `true`/`false` |
| `stream` | 流式输出 | `true`/`false` |

---

## 注意事项

1. **音频 URL 有效期 24 小时**，请及时下载
2. **流式输出** 采样率 24000Hz，16bit PCM
3. **DashScope SDK 版本**：Python >= 1.24.6，Java >= 2.21.9
4. **新接口**：`MultiModalConversation` 已取代 `SpeechSynthesizer`
5. `language_type` 建议与文本语种一致，以获得正确的发音和自然的语调
