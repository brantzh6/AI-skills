# 阿里云百炼长视频生成指南

**生成 5 分钟+ 长视频的完整解决方案**

---

## 🎯 核心挑战

| 挑战 | 原因 | 解决方案 |
|------|------|---------|
| **时长限制** | 单次生成最长 15 秒 | 分段生成 + 后期拼接 |
| **角色一致性** | 每次生成都重新采样 | 固定种子 + 参考视频 + 角色设定 |
| **场景流畅性** | 场景间无关联 | 过渡镜头 + 统一风格提示词 |
| **成本控制** | 长视频成本高 | 优化分段策略 + 选择合适模型 |

---

## 📋 方案 1：分段生成 + 拼接（推荐）

### 工作流程

```
1. 剧本拆分 → 2. 角色设定 → 3. 分镜设计 → 4. 分段生成 → 5. 后期拼接
     ↓              ↓              ↓              ↓              ↓
  5 分钟=60 个     固定角色描述    每个镜头       15 秒/段        使用视频
  5 秒镜头         和外观参数      5-15 秒        生成 60 段       编辑软件
```

### 步骤 1：剧本拆分

```python
# 5 分钟视频拆分示例
script = """
【0:00-0:15】开场：未来城市全景，空中花园
【0:15-0:30】镜头 1：机器人园丁修剪植物
【0:30-0:45】镜头 2：阳光透过穹顶
【0:45-1:00】镜头 3：女孩走进花园
...
【4:45-5:00】结尾：镜头拉远，城市全景
"""

# 拆分为 60 个镜头，每个 5 秒
scenes = [
    {"id": 1, "start": "0:00", "end": "0:15", "prompt": "未来城市全景...", "type": "开场"},
    {"id": 2, "start": "0:15", "end": "0:30", "prompt": "机器人园丁...", "type": "角色"},
    # ... 共 60 个镜头
]
```

### 步骤 2：固定角色设定

```python
# 角色一致性关键：固定描述词
character_template = """
主角设定：
- 姓名：小艾
- 年龄：20 岁女性
- 发型：黑色长直发，齐刘海
- 服装：白色连衣裙，蓝色腰带
- 特征：大眼睛，微笑，皮肤白皙

每次生成时都包含以下关键词：
"20 岁亚洲女性，黑色长直发，齐刘海，白色连衣裙，蓝色腰带，大眼睛，微笑"
"""

# 使用示例
prompt = f"""
{character_template}

场景：小艾走进未来花园，好奇地环顾四周。
镜头：中景，缓慢推进。
风格：3D 卡通，明亮色彩，电影感。
"""
```

### 步骤 3：使用参考视频保持一致性

```python
from dashscope import VideoSynthesis

# 生成第一个镜头（建立角色参考）
first_scene = VideoSynthesis.async_call(
    api_key=api_key,
    model='wan2.6-t2v',
    prompt='20 岁亚洲女性，黑色长直发，齐刘海，白色连衣裙...（完整角色描述）',
    duration=15,
    seed=12345  # 固定随机种子
)

# 等待完成
first_result = VideoSynthesis.wait(task=first_scene, api_key=api_key)
reference_video_url = first_result.output.video_url

# 后续镜头使用参考视频
for scene in scenes[1:]:
    rsp = VideoSynthesis.async_call(
        api_key=api_key,
        model='wan2.6-r2v',  # 使用参考生视频模型
        prompt=scene['prompt'],
        video_url=reference_video_url,  # 参考第一个镜头的角色
        duration=15,
        seed=12345  # 使用相同种子
    )
```

### 步骤 4：场景过渡技巧

```python
# 过渡镜头提示词模板
transition_prompts = {
    "淡入": "画面从黑暗中逐渐亮起，镜头缓慢推进...",
    "淡出": "画面逐渐变暗，镜头慢慢拉远...",
    "切换": "镜头快速切换到下一个场景...",
    "溶解": "当前场景慢慢溶解为下一个场景...",
    "匹配剪辑": "相似的形状/动作匹配切换到下一场景..."
}

# 在场景间插入过渡镜头
scenes_with_transitions = []
for i, scene in enumerate(scenes):
    scenes_with_transitions.append(scene)
    if i < len(scenes) - 1:
        # 插入 2 秒过渡镜头
        transition = {
            "id": f"{scene['id']}_trans",
            "prompt": transition_prompts["切换"],
            "duration": 2
        }
        scenes_with_transitions.append(transition)
```

### 步骤 5：批量生成 + 拼接

```python
import subprocess
from pathlib import Path

# 批量生成所有片段
output_dir = Path("./video_segments")
output_dir.mkdir(exist_ok=True)

generated_videos = []
for i, scene in enumerate(scenes):
    print(f"生成片段 {i+1}/{len(scenes)}...")
    
    rsp = VideoSynthesis.async_call(
        api_key=api_key,
        model='wan2.6-t2v',
        prompt=scene['prompt'],
        duration=scene.get('duration', 15),
        seed=12345,  # 固定种子
        size="1280*720"
    )
    
    result = VideoSynthesis.wait(task=rsp, api_key=api_key)
    video_url = result.output.video_url
    
    # 下载视频
    import requests
    video_data = requests.get(video_url).content
    video_path = output_dir / f"segment_{i:03d}.mp4"
    with open(video_path, 'wb') as f:
        f.write(video_data)
    
    generated_videos.append(str(video_path))

# 使用 ffmpeg 拼接所有片段
with open("video_list.txt", "w") as f:
    for video in generated_videos:
        f.write(f"file '{video}'\n")

# 拼接命令
subprocess.run([
    "ffmpeg", "-f", "concat", "-safe", "0",
    "-i", "video_list.txt",
    "-c", "copy",
    "final_video.mp4"
])

print("视频拼接完成！")
```

---

## 🎭 方案 2：数字人长视频（适合播报类）

### 使用灵动人像 LivePortrait

**适用场景**: 新闻播报、课程讲解、产品介绍

```python
from dashscope import LivePortrait

# 灵动人像支持最长 180 秒（3 分钟）
rsp = LivePortrait.call(
    api_key=api_key,
    model='liveportrait',
    image_url='https://example.com/presenter.jpg',
    audio_url='https://example.com/full_audio.mp3'  # 3 分钟音频
)

result = LivePortrait.wait(task=rsp, api_key=api_key)
video_url = result.output.video_url
```

### 分段数字人方案

```python
# 如果音频超过 3 分钟，需要分段
audio_segments = [
    {"start": 0, "end": 180, "file": "audio_part1.mp3"},
    {"start": 180, "end": 300, "file": "audio_part2.mp3"},
]

generated_videos = []
for i, seg in enumerate(audio_segments):
    rsp = LivePortrait.call(
        api_key=api_key,
        model='liveportrait',
        image_url='https://example.com/presenter.jpg',
        audio_url=f"https://example.com/{seg['file']}"
    )
    result = LivePortrait.wait(task=rsp, api_key=api_key)
    generated_videos.append(download_video(result.output.video_url))

# 拼接
concatenate_videos(generated_videos, "final_presentation.mp4")
```

---

## 🎬 方案 3：混合方案（最佳效果）

### 结合多种模型

```
5 分钟视频结构:
├── 0:00-0:30  开场动画 (文生视频)
├── 0:30-2:00  主讲人播报 (数字人 LivePortrait)
├── 2:00-3:30  场景演示 (图生视频)
├── 3:30-4:30  案例分析 (参考生视频)
└── 4:30-5:00  结尾动画 (文生视频)
```

### 实现代码

```python
def generate_long_video(script_structure):
    """
    生成长视频的混合方案
    
    script_structure = [
        {"type": "text2video", "prompt": "...", "duration": 30},
        {"type": "digital_human", "image": "...", "audio": "...", "duration": 90},
        {"type": "image2video", "image": "...", "prompt": "...", "duration": 90},
        {"type": "reference2video", "video": "...", "prompt": "...", "duration": 60},
        {"type": "text2video", "prompt": "...", "duration": 30},
    ]
    """
    from dashscope import VideoSynthesis, DigitalHuman, LivePortrait
    
    segments = []
    
    for i, scene in enumerate(script_structure):
        print(f"生成片段 {i+1}/{len(script_structure)}: {scene['type']}")
        
        if scene['type'] == 'text2video':
            rsp = VideoSynthesis.async_call(
                api_key=api_key,
                model='wan2.6-t2v',
                prompt=scene['prompt'],
                duration=min(scene['duration'], 15)  # 单次最长 15 秒
            )
        elif scene['type'] == 'digital_human':
            rsp = LivePortrait.call(
                api_key=api_key,
                model='liveportrait',
                image_url=scene['image'],
                audio_url=scene['audio']
            )
        elif scene['type'] == 'image2video':
            rsp = VideoSynthesis.async_call(
                api_key=api_key,
                model='wan2.6-i2v',
                prompt=scene['prompt'],
                image_url=scene['image'],
                duration=min(scene['duration'], 15)
            )
        elif scene['type'] == 'reference2video':
            rsp = VideoSynthesis.async_call(
                api_key=api_key,
                model='wan2.6-r2v',
                prompt=scene['prompt'],
                video_url=scene['reference_video'],
                duration=min(scene['duration'], 10)
            )
        
        result = VideoSynthesis.wait(task=rsp, api_key=api_key)
        segments.append(download_video(result.output.video_url))
    
    # 拼接所有片段
    final_video = concatenate_videos_with_transitions(
        segments,
        transition_type="fade",
        transition_duration=1.0
    )
    
    return final_video
```

---

## 🔑 角色一致性关键技术

### 1. 固定随机种子

```python
# 所有片段使用相同种子
seed = 12345

for scene in scenes:
    rsp = VideoSynthesis.async_call(
        api_key=api_key,
        model='wan2.6-t2v',
        prompt=scene['prompt'],
        seed=seed,  # 固定种子
        duration=15
    )
```

### 2. 详细角色描述模板

```python
CHARACTER_TEMPLATE = """
【角色设定 - 每次生成都必须包含】
主角：小艾
- 性别年龄：20 岁亚洲女性
- 发型发色：黑色长直发，齐刘海，发梢微卷
- 眼睛：大眼睛，双眼皮，黑色瞳孔
- 服装：白色连衣裙，蓝色腰带，白色运动鞋
- 配饰：银色项链，左手手表
- 肤色：白皙
- 体型：苗条

【生成参数】
风格：3D 卡通，皮克斯风格
光照：柔和自然光
镜头：中景，平视角度
"""

# 使用
prompt = f"""
{CHARACTER_TEMPLATE}

【当前场景】
小艾走进未来花园，好奇地环顾四周，脸上露出惊喜的笑容。
"""
```

### 3. 使用参考视频

```python
# 第一个镜头生成角色参考视频
reference_rsp = VideoSynthesis.async_call(
    api_key=api_key,
    model='wan2.6-t2v',
    prompt=CHARACTER_TEMPLATE + "主角特写镜头",
    duration=15,
    seed=12345
)
reference_result = VideoSynthesis.wait(task=reference_rsp, api_key=api_key)
reference_video = reference_result.output.video_url

# 后续镜头使用参考视频
for scene in scenes[1:]:
    rsp = VideoSynthesis.async_call(
        api_key=api_key,
        model='wan2.6-r2v',  # 参考生视频模型
        prompt=scene['prompt'],
        video_url=reference_video,  # 保持角色一致
        duration=15,
        seed=12345
    )
```

### 4. 使用图生视频保持角色

```python
# 生成角色标准图像
character_image = generate_character_image()  # 使用文生图生成标准角色图

# 所有镜头都使用这张图作为首帧
for scene in scenes:
    rsp = VideoSynthesis.async_call(
        api_key=api_key,
        model='wan2.6-i2v',
        prompt=scene['prompt'],
        image_url=character_image,  # 固定角色图像
        duration=15,
        seed=12345
    )
```

---

## 🌅 场景流畅性保证

### 1. 过渡镜头设计

```python
transition_scenes = [
    # 淡入
    {"prompt": "画面从黑暗中逐渐亮起，镜头缓慢推进", "duration": 3},
    
    # 场景切换
    {"prompt": "镜头快速切换到下一个场景", "duration": 2},
    
    # 匹配剪辑
    {"prompt": "相似的圆形物体匹配切换", "duration": 2},
    
    # 淡出
    {"prompt": "画面逐渐变暗，镜头慢慢拉远", "duration": 3},
]
```

### 2. 统一视觉风格

```python
STYLE_TEMPLATE = """
【视觉风格 - 所有镜头统一】
风格：3D 卡通，皮克斯风格
色彩：明亮饱和，高对比度
光照：柔和自然光，温暖色调
画质：电影感，景深效果
"""

# 每个镜头都包含风格描述
for scene in scenes:
    full_prompt = f"""
    {STYLE_TEMPLATE}
    {CHARACTER_TEMPLATE}
    {scene['prompt']}
    """
    # 生成视频...
```

### 3. 使用视频编辑添加过渡

```python
import subprocess

def add_transitions(video_segments, output_file, transition_duration=1.0):
    """使用 ffmpeg 添加过渡效果"""
    
    # 创建滤镜链
    filter_complex = ""
    for i in range(len(video_segments) - 1):
        filter_complex += f"[{i}][{i+1}]xfade=transition=fade:duration={transition_duration}:offset={i*15-transition_duration}[v{i}];"
    
    # ffmpeg 命令
    cmd = [
        "ffmpeg",
        "-i", *video_segments,
        "-filter_complex", filter_complex.rstrip(";"),
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "23",
        output_file
    ]
    
    subprocess.run(cmd)
```

---

## 💰 成本优化

### 5 分钟视频成本估算

| 方案 | 片段数 | 单价 | 总成本 |
|------|--------|------|--------|
| 文生视频 (wan2.6-t2v) | 60 段×15 秒 | ¥0.5/秒 | ¥450 |
| 图生视频 (wan2.6-i2v) | 60 段×15 秒 | ¥0.6/秒 | ¥540 |
| 参考生视频 (wan2.6-r2v) | 60 段×10 秒 | ¥0.8/秒 | ¥480 |
| 混合方案 (推荐) | 20 段文生 +20 段图生 +20 段参考 | - | ¥350 |
| 数字人 (LivePortrait) | 2 段×180 秒 | ¥1.0/秒 | ¥360 |

### 优化建议

1. **减少片段数**: 每段 15 秒→每段 30 秒（需要后期拼接）
2. **使用加速模型**: wan2.6-t2v → wanx2.1-t2v-turbo
3. **降低分辨率**: 1080P → 720P (节省约 30% 成本)
4. **混合方案**: 关键场景用高质量模型，过渡场景用加速模型

---

## 📋 完整工作流程示例

```python
"""
5 分钟动画短片生成流程
"""

# 1. 准备阶段
script = load_script("my_story.txt")  # 加载剧本
scenes = split_into_scenes(script, max_duration=15)  # 拆分为 15 秒镜头
character_sheet = create_character_sheet()  # 创建角色设定表

# 2. 生成参考视频
reference_video = generate_reference_video(
    prompt=character_sheet,
    model='wan2.6-t2v',
    duration=15
)

# 3. 批量生成所有片段
generated_segments = []
for i, scene in enumerate(scenes):
    print(f"生成片段 {i+1}/{len(scenes)}")
    
    rsp = VideoSynthesis.async_call(
        api_key=api_key,
        model='wan2.6-r2v',  # 使用参考生视频保持角色一致
        prompt=f"{character_sheet}\n{scene['prompt']}",
        video_url=reference_video,
        duration=scene['duration'],
        seed=12345  # 固定种子
    )
    
    result = VideoSynthesis.wait(task=rsp, api_key=api_key)
    segment_path = download_video(result.output.video_url, f"segment_{i:03d}.mp4")
    generated_segments.append(segment_path)

# 4. 添加过渡效果
add_transitions(
    generated_segments,
    "final_video.mp4",
    transition_duration=1.0
)

# 5. 添加背景音乐和音效
add_audio_tracks(
    "final_video.mp4",
    background_music="bgm.mp3",
    sound_effects=["sfx1.mp3", "sfx2.mp3"]
)

print("长视频生成完成！")
```

---

## ⚠️ 注意事项

1. **视频 URL 有效期 24 小时** - 生成后立即下载
2. **固定种子不能保证 100% 一致** - 仍需后期检查
3. **长视频成本高** - 建议先测试 1 分钟版本
4. **生成时间** - 60 段视频约需 2-4 小时
5. **存储需求** - 5 分钟视频约 500MB-1GB

---

**推荐工具**:
- 视频拼接：ffmpeg, Adobe Premiere, DaVinci Resolve
- 音频处理：Audacity, Adobe Audition
- 过渡效果：ffmpeg xfade 滤镜

---

**最后更新**: 2026-04-01  
**维护人**: 胖福
