---
name: creative-studio-research
description: Creative Studio Research Lab. Continuously researches AI image/video prompt engineering, maintains prompt libraries, scene libraries, and best practices. Updates regularly from industry sources.
---

# Creative Studio Research Lab 🔬🎨🎬

创作研究室。持续追踪 AI 生图/生视频领域的最佳 prompt 实践、技巧、模板，维护 Prompt 库和场景库。

## 使命

不是简单的 API 调用器，而是创作专家。让每一次生成都有据可循、有例可参、有法可依。

---

## 研究方法论

### 信息源监控

| 类型 | 来源 | 更新频率 |
|------|------|----------|
| **官方文档** | 阿里云百炼、Runway、OpenAI、Google Veo | 每周 |
| **GitHub 精选** | awesome-ai-video-prompts, prompt repos | 每两周 |
| **创作者社区** | Apatero、RunwayML Blog、Civitai、Liblib | 每周 |
| **论文/技术** | arXiv 视频生成论文、模型发布 | 每月 |
| **实战案例** | 用户生成结果、效果对比 | 持续 |

### 研究流程

```
1. 发现 → 从各渠道收集新 prompt 技巧/模板
2. 验证 → 实际调用 API 测试效果
3. 对比 → 与已有 prompt 对比生成质量
4. 记录 → 存入 Prompt 库或场景库
5. 分类 → 按类型/风格/场景归档
6. 更新 → 更新 SKILL.md 和文档
```

---

## 📝 Prompt 工程核心原则

### 通用公式（跨模型）

```
[媒介/风格] + [主体+细节] + [环境/场景] + [光影/氛围] + [构图/镜头] + [技术参数/画质]
```

### 关键原则

1. **词序即权重**：前面的词影响力最大
2. **具体 > 抽象**："午后阳光透过百叶窗" > "明亮"
3. **技术术语有效**：相机型号、镜头、光圈影响风格
4. **负面提示同样重要**：排除不想要的元素
5. **30 词精准 > 100 词啰嗦**
6. **迭代 3-5 次是常态**，不要期待一次完美

---

## 📚 Prompt 库（按类别）

> 每个 prompt 都经过验证，标注效果和适用模型。
> 详细 Prompt 库见 `prompts/` 目录。

### 图片生成 Prompt

| 类别 | 文件 | 数量 |
|------|------|------|
| 人物写真 | `prompts/portrait.md` | 10+ |
| 风景自然 | `prompts/landscape.md` | 10+ |
| 产品摄影 | `prompts/product.md` | 8+ |
| 美食 | `prompts/food.md` | 6+ |
| 建筑室内 | `prompts/architecture.md` | 8+ |
| 动物 | `prompts/animals.md` | 6+ |
| 抽象艺术 | `prompts/abstract.md` | 6+ |
| 赛博朋克 | `prompts/cyberpunk.md` | 6+ |

### 视频生成 Prompt

| 类别 | 文件 | 数量 |
|------|------|------|
| 人物动作 | `prompts/video-character.md` | 8+ |
| 风景延时 | `prompts/video-timelapse.md` | 6+ |
| 产品展示 | `prompts/video-product.md` | 6+ |
| 情感叙事 | `prompts/video-narrative.md` | 8+ |
| 多角色互动 | `prompts/video-multi-char.md` | 6+ |
| 多镜头叙事 | `prompts/video-multishot.md` | 6+ |
| 音乐 MV | `prompts/video-music.md` | 4+ |

---

## 🎬 场景库（按场景类型）

> 场景库 = 完整可用的创作模板，包含 prompt + 参数建议。
> 详细场景库见 `scenes/` 目录。

| 场景 | 文件 | 包含 |
|------|------|------|
| 品牌宣传片 | `scenes/brand-commercial.md` | 5 个完整方案 |
| 产品展示 | `scenes/product-showcase.md` | 8 个方案 |
| 个人写真 | `scenes/portrait-session.md` | 6 个方案 |
| 风景旅行 | `scenes/travel-landscape.md` | 6 个方案 |
| 美食餐饮 | `scenes/food-dining.md` | 6 个方案 |
| 短视频剧情 | `scenes/short-drama.md` | 5 个完整剧本+分镜 |
| 音乐 MV | `scenes/music-video.md` | 4 个方案 |
| 教育科普 | `scenes/education.md` | 4 个方案 |

### 场景文件结构

每个场景文件包含：
```markdown
# 场景名称

## 需求分析
- 目标效果
- 关键要素

## 方案 1: 方案名称
- 风格方向
- 使用模型
- 完整 Prompt
- 推荐参数
- 预期效果
- 适用场景

## 参考案例
- 成功案例截图/链接
- 失败案例和原因分析
```

---

## 🎨 风格词库

### 图片风格关键词

| 风格 | 核心关键词 | 适用场景 |
|------|-----------|----------|
| **商业摄影** | `商业摄影, 杂志品质, 专业布光, 精细修图` | 产品、人像 |
| **电影质感** | `电影帧, 变形宽银幕镜头, 电影级调色, 24fps` | 叙事、氛围 |
| **日系小清新** | `日系风格, 柔和色调, 自然光, 清新淡雅` | 人像、生活 |
| **赛博朋克** | `赛博朋克, 霓虹灯, 蓝紫主色调, 未来城市` | 科幻、科技 |
| **水彩画** | `水彩画, 湿画法, 颜料晕染, 柔和边缘` | 艺术、插画 |
| **油画** | `油画, 厚涂, 笔触感, 古典大师风格` | 艺术、肖像 |
| **3D 渲染** | `3D 渲染, C4D, Blender, OC 渲染器, 次表面散射` | 产品、概念 |
| **皮克斯风格** | `皮克斯动画风格, 迪士尼风格, 3D 卡通, Q 版` | 角色、故事 |

### 视频镜头语言词

| 镜头运动 | 关键词 | 效果 |
|----------|--------|------|
| 推 | `slow zoom in, camera pushing forward` | 聚焦、紧张 |
| 拉 | `slow zoom out, camera pulling back` | 释然、全景 |
| 摇 | `slow pan right/left` | 环视、跟随 |
| 移 | `tracking shot, dolly shot` | 流动、伴随 |
| 跟 | `following shot, tracking from behind` | 沉浸、追逐 |
| 升 | `crane up, aerial rising` | 开阔、升华 |
| 固定 | `static camera, locked off shot` | 客观、稳定 |

---

## 📖 学习资源索引

### 核心资源

| 资源 | 链接 | 类型 |
|------|------|------|
| 阿里云万相文生图 API | https://help.aliyun.com/zh/model-studio/text-to-image-v2-api-reference | 官方文档 |
| 阿里云万相文生视频 API | https://help.aliyun.com/zh/model-studio/text-to-video-api-reference | 官方文档 |
| 阿里云万相图生视频 API | https://help.aliyun.com/zh/model-studio/image-to-video-api-reference | 官方文档 |
| 阿里云万相参考生视频 API | https://help.aliyun.com/zh/model-studio/wan-video-to-video-api-reference | 官方文档 |
| Apatero Prompt 工程指南 | https://apatero.com/blog/ai-image-prompts-engineering-guide-2026 | 教程 |
| Runway Prompt 指南 | https://runwayml.com/resources/ai-video-prompting-guide | 官方教程 |
| Awesome AI Video Prompts | https://github.com/geekjourneyx/awesome-ai-video-prompts | GitHub 精选 |

---

## 🔧 使用方式

### 查询 Prompt

```
/research prompt portrait photography
→ 返回人物写真相关的 prompt 模板和最佳实践
```

### 查询场景

```
/research scene product showcase
→ 返回产品展示场景的完整方案
```

### 研究新技巧

```
/research latest video techniques
→ 搜索最新视频生成技巧并更新知识库
```

### 对比测试

```
/research compare prompt "prompt A" vs "prompt B"
→ 用两个 prompt 分别生成，对比效果
```

### 定期更新

通过 cron 任务自动更新（见 HEARTBEAT.md 或 cron 配置）：
- 每周检查信息源更新
- 每月整理并归档新 prompt
- 每季度更新风格词库

---

## 📊 更新日志

> 记录每次研究发现的更新。

详见 `docs/update-log.md`

---

## ⚠️ 注意事项

- 所有 prompt 需经过实际测试验证后才能入库
- 标注每个 prompt 适用的模型和版本
- 记录生成效果评分（1-5 星）
- 保留失败案例作为反面教材
- 不同模型对同一 prompt 的响应可能差异很大
