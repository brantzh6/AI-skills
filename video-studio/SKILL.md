---
name: video-studio
description: AI video generation with Alibaba Cloud Wan 2.6/2.7. Text-to-video, image-to-video (first frame, first+last frame), reference video generation with multi-character, multi-shot support.
---

# Video Studio 🎬

AI video generation powered by Alibaba Cloud Wan 2.6/2.7 models.

## Capabilities

| Mode | Model | Description |
|------|-------|-------------|
| **Text-to-Video** | wan2.7-t2v, wan2.6-t2v | Generate video from text prompt |
| **Image-to-Video** | wan2.6-i2v | First frame or first+last frame → video |
| **Reference-to-Video** | wan2.7-r2v, wan2.6-r2v | Multiple reference images/videos → multi-character video |

## Usage

### Text to Video
```
/video <prompt>
/video A cat walking in a garden, cinematic lighting --duration 10 --resolution 720P
```

### Image to Video
```
# First frame only
/video --mode i2v --image <first_frame.jpg> <prompt>

# First + Last frame (controlled transition)
/video --mode i2v --first <start.jpg> --last <end.jpg> <prompt>
```

### Reference to Video (Multi-character, Multi-shot)
```
# Single character reference (video)
/video --mode r2v --ref <character_video.mp4> <prompt>
  → Use "character1" or "参考视频" in prompt

# Single character reference (image)
/video --mode r2v --ref <character.jpg> <prompt>
  → Use "图1" or "参考图片" in prompt

# Multi-character interaction (up to 3 videos + 2 images = 5 total)
/video --mode r2v \
  --ref <char1.mp4> --ref <char2.mp4> --ref <prop.jpg> \
  "视频1抱着图3在咖啡厅弹奏民谣，视频2笑着看着视频1"

# Multi-shot storytelling with storyboard image
/video --mode r2v --ref <storyboard.png> <prompt>
  → Describe storyboard panels in prompt (panel 1, panel 2, etc.)

# With first frame control
/video --mode r2v \
  --ref <char1.mp4> --ref <char2.mp4> \
  --first-frame <opening_scene.jpg> \
  "视频1和图1在花园里对话"
```

## Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--mode` | t2v, i2v, r2v | t2v |
| `--model` | Model name (auto-detected from mode) | wan2.6-t2v |
| `--image` | First frame image (i2v mode) | - |
| `--first` | First frame image (i2v mode, alias for --image) | - |
| `--last` | Last frame image (i2v mode) | - |
| `--ref` | Reference video/image URL or path (r2v mode, repeatable) | - |
| `--first-frame` | First frame for r2v mode (controls opening shot) | - |
| `--audio` | Audio file URL for video soundtrack | - |
| `--reference-voice` | Audio URL for character voice reference (r2v) | - |
| `--duration` | Video duration in seconds | t2v: 5, i2v: 5, r2v: 5 |
| `--resolution` | 480P, 720P, 1080P | 720P |
| `--ratio` | 16:9, 9:16, 1:1, 4:3, 3:4 | 16:9 |
| `--shot-type` | single (单镜头) or multi (多镜头) | single |
| `--no-audio` | Generate silent video (wan2.6-r2v-flash only) | - |
| `--seed` | Random seed | random |
| `--negative` | Negative prompt | - |
| `--no-prompt-extend` | Disable prompt enhancement | - |
| `--watermark` | Add "AI generated" watermark | - |
| `--task-id` | Task ID to check status | - |
| `--poll` | Poll task until completion | - |

## Reference-to-Video Details

### Role Reference Convention
References are identified by their order in the `--ref` array:

| Order | wan2.7 (media array) | wan2.6 (reference_urls) |
|-------|---------------------|------------------------|
| 1st video | 视频1 | character1 |
| 2nd video | 视频2 | character2 |
| 1st image | 图1 | character1 |
| 2nd image | 图2 | character2 |

### Limits (wan2.7-r2v)
- Reference images: up to 5
- Reference videos: up to 3
- Total images + videos: ≤ 5
- First frame: max 1
- Each reference contains one character/subject

### Limits (wan2.6-r2v)
- Reference images: up to 5
- Reference videos: up to 3
- Total images + videos: ≤ 5

### Prompt Examples for Multi-character
```
# 2 characters interacting
"视频1对视频2说：明天见！视频2笑着挥手告别"

# Character with prop
"character1抱着character3在窗边看书"

# Storyboard-driven multi-shot
"参考图片中的冒险故事：小男孩和小机器人在奇幻森林中寻找宝藏，保持角色和场景一致，不要加入文字"
```

## API Details

- **Provider**: Alibaba Cloud Bailian (DashScope)
- **Models**: wan2.7-t2v, wan2.6-t2v, wan2.6-i2v, wan2.7-r2v, wan2.6-r2v, wan2.6-r2v-flash
- **API Key**: From bailian auth profile
- **Base URL**: https://dashscope.aliyuncs.com

## Notes

- All video generation is asynchronous (1-5 minutes)
- Video URLs expire after 24 hours - download immediately
- Output format: MP4 (H.264)
- wan2.7 supports auto-generated audio from video content
- wan2.6-r2v-flash supports silent video generation (`--no-audio`)
