---
name: aliyun-bailian-video-generation
description: 阿里云百炼专业视频生成技能包 (Wan 2.7 首选)，支持 4K 原生、原生音频、首尾帧控制、9 宫格图生视频、角色克隆及指令编辑。
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

# 阿里云百炼视频生成技能包 (Wan 2.7 Pro)

**版本**: v2.0  
**更新时间**: 2026-04-04  
**首选模型**: **Wan 2.7** (原生 4K, 30s, 原生音频)  
**适用场景**: 专业影视制作、多镜头叙事、品牌视频、YouTube 规模化

---

## 🎯 功能概览 (Wan 2.7 增强版)

本技能包提供行业领先的视频生成能力：

### 🚀 核心生成 (Wan 2.7)
- ✅ **原生 4K 视频生成** (最高 4K 分辨率)
- ✅ **原生音频同步** (自动生成环境音 + 角色配音)
- ✅ **首尾帧精确控制** (First/Last Frame Control)
- ✅ **9 宫格图生视频** (3x3 Grid Image-to-Video)
- ✅ **长镜头生成** (单镜头最长 30 秒)
- ✅ **角色 + 声音克隆** (Subject + Voice Cloning)
- ✅ **指令式编辑** (Instruction-Based Editing, Beta)

### 🎬 通用视频生成
- ✅ **文生视频** (T2V)
- ✅ **图生视频** (I2V)
- ✅ **参考生视频** (R2V)

### 🤵 数字人/人像视频
- ✅ **数字人** (Digital Human)
- ✅ **图生动作** (Image-to-Action)
- ✅ **视频换人** (Video Character Replacement)
- ✅ **舞动人像** (Animate Anyone)
- ✅ **悦动人像** (EMO)
- ✅ **灵动人像** (LivePortrait)
- ✅ **表情包** (Emoji)
- ✅ **声动人像** (VideoRetalk)
- ✅ **视频风格重绘** (Video Style Transform)

### 第三方模型
- ✅ **爱诗系列** (PixVerse)

---

## 📋 模型选型指南

### 场景 1：通用视频创作

| 需求 | 推荐模型 | 输入 | 输出时长 | 文档 |
|------|---------|------|---------|------|
| 文字→视频 | 万相 - 文生视频 | 文本 + 音频 | 2-15 秒 | [详情](#万相 - 文生视频) |
| 一张图→电影感镜头 | 万相 - 图生视频 - 首帧 | 图 + 文本 + 音频 | 2-15 秒 | [详情](#万相 - 图生视频 - 首帧) |
| 首尾图→过渡视频 | 万相 - 图生视频 - 首尾帧 | 首帧图 + 尾帧图 + 文本 | 5 秒 | [详情](#万相 - 图生视频 - 首尾帧) |
| 复刻角色表演 | 万相 - 参考生视频 | 参考视频 + 文本 | 2-10 秒 | [详情](#万相 - 参考生视频) |

### 场景 2：数字人制作

| 需求 | 推荐模型 | 输入 | 输出时长 | 备注 |
|------|---------|------|---------|------|
| 照片说话/唱歌 | **万相 - 数字人** (首选) | 图 + 音频 | ≤20 秒 | 效果最佳 |
| 长视频播报 (>20 秒) | 灵动人像 LivePortrait | 图 + 音频 | ≤180 秒 | 简单头部动作 |
| 表情包制作 | 表情包 Emoji | 图 + 模板 ID | ≤5 秒 | 固定模板 |

### 场景 3：视频编辑

| 需求 | 推荐模型 | 输入 | 输出 |
|------|---------|------|------|
| 视频局部编辑 | 万相 - 通用视频编辑 | 视频 + 掩码 + 文本 | 编辑后视频 |
| 视频延展 | 万相 - 通用视频编辑 | 视频 + 文本 | 延长视频 |
| 视频换人 | 万相 - 视频换人 | 视频 + 替换图 | 换人后视频 |
| 视频风格转换 | 视频风格重绘 | 视频 + 风格 ID | 重绘视频 |
| 跳舞换人 | 万相 - 图生动作 | 图 + 参考视频 | 跳舞视频 |

---

## 🎬 万相 - 文生视频

### 功能说明

根据文本提示词生成视频，支持输入文本 + 音频，输出电影级多镜头视频。

### 支持模型 (Wan 2.7 首选)

| 模型 | 地域 | 有声/无声 | 分辨率 | 时长 | 特点 |
|------|------|---------|--------|------|------|
| **wan2.7-t2v** ⭐首选 | 北京 | **原生音频** | **1080P/4K** | **15-30 秒** | 首尾帧控制、原生音频 |
| wan2.6-t2v | 北京/新加坡 | 有声 | 720P/1080P | 2-15 秒 | 多镜头叙事 |
| wan2.5-t2v-preview | 北京/新加坡 | 有声 | 480P/720P/1080P | 5s/10s | 声画同步 |

### 使用示例

#### Python SDK

```python
import os
from http import HTTPStatus
from dashscope import VideoSynthesis
import dashscope

# 配置北京地域 URL
dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'
api_key = os.getenv("DASHSCOPE_API_KEY")

# 异步调用文生视频 (Wan 2.7)
rsp = VideoSynthesis.async_call(
    api_key=api_key,
    model='wan2.7-t2v',
    prompt='一段紧张刺激的侦探追查故事...原生环境音：雨声、警笛声。',
    size="1920*1080",
    duration=30,
    shot_type="multi",
    prompt_extend=True,
    native_audio=True  # 开启原生音频
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

### 核心能力

#### 多镜头叙事 (wan2.6 系列)

**参数设置**:
- `shot_type`: "multi" (必须)
- `prompt_extend`: true (必须，开启智能改写)

**示例提示词**:
```
展现未来科技与自然和谐共存的美好愿景。
第 1 个镜头 [0-2 秒] 未来城市的空中花园全景，悬浮植物在微风中摇曳。
第 2 个镜头 [2-4 秒] 机器人园丁正在精心修剪植物，动作精准而优雅。
第 3 个镜头 [4-7 秒] 阳光透过透明穹顶洒下，照亮整个花园。
第 4 个镜头 [7-10 秒] 镜头拉远，展现整个未来城市的壮观景象。
```

#### 声画同步 (wan2.5/wan2.6 系列)

**参数设置**:
- `audio_url`: 传入音频文件 URL (可选)
- 不传 `audio_url` 则自动配音

**示例**:
```python
rsp = VideoSynthesis.async_call(
    api_key=api_key,
    model='wan2.6-t2v',
    prompt='一幅史诗级可爱的场景。一只小巧可爱的卡通小猫将军...',
    audio_url='https://example.com/audio.mp3',  # 传入音频
    size='1280*720',
    duration=10
)
```

---

## 🖼️ 万相 - 图生视频 - 首帧

### 功能说明

根据给定的首帧图像生成视频，支持输入文本 + 首帧图像 + 音频。

### 支持模型

| 模型 | 地域 | 有声/无声 | 分辨率 | 时长 | 特点 |
|------|------|---------|--------|------|------|
| **wan2.6-i2v-flash** ⭐推荐 | 北京/新加坡 | 有声/无声 | 720P/1080P | 2-15 秒 | 速度快、性价比高 |
| **wan2.6-i2v** ⭐推荐 | 北京/新加坡/弗吉尼亚 | 有声 | 720P/1080P | 2-15 秒 | 多镜头叙事 |
| **wan2.5-i2v-preview** | 北京/新加坡 | 有声 | 480P/720P/1080P | 5s/10s | 声画同步 |
| **wan2.2-i2v-flash** | 北京/新加坡 | 无声 | 480P/720P/1080P | 5 秒 | 速度提升 50% |

### 使用示例

```python
rsp = VideoSynthesis.async_call(
    api_key=api_key,
    model='wan2.6-i2v',
    prompt='一幅都市奇幻艺术的场景。一个充满动感的涂鸦艺术角色...',
    image_url='https://example.com/first_frame.jpg',  # 首帧图像
    audio_url='https://example.com/audio.mp3',  # 可选音频
    size='1280*720',
    duration=10,
    shot_type="multi"  # 多镜头
)
```

---

## 🎞️ 万相 - 图生视频 - 首尾帧

### 功能说明

根据给定的首帧图像和尾帧图像，生成过渡自然的视频。

### 支持模型

| 模型 | 地域 | 分辨率 | 时长 | 特点 |
|------|------|--------|------|------|
| **wan2.2-kf2v-flash** ⭐推荐 | 北京/新加坡 | 480P/720P/1080P | 5 秒 | 稳定性提升 |
| **wanx2.1-kf2v-plus** | 北京/新加坡 | 720P | 5 秒 | 标准质量 |

### 使用示例

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

## 🎭 万相 - 参考生视频

### 功能说明

复刻视频中的角色的形象和声音表演新剧本。支持单角色/多角色。

### 支持模型

| 模型 | 地域 | 有声/无声 | 分辨率 | 时长 | 特点 |
|------|------|---------|--------|------|------|
| **wan2.6-r2v-flash** ⭐推荐 | 北京/新加坡 | 有声/无声 | 720P/1080P | 2-10 秒 | 速度快、性价比高 |
| **wan2.6-r2v** ⭐推荐 | 北京/新加坡/弗吉尼亚 | 有声 | 720P/1080P | 2-10 秒 | 多镜头叙事 |

### 使用示例

```python
rsp = VideoSynthesis.async_call(
    api_key=api_key,
    model='wan2.6-r2v-flash',
    prompt='character1 对 character2 说："I'll rely on you tomorrow morning!" character2 回答："You can count on me!"',
    video_url='https://example.com/reference_video.mp4',  # 参考视频
    size='1280*720',
    duration=10
)
```

---

## ✂️ 万相 - 通用视频编辑

### 功能说明

视频编辑通用模型，支持多图参考、视频重绘、局部编辑、视频延展、画面扩展。

### 支持模型

| 模型 | 地域 | 功能 | 分辨率 | 时长 |
|------|------|------|--------|------|
| **wanx2.1-vace-plus** | 北京/新加坡 | 多图参考/视频重绘/局部编辑/视频延展/画面扩展 | 720P | ≤5 秒 |

### 功能示例

#### 功能 1：多图参考生成

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

#### 功能 2：视频延展

```python
rsp = VideoSynthesis.async_call(
    api_key=api_key,
    model='wanx2.1-vace-plus',
    prompt='把视频延长到 5 秒',
    video_url='https://example.com/short_video.mp4',
    extend_duration=5  # 延长到 5 秒
)
```

---

## 🎤 万相 - 数字人

### 功能说明

让静态照片说话、唱歌或播报，自动匹配口型、面部表情、头部及身体动作。

### 支持模型

| 模型 | 功能 | 输入 | 输出规格 |
|------|------|------|---------|
| **wan2.2-s2v-detect** | 图像检测 | 图像 | 检测状态 |
| **wan2.2-s2v** ⭐推荐 | 视频生成 | 图像 + 音频 | 480P/720P, ≤20 秒 |

### 使用示例

#### 步骤 1：图像检测

```python
from dashscope import DigitalHuman

# 先检测图像是否适合
detect_rsp = DigitalHuman.detect(
    api_key=api_key,
    model='wan2.2-s2v-detect',
    image_url='https://example.com/person.jpg'
)

if detect_rsp.output.status == 'PASS':
    print("图像检测通过")
else:
    print("图像检测失败")
```

#### 步骤 2：生成数字人视频

```python
rsp = DigitalHuman.generate(
    api_key=api_key,
    model='wan2.2-s2v',
    image_url='https://example.com/person.jpg',
    audio_url='https://example.com/audio.mp3',
    resolution='720P'
)
```

---

## 💃 万相 - 图生动作

### 功能说明

让图像的人参考视频动起来，保持图像背景不变。

### 支持模型

| 模型 | 地域 | 模式 | 分辨率 | 时长 |
|------|------|------|--------|------|
| **wan2.2-animate-move** ⭐推荐 | 北京/新加坡 | 标准模式 wan-std / 专业模式 wan-pro | 720P | 2-30 秒 |

### 使用示例

```python
rsp = VideoSynthesis.async_call(
    api_key=api_key,
    model='wan2.2-animate-move',
    image_url='https://example.com/person.jpg',  # 人物图像
    video_url='https://example.com/reference_video.mp4',  # 参考动作视频
    mode='wan-pro',  # 标准模式：wan-std, 专业模式：wan-pro
    resolution='720P'
)
```

---

## 🎭 万相 - 视频换人

### 功能说明

把视频中的人换成图像中的人，保留原视频背景。

### 支持模型

| 模型 | 地域 | 模式 | 分辨率 | 时长 |
|------|------|------|--------|------|
| **wan2.2-animate-mix** ⭐推荐 | 北京/新加坡 | 标准模式 wan-std / 专业模式 wan-pro | 720P | 2-30 秒 |

### 使用示例

```python
rsp = VideoSynthesis.async_call(
    api_key=api_key,
    model='wan2.2-animate-mix',
    video_url='https://example.com/original_video.mp4',  # 原视频
    image_url='https://example.com/new_person.jpg',  # 替换人物图像
    mode='wan-pro',
    resolution='720P'
)
```

---

## 📊 第三方模型 - 爱诗系列

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

## 🎯 场景化解决方案

### 场景 1：电商产品视频

**需求**: 快速生成产品展示视频

**推荐方案**:
```python
# 方案 A: 文生视频
rsp = VideoSynthesis.async_call(
    api_key=api_key,
    model='wan2.6-t2v',
    prompt='3C 产品展示视频，现代简约风格，白色背景，产品 360 度旋转展示...',
    duration=10,
    size='1280*720'
)

# 方案 B: 图生视频 (已有产品图)
rsp = VideoSynthesis.async_call(
    api_key=api_key,
    model='wan2.6-i2v',
    prompt='产品缓慢旋转，展示各个角度...',
    image_url='https://example.com/product.jpg',
    duration=10
)
```

### 场景 2：教育培训视频

**需求**: 制作讲师授课视频

**推荐方案**:
```python
# 使用数字人
rsp = DigitalHuman.generate(
    api_key=api_key,
    model='wan2.2-s2v',
    image_url='https://example.com/teacher.jpg',
    audio_url='https://example.com/lecture.mp3',
    resolution='720P'
)
```

### 场景 3：社交媒体内容

**需求**: 快速生成短视频内容

**推荐方案**:
```python
# 使用加速模型
rsp = VideoSynthesis.async_call(
    api_key=api_key,
    model='wan2.6-t2v',
    prompt='快节奏社交媒体视频，动感音乐...',
    duration=15,
    size='1280*720',
    shot_type="multi"
)
```

### 场景 4：视频本地化

**需求**: 视频配音口型替换

**推荐方案**:
```python
# 使用声动人像
from dashscope import VideoRetalk

rsp = VideoRetalk.call(
    api_key=api_key,
    model='videoretalk',
    video_url='https://example.com/original_video.mp4',
    audio_url='https://example.com/new_audio.mp3'
)
```

---

## ⚠️ 注意事项

### 地域限制

- **确保模型、Endpoint URL 和 API Key 属于同一地域**
- 跨地域调用会失败

### 版本要求

- **DashScope Python SDK**: ≥ 1.25.8
- **DashScope Java SDK**: ≥ 2.22.6

### 视频 URL 有效期

- 生成的视频 URL 有效期**24 小时**
- 请及时下载保存

### 计费说明

- **有声视频**和**无声视频**价格不同
- **计费时长** = 输出视频时长
- 部分模型支持输入视频计费 (如参考生视频)

---

## 📚 相关文档

- **使用指南**: https://help.aliyun.com/zh/model-studio/use-video-generation
- **API 参考**: https://help.aliyun.com/zh/model-studio/video-generation-api/
- **Prompt 指南**: https://help.aliyun.com/zh/model-studio/text-to-video-prompt
- **模型价格**: https://help.aliyun.com/zh/model-studio/model-pricing

---

**版本**: v1.0  
**最后更新**: 2026-04-01  
**维护人**: 胖福
