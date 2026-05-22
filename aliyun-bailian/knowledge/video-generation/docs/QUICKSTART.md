# 视频生成技能包 - 快速入门

**5 分钟快速上手视频生成**

---

## 🚀 第一步：安装依赖

```bash
pip install dashscope>=1.25.8
```

---

## 📝 第二步：配置 API Key

### Windows PowerShell

```powershell
$env:DASHSCOPE_API_KEY="sk-your-api-key"
```

### Linux/macOS

```bash
export DASHSCOPE_API_KEY="sk-your-api-key"
```

---

## 🎬 第三步：生成第一个视频

### 文生视频 (最简单)

```python
import os
from http import HTTPStatus
from dashscope import VideoSynthesis
import dashscope

# 配置
dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'
api_key = os.getenv("DASHSCOPE_API_KEY")

# 调用
rsp = VideoSynthesis.async_call(
    api_key=api_key,
    model='wan2.6-t2v',
    prompt='一只可爱的小猫在阳光下玩耍，4K 画质，电影感',
    size="1280*720",
    duration=10
)

# 等待结果
if rsp.status_code == HTTPStatus.OK:
    print("任务 ID:", rsp.output.task_id)
    result = VideoSynthesis.wait(task=rsp, api_key=api_key)
    if result.status_code == HTTPStatus.OK:
        print("视频 URL:", result.output.video_url)
        # 下载视频
        import requests
        video = requests.get(result.output.video_url)
        with open('my_video.mp4', 'wb') as f:
            f.write(video.content)
        print("视频已保存到 my_video.mp4")
else:
    print('失败:', rsp.code, rsp.message)
```

---

## 🎯 常用场景速查

### 场景 1：文字→视频

```python
VideoSynthesis.async_call(
    api_key=api_key,
    model='wan2.6-t2v',
    prompt='你的提示词',
    duration=10
)
```

### 场景 2：图片→视频

```python
VideoSynthesis.async_call(
    api_key=api_key,
    model='wan2.6-i2v',
    prompt='你的提示词',
    image_url='https://example.com/image.jpg',
    duration=10
)
```

### 场景 3：照片说话 (数字人)

```python
from dashscope import DigitalHuman

DigitalHuman.generate(
    api_key=api_key,
    model='wan2.2-s2v',
    image_url='https://example.com/person.jpg',
    audio_url='https://example.com/audio.mp3'
)
```

### 场景 4：视频换人

```python
from dashscope import Animate

Animate.animate_mix(
    api_key=api_key,
    model='wan2.2-animate-mix',
    video_url='https://example.com/video.mp4',
    image_url='https://example.com/new_person.jpg'
)
```

---

## 📊 模型选择指南

| 需求 | 推荐模型 | 价格 |
|------|---------|------|
| 文字→视频 | wan2.6-t2v | ¥0.5/秒 |
| 图片→视频 | wan2.6-i2v | ¥0.6/秒 |
| 首尾帧→视频 | wan2.2-kf2v-flash | ¥0.5/秒 |
| 参考视频→新视频 | wan2.6-r2v-flash | ¥0.8/秒 |
| 照片说话 | wan2.2-s2v | ¥1.0/秒 |
| 视频换人 | wan2.2-animate-mix | ¥1.2/秒 |

---

## ⚠️ 注意事项

1. **视频 URL 有效期 24 小时** - 及时下载
2. **确保地域一致** - 模型、URL、API Key 必须同地域
3. **异步任务** - 需要等待，使用 `wait()` 轮询
4. **SDK 版本** - 必须 ≥ 1.25.8

---

## 📚 下一步

- 查看完整文档：`SKILL.md`
- 查看更多示例：`docs/examples.md`
- API 参考：https://help.aliyun.com/zh/model-studio/video-generation-api/

---

**开始创作你的第一个 AI 视频吧！** 🎬
