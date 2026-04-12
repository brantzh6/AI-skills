# 🎬 电影级 AI 视频工作流标准

**版本**: v2.0 (专业级)  
**更新时间**: 2026-04-07  
**适用模型**: Wan 2.7-t2v

---

## 📋 专业分镜脚本格式（六大要素）

每个镜头必须包含以下要素：

```
镜头 X [起始 - 结束秒数]
- 🎥 镜头语言：景别 + 角度 + 运动（如：特写 + 低角度 + 缓慢推进）
- 👤 主体细节：具体外貌 + 微表情 + 肢体动作（如：瞳孔放大、胡须颤抖）
- 🌍 环境/粒子：天气 + 光线 + 粒子效果（如：雪花慢动作飘落）
- 💡 光影设计：光源方向 + 色温 + 对比度（如：冷蓝色侧光，高对比度）
- 🎭 情绪氛围：抽象情绪的具体视觉化（如：紧张=爪子抓进雪里）
- 🔊 声音设计：BGM+ 音效 + 节奏（如：低沉贝斯 + 风声呼啸）
```

---

## 🎭 情绪视觉化对照表

| 抽象情绪 | 具体视觉表现 |
|---------|-------------|
| **紧张** | 瞳孔放大、肌肉紧绷、爪子抓进物体、慢动作、冷色调 |
| **幽默** | 夸张表情、舌头甩出、眼珠转圈、倾斜构图、暖色调 |
| **悲伤** | 低头、眼泪、雨水、灰蓝色调、慢速镜头 |
| **喜悦** | 跳跃动作、尾巴摇摆、阳光破云、暖金色调、快速剪辑 |
| **恐惧** | 后退动作、瞳孔收缩、颤抖、阴影笼罩、低角度 |

---

## 🎥 镜头语言库

### 景别定义
| 景别 | 画面范围 | 用途 |
|------|----------|------|
| **大远景** | 环境为主，人物很小 | 交代场景、氛围 |
| **全景** | 人物全身 + 部分环境 | 人物与环境关系 |
| **中景** | 人物膝盖以上 | 叙事主力，对话场景 |
| **近景** | 人物胸部以上 | 表情、情绪 |
| **特写** | 面部/手部/物体细节 | 强调关键元素 |
| **大特写** | 眼睛/嘴唇/微小细节 | 极致情绪表达 |

### 镜头运动
| 运动 | 效果 | 示例 |
|------|------|------|
| **固定** | 稳定、客观 | 对话、静物 |
| **缓慢推进** | 聚焦、紧张 | 发现、揭示 |
| **快速推进** | 冲击、震惊 | 突发事件 |
| **拉远** | 远离、释然 | 结局、离别 |
| **摇摄** | 环视、搜索 | 探索、观察 |
| **跟拍** | 伴随、沉浸 | 追逐、同行 |
| **甩镜头** | 能量、转场 | 动作场景 |

---

## 🔊 声音设计指南

### Wan 2.7 音频能力说明
- ✅ 支持自动匹配环境音/轻音效
- ⚠️ 复杂配乐仍需后期叠加
- ✅ 可在 prompt 中描述声音氛围

### Prompt 中的声音描述格式
```
SOUND DESIGN: [BGM 类型] + [具体音效] + [节奏变化]

示例：
SOUND DESIGN: Tense orchestral music building up, sudden dramatic boom sound, then comedic playful flute music.
```

### 音效库参考
| 场景 | 音效描述 |
|------|---------|
| **紧张 buildup** | Low rumbling bass, tense strings, wind howling |
| **动作爆发** | Sudden dramatic BOOM, whoosh sound |
| **喜剧效果** | Comedic trombone slide, playful flute |
| **角色音效** | Fox squeaks, cat purring, whimpering |

---

## 📝 专业级 Prompt 模板

```
[风格定义], [预算级别].

SOUND DESIGN: [声音设计描述].

The first shot [0-3 seconds] [镜头语言]: [主体细节]. [环境/粒子]. [光影设计]. SOUND: [声音描述].

The second shot [3-6 seconds] [镜头语言]: [主体细节]. [环境/粒子]. [光影设计]. SOUND: [声音描述].

The third shot [6-10 seconds] [镜头语言]: [主体细节]. [环境/粒子]. [光影设计]. SOUND: [声音描述].
```

---

## 🎬 完整案例：布偶猫雪山抓狐狸

```
Pixar 3D animation style, high budget animated short film quality.

SOUND DESIGN: Tense orchestral music building up, sudden dramatic boom sound, then comedic playful flute music.

The first shot [0-3 seconds] extreme close-up on cat's eyes, low angle, slow dramatic push-in: A fluffy seal-point ragdoll cat's pupils dilate dramatically, whiskers trembling, claws dig deep into snow. Snow particles falling in slow motion. Cold blue lighting, dramatic shadows. SOUND: Low rumbling bass, tense strings, wind howling.

The second shot [3-6 seconds] dynamic action shot, fast tracking shot with motion blur: The cat explodes forward in a powerful leap, body fully stretched, fur flowing backward. Fox's eyes wide with terror, mouth open in silent scream. Snow explodes upward in mushroom cloud. SOUND: Sudden dramatic BOOM, whoosh sound, fox squeaks.

The third shot [6-10 seconds] comedic close-up, slight Dutch angle: Cat lands with triumphant thud, pinning fox under fluffy paws. Cat has exaggerated smug grin, tail wagging. Fox comically pedals legs in air, tongue lolling out, eyes spinning. Warm golden sunlight bursts through clouds. SOUND: Comedic trombone slide, playful flute, cat purring triumphantly.
```

---

## 🚧 当前局限性与改进方向

### 已实现 ✅
- [x] 时间戳分镜格式 (`[0-3 seconds]`)
- [x] 多镜头叙事支持
- [x] 基础声音氛围匹配
- [x] 720P/1080P 分辨率
- [x] 10-15 秒时长

### 待改进 ⚠️
- [ ] **音频能力弱**：Wan 2.7 仅能生成环境音，无法生成复杂配乐
  - **改进方案**：后期用 Suno/Udio 生成 BGM + FFmpeg 合成
- [ ] **画面细节控制弱**：抽象情绪词（如"紧张"）无法理解
  - **改进方案**：建立情绪→视觉对照表，用具体肢体语言描述
- [ ] **镜头切换生硬**：时间戳格式有时被忽略
  - **改进方案**：在 prompt 开头明确声明"multi-shot video with clear cuts"
- [ ] **物理运动不自然**：AI 对重力、惯性理解有限
  - **改进方案**：用"explodes forward"、"slams down"等强动词

### 未来路线图 📅
| 阶段 | 目标 | 预计时间 |
|------|------|---------|
| **Phase 1** | 建立专业 Prompt 模板库 | 已完成 |
| **Phase 2** | 集成 Suno BGM 生成 | 待实现 |
| **Phase 3** | FFmpeg 自动合成工作流 | 待实现 |
| **Phase 4** | 镜头语言自动优化 | 待实现 |

---

## 📚 参考资料
- Wan 2.7 API 文档：https://help.aliyun.com/zh/model-studio/text-to-video-api-reference
- 镜头语言百科：https://en.wikipedia.org/wiki/Cinematography
- 声音设计基础：https://www.filmsound.org/
