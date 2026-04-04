---
name: image-studio
description: AI image generation and editing with Alibaba Cloud Wan 2.6. Text-to-image, image editing with reference images, style transfer, and more.
---

# Image Studio 🎨

AI image generation and editing powered by Alibaba Cloud Wan 2.6 models.

## Capabilities

| Mode | Model | Description |
|------|-------|-------------|
| **Text-to-Image** | wan2.6-t2i | Generate images from text prompts |
| **Image Editing** | wan2.6-image | Edit images with reference images + prompts |
| **Style Transfer** | wan2.6-image | Transfer style from reference to new content |
| **Multi-Image Edit** | wan2.6-image | Use 1-4 reference images for editing |

## Usage

### Generate Image from Text
```
/image <prompt>
/image A beautiful sunset over mountains, oil painting style
/image 一只可爱的猫咪坐在窗台上，阳光洒进来
```

### Edit Image with Reference
```
/image-edit <image> <edit instruction>
/image-edit cat.jpg make it wear a cowboy hat
```

### Style Transfer
```
/image-edit <reference_image> "generate <subject> in this style"
```

### Advanced Options
```
/image <prompt> --size 1696*960 --n 1 --seed 42
/image <prompt> --negative "low quality, blurry"
```

## Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--size W*H` | Image resolution (see sizes below) | 1280*1280 |
| `--n N` | Number of images (1-4) | 1 |
| `--seed N` | Random seed for reproducibility | random |
| `--negative TEXT` | Negative prompt | - |
| `--no-prompt-extend` | Disable prompt enhancement | - |
| `--watermark` | Add "AI generated" watermark | - |

### Common Resolutions
| Ratio | Size |
|-------|------|
| 1:1 | 1280*1280 |
| 3:4 | 1104*1472 |
| 4:3 | 1472*1104 |
| 16:9 | 1696*960 |
| 9:16 | 960*1696 |

## API Details

- **Provider**: Alibaba Cloud Bailian (DashScope)
- **Models**: wan2.6-t2i, wan2.6-image
- **API Key**: From bailian auth profile
- **Base URL**: https://dashscope.aliyuncs.com

## Notes

- Generated images are PNG format
- Image URLs expire after 24 hours - download immediately
- Image editing requires at least 1 reference image
- Maximum 4 reference images for editing mode
