# Creative Studio Research - Update Log

> 记录每次研究发现的更新

---

## 2026-04-04 — 初始化

### 新增 Prompt 库

| 文件 | 数量 | 状态 |
|------|------|------|
| prompts/portrait.md | 8 个 prompt | ✅ 已创建 |
| prompts/landscape.md | 6 个 prompt | ✅ 已创建 |
| prompts/video-character.md | 5 个 prompt | ✅ 已创建 |

### 新增场景库

| 文件 | 数量 | 状态 |
|------|------|------|
| scenes/product-showcase.md | 3 个方案 | ✅ 已创建 |

### 新增研究资源

| 资源 | 类型 | 状态 |
|------|------|------|
| Apatero Prompt 工程指南 | 教程 | ✅ 已收录 |
| awesome-ai-video-prompts | GitHub 精选 | ✅ 已收录 |
| Runway Prompt 指南 | 官方教程 | ✅ 已收录 |
| 阿里云官方 API 文档 | 官方文档 | ✅ 已收录 |

### 核心发现

1. **Prompt 公式通用性**：`[媒介/风格] + [主体+细节] + [环境] + [光影] + [构图] + [技术参数]` 适用于大多数 AI 生图模型
2. **视频 Prompt 关键区别**：必须有明确动作描述和镜头运动，静态描述效果差
3. **多角色引用差异**：wan2.7 用"视频1/图1"，wan2.6 用"character1"
4. **负面提示词重要性**：对 Stable Diffusion 类模型效果显著，对 Wan 系列也有帮助
5. **词序权重**：前面的词影响力最大，重要信息放前面

### 待研究

- [ ] 阿里云万相官方 Prompt 指南
- [ ] Midjourney v6/v7 最新 prompt 技巧
- [ ] Flux 模型 prompt 特点
- [ ] Kling 视频生成 prompt 最佳实践
- [ ] Sora / Veo prompt 技巧（如可用）
- [ ] 声音设计 prompt 模板

---

> 下次更新计划：2026-04-11（一周后）
