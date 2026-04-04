# 多角色多造型视频生成指南

**解决复杂场景、多人物、多造型的视频生成方案**

---

## 🎭 核心挑战

| 挑战 | 原因 | 解决方案 |
|------|------|---------|
| **多角色一致性** | 每个角色需独立保持特征 | 角色分离管理 + 独立参考视频 |
| **造型变化** | 不同场景妆容服装不同 | 造型模板 + 场景化提示词 |
| **多人同框** | 角色间相互影响 | 分步生成 + 后期合成 |
| **角色互动** | 动作表情需协调 | 参考视频 + 详细互动描述 |

---

## 📋 方案 1：角色分离管理法（推荐）

### 核心思路

```
为每个角色创建独立的：
1. 角色设定表 (Character Sheet)
2. 参考视频 (Reference Video)
3. 造型模板 (Style Template)

生成时根据场景调用对应的角色配置
```

### 步骤 1：创建角色档案

```python
# 角色管理系统
class CharacterManager:
    def __init__(self):
        self.characters = {}
    
    def add_character(self, name, character_data):
        """
        添加角色档案
        
        character_data = {
            "base_description": "基础描述（不变）",
            "styles": {
                "casual": "日常造型",
                "formal": "正式造型",
                "action": "动作造型"
            },
            "reference_video": "参考视频 URL",
            "seed": 固定种子
        }
        """
        self.characters[name] = character_data
    
    def get_prompt(self, name, style=None, scene_context=""):
        """生成包含角色描述的完整提示词"""
        char = self.characters[name]
        
        # 基础描述
        prompt = char["base_description"]
        
        # 添加造型
        if style and style in char["styles"]:
            prompt += f"\n造型：{char['styles'][style]}"
        
        # 添加场景
        if scene_context:
            prompt += f"\n场景：{scene_context}"
        
        return prompt

# 使用示例
manager = CharacterManager()

# 添加女主角 - 小艾
manager.add_character("小艾", {
    "base_description": """
    主角：小艾
    - 20 岁亚洲女性，黑色长直发，齐刘海
    - 大眼睛，双眼皮，黑色瞳孔
    - 身材苗条，肤色白皙
    - 面部特征：高鼻梁，樱桃小嘴
    """,
    "styles": {
        "casual": """
        日常造型：
        - 白色连衣裙，蓝色腰带
        - 白色运动鞋
        - 银色项链，左手手表
        - 淡妆，粉色唇彩
        """,
        "formal": """
        正式造型：
        - 黑色职业套装，白色衬衫
        - 黑色高跟鞋
        - 珍珠耳环，精致手提包
        - 精致妆容，红色口红
        """,
        "action": """
        动作造型：
        - 运动紧身衣，黑色短裤
        - 运动鞋，护腕
        - 马尾辫
        - 无妆，自然状态
        """
    },
    "seed": 12345
})

# 添加男主角 - 阿明
manager.add_character("阿明", {
    "base_description": """
    主角：阿明
    - 25 岁亚洲男性，黑色短发
    - 浓眉，大眼睛
    - 身材健壮，肤色健康
    - 面部特征：方正脸型，坚毅表情
    """,
    "styles": {
        "casual": """
        日常造型：
        - 蓝色 T 恤，牛仔裤
        - 白色运动鞋
        - 运动手表
        """,
        "formal": """
        正式造型：
        - 深蓝色西装，白色衬衫
        - 黑色皮鞋
        - 领带夹
        """,
        "action": """
        动作造型：
        - 战术背心，工装裤
        - 作战靴
        - 手套，护目镜
        """
    },
    "seed": 67890
})
```

### 步骤 2：为每个角色生成参考视频

```python
from dashscope import VideoSynthesis

def generate_character_references(manager):
    """为所有角色生成参考视频"""
    
    for name, char in manager.characters.items():
        print(f"生成 {name} 的参考视频...")
        
        # 生成基础造型参考视频
        rsp = VideoSynthesis.async_call(
            api_key=api_key,
            model='wan2.6-t2v',
            prompt=manager.get_prompt(name, style='casual', 
                                     scene_context='角色特写镜头，360 度展示'),
            duration=15,
            seed=char['seed'],
            size="1280*720"
        )
        
        result = VideoSynthesis.wait(task=rsp, api_key=api_key)
        char['reference_video'] = result.output.video_url
        print(f"{name} 参考视频已生成：{char['reference_video']}")
        
        # 为每个造型生成额外参考视频
        char['style_references'] = {}
        for style_name in char['styles']:
            rsp = VideoSynthesis.async_call(
                api_key=api_key,
                model='wan2.6-t2v',
                prompt=manager.get_prompt(name, style=style_name,
                                         scene_context='角色造型展示，正面和侧面'),
                duration=15,
                seed=char['seed'],
                size="1280*720"
            )
            
            result = VideoSynthesis.wait(task=rsp, api_key=api_key)
            char['style_references'][style_name] = result.output.video_url
            print(f"  - {style_name} 造型参考：{char['style_references'][style_name]}")

# 执行
generate_character_references(manager)
```

### 步骤 3：场景化生成

```python
# 剧本场景定义
scenes = [
    {
        "id": 1,
        "description": "咖啡厅相遇",
        "characters": [
            {"name": "小艾", "style": "casual"},
            {"name": "阿明", "style": "casual"}
        ],
        "action": "小艾和阿明在咖啡厅见面，愉快地交谈"
    },
    {
        "id": 2,
        "description": "公司会议",
        "characters": [
            {"name": "小艾", "style": "formal"},
            {"name": "阿明", "style": "formal"}
        ],
        "action": "小艾和阿明在会议室进行商务谈判"
    },
    {
        "id": 3,
        "description": "健身房训练",
        "characters": [
            {"name": "小艾", "style": "action"},
            {"name": "阿明", "style": "action"}
        ],
        "action": "小艾和阿明一起在健身房训练"
    }
]

# 根据场景生成视频
for scene in scenes:
    print(f"生成场景 {scene['id']}: {scene['description']}")
    
    # 多角色场景：分步生成
    character_clips = []
    
    for char_info in scene['characters']:
        char_name = char_info['name']
        char_style = char_info['style']
        char_data = manager.characters[char_name]
        
        # 使用对应造型的参考视频
        reference_video = char_data['style_references'].get(
            char_style, 
            char_data['reference_video']
        )
        
        # 生成该角色的片段
        rsp = VideoSynthesis.async_call(
            api_key=api_key,
            model='wan2.6-r2v',  # 参考生视频
            prompt=f"""
            {manager.get_prompt(char_name, style=char_style)}
            
            场景：{scene['action']}
            镜头：中景，电影感
            """,
            video_url=reference_video,
            duration=15,
            seed=char_data['seed']
        )
        
        result = VideoSynthesis.wait(task=rsp, api_key=api_key)
        character_clips.append({
            "name": char_name,
            "video": result.output.video_url,
            "style": char_style
        })
    
    # 后期合成多角色场景（见下方合成方案）
    composite_scene(character_clips, f"scene_{scene['id']}.mp4")
```

---

## 🎬 方案 2：多人同框处理技术

### 技术 1：分步生成 + 后期合成

**适用场景**: 2-3 人对话、互动场景

```python
def composite_scene(character_clips, output_file):
    """
    合成多角色场景
    
    character_clips = [
        {"name": "小艾", "video": "xiaoi_clip.mp4"},
        {"name": "阿明", "video": "aming_clip.mp4"}
    ]
    """
    import subprocess
    
    # 使用 ffmpeg 合成（左右分屏示例）
    filter_complex = """
    [0:v]scale=640:720[left];
    [1:v]scale=640:720[right];
    [left][right]hstack=inputs=2[merged];
    [merged]crop=1280:720:(ow-iw)/2:(oh-ih)/2
    """
    
    input_args = []
    for clip in character_clips:
        input_args.extend(["-i", clip["video"]])
    
    cmd = [
        "ffmpeg",
        *input_args,
        "-filter_complex", filter_complex,
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "23",
        output_file
    ]
    
    subprocess.run(cmd)
    print(f"场景合成完成：{output_file}")

# 使用
composite_scene(character_clips, "scene_1_cafe.mp4")
```

### 技术 2：绿幕合成（专业方案）

```python
def generate_with_green_screen(character_clips, background_video, output_file):
    """
    绿幕合成方案
    
    1. 生成角色时指定绿幕背景
    2. 抠像后合成到真实背景
    """
    import subprocess
    
    # 1. 为每个角色视频抠像
    keyed_clips = []
    for i, clip in enumerate(character_clips):
        keyed_file = f"keyed_{i}.mp4"
        
        # 使用 chromakey 滤镜抠除绿色背景
        cmd = [
            "ffmpeg",
            "-i", clip["video"],
            "-vf", "chromakey=0x00FF00:0.1:0.2",
            "-c:v", "libx264",
            "-pix_fmt", "yuva420p",
            keyed_file
        ]
        subprocess.run(cmd)
        keyed_clips.append(keyed_file)
    
    # 2. 合成到背景
    filter_complex = ""
    for i, keyed_file in enumerate(keyed_clips):
        # 根据场景调整位置
        positions = [
            "100:100",  # 角色 1 位置
            "700:100",  # 角色 2 位置
        ]
        filter_complex += f"[{i+1}:v]scale=400:720,setsar=1[char{i}];"
        filter_complex += f"[0:v][char{i}]overlay={positions[i]}[out{i}];"
    
    cmd = [
        "ffmpeg",
        "-i", background_video,
        "-i", *keyed_clips,
        "-filter_complex", filter_complex.rstrip(";"),
        "-c:v", "libx264",
        "-preset", "medium",
        output_file
    ]
    
    subprocess.run(cmd)
```

### 技术 3：提示词控制多人位置

```python
# 多人场景提示词模板
multi_character_prompt = """
【场景描述】
咖啡厅内，两个人坐在桌子两侧

【角色位置】
- 小艾：画面左侧，面向右侧，坐在椅子上
- 阿明：画面右侧，面向左侧，坐在椅子上

【角色描述】
小艾：20 岁亚洲女性，黑色长直发，白色连衣裙，淡妆，微笑
阿明：25 岁亚洲男性，黑色短发，蓝色 T 恤，自然表情

【互动动作】
两人愉快地交谈，小艾用手比划，阿明点头回应

【镜头】
中景，包含两人上半身，轻微左右摇摄

【风格】
3D 卡通，皮克斯风格，温暖色调，电影感
"""

rsp = VideoSynthesis.async_call(
    api_key=api_key,
    model='wan2.6-t2v',
    prompt=multi_character_prompt,
    duration=15,
    seed=12345
)
```

---

## 💄 方案 3：造型变化管理

### 造型转换镜头

```python
# 在不同造型间添加转换镜头
transformation_scenes = [
    {
        "type": "makeup_transition",
        "from": "casual",
        "to": "formal",
        "prompt": """
        化妆间内，镜头聚焦在化妆台上
        化妆品、发型工具整齐摆放
        通过镜子反射暗示角色正在化妆
        时长：3 秒
        """
    },
    {
        "type": "outfit_change",
        "character": "小艾",
        "from": "白色连衣裙",
        "to": "黑色职业套装",
        "prompt": """
        更衣室场景，衣架上挂着不同服装
        镜头扫过衣架，暗示换装
        时长：2 秒
        """
    }
]

# 在场景间插入造型转换镜头
final_scenes = []
for i, scene in enumerate(scenes):
    final_scenes.append(scene)
    
    # 如果下一个场景造型不同，插入转换镜头
    if i < len(scenes) - 1:
        next_scene = scenes[i + 1]
        for char in scene['characters']:
            next_char = next((c for c in next_scene['characters'] if c['name'] == char['name']), None)
            if next_char and next_char['style'] != char['style']:
                # 插入造型转换镜头
                transition = create_style_transition(
                    character=char['name'],
                    from_style=char['style'],
                    to_style=next_char['style']
                )
                final_scenes.append(transition)
```

### 渐进式造型变化

```python
def gradual_style_change(character, from_style, to_style, num_steps=3):
    """
    渐进式造型变化
    
    适用于需要展示造型变化过程的场景
    """
    prompts = []
    
    for i in range(num_steps):
        progress = i / (num_steps - 1)
        
        prompt = f"""
        {character} 的造型变化过程
        
        阶段：{i+1}/{num_steps}
        变化进度：{progress*100:.0f}%
        
        当前造型：
        - 服装：{interpolate_style(from_style['outfit'], to_style['outfit'], progress)}
        - 妆容：{interpolate_style(from_style['makeup'], to_style['makeup'], progress)}
        - 发型：{interpolate_style(from_style['hair'], to_style['hair'], progress)}
        
        场景：化妆间，镜子前
        镜头：特写，聚焦面部和上半身
        """
        prompts.append(prompt)
    
    return prompts

# 生成渐进变化视频
change_prompts = gradual_style_change(
    character="小艾",
    from_style=manager.characters["小艾"]["styles"]["casual"],
    to_style=manager.characters["小艾"]["styles"]["formal"],
    num_steps=3
)

for i, prompt in enumerate(change_prompts):
    rsp = VideoSynthesis.async_call(
        api_key=api_key,
        model='wan2.6-t2v',
        prompt=prompt,
        duration=5,
        seed=12345
    )
    # 下载并拼接...
```

---

## 🎭 方案 4：多角色互动场景

### 对话场景处理

```python
def generate_dialogue_scene(characters, dialogue_script):
    """
    生成对话场景
    
    characters = ["小艾", "阿明"]
    dialogue_script = [
        {"speaker": "小艾", "text": "你好啊！", "action": "挥手"},
        {"speaker": "阿明", "text": "好久不见！", "action": "微笑"},
        ...
    ]
    """
    clips = []
    
    for line in dialogue_script:
        speaker = line["speaker"]
        char_data = manager.characters[speaker]
        
        # 生成说话镜头
        prompt = f"""
        {manager.get_prompt(speaker)}
        
        动作：{line['action']}
        台词："{line['text']}"
        镜头：特写，聚焦面部表情
        口型：与台词同步
        """
        
        rsp = VideoSynthesis.async_call(
            api_key=api_key,
            model='wan2.6-r2v',
            prompt=prompt,
            video_url=char_data['reference_video'],
            duration=5,
            seed=char_data['seed']
        )
        
        result = VideoSynthesis.wait(task=rsp, api_key=api_key)
        clips.append({
            "speaker": speaker,
            "video": result.output.video_url,
            "duration": 5
        })
    
    # 剪辑对话场景（正反打镜头）
    edit_dialogue_scene(clips, "dialogue_scene.mp4")
```

### 正反打镜头剪辑

```python
def edit_dialogue_scene(clips, output_file):
    """
    剪辑对话场景
    
    使用电影正反打技巧：
    - 说话者特写
    - 听话者反应镜头
    - 双人中景
    """
    import subprocess
    
    # 创建剪辑列表
    edit_sequence = []
    for i, clip in enumerate(clips):
        # 说话者特写 (3 秒)
        edit_sequence.append((clip["video"], 0, 3))
        
        # 如果有下一个镜头，插入反应镜头
        if i < len(clips) - 1:
            next_clip = clips[i + 1]
            # 听话者反应 (2 秒)
            edit_sequence.append((next_clip["video"], 0, 2))
    
    # 使用 ffmpeg 剪辑
    filter_complex = ""
    inputs = []
    
    for i, (video, start, duration) in enumerate(edit_sequence):
        inputs.extend(["-i", video])
        filter_complex += f"[{i}:v]trim=start={start}:duration={duration},setpts=PTS-STARTPTS[v{i}];"
    
    # 拼接所有片段
    for i in range(len(edit_sequence)):
        filter_complex += f"[v{i}]"
    filter_complex += f"concat=n={len(edit_sequence)}:v=1:a=0[outv]"
    
    cmd = [
        "ffmpeg",
        *inputs,
        "-filter_complex", filter_complex,
        "-map", "[outv]",
        "-c:v", "libx264",
        output_file
    ]
    
    subprocess.run(cmd)
```

---

## 📊 完整工作流示例

```python
"""
多角色多造型视频完整工作流
"""

# 1. 创建角色管理系统
manager = CharacterManager()

# 2. 添加所有角色
manager.add_character("小艾", {...})
manager.add_character("阿明", {...})
manager.add_character("反派", {...})
# ... 更多角色

# 3. 为每个角色生成参考视频
generate_character_references(manager)

# 4. 定义完整剧本
script = [
    {
        "scene": 1,
        "location": "咖啡厅",
        "time": "白天",
        "characters": [
            {"name": "小艾", "style": "casual"},
            {"name": "阿明", "style": "casual"}
        ],
        "action": "相遇对话",
        "dialogue": [...]
    },
    {
        "scene": 2,
        "location": "公司",
        "time": "白天",
        "characters": [
            {"name": "小艾", "style": "formal"},
            {"name": "阿明", "style": "formal"}
        ],
        "action": "商务谈判",
        "dialogue": [...]
    },
    # ... 更多场景
]

# 5. 按场景生成
all_clips = []
for scene in script:
    print(f"生成场景 {scene['scene']}: {scene['location']}")
    
    # 检查是否需要造型转换
    if scene['scene'] > 1:
        prev_scene = script[scene['scene'] - 2]
        transitions = check_style_changes(prev_scene, scene, manager)
        for trans in transitions:
            all_clips.append(generate_transition(trans))
    
    # 生成场景视频
    scene_clip = generate_scene(scene, manager)
    all_clips.append(scene_clip)

# 6. 后期合成
final_video = composite_all_clips(
    all_clips,
    add_background_music=True,
    add_sound_effects=True,
    add_color_grading=True
)

print(f"长视频生成完成：{final_video}")
```

---

## ⚠️ 注意事项

### 角色一致性检查清单

- [ ] 每个角色有独立档案
- [ ] 每个造型有参考视频
- [ ] 使用固定随机种子
- [ ] 提示词包含完整角色描述
- [ ] 多角色场景分步生成

### 成本控制

| 项目 | 单价 | 优化建议 |
|------|------|---------|
| 角色参考视频 | ¥0.5/秒×3 造型 | 每个角色必做 |
| 多人场景分步生成 | 成本×人数 | 2-3 人适用 |
| 造型转换镜头 | ¥0.5/秒 | 按需添加 |
| 绿幕合成 | 额外后期成本 | 专业场景使用 |

### 推荐工具

- **角色管理**: 自建 CharacterManager 类
- **视频合成**: ffmpeg, Adobe After Effects
- **绿幕抠像**: ffmpeg chromakey, After Effects
- **剪辑**: Adobe Premiere, DaVinci Resolve

---

**最后更新**: 2026-04-02  
**维护人**: 胖福
