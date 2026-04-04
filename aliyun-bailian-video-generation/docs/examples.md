# 视频生成技能包 - 使用示例

本文档提供各场景的完整代码示例。

---

## 📋 前置准备

### 1. 安装依赖

```bash
pip install dashscope>=1.25.8
```

### 2. 配置环境变量

```bash
# Windows PowerShell
$env:DASHSCOPE_API_KEY="sk-xxx"

# Linux/macOS
export DASHSCOPE_API_KEY="sk-xxx"
```

---

## 🎬 场景 1：文生视频

### 基础示例

```python
import os
from http import HTTPStatus
from dashscope import VideoSynthesis
import dashscope

# 配置地域 URL
dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'
api_key = os.getenv("DASHSCOPE_API_KEY")

# 异步调用
rsp = VideoSynthesis.async_call(
    api_key=api_key,
    model='wan2.6-t2v',
    prompt='一段紧张刺激的侦探追查故事，展现电影级叙事能力。',
    size="1280*720",
    duration=15
)

if rsp.status_code == HTTPStatus.OK:
    print("task_id:", rsp.output.task_id)
    
    # 等待任务完成
    result = VideoSynthesis.wait(task=rsp, api_key=api_key)
    if result.status_code == HTTPStatus.OK:
        print("video_url:", result.output.video_url)
else:
    print('Failed:', rsp.code, rsp.message)
```

### 多镜头叙事示例

```python
rsp = VideoSynthesis.async_call(
    api_key=api_key,
    model='wan2.6-t2v',
    prompt='''展现未来科技与自然和谐共存的美好愿景。
第 1 个镜头 [0-2 秒] 未来城市的空中花园全景，悬浮植物在微风中摇曳。
第 2 个镜头 [2-4 秒] 机器人园丁正在精心修剪植物，动作精准而优雅。
第 3 个镜头 [4-7 秒] 阳光透过透明穹顶洒下，照亮整个花园。
第 4 个镜头 [7-10 秒] 镜头拉远，展现整个未来城市的壮观景象。''',
    size="1280*720",
    duration=10,
    shot_type="multi",  # 多镜头
    prompt_extend=True,  # 智能改写
    watermark=True
)
```

### 声画同步示例

```python
rsp = VideoSynthesis.async_call(
    api_key=api_key,
    model='wan2.6-t2v',
    prompt='一幅史诗级可爱的场景。一只小巧可爱的卡通小猫将军...',
    audio_url='https://example.com/audio.mp3',  # 传入音频
    size='1280*720',
    duration=10,
    shot_type="multi"
)
```

---

## 🖼️ 场景 2：图生视频 - 首帧

```python
from dashscope import VideoSynthesis

rsp = VideoSynthesis.async_call(
    api_key=api_key,
    model='wan2.6-i2v',
    prompt='一幅都市奇幻艺术的场景。一个充满动感的涂鸦艺术角色...',
    image_url='https://example.com/first_frame.jpg',  # 首帧图像
    audio_url='https://example.com/audio.mp3',  # 可选音频
    size='1280*720',
    duration=10,
    shot_type="multi"
)
```

---

## 🎞️ 场景 3：图生视频 - 首尾帧

```python
from dashscope import VideoSynthesis

rsp = VideoSynthesis.async_call(
    api_key=api_key,
    model='wan2.2-kf2v-flash',
    prompt='写实风格，一只黑色小猫好奇地看向天空，镜头从平视逐渐上升...',
    first_image_url='https://example.com/first_frame.jpg',  # 首帧
    last_image_url='https://example.com/last_frame.jpg',    # 尾帧
    size='1280*720',
    duration=5
)
```

---

## 🎭 场景 4：参考生视频

### 单角色参考

```python
rsp = VideoSynthesis.async_call(
    api_key=api_key,
    model='wan2.6-r2v-flash',
    prompt='character1 说："I'll rely on you tomorrow morning!"',
    video_url='https://example.com/reference_video.mp4',  # 参考视频
    size='1280*720',
    duration=10
)
```

### 多角色对话

```python
rsp = VideoSynthesis.async_call(
    api_key=api_key,
    model='wan2.6-r2v-flash',
    prompt='''character1 对 character2 说："I'll rely on you tomorrow morning!"
character2 回答："You can count on me!"''',
    video_url='https://example.com/reference_video.mp4',
    size='1280*720',
    duration=10
)
```

---

## ✂️ 场景 5：视频编辑

### 多图参考生成

```python
rsp = VideoSynthesis.async_call(
    api_key=api_key,
    model='wanx2.1-vace-plus',
    prompt='一位女孩自晨雾缭绕的古老森林深处款款走出...',
    image_urls=[
        'https://example.com/subject.jpg',  # 参考主体
        'https://example.com/background.jpg'  # 参考背景
    ],
    size='1280*720'
)
```

### 视频延展

```python
rsp = VideoSynthesis.async_call(
    api_key=api_key,
    model='wanx2.1-vace-plus',
    prompt='把视频延长到 5 秒',
    video_url='https://example.com/short_video.mp4',
    extend_duration=5
)
```

### 视频局部编辑

```python
rsp = VideoSynthesis.async_call(
    api_key=api_key,
    model='wanx2.1-vace-plus',
    prompt='替换视频中的主体衣服为红色',
    video_url='https://example.com/video.mp4',
    mask_url='https://example.com/mask.png'  # 掩码图像
)
```

---

## 🎤 场景 6：数字人

### 步骤 1：图像检测

```python
from dashscope import DigitalHuman

detect_rsp = DigitalHuman.detect(
    api_key=api_key,
    model='wan2.2-s2v-detect',
    image_url='https://example.com/person.jpg'
)

if detect_rsp.output.status == 'PASS':
    print("图像检测通过")
else:
    print("图像检测失败:", detect_rsp.output.message)
```

### 步骤 2：生成数字人视频

```python
rsp = DigitalHuman.generate(
    api_key=api_key,
    model='wan2.2-s2v',
    image_url='https://example.com/person.jpg',
    audio_url='https://example.com/audio.mp3',
    resolution='720P'
)

# 等待任务完成
result = DigitalHuman.wait(task=rsp, api_key=api_key)
if result.status_code == HTTPStatus.OK:
    print("video_url:", result.output.video_url)
```

---

## 💃 场景 7：图生动作

```python
from dashscope import Animate

rsp = Animate.animate_move(
    api_key=api_key,
    model='wan2.2-animate-move',
    image_url='https://example.com/person.jpg',  # 人物图像
    video_url='https://example.com/reference_video.mp4',  # 参考动作视频
    mode='wan-pro',  # 标准模式：wan-std, 专业模式：wan-pro
    resolution='720P'
)
```

---

## 🎭 场景 8：视频换人

```python
from dashscope import Animate

rsp = Animate.animate_mix(
    api_key=api_key,
    model='wan2.2-animate-mix',
    video_url='https://example.com/original_video.mp4',  # 原视频
    image_url='https://example.com/new_person.jpg',  # 替换人物图像
    mode='wan-pro',
    resolution='720P'
)
```

---

## 🎵 场景 9：视频口型替换

```python
from dashscope import VideoRetalk

rsp = VideoRetalk.call(
    api_key=api_key,
    model='videoretalk',
    video_url='https://example.com/original_video.mp4',
    audio_url='https://example.com/new_audio.mp3'
)

result = VideoRetalk.wait(task=rsp, api_key=api_key)
if result.status_code == HTTPStatus.OK:
    print("video_url:", result.output.video_url)
```

---

## 🎨 场景 10：视频风格重绘

```python
from dashscope import VideoStyleTransform

rsp = VideoStyleTransform.call(
    api_key=api_key,
    model='video-style-transform',
    video_url='https://example.com/original_video.mp4',
    style_id='anime_japanese'  # 日式漫画风格
)
```

---

## 📊 第三方模型示例

### 爱诗 - 文生视频

```python
rsp = VideoSynthesis.async_call(
    api_key=api_key,
    model='pixverse/pixverse-v5.6-t2v',
    prompt='一段电影级场景...',
    resolution='1080P',
    duration=10
)
```

### 爱诗 - 图生视频 - 首帧

```python
rsp = VideoSynthesis.async_call(
    api_key=api_key,
    model='pixverse/pixverse-v5.6-it2v',
    prompt='电影感镜头...',
    image_url='https://example.com/first_frame.jpg',
    resolution='1080P',
    duration=10
)
```

### 爱诗 - 图生视频 - 首尾帧

```python
rsp = VideoSynthesis.async_call(
    api_key=api_key,
    model='pixverse/pixverse-v5.6-kf2v',
    prompt='过渡自然...',
    first_image_url='https://example.com/first_frame.jpg',
    last_image_url='https://example.com/last_frame.jpg',
    resolution='720P',
    duration=5
)
```

---

## ⚠️ 常见问题

### Q1: 任务一直处于 PENDING 状态？

**A**: 视频生成是异步任务，需要等待。使用 `VideoSynthesis.wait()` 轮询任务状态。

```python
result = VideoSynthesis.wait(task=rsp, api_key=api_key, timeout=300)  # 最多等待 5 分钟
```

### Q2: 生成的视频 URL 无法访问？

**A**: 视频 URL 有效期**24 小时**，请及时下载。

```python
import requests

video_url = result.output.video_url
response = requests.get(video_url)
with open('output.mp4', 'wb') as f:
    f.write(response.content)
```

### Q3: 跨地域调用失败？

**A**: 确保模型、Endpoint URL 和 API Key 属于同一地域。

```python
# 北京地域
dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

# 新加坡地域
dashscope.base_http_api_url = 'https://dashscope-intl.aliyuncs.com/api/v1'

# 美国地域
dashscope.base_http_api_url = 'https://dashscope-us.aliyuncs.com/api/v1'
```

### Q4: 如何检查任务状态？

```python
from dashscope import VideoSynthesis

task_status = VideoSynthesis.get_task(
    task_id='your_task_id',
    api_key=api_key
)

print("任务状态:", task_status.output.task_status)
# PENDING | RUNNING | SUCCEEDED | FAILED
```

---

**最后更新**: 2026-04-01  
**维护人**: 胖福
