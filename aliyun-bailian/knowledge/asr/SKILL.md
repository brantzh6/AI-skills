# 语音识别（ASR）

> 更新时间：2026-04-12
> 来源：https://help.aliyun.com/zh/model-studio/speech-recognition

---

## 概述

百炼平台提供多种语音识别（Speech Recognition）模型，支持语音转文字。

---

## 支持的模型

| 模型 | 说明 |
|------|------|
| **Paraformer** | 语音识别模型，支持录音文件识别 |

---

## 快速开始

### 录音文件识别

通过 DashScope API 调用：

```python
import dashscope

response = dashscope.audio.asr.Transcription.call(
    model="paraformer",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 通过 file_urls 传入音频文件 URL
    file_urls=["https://example.com/audio.wav"]
)
```

**注意：** 使用 Paraformer 录音文件识别时，需在请求参数中传入 `file_urls`，否则会报错 `input must contain file_urls`。

---

## 支持语种

- 中文（普通话、粤语等方言）
- 英文
- 日语
- 韩语
- 详见[模型列表](https://help.aliyun.com/zh/model-studio/models#696c1bf328gf9)

---

## 注意事项

1. 音频格式支持：WAV、MP3 等
2. 通过公网 URL 或本地文件传入
3. 详见[语音识别文档](https://help.aliyun.com/zh/model-studio/speech-recognition)
