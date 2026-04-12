---
name: aliyun-bailian-video-generation
description: 阿里云百炼专业视频生成技能包 (Wan 2.7 首选)，支持 1080P、原生音频、首尾帧控制、视频续写、角色克隆及指令编辑。
homepage: https://help.aliyun.com/zh/model-studio/use-video-generation
metadata:
  {
    "openclaw":
      {
        "emoji": "🎬",
        "requires": { "tools": ["exec"] },
        "install":
          [
            {
              "id": "pip",
              "kind": "pip",
              "packages": ["dashscope>=1.25.8"],
              "label": "Install DashScope SDK for video generation",
            },
          ],
      },
  }
---

# 阿里云百炼视频生成技能包 (Wan 2.7)

**版本**: v3.0  
**更新时间**: 2026-04-09  
**首选模型**: **Wan 2.7** (2026-04-03 发布)  
**适用场景**: 专业视频制作、多镜头叙事、品牌视频、数字人、短视频

---

## 🎯 功能概览

### 🚀 Wan 2.7 四大核心模型

| 模型 | 功能 | 分辨率 | 时长 | 输入 |
|------|------|--------|------|------|
| **wan2.7-t2v** | 文生视频 | 720P/1080P | 2-15 秒 | 文本 + 音频(可选) |
| **wan2.7-i2v** | 图生视频 | 720P/1080P | 2-15 秒 | 首帧/首尾帧/首段视频 + 音频(可选) |
| **wan2.7-r2v** | 参考生视频 | 720P/1080P | 2-10 秒 | 参考图/视频(最多5个) |
| **wan2.7-videoedit** | 视频编辑 | 720P/1080P | 2-10 秒 | 视频 + 参考图(可选) |

### 🤵 数字人/人像视频
- ✅ **数字人** (wan2.2-s2v): 照片说话/唱歌
- ✅ **图生动作** (wan2.2-animate-move): 图像参考视频动起来
- ✅ **视频换人** (wan2.2-animate-mix): 视频换人
- ✅ **灵动人像** (LivePortrait): 长视频播报 ≤180 秒
- ✅ **声动人像** (VideoRetalk): 视频配音口型替换

### 第三方模型
- ✅ **爱诗系列** (PixVerse V5.6)

---

## 📋 模型选型指南

### 场景 1：通用视频创作

| 需求 | 推荐模型 | 输入 | 输出时长 |
|------|---------|------|---------|
| 文字→视频 | **wan2.7-t2v** ⭐ | 文本 + 音频(可选) | 2-15 秒 |
| 一张图→动起来 | **wan2.7-i2v** ⭐ | 首帧图 + 文本 + 音频(可选) | 2-15 秒 |
| 首尾图→过渡 | **wan2.7-i2v** ⭐ | 首帧 + 尾帧 + 文本 | 2-15 秒 |
| 基于已有视频续写 | **wan2.7-i2v** ⭐ | 首段视频 + 文本 | 2-15 秒 |
| 复刻角色表演 | **wan2.6-r2v-flash** ⭐ | 参考视频/图 + 文本 | 2-10 秒 |

### 场景 2：数字人制作

| 需求 | 推荐模型 | 输入 | 输出时长 |
|------|---------|------|---------|
| 照片说话/唱歌 | **wan2.2-s2v** ⭐ | 图 + 音频 | ≤20 秒 |
| 长视频播报 | LivePortrait | 图 + 音频 | ≤180 秒 |
| 已有视频换口型 | VideoRetalk | 视频 + 新音频 | 原视频时长 |

### 场景 3：视频编辑

| 需求 | 推荐模型 | 输入 |
|------|---------|------|
| 指令编辑视频 | **wan2.7-videoedit** ⭐ | 视频 + 文本指令 + 参考图(可选) |
| 视频风格转换 | wan2.7-videoedit | 视频 + 风格描述 |
| 视频换人 | wan2.2-animate-mix | 视频 + 替换图 |
| 跳舞换人 | wan2.2-animate-move | 图 + 参考视频 |

---

## 🎬 万相 - 文生视频 (Wan 2.7)

### 模型：wan2.7-t2v

| 参数 | 值 |
|------|-----|
| 分辨率 | 720P / 1080P (默认 1080P) |
| 时长 | 2-15 秒 (默认 5 秒) |
| 宽高比 | 16:9 / 9:16 / 1:1 / 4:3 / 3:4 |
| Prompt 限制 | ≤5000 字符 |
| 反向提示词 | ≤500 字符 |
| 音频 | wav/mp3, 2-30 秒, ≤15MB |

### HTTP 调用

```bash
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
 -H 'X-DashScope-Async: enable' \
 -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
 -H 'Content-Type: application/json' \
 -d '{
  "model": "wan2.7-t2v",
  "input": {
    "prompt": "一段紧张刺激的侦探追查故事。第1个镜头[0-3秒] 全景：雨夜的纽约街头，霓虹灯闪烁。第2个镜头[3-6秒] 中景：侦探进入老旧建筑。第3个镜头[6-9秒] 特写：侦探眼神坚毅专注。",
    "audio_url": "https://example.com/rain.mp3"
  },
  "parameters": {
    "resolution": "720P",
    "ratio": "16:9",
    "duration": 9,
    "prompt_extend": true
  }
}'
```

### 关键变化 (vs wan2.6)

| 特性 | wan2.6 | wan2.7 |
|------|--------|--------|
| 多镜头控制 | 需设 `shot_type: "multi"` + `prompt_extend: true` | **无需 shot_type**，自然语言描述分镜即可 |
| 参数名 | `size: "1280*720"` | `resolution: "720P"` + `ratio: "16:9"` |
| Prompt 上限 | 1500 字符 | **5000 字符** |
| 时长范围 | 2-15 秒 | 2-15 秒 |
| 反向提示词 | ✅ | ✅ (新增支持) |

### 多镜头叙事示例 (wan2.7)

Wan 2.7 不再需要 `shot_type` 参数，直接在 prompt 中用时间戳描述分镜：

```
第1个镜头[0-3秒] 全景：未来城市空中花园，悬浮植物在微风中摇曳。
第2个镜头[3-6秒] 中景：机器人园丁修剪植物，动作精准优雅。
第3个镜头[6-9秒] 近景：阳光透过穹顶洒下，照亮整个花园。
第4个镜头[9-12秒] 全景拉远：展现整个未来城市壮观景象。
```

### Python SDK (wan2.6 兼容，wan2.7 用 HTTP)

> ⚠️ **DashScope SDK 暂不支持 wan2.7 模型**，请使用 HTTP 调用。
> wan2.6 及早期模型可使用 SDK：

```python
import os
from http import HTTPStatus
from dashscope import VideoSynthesis
import dashscope

dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'
api_key = os.getenv("DASHSCOPE_API_KEY")

# wan2.6 多镜头叙事
rsp = VideoSynthesis.async_call(
    api_key=api_key,
    model='wan2.6-t2v',
    prompt='一幅史诗级可爱的场景。一只卡通小猫将军...',
    size='1280*720',
    duration=10,
    shot_type="multi",
    prompt_extend=True
)
```

---

## 🖼️ 万相 - 图生视频 (Wan 2.7)

### 模型：wan2.7-i2v

wan2.7-i2v 统一了三大任务：

| 任务 | media 组合 | 说明 |
|------|-----------|------|
| **首帧生视频** | `first_frame` + `driving_audio`(可选) | 基于首帧图像生成视频 |
| **首尾帧生视频** | `first_frame` + `last_frame` + `driving_audio`(可选) | 首尾帧过渡视频 |
| **视频续写** | `first_clip` + `last_frame`(可选) | 基于已有视频续写后续内容 |

### 参数规格

| 参数 | 值 |
|------|-----|
| 分辨率 | 720P / 1080P (默认 1080P) |
| 时长 | 2-15 秒 (默认 5 秒) |
| Prompt 限制 | ≤5000 字符 |
| 反向提示词 | ≤500 字符 |
| 音频 | wav/mp3, 2-30 秒, ≤15MB |
| 首帧/尾帧图像 | JPG/PNG/BMP/WEBP, 240-8000px, ≤20MB |
| 首段视频 | mp4/mov, 2-10 秒, 240-4096px, ≤100MB |

### 首帧生视频

```bash
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
 -H 'X-DashScope-Async: enable' \
 -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
 -H 'Content-Type: application/json' \
 -d '{
  "model": "wan2.7-i2v",
  "input": {
    "prompt": "一幅都市奇幻艺术的场景。一个由喷漆所画成的少年，正从一面混凝土墙上活过来，一边演唱英文rap，一边摆着充满活力的说唱歌手姿势。",
    "media": [
      { "type": "first_frame", "url": "https://example.com/rap.png" },
      { "type": "driving_audio", "url": "https://example.com/rap.mp3" }
    ]
  },
  "parameters": {
    "resolution": "720P",
    "duration": 10,
    "prompt_extend": true
  }
}'
```

### 首尾帧生视频

```bash
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
 -H 'X-DashScope-Async: enable' \
 -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
 -H 'Content-Type: application/json' \
 -d '{
  "model": "wan2.7-i2v",
  "input": {
    "prompt": "写实风格，一只小黑猫好奇地仰望天空，镜头从平视逐渐上升，最后以俯视角度捕捉到它好奇的眼神。",
    "media": [
      { "type": "first_frame", "url": "https://example.com/first.png" },
      { "type": "last_frame", "url": "https://example.com/last.png" }
    ]
  },
  "parameters": {
    "resolution": "720P",
    "duration": 10,
    "prompt_extend": false
  }
}'
```

### 视频续写

```bash
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
 -H 'X-DashScope-Async: enable' \
 -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
 -H 'Content-Type: application/json' \
 -d '{
  "model": "wan2.7-i2v",
  "input": {
    "prompt": "一个女孩对镜自拍，自拍结束后背着书包出门",
    "media": [
      { "type": "first_clip", "url": "https://example.com/clip1.mp4" }
    ]
  },
  "parameters": {
    "resolution": "720P",
    "duration": 10,
    "prompt_extend": true
  }
}'
```

> 📌 **视频续写计费**: 总输出时长 = duration 值。例如 first_clip 为 3 秒，duration=15，则续写 12 秒，按 15 秒计费。

---

## 🎭 万相 - 参考生视频

### 模型：wan2.6-r2v-flash ⭐ / wan2.6-r2v

> ⚠️ Wan 2.7 系列暂未推出独立的 R2V 模型，当前参考生视频仍使用 wan2.6-r2v 系列。

### 参数规格

| 参数 | 值 |
|------|-----|
| 分辨率 | 720P / 1080P |
| 时长 | 2-10 秒 (默认 5 秒) |
| 参考素材 | 图像 0-5 张 + 视频 0-3 个，**总数 ≤ 5** |
| 参考视频 | mp4/mov, 1-30 秒, ≤100MB |
| 参考图像 | JPG/PNG/BMP/WEBP, 240-8000px, ≤10MB |
| Prompt 限制 | ≤1500 字符 |

### 多角色互动 (最多 5 角色)

```bash
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
 -H 'X-DashScope-Async: enable' \
 -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
 -H 'Content-Type: application/json' \
 -d '{
  "model": "wan2.6-r2v-flash",
  "input": {
    "prompt": "Character2 坐在靠窗的椅子上，手持 character3，在 character4 旁演奏一首舒缓的乡村民谣。Character1 对 Character2 说：\"that sounds great\"",
    "reference_urls": [
      "https://example.com/role1.mp4",
      "https://example.com/role2.mp4",
      "https://example.com/object.png",
      "https://example.com/background.png"
    ]
  },
  "parameters": {
    "size": "1280*720",
    "duration": 10,
    "audio": true,
    "shot_type": "multi"
  }
}'
```

### 单角色多镜头表演

```bash
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
 -H 'X-DashScope-Async: enable' \
 -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
 -H 'Content-Type: application/json' \
 -d '{
  "model": "wan2.6-r2v-flash",
  "input": {
    "prompt": "展示最新款智能手表。第1个镜头[0-3秒] character1在办公室查看手表日程。第2个镜头[3-5秒] 特写手表健康界面。第3个镜头[5-8秒] character1在健身房运动。第4个镜头[8-10秒] 手表收到通知，character1轻触查看。",
    "reference_urls": ["https://example.com/character.mp4"]
  },
  "parameters": {
    "size": "1280*720",
    "duration": 10,
    "shot_type": "multi"
  }
}'
```

---

## ✂️ 万相 - 视频编辑 (Wan 2.7)

### 模型：wan2.7-videoedit

**自然语言指令编辑视频**，支持：
- 风格转换（"将整个画面转换为黏土风格"）
- 内容替换（"将视频中女孩的衣服替换为图片中的衣服"）
- 运镜调整（"Slow down the camera pan in the second half"）
- 光影调整（"Make the lighting more dramatic"）

### 参数规格

| 参数 | 值 |
|------|-----|
| 分辨率 | 720P / 1080P (默认 1080P) |
| 视频输入 | mp4/mov, 2-10 秒, 240-4096px, ≤100MB |
| 参考图像 | 最多 3 张, JPG/PNG/BMP/WEBP, 240-8000px, ≤20MB |
| Prompt 限制 | ≤5000 字符 |
| 音频设置 | auto(默认)/origin(保留原声) |

### 风格转换

```bash
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
 -H 'X-DashScope-Async: enable' \
 -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
 -H 'Content-Type: application/json' \
 -d '{
  "model": "wan2.7-videoedit",
  "input": {
    "prompt": "将整个画面转换为黏土风格",
    "media": [
      { "type": "video", "url": "https://example.com/original.mp4" }
    ]
  },
  "parameters": {
    "resolution": "720P",
    "prompt_extend": true
  }
}'
```

### 内容替换（参考图）

```bash
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
 -H 'X-DashScope-Async: enable' \
 -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
 -H 'Content-Type: application/json' \
 -d '{
  "model": "wan2.7-videoedit",
  "input": {
    "prompt": "将视频中女孩的衣服替换为图片中的衣服",
    "media": [
      { "type": "video", "url": "https://example.com/original.mp4" },
      { "type": "reference_image", "url": "https://example.com/new_clothes.png" }
    ]
  },
  "parameters": {
    "resolution": "720P",
    "prompt_extend": true
  }
}'
```

### 视频延长/截断

```bash
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
 -H 'X-DashScope-Async: enable' \
 -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
 -H 'Content-Type: application/json' \
 -d '{
  "model": "wan2.7-videoedit",
  "input": {
    "prompt": "延长视频结尾",
    "media": [
      { "type": "video", "url": "https://example.com/short.mp4" }
    ]
  },
  "parameters": {
    "resolution": "720P",
    "duration": 8
  }
}'
```

> 📌 **计费**: 输入视频 + 输出视频均计费。总时长 = 输入视频时长 + 输出视频时长。

---

## 🎤 万相 - 数字人

### 模型：wan2.2-s2v

| 参数 | 值 |
|------|-----|
| 分辨率 | 480P / 720P |
| 时长 | ≤20 秒 |
| 输入 | 图像 + 音频 |

```python
from dashscope import DigitalHuman

# 步骤 1: 图像检测
detect_rsp = DigitalHuman.detect(
    api_key=api_key,
    model='wan2.2-s2v-detect',
    image_url='https://example.com/person.jpg'
)

# 步骤 2: 生成数字人视频
if detect_rsp.output.status == 'PASS':
    rsp = DigitalHuman.generate(
        api_key=api_key,
        model='wan2.2-s2v',
        image_url='https://example.com/person.jpg',
        audio_url='https://example.com/audio.mp3',
        resolution='720P'
    )
```

---

## 💃 万相 - 图生动作 / 视频换人

### 图生动作 (wan2.2-animate-move)

让图像中的人参考视频动起来。

```python
rsp = VideoSynthesis.async_call(
    api_key=api_key,
    model='wan2.2-animate-move',
    image_url='https://example.com/person.jpg',
    video_url='https://example.com/dance.mp4',
    mode='wan-pro',  # wan-std / wan-pro
    resolution='720P'
)
```

### 视频换人 (wan2.2-animate-mix)

把视频中的人替换为图像中的人。

```python
rsp = VideoSynthesis.async_call(
    api_key=api_key,
    model='wan2.2-animate-mix',
    video_url='https://example.com/original.mp4',
    image_url='https://example.com/new_person.jpg',
    mode='wan-pro',
    resolution='720P'
)
```

---

## 📊 第三方模型 - 爱诗系列

| 模型 | 功能 | 分辨率 | 时长 |
|------|------|--------|------|
| pixverse/pixverse-v5.6-t2v | 文生视频 | 1080P | 10 秒 |
| pixverse/pixverse-v5.6-it2v | 图生视频-首帧 | 1080P | 10 秒 |
| pixverse/pixverse-v5.6-kf2v | 图生视频-首尾帧 | 720P | 5 秒 |

---

## 🎯 场景化解决方案

### 场景 1：电商产品视频

```bash
# wan2.7-t2v 文生视频
curl -X POST 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
 -H 'X-DashScope-Async: enable' \
 -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
 -H 'Content-Type: application/json' \
 -d '{
  "model": "wan2.7-t2v",
  "input": {
    "prompt": "3C 产品展示视频，现代简约风格，白色背景，产品 360 度旋转展示，光影流动，专业商业摄影质感。"
  },
  "parameters": {
    "resolution": "1080P",
    "ratio": "16:9",
    "duration": 10,
    "prompt_extend": true
  }
}'
```

### 场景 2：教育培训视频（数字人）

```python
# 使用 CosyVoice 生成讲师音频 → wan2.2-s2v 生成数字人视频
from dashscope import DigitalHuman

rsp = DigitalHuman.generate(
    api_key=api_key,
    model='wan2.2-s2v',
    image_url='https://example.com/teacher.jpg',
    audio_url='https://example.com/lecture.mp3',
    resolution='720P'
)
```

### 场景 3：社交媒体内容

```bash
# wan2.7-t2v 快速生成
curl -X POST 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
 -H 'X-DashScope-Async: enable' \
 -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
 -H 'Content-Type: application/json' \
 -d '{
  "model": "wan2.7-t2v",
  "input": {
    "prompt": "快节奏社交媒体视频，动感音乐，年轻人在城市街头跳舞，镜头跟随移动。"
  },
  "parameters": {
    "resolution": "1080P",
    "ratio": "9:16",
    "duration": 10,
    "prompt_extend": true
  }
}'
```

### 场景 4：视频编辑/风格转换

```bash
# wan2.7-videoedit 指令编辑
curl -X POST 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
 -H 'X-DashScope-Async: enable' \
 -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
 -H 'Content-Type: application/json' \
 -d '{
  "model": "wan2.7-videoedit",
  "input": {
    "prompt": "将整个画面转换为赛博朋克风格，霓虹灯光，蓝紫色调",
    "media": [
      { "type": "video", "url": "https://example.com/original.mp4" }
    ]
  },
  "parameters": {
    "resolution": "1080P",
    "prompt_extend": true
  }
}'
```

---

## ⚠️ 注意事项

### 地域限制

- **确保模型、Endpoint URL 和 API Key 属于同一地域**
- 跨地域调用会失败

### Wan 2.7 调用方式

- **wan2.7-t2v / wan2.7-i2v / wan2.7-videoedit** 使用 **HTTP 调用**（新协议）
- DashScope Python SDK **暂不支持** wan2.7 模型
- 请使用 `dashscope>=1.25.8`，但 wan2.7 需直接发 HTTP 请求

### 视频 URL 有效期

- 生成的视频 URL 有效期 **24 小时**
- 请及时下载保存

### 计费说明

- 有声视频和无声视频价格不同
- wan2.7-t2v / wan2.7-i2v: 按输出视频时长计费
- wan2.7-videoedit: 输入视频 + 输出视频均计费
- wan2.6-r2v: 输入视频（上限5秒）+ 输出视频均计费
- 调用失败不产生费用

### 分辨率对照表

| 档位 | 16:9 | 9:16 | 1:1 | 4:3 | 3:4 |
|------|------|------|-----|-----|-----|
| **720P** | 1280×720 | 720×1280 | 960×960 | 1104×832 | 832×1104 |
| **1080P** | 1920×1080 | 1080×1920 | 1440×1440 | 1648×1248 | 1248×1648 |

---

## 📚 相关文档

- **使用指南**: https://help.aliyun.com/zh/model-studio/use-video-generation
- **文生视频 API**: https://help.aliyun.com/zh/model-studio/text-to-video-api-reference
- **图生视频 API**: https://help.aliyun.com/zh/model-studio/image-to-video-general-api-reference
- **参考生视频 API**: https://help.aliyun.com/zh/model-studio/wan-video-to-video-api-reference
- **视频编辑 API**: https://help.aliyun.com/zh/model-studio/wan-video-editing-api-reference
- **Prompt 指南**: https://help.aliyun.com/zh/model-studio/text-to-video-prompt
- **模型价格**: https://help.aliyun.com/zh/model-studio/model-pricing

---

**版本**: v3.0  
**最后更新**: 2026-04-09  
**维护人**: 胖福
