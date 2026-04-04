# 阿里云百炼全系列能力清单

**版本**: v26.4.1  
**更新时间**: 2026-04-01  
**下次更新**: 2026-04-08 (每周更新)  
**负责人**: 胖福

---

## 📊 信息概览

| 类别 | 模型数量 | 厂商数量 | 最后核实 | 文档链接 |
|------|---------|---------|---------|----------|
| 千问系列 | 15+ | 1 | 2026-04-01 | [⬇️](#-千问-qwen-系列) |
| 第三方模型 | 20+ | 4 | 2026-04-01 | [⬇️](#-第三方模型) |
| **图像生成** | **27+** | **1** | **2026-04-01** | **[⬇️](#-图像生成与编辑)** |
| **视频生成** | **20+** | **1** | **2026-04-01** | **[⬇️](#-视频生成与编辑)** |
| **语音处理** | **10+** | **1** | **2026-04-01** | **[⬇️](#-语音处理)** |
| **全模态** | **11+** | **1** | **2026-04-01** | **[⬇️](#-全模态模型)** |
| Embedding | 2+ | 1 | 2026-04-01 | [⬇️](#-embedding-向量模型) |
| **总计** | **110+** | **7** | **2026-04-01** | - |

---

## 🔗 官方信息源

### 核心文档
| 文档名称 | URL | 用途 |
|---------|-----|------|
| 模型大全 | https://help.aliyun.com/zh/model-studio/models | 完整模型列表和价格 |
| API 参考 | https://help.aliyun.com/zh/model-studio/model-api-reference/ | API 调用文档 |
| 定价详情 | https://help.aliyun.com/zh/model-studio/model-pricing | 价格明细 |
| 开发文档 | https://help.aliyun.com/zh/model-studio/development-documentation/ | 开发指南 |

### 第三方模型文档
| 厂商 | 文档 URL | 说明 |
|------|---------|------|
| **智谱 GLM** | https://help.aliyun.com/zh/model-studio/glm | GLM 系列模型 |
| **Kimi** | https://help.aliyun.com/zh/model-studio/kimi-api | Kimi 系列模型 |
| **DeepSeek** | https://help.aliyun.com/zh/model-studio/deepseek-api | DeepSeek 系列 |
| **MiniMax** | https://help.aliyun.com/zh/model-studio/minimax-api | MiniMax 系列 |

### 专项能力文档（已验证独立页面）

| 能力类别 | 独立文档 URL | 验证状态 |
|---------|------------|---------|
| **🎨 图像生成** | https://help.aliyun.com/zh/model-studio/image-generation/ | ✅ 已验证 |
| **🎨 图像编辑** | https://help.aliyun.com/zh/model-studio/image-editing-and-generation/ | ✅ 已验证 |
| **🎨 文生图 API** | https://help.aliyun.com/zh/model-studio/qwen-image-api | ✅ 已验证 |
| **🎨 图像编辑 API** | https://help.aliyun.com/zh/model-studio/qwen-image-edit-guide | ✅ 已验证 |
| **🎨 万相图像编辑** | https://help.aliyun.com/zh/model-studio/wanx-image-edit | ✅ 已验证 |
| **🎬 视频生成** | https://help.aliyun.com/zh/model-studio/use-video-generation | ✅ 已验证 |
| **🎬 文生视频** | https://help.aliyun.com/zh/model-studio/text-to-video-guide/ | ✅ 已验证 |
| **🎬 视频 API** | https://help.aliyun.com/zh/model-studio/first-call-to-image-and-video-api | ✅ 已验证 |
| **🎤 语音识别** | https://help.aliyun.com/zh/model-studio/speech-recognition/ | ✅ 已验证 |
| **🎤 实时语音识别** | https://help.aliyun.com/zh/model-studio/real-time-speech-recognition | ✅ 已验证 |
| **🎤 Fun-ASR API** | https://help.aliyun.com/zh/model-studio/fun-asr-real-time-speech-recognition-api-reference/ | ✅ 已验证 |
| **🎤 语音合成 (TTS)** | https://help.aliyun.com/zh/model-studio/text-to-speech | ✅ 已验证 |
| **🎤 千问语音合成** | https://help.aliyun.com/zh/model-studio/qwen-tts | ✅ 已验证 |
| **🔮 全模态 Omni** | https://help.aliyun.com/zh/model-studio/qwen-omni | ✅ 已验证 |
| **👁️ 视觉理解** | https://help.aliyun.com/zh/model-studio/vision | ✅ 已验证 |
| **👁️ 视觉推理** | https://help.aliyun.com/zh/model-studio/visual-reasoning | ✅ 已验证 |
| **👁️ 添加视觉能力** | https://help.aliyun.com/zh/model-studio/add-vision-skill | ✅ 已验证 |
| **🔢 多模态** | https://help.aliyun.com/zh/model-studio/multimodal | ✅ 已验证 |
| **🔢 多模态配置** | https://help.aliyun.com/zh/model-studio/multimodal-app-configuration | ✅ 已验证 |
| **🔢 第三方语音集成** | https://help.aliyun.com/zh/model-studio/third-party-voice-integration | ✅ 已验证 |
| 深度思考 | https://help.aliyun.com/zh/model-studio/deep-thinking | ✅ 已验证 |
| 联网搜索 | https://help.aliyun.com/zh/model-studio/web-search | ✅ 已验证 |
| Function Calling | https://help.aliyun.com/zh/model-studio/qwen-function-calling | ✅ 已验证 |
| 上下文缓存 | https://help.aliyun.com/zh/model-studio/context-cache | ✅ 已验证 |
| Coding Plan | https://help.aliyun.com/zh/model-studio/coding-plan | ✅ 已验证 |
| 模型总览 | https://help.aliyun.com/zh/model-studio/models | ✅ 总页面 |
| 模型更新 | https://help.aliyun.com/zh/model-studio/newly-released-models | ✅ 已验证 |

---

## 📝 更新日志

| 版本 | 日期 | 更新内容 | 操作人 |
|------|------|---------|--------|
| v26.4.1 | 2026-04-01 | 新增万相 2.7 图像生成、Qwen3.5-Omni 系列全模态模型 | 胖福 |
| v1.0 | 2026-03-31 | 初始版本，完成全量信息收集 | 胖福 |
| | | | |

---

## 🎯 千问 (Qwen) 系列

### 旗舰模型

| 模型 | 上下文 | Think | 搜索 | 多模态 | 价格 (输入/输出) | 地域 | 状态 |
|------|--------|-------|------|--------|-----------------|------|------|
| **Qwen3-Max** | 256K | ✅ | ✅ | ❌ | ¥2.5-15 / ¥10-60 | 北京 | ✅ |
| **Qwen3.5-Plus** | 1M | ✅ | ✅ | ✅ 图/视频 | ¥0.8 / ¥4.8 | 北京/新加坡 | ✅ 推荐 |
| **Qwen3.5-Flash** | 1M | ❌ | ✅ | ❌ | ¥0.2 / ¥2 | 北京/新加坡 | ✅ |

---

## 🎨 图像生成与编辑

### 文生图模型

| 模型 | 类型 | 价格 | 特点 | 文档 |
|------|------|------|------|------|
| **万相 2.7-Image-Pro** | 文生图/编辑 | ¥0.08/张 | **4K 输出**、文字渲染强、专业版 | [详情](https://help.aliyun.com/zh/model-studio/wan-image-generation-api-reference) |
| **万相 2.7-Image** | 文生图/编辑 | ¥0.06/张 | 4K 输出、主体一致性强、加速版 | [详情](https://help.aliyun.com/zh/model-studio/wan-image-generation-api-reference) |
| **千问文生图** | 通用 | ¥0.05/张 | 复杂指令、高清写实、中英文本渲染 | [详情](https://help.aliyun.com/zh/model-studio/qwen-image-api) |
| **万相基础文生图** | 人像/电商 | ¥0.03/张 | 证件照、电商图、动漫/国风/二次元 | [详情](https://help.aliyun.com/zh/model-studio/wanx-image-edit) |
| **Z-Image** | 轻量级 | ¥0.02/张 | 快速生成、中英双语、多风格 | [详情](https://help.aliyun.com/zh/model-studio/models#d7ef4964cd1vk) |
| **图文混排输出** | 文 + 图 | ¥0.08/次 | 先生成文字再生成对应图像 | [详情](https://help.aliyun.com/zh/model-studio/models#157125edeb9tx) |
| **Stable Diffusion** | 第三方 | ¥0.03/张 | 开源生态、艺术创作 | [详情](https://help.aliyun.com/zh/model-studio/models#a4321a2dc7zg7) |
| **FLUX** | 第三方 | ¥0.05/张 | 高质量生成 | [详情](https://help.aliyun.com/zh/model-studio/models#8b57fb1fbf2op) |
| **可灵 - 图像生成** | 第三方 | ¥0.04/张 | 快手可灵 | [详情](https://help.aliyun.com/zh/model-studio/models#e36820d56d3km) |

### 图像编辑模型

| 模型 | 功能 | 价格 | 适用场景 | 文档 |
|------|------|------|----------|------|
| **千问图像编辑** | 风格迁移/文字修改/物体编辑 | ¥0.06/张 | 复杂图文编辑 | [详情](https://help.aliyun.com/zh/model-studio/models#bfe15d8aa2lxh) |
| **万相图像编辑 2.6** | 多图融合/风格迁移/修复 | ¥0.04/张 | 通用编辑 | [详情](https://help.aliyun.com/zh/model-studio/models#157125edeb9tx) |
| **万相涂鸦作画** | 涂鸦→成品图 | ¥0.03/张 | 创意绘画 | [详情](https://help.aliyun.com/zh/model-studio/models#5a4a19ad53er2) |
| **万相局部重绘** | 指定区域重绘 | ¥0.04/张 | 局部修改 | [详情](https://help.aliyun.com/zh/model-studio/models#d1cc07f214l3u) |
| **人像风格重绘** | 人像风格转换 | ¥0.05/张 | 人像美化 | [详情](https://help.aliyun.com/zh/model-studio/models#c831fed18dhqv) |
| **图像背景生成** | 自动抠图 + 背景 | ¥0.04/张 | 电商图 | [详情](https://help.aliyun.com/zh/model-studio/models#60547f06c6qrm) |
| **图像画面扩展** | Outpainting | ¥0.04/张 | 扩展画幅 | [详情](https://help.aliyun.com/zh/model-studio/models#8e9b6350c62zt) |
| **虚拟模特** | AI 模特生成 | ¥0.08/张 | 服装展示 | [详情](https://help.aliyun.com/zh/model-studio/models#c5467902ebwjo) |
| **AI 试衣** | 虚拟试衣 | ¥0.10/张 | 电商试衣 | [详情](https://help.aliyun.com/zh/model-studio/models#b11d85fe06ogg) |
| **人物写真生成** | FaceChain | ¥0.06/张 | 个人写真 | [详情](https://help.aliyun.com/zh/model-studio/models#4eba270341qlv) |

### 专项图像模型

| 模型 | 功能 | 价格 | 文档 |
|------|------|------|------|
| **千问图像翻译** | 图像内文字翻译 | ¥0.08/张 | [详情](https://help.aliyun.com/zh/model-studio/qwen-mt-image-api) |
| **创意海报生成** | 海报设计 | ¥0.10/张 | [详情](https://help.aliyun.com/zh/model-studio/models#8a3d8eb0e8afq) |
| **创意文字生成 -WordArt** | 艺术字生成 | ¥0.03/张 | [详情](https://help.aliyun.com/zh/model-studio/models#e9cc0a9c44sdv) |

---

## 🎬 视频生成与编辑

### 文生视频

| 模型 | 时长 | 价格 | 特点 | 文档 |
|------|------|------|------|------|
| **万相文生视频** | 5-10 秒 | ¥0.5/秒 | 风格丰富、画质细腻 | [详情](https://help.aliyun.com/zh/model-studio/models#7a13292788yvp) |
| **爱诗 - 文生视频** | 5-15 秒 | ¥0.8/秒 | 高质量、电影感 | [详情](https://help.aliyun.com/zh/model-studio/models#0f70069440fuf) |
| **Vidu-文生视频** | 5-10 秒 | ¥0.7/秒 | 快速生成 | [详情](https://help.aliyun.com/zh/model-studio/models#601c240fcd9nw) |
| **可灵 - 视频生成** | 5-10 秒 | ¥0.9/秒 | 快手可灵 | [详情](https://help.aliyun.com/zh/model-studio/models#93251aa4ebi3q) |

### 图生视频

| 模型 | 类型 | 价格 | 功能 | 文档 |
|------|------|------|------|------|
| **首帧生视频** | 图→视频 | ¥0.6/秒 | 以输入图为视频首帧 | [详情](https://help.aliyun.com/zh/model-studio/models#af6bc5a9c3cp9) |
| **首尾帧生视频** | 图→视频 | ¥0.8/秒 | 提供首尾帧生成过渡视频 | [详情](https://help.aliyun.com/zh/model-studio/models#90cb98a2b9s2q) |
| **多图生视频** | 多图→视频 | ¥0.7/秒 | 参考多张图生成视频 | [详情](https://help.aliyun.com/zh/model-studio/models#f7de663db89xi) |
| **爱诗 - 图生视频 (首帧)** | 图→视频 | ¥0.8/秒 | 高质量图生视频 | [详情](https://help.aliyun.com/zh/model-studio/models#62b5c1d4d6ijo) |
| **爱诗 - 图生视频 (首尾帧)** | 图→视频 | ¥1.0/秒 | 首尾帧过渡 | [详情](https://help.aliyun.com/zh/model-studio/models#4e4ebc10f7cvw) |
| **Vidu-图生视频 (首帧)** | 图→视频 | ¥0.7/秒 | Vidu 平台 | [详情](https://help.aliyun.com/zh/model-studio/models#e9c949c200dw7) |
| **Vidu-图生视频 (首尾帧)** | 图→视频 | ¥0.9/秒 | Vidu 平台 | [详情](https://help.aliyun.com/zh/model-studio/models#ba9aa2e28dyq0) |

### 数字人/人像视频

| 模型 | 输入 | 价格 | 功能 | 文档 |
|------|------|------|------|------|
| **万相 - 数字人** | 图 + 音频 | ¥1.0/秒 | 生成对口型视频，动作自然 | [详情](https://help.aliyun.com/zh/model-studio/models#3bff5da885yx3) |
| **悦动人像 EMO** | 图 + 音频 | ¥1.2/秒 | 口型表情强，适合特写 | [详情](https://help.aliyun.com/zh/model-studio/models#c6384886fd3s8) |
| **灵动人像 LivePortrait** | 图 + 音频 | ¥0.8/秒 | 语音播报场景 | [详情](https://help.aliyun.com/zh/model-studio/models#45109ade609nr) |
| **舞动人像 AnimateAnyone** | 图 + 动作视频 | ¥1.5/秒 | 生成舞蹈视频 | [详情](https://help.aliyun.com/zh/model-studio/models#a54957baf9exo) |
| **表情包 Emoji** | 人脸图 + 模板 | ¥0.3/张 | 生成人脸表情包 | [详情](https://help.aliyun.com/zh/model-studio/models#f62472e1b6m3b) |

### 视频编辑

| 模型 | 功能 | 价格 | 文档 |
|------|------|------|------|
| **通用视频编辑** | 视频风格/内容修改 | ¥0.8/秒 | [详情](https://help.aliyun.com/zh/model-studio/models#f7de663db89xi) |
| **声动人像 VideoRetalk** | 视频口型替换 | ¥1.0/秒 | [详情](https://help.aliyun.com/zh/model-studio/models#3714ddc2e6a0p) |
| **视频风格重绘** | 视频风格转换 (日漫/美漫) | ¥0.9/秒 | [详情](https://help.aliyun.com/zh/model-studio/models#21cd0ccad2ota) |
| **参考生视频** | 参考视频/图生成表演 | ¥1.0/秒 | [详情](https://help.aliyun.com/zh/model-studio/models#62b53b525bud3) |
| **爱诗 - 参考生视频** | 参考视频生成 | ¥1.2/秒 | [详情](https://help.aliyun.com/zh/model-studio/models#0080eb1384z27) |
| **Vidu-参考生视频** | 参考视频生成 | ¥1.0/秒 | [详情](https://help.aliyun.com/zh/model-studio/models#9e43ea149dw8k) |

---

## 🎤 语音处理

### 语音识别 (ASR)

| 模型 | 语言 | 价格 | 延迟 | 文档 |
|------|------|------|------|------|
| **千问实时语音识别** | 中/英/日/韩 | ¥0.006/分钟 | 实时 | [详情](https://help.aliyun.com/zh/model-studio/models#04625778f9jd5) |
| **千问录音文件识别** | 中/英 | ¥0.004/分钟 | 离线 | [详情](https://help.aliyun.com/zh/model-studio/models#8017a37ad5a66) |
| **Fun-ASR 语音识别** | 多语言 | ¥0.005/分钟 | 低 | [详情](https://help.aliyun.com/zh/model-studio/models#140159cc9b5iz) |
| **Paraformer 语音识别** | 中文 | ¥0.004/分钟 | 低 | [详情](https://help.aliyun.com/zh/model-studio/models#c018769cd7y88) |
| **SenseVoice 语音识别** | 多语言 + 情感 | ¥0.008/分钟 | 低 | [详情](https://help.aliyun.com/zh/model-studio/models#511fe328d19af) |
| **Gummy 语音识别/翻译** | 多语言 | ¥0.01/分钟 | 低 | 支持翻译 [详情](https://help.aliyun.com/zh/model-studio/models#9e21336740rk2) |

### 语音合成 (TTS)

| 模型 | 音色 | 价格 | 特点 | 文档 |
|------|------|------|------|------|
| **千问实时语音合成** | 多音色 | ¥0.012/分钟 | 实时流式 | [详情](https://help.aliyun.com/zh/model-studio/models#05782f7968r7g) |
| **千问语音合成** | 多音色 | ¥0.01/分钟 | 高质量 | [详情](https://help.aliyun.com/zh/model-studio/models#e62b64f642k63) |
| **CosyVoice 语音合成** | 多音色 | ¥0.008/分钟 | 自然流畅 | [详情](https://help.aliyun.com/zh/model-studio/models#7a960cc042zwt) |
| **Sambert 语音合成** | 多音色 | ¥0.006/分钟 | 性价比高 | [详情](https://help.aliyun.com/zh/model-studio/models#95be68362c11b) |

---

## 🔮 全模态模型

### Qwen-Omni 系列

| 模型 | 输入模态 | 输出模态 | 实时 | 价格 | 文档 |
|------|---------|---------|------|------|------|
| **Qwen3.5-Omni-Plus** | 视频 + 音频 + 图片 + 文本 | 文本 + 音频 | ❌ | ¥3/千次 | [详情](https://help.aliyun.com/zh/model-studio/qwen-omni) |
| **Qwen3.5-Omni-Plus-Realtime** | **流式音频** + 文本 | **流式音频** + 文本 | ✅ | ¥4/千次 | [详情](https://help.aliyun.com/zh/model-studio/realtime) |
| **Qwen3.5-Omni-Flash** | 视频 + 音频 + 图片 + 文本 | 文本 + 音频 | ❌ | ¥2/千次 | [详情](https://help.aliyun.com/zh/model-studio/qwen-omni) |
| **Qwen3.5-Omni-Flash-Realtime** | **流式音频** + 文本 | **流式音频** + 文本 | ✅ | ¥3/千次 | [详情](https://help.aliyun.com/zh/model-studio/realtime) |
| **Qwen-Omni** | 视频 + 音频 + 图片 + 文本 | 文本 + 音频 | ❌ | ¥2/千次 | [详情](https://help.aliyun.com/zh/model-studio/qwen-omni) |
| **Qwen-Omni-Realtime** | **流式音频** + 文本 | **流式音频** + 文本 | ✅ | ¥3/千次 | [详情](https://help.aliyun.com/zh/model-studio/realtime) |
| **Qwen-Audio** | 音频 + 文本 | 文本 | ❌ | ¥0.5/千 token | [详情](https://help.aliyun.com/zh/model-studio/qwen-omni) |

**Qwen3.5-Omni 系列新特性** (2026-03-30 新增):
- ✅ 支持 113 种语言识别
- ✅ 支持 36 种语言音频生成
- ✅ 可处理 3 小时音频 / 1 小时视频
- ✅ 支持联网搜索
- ✅ 支持音量/语速/情绪控制
- ✅ 实时版支持语音打断

### Qwen-VL 系列 (视觉理解)

| 模型 | 输入 | 输出 | Think | 价格 | 文档 |
|------|------|------|-------|------|------|
| **Qwen-VL-Max** | 图 + 文 | 文本 | ❌ | ¥1.5 / ¥6 | [详情](https://help.aliyun.com/zh/model-studio/models#3f1f1c8913fvo) |
| **Qwen-VL-Plus** | 图 + 文 | 文本 | ❌ | ¥0.5 / ¥2 | [详情](https://help.aliyun.com/zh/model-studio/models#3f1f1c8913fvo) |
| **QVQ** | 图 + 文 | 文本 | ✅ | ¥2 / ¥8 | [详情](https://help.aliyun.com/zh/model-studio/models#40e07d9a04nx8) |
| **Qwen3.5-Plus** | 图/视频 + 文 | 文本 | ✅ | ¥0.8 / ¥4.8 | [详情](https://help.aliyun.com/zh/model-studio/models#5ef284d4ed42p) |

---

## 🔢 Embedding (向量模型)

| 模型 | 维度 | 输入 | 价格 | 文档 |
|------|------|------|------|------|
| **text-embedding-v3** | 1024 | 文本 | ¥0.0005/千 token | [详情](https://help.aliyun.com/zh/model-studio/models#3383780daf8hw) |
| **multimodal-embedding-v1** | 1024 | 文本 + 图像 + 语音 | ¥0.001/千 token | [详情](https://help.aliyun.com/zh/model-studio/models#9bda215aa7mko) |

### 开源系列
| 模型 | 上下文 | Think | 价格 | 备注 |
|------|--------|-------|------|------|
| Qwen3.5-397B | 256K | ✅ | - | 本地部署 |
| Qwen3.5-122B | 256K | ✅ | - | 本地部署 |
| Qwen3.5-27B | 256K | ✅ | - | 本地部署 |
| Qwen3.5-35B-A3B | 256K | ✅ | - | 本地部署 |

### 代码专用
| 模型 | 上下文 | 价格 | 适用场景 |
|------|--------|------|----------|
| Qwen-Coder-Next | 256K | ¥1 / ¥5 | 代码生成 |
| Qwen-Coder-Plus | 256K | ¥1 / ¥5 | 代码理解 |

---

## 🌐 第三方模型

### 智谱 AI - GLM 系列

| 模型 | 上下文 | Think | 搜索 | Function Call | 价格 | 文档 |
|------|--------|-------|------|--------------|------|------|
| **GLM-5** | 202K | ✅ | ✅ | ✅ (流式) | ¥1 / ¥4 | [详情](https://help.aliyun.com/zh/model-studio/glm) |
| **GLM-4.7** | 170K | ✅ | ✅ | ✅ | ¥0.5 / ¥2 | [详情](https://help.aliyun.com/zh/model-studio/glm) |
| **GLM-4.6** | 131K | ✅ | ✅ | ✅ | ¥0.5 / ¥2 | [详情](https://help.aliyun.com/zh/model-studio/glm) |
| **GLM-4.5** | 131K | ✅ | ✅ | ✅ | ¥0.5 / ¥2 | [详情](https://help.aliyun.com/zh/model-studio/glm) |
| **GLM-4.5-Air** | 131K | ❌ | ✅ | ✅ | ¥0.2 / ¥0.8 | [详情](https://help.aliyun.com/zh/model-studio/glm) |

### 月之暗面 - Kimi 系列

| 模型 | 上下文 | Think | 搜索 | 多模态 | 价格 | 文档 |
|------|--------|-------|------|--------|------|------|
| **Kimi-K2.5** | 256K | ✅ | ✅ | ✅ 图/视频 | ¥4 / ¥21 | [详情](https://help.aliyun.com/zh/model-studio/kimi-api) |
| **Kimi-K2-Thinking** | 256K | ✅ (仅) | ✅ | ❌ | ¥4 / ¥16 | [详情](https://help.aliyun.com/zh/model-studio/kimi-api) |
| **Kimi-K2-Instruct** | 128K | ❌ | ✅ | ❌ | ¥4 / ¥16 | [详情](https://help.aliyun.com/zh/model-studio/kimi-api) |

### 深度求索 - DeepSeek 系列

| 模型 | 参数 | 上下文 | Think | 搜索 | 价格 | 文档 |
|------|------|--------|-------|------|------|------|
| **DeepSeek-V3.2** | 685B | 128K | ✅ | ✅ | ¥0.5 / ¥2 | [详情](https://help.aliyun.com/zh/model-studio/deepseek-api) |
| **DeepSeek-V3.2-Exp** | 685B | 128K | ✅ | ⚠️ | ¥0.5 / ¥2 | [详情](https://help.aliyun.com/zh/model-studio/deepseek-api) |
| **DeepSeek-V3.1** | 685B | 128K | ✅ | ⚠️ | ¥0.5 / ¥2 | [详情](https://help.aliyun.com/zh/model-studio/deepseek-api) |
| **DeepSeek-V3** | 671B | 128K | ❌ | ✅ | ¥0.5 / ¥2 | [详情](https://help.aliyun.com/zh/model-studio/deepseek-api) |
| **DeepSeek-R1** | 685B | 128K | ✅ (仅) | ✅ | ¥1 / ¥4 | [详情](https://help.aliyun.com/zh/model-studio/deepseek-api) |

**蒸馏模型 (本地部署)**:
- R1-Distill-Qwen-1.5B/7B/14B/32B
- R1-Distill-Llama-8B/70B

### MiniMax - M 系列

| 模型 | 上下文 | Think | 搜索 | 价格 | 文档 |
|------|--------|-------|------|------|------|
| **MiniMax-M2.5** | 196K | ✅ | ✅ | ¥0.5 / ¥2 | [详情](https://help.aliyun.com/zh/model-studio/minimax-api) |
| **MiniMax-M2.1** | 204K | ✅ (仅) | ✅ | ¥0.5 / ¥2 | [详情](https://help.aliyun.com/zh/model-studio/minimax-api) |

---

## 💼 Coding Plan

**套餐**: Pro 高级套餐  
**价格**: ¥200/月  
**额度**: 6K/5 小时，45K/周，90K/月  
**专属 API Key**: `sk-sp-xxxxx`  
**专属 Base URL**: `https://coding.dashscope.aliyuncs.com/v1`

**支持模型**:
- ✅ Qwen3.5-Plus (推荐)
- ✅ Kimi-K2.5 (推荐)
- ✅ GLM-5 (推荐)
- ✅ MiniMax-M2.5 (推荐)
- ✅ Qwen3-Max
- ✅ Qwen-Coder 系列
- ✅ GLM-4.7

**文档**: [Coding Plan 详情](https://help.aliyun.com/zh/model-studio/coding-plan)

---

## 📊 能力矩阵

### Think 模式支持
| 支持 | 模型 |
|------|------|
| ✅ | Qwen3-Max, Qwen3.5-Plus, GLM-5/4.7/4.6/4.5, Kimi-K2.5/K2-Thinking, DeepSeek-V3.2/V3.1/R1, MiniMax-M2.5/M2.1 |
| ❌ | Qwen3.5-Flash, Kimi-K2-Instruct, DeepSeek-V3, GLM-4.5-Air |

### 联网搜索支持
| 支持 | 模型 |
|------|------|
| ✅ | Qwen3-Max, Qwen3.5-Plus/Flash, GLM 全系列, Kimi 全系列, DeepSeek 全系列, MiniMax-M2.5/M2.1 |

### Function Calling 支持
| 支持 | 模型 |
|------|------|
| ✅ | Qwen3-Max, Qwen3.5-Plus, GLM 全系列 (流式), Kimi 全系列, DeepSeek 全系列, MiniMax-M2.5/M2.1 |

### 多模态支持
| 支持 | 模型 |
|------|------|
| ✅ | Qwen3.5-Plus (图/视频), Kimi-K2.5 (图/视频), Qwen-VL 系列, Qwen-Omni 系列 |

---

## 🔄 更新方法

详见：[[阿里云百炼信息收集和爬取方法]]

---

**文档维护**: 本内容由 OpenClaw 自动维护，每周自动更新一次。
**最后同步**: 2026-03-31 08:30 GMT+8
