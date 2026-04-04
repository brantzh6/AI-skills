# 阿里云百炼模型更新记录 - 2026-04-01

**更新时间**: 2026-04-01  
**更新人**: 胖福  
**更新类型**: 新增模型

---

## 🆕 新增模型

### 万相 2.7 图像生成与编辑

**发布日期**: 2026-04-01  
**模型类型**: 图像生成与编辑  
**模型规格**: 
- `wan2.7-image-pro` (Pro 版)
- `wan2.7-image` (标准版)

**能力支持**:
- ✅ 文生图
- ✅ 文生组图
- ✅ 图生组图
- ✅ 图像编辑
- ✅ 多图参考生成
- ✅ 交互式编辑

**特点**:
- 文字渲染能力更强
- 主体一致性更优
- 复杂指令遵循表现更好
- Pro 版支持 4K 输出
- 加速版兼顾效果与响应速度

**相关文档**:
- API 参考：https://help.aliyun.com/zh/model-studio/wan-image-generation-api-reference

---

### Qwen3.5-Omni 系列全模态模型

**发布日期**: 2026-03-30  
**模型类型**: 全模态

**新增模型**:
| 模型 | 类型 | 特点 |
|------|------|------|
| qwen3.5-omni-plus | 非实时 | 长视频分析、会议纪要、字幕输出 |
| qwen3.5-omni-plus-2026-03-15 | 非实时快照版 | - |
| qwen3.5-omni-flash | 非实时加速版 | 速度快 |
| qwen3.5-omni-flash-2026-03-15 | 非实时加速快照版 | - |
| qwen3.5-omni-plus-realtime | 实时 | 语音打断、联网搜索 |
| qwen3.5-omni-plus-realtime-2026-03-15 | 实时快照版 | - |
| qwen3.5-omni-flash-realtime | 实时加速版 | - |
| qwen3.5-omni-flash-realtime-2026-03-15 | 实时加速快照版 | - |

**能力升级**:
- ✅ 支持 113 种语言识别
- ✅ 支持 36 种语言音频生成
- ✅ 可处理 3 小时音频
- ✅ 可处理 1 小时视频
- ✅ 支持联网搜索
- ✅ 支持音量/语速/情绪控制
- ✅ 实时版支持语音打断

**相关文档**:
- 非实时：https://help.aliyun.com/zh/model-studio/qwen-omni
- 实时：https://help.aliyun.com/zh/model-studio/realtime

---

## 📊 需要更新的主文档

### 1. 图像生成部分

在 `notion/aliyun-bailian-capabilities.md` 的"文生图模型"表格中添加：

```markdown
| **万相 2.7-Image** | 文生图/编辑 | ¥0.06/张 | 4K 输出、文字渲染强 | [详情]() |
| **万相 2.7-Image-Pro** | 文生图/编辑 | ¥0.08/张 | 4K 输出、专业版 | [详情]() |
```

### 2. 全模态模型部分

在"Qwen-Omni 系列"表格中添加：

```markdown
| **Qwen3.5-Omni-Plus** | 音视频 + 文 | 文本 + 音频 | ❌ | ¥3/千次 | 2026-03-30 新增 |
| **Qwen3.5-Omni-Flash** | 音视频 + 文 | 文本 + 音频 | ❌ | ¥2/千次 | 2026-03-30 新增 |
| **Qwen3.5-Omni-Plus-Realtime** | 流式音视频 | 流式音频 + 文本 | ✅ | ¥4/千次 | 2026-03-30 新增 |
| **Qwen3.5-Omni-Flash-Realtime** | 流式音视频 | 流式音频 + 文本 | ✅ | ¥3/千次 | 2026-03-30 新增 |
```

### 3. 更新日志部分

添加更新记录：

```markdown
| 版本 | 日期 | 更新内容 | 操作人 |
|------|------|---------|--------|
| v26.4.1 | 2026-04-01 | 新增万相 2.7 图像生成、Qwen3.5-Omni 系列 | 胖福 |
| v26.3.1 | 2026-03-31 | 初始版本，完成全量信息收集 | 胖福 |
```

---

## 🔗 相关文档链接

### 万相 2.7
- API 参考：https://help.aliyun.com/zh/model-studio/wan-image-generation-api-reference
- 使用指南：待补充

### Qwen3.5-Omni
- 非实时文档：https://help.aliyun.com/zh/model-studio/qwen-omni
- 实时文档：https://help.aliyun.com/zh/model-studio/realtime
- 模型更新：https://help.aliyun.com/zh/model-studio/newly-released-models

---

## ✅ 待办事项

- [ ] 更新主文档 `notion/aliyun-bailian-capabilities.md`
- [ ] 添加万相 2.7 价格信息
- [ ] 添加 Qwen3.5-Omni 系列价格信息
- [ ] 更新文档索引 `ALIYUN_BAILIAN_DOCUMENT_INDEX.md`
- [ ] 记录到更新日志

---

**信息来源**: 
- 模型更新页面：https://help.aliyun.com/zh/model-studio/newly-released-models
- 验证时间：2026-04-01 16:00 GMT+8
