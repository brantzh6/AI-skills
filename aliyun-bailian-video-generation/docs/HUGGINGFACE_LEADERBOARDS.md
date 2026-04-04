# HuggingFace 权威视频生成榜单汇总

**多个权威 Leaderboard 完整整理**  
**更新时间**: 2026-04-02

---

## 🏆 HuggingFace 视频生成榜单列表

### 1. VBench Leaderboard (最权威学术评测)

**来源**: Vchitect (CVPR 2024 Highlight)  
**HuggingFace**: https://huggingface.co/spaces/Vchitect/VBench_Leaderboard  
**GitHub**: https://github.com/Vchitect/VBench  
**评测方法**: 综合基准测试套件  
**可靠性**: ⭐⭐⭐⭐⭐

**评测维度** (分层评估体系):
```
视频生成质量分解为多个维度:
├─ 视频质量
│  ├─ 主体一致性
│  ├─ 背景一致性
│  ├─ 运动流畅度
│  └─ 视觉质量
├─ 文本对齐
│  ├─ 文本内容准确性
│  └─ 时空绑定准确性
└─ 其他维度
   ├─ 物理准确性
   ├─ 多视角一致性
   └─ 美学质量
```

**VBench-2.0 最新结果** (2025-2026):

| 模型 | 综合得分 | 视频质量 | 文本对齐 | 排名 |
|------|---------|---------|---------|------|
| **Kling 1.6** | TBD | TBD | TBD | **1** |
| **Sora-480p** | TBD | TBD | TBD | **2** |
| **HunyuanVideo** | TBD | TBD | TBD | **3** |
| **CogVideoX-1.5** | TBD | TBD | TBD | **4** |

*注：具体分数需访问 HuggingFace Space 查看实时数据*

**特点**:
- ✅ CVPR 2024 亮点论文
- ✅ 分层评估体系
- ✅ 细粒度客观评估
- ✅ 学术引用最多

---

### 2. Video-Bench Leaderboard (人类偏好对齐)

**来源**: LanguageBind (上海交大等 12 机构)  
**HuggingFace**: https://huggingface.co/spaces/LanguageBind/Video-Bench  
**GitHub**: https://github.com/Video-Bench/Video-Bench  
**评测方法**: 多模态 LLM + 人类偏好  
**可靠性**: ⭐⭐⭐⭐⭐

**评测维度**:
1. **Video Quality** (视频质量)
2. **Video-Condition Alignment** (视频 - 条件对齐)
3. **Overall Rank** (综合排名)

**最新排名**:

| 排名 | 模型 | 视频质量 | 条件对齐 | 平均排名 |
|------|------|---------|---------|---------|
| 1 | **Gen3** (Runway) | 4.66 | 4.38 | **1** |
| 2 | **CogVideoX** (智谱) | 3.84 | 4.62 | **2** |
| 3 | **VideoCrafter2** (腾讯) | 4.08 | 4.18 | **3** |
| 4 | **Kling** (快手) | 4.26 | 4.07 | **4** |
| 5 | **Show-1** (Showlab) | 3.30 | 4.21 | **5** |
| 6 | **LaVie** (清华) | 3.00 | 3.71 | **6** |
| 7 | **Pika-Beta** | 3.76 | 2.60 | **7** |

**人类偏好对齐度** (Spearman 相关系数):
- HU-HU (人类 - 人类): **0.63** (视频质量), **0.47** (条件对齐)
- HU-GPT (人类-GPT): 0.51, 0.47
- HU-HA (人类-HA): 0.61, 0.50

**特点**:
- ✅ 12 所顶尖大学联合发布
- ✅ 人类偏好对齐验证
- ✅ 多模态 LLM 自动评估
- ✅ 开源评测框架

---

### 3. VideoScore Leaderboard (自动评估)

**来源**: TIGER-Lab  
**HuggingFace**: https://huggingface.co/spaces/TIGER-Lab/VideoScore-Leaderboard  
**评测方法**: 自动视频评分  
**可靠性**: ⭐⭐⭐⭐

**评测维度**:
- 整体质量
- 文本对齐
- 运动质量
- 视觉质量

**特点**:
- ✅ 自动评估
- ✅ 快速出分
- ✅ 持续更新

---

### 4. ArtificialAnalysis Video Arena (用户偏好)

**来源**: ArtificialAnalysis  
**HuggingFace**: https://huggingface.co/spaces/ArtificialAnalysis/Video-Generation-Arena-Leaderboard  
**评测方法**: 众包用户盲测投票  
**可靠性**: ⭐⭐⭐⭐⭐

**评测方法**:
```
1. 用户观看两个匿名视频
2. 投票选择更好的一个
3. 基于 Elo 系统计算排名
4. 持续更新
```

**特点**:
- ✅ 类似 LMSYS Chatbot Arena
- ✅ 真实用户盲测
- ✅ Elo 评分系统
- ✅ 持续更新

---

### 5. VBVR-Bench Leaderboard (视频推理)

**来源**: Video-Reason  
**HuggingFace**: https://huggingface.co/spaces/Video-Reason/VBVR-Bench-Leaderboard  
**评测方法**: 视频推理能力评估  
**可靠性**: ⭐⭐⭐⭐

**评测重点**:
- 视频推理能力
- 因果关系理解
- 时序逻辑

**特点**:
- ✅ 专注于推理能力
- ✅ 多维度指标
- ✅ 彩色热力图展示

---

### 6. OpenVLM Video Leaderboard (视频理解)

**来源**: OpenCompass  
**HuggingFace**: https://huggingface.co/spaces/opencompass/openvlm_video_leaderboard  
**评测方法**: 视频理解基准  
**可靠性**: ⭐⭐⭐⭐

**覆盖范围**:
- 49 个不同 VLM
- 5 个不同视频理解基准
- 包括 GPT-4o, Gemini-1.5, LLaVA-OneVision 等

**特点**:
- ✅ 视频理解而非生成
- ✅ 多模型对比
- ✅ 多基准测试

---

### 7. VideoGen-RewardBench (奖励模型)

**来源**: KwaiVGI (快手)  
**HuggingFace**: https://huggingface.co/spaces/KwaiVGI/VideoGen-RewardBench  
**评测方法**: 奖励模型基准  
**可靠性**: ⭐⭐⭐⭐

**特点**:
- ✅ 奖励模型评估
- ✅ 视频对比
- ✅ 可筛选搜索

---

### 8. MVBench Leaderboard (多模态理解)

**来源**: OpenGVLab  
**HuggingFace**: https://huggingface.co/spaces/OpenGVLab/MVBench_Leaderboard  
**评测方法**: 多模态理解基准  
**可靠性**: ⭐⭐⭐⭐

**特点**:
- ✅ 多模态理解
- ✅ 视频 + 图像
- ✅ JSON 提交

---

### 9. MMEB Leaderboard (多模态嵌入)

**来源**: TIGER-Lab  
**HuggingFace**: https://huggingface.co/spaces/TIGER-Lab/MMEB-Leaderboard  
**评测方法**: 多模态嵌入基准  
**可靠性**: ⭐⭐⭐⭐

**评测范围**:
- 图像
- 视频
- 视觉文档

---

## 📊 各榜单权威性对比

| 榜单 | 来源 | 评测方法 | 权威性 | 适用场景 |
|------|------|---------|--------|---------|
| **VBench** | Vchitect (CVPR 2024) | 综合基准 | ⭐⭐⭐⭐⭐ | 技术准确性 |
| **Video-Bench** | 12 所大学 | LLM+ 人类偏好 | ⭐⭐⭐⭐⭐ | 人类对齐度 |
| **Video Arena** | ArtificialAnalysis | 用户盲测 | ⭐⭐⭐⭐⭐ | 主观体验 |
| **VideoScore** | TIGER-Lab | 自动评估 | ⭐⭐⭐⭐ | 快速评估 |
| **VBVR-Bench** | Video-Reason | 推理能力 | ⭐⭐⭐⭐ | 推理能力 |
| **OpenVLM** | OpenCompass | 视频理解 | ⭐⭐⭐⭐ | 理解能力 |
| **VideoGen** | KwaiVGI | 奖励模型 | ⭐⭐⭐⭐ | 奖励训练 |

---

## 🎯 如何使用这些榜单

### 对于技术选型

```
步骤 1: 查看 VBench 排名
- 关注技术准确性
- 关注各维度细粒度分数

步骤 2: 查看 Video-Bench 排名
- 关注人类偏好对齐度
- 关注视频 - 条件对齐

步骤 3: 查看 Video Arena 排名
- 关注用户主观体验
- 关注实际使用反馈

步骤 4: 综合决策
- 技术准确性 (VBench)
- 人类对齐度 (Video-Bench)
- 用户体验 (Arena)
```

### 对于研究参考

```
推荐关注:
1. VBench 详细评测报告
2. Video-Bench 人类对齐分析
3. 各模型技术论文
4. 社区实际使用反馈

数据来源:
- HuggingFace Spaces (实时数据)
- GitHub (代码/数据)
- arXiv (研究论文)
```

---

## 🔗 快速访问链接

### 综合评测

| 榜单 | 链接 |
|------|------|
| VBench | https://huggingface.co/spaces/Vchitect/VBench_Leaderboard |
| Video-Bench | https://huggingface.co/spaces/LanguageBind/Video-Bench |
| Video Arena | https://huggingface.co/spaces/ArtificialAnalysis/Video-Generation-Arena-Leaderboard |

### 自动评估

| 榜单 | 链接 |
|------|------|
| VideoScore | https://huggingface.co/spaces/TIGER-Lab/VideoScore-Leaderboard |
| VBVR-Bench | https://huggingface.co/spaces/Video-Reason/VBVR-Bench-Leaderboard |

### 理解能力

| 榜单 | 链接 |
|------|------|
| OpenVLM | https://huggingface.co/spaces/opencompass/openvlm_video_leaderboard |
| MVBench | https://huggingface.co/spaces/OpenGVLab/MVBench_Leaderboard |

### 其他

| 榜单 | 链接 |
|------|------|
| VideoGen-RewardBench | https://huggingface.co/spaces/KwaiVGI/VideoGen-RewardBench |
| MMEB | https://huggingface.co/spaces/TIGER-Lab/MMEB-Leaderboard |

---

## ⚠️ 榜单局限性

### VBench 局限

```
❌ 商业模型可能无法获取
❌ 评测集可能有限
❌ 新模型更新可能滞后
```

### Video-Bench 局限

```
❌ LLM 评估可能有偏差
❌ 人类样本量有限
❌ 文化差异可能影响
```

### Video Arena 局限

```
❌ 用户群体可能有偏差
❌ 投票者专业度不同
❌ 可能受流行度影响
```

---

## 📝 总结

### 最权威榜单推荐

**技术准确性**: VBench (CVPR 2024)  
**人类对齐度**: Video-Bench (12 所大学)  
**用户体验**: Video Arena (用户盲测)

### 推荐查询顺序

```
1. VBench → 技术准确性
2. Video-Bench → 人类对齐度
3. Video Arena → 用户体验
4. 其他榜单 → 特定维度
```

### 关键建议

```
✅ 结合多种榜单
✅ 关注评测方法论
✅ 考虑具体使用场景
✅ 实际测试验证
```

---

**最后更新**: 2026-04-02  
**维护人**: 胖福  
**数据来源**: HuggingFace Spaces
