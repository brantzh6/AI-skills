---
name: video-studio
description: AI video generation with Alibaba Cloud Wan 2.6/2.7. Text-to-video, image-to-video, reference video generation, and more.
---

# Video Studio 🎬

AI video generation powered by Alibaba Cloud Wan 2.6/2.7 models.

## Capabilities

| Mode | Model | Description |
|------|-------|-------------|
| **Text-to-Video** | wan2.7-t2v / wan2.6-t2v | Generate video from text prompt |
| **Image-to-Video (First Frame)** | wan2.6-i2v | First frame image → video |
| **Image-to-Video (First+Last)** | wan2.6-i2v | First + last frame → controlled video |
| **Reference Video** | wan2.6-r2v | Reference video style → new video |

## Usage

### Text to Video
```
/video <prompt>
/video A cat walking in a garden, cinematic lighting
/video 一只小猫在月光下奔跑
```

### Image to Video (First Frame)
```
/video --mode i2v --image <image_path> <prompt>
```

### Image to Video (First + Last Frame)
```
/video --mode i2v --first <first_frame> --last <last_frame> <prompt>
```

### Reference Video Generation
```
/video --mode r2v --ref <reference_video> <prompt>
```

### Advanced Options
```
/video <prompt> --duration 10 --resolution 720P --ratio 16:9 --seed 42
/video <prompt> --model wan2.6-t2v --negative "blurry, low quality"
```

## Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--mode` | Mode: t2v, i2v, r2v | t2v |
| `--model` | Model: wan2.7-t2v, wan2.6-t2v, wan2.6-i2v, wan2.6-r2v | wan2.6-t2v |
| `--image` | Input image for i2v mode (first frame) | - |
| `--first` | First frame image for i2v | - |
| `--last` | Last frame image for i2v | - |
| `--ref` | Reference video for r2v mode | - |
| `--duration` | Video duration in seconds (2-15) | 5 |
| `--resolution` | Resolution: 480P, 720P, 1080P | 720P |
| `--ratio` | Aspect ratio: 16:9, 9:16, 1:1, 4:3, 3:4 | 16:9 |
| `--seed` | Random seed for reproducibility | random |
| `--negative` | Negative prompt | - |
| `--no-prompt-extend` | Disable prompt enhancement | - |
| `--watermark` | Add "AI generated" watermark | - |
| `--audio` | Audio file URL for video soundtrack | - |
| `--task-id` | Task ID to check status | - |
| `--poll` | Poll task until completion | - |

## API Details

- **Provider**: Alibaba Cloud Bailian (DashScope)
- **Models**: wan2.7-t2v, wan2.6-t2v, wan2.6-i2v, wan2.6-r2v
- **API Key**: From bailian auth profile
- **Base URL**: https://dashscope.aliyuncs.com

## Video Generation Flow

All video generation is **asynchronous**:
1. Submit task → get `task_id`
2. Poll status with `--task-id <id> --poll`
3. Download video when `SUCCEEDED`

Video URLs expire after 24 hours - download immediately.

## Notes

- Video generation takes 1-5 minutes typically
- wan2.7 supports up to 15 seconds duration
- wan2.6 supports up to 10 seconds
- Videos include auto-generated audio by default (wan2.6+)
- Output format: MP4 (H.264)
