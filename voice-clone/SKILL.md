---
name: voice-clone
description: Digital voice cloning and TTS with Alibaba Cloud CosyVoice. Clone your voice from audio, design new voices from text descriptions, and generate speech.
---

# Voice Clone 🎙️

Digital voice cloning and text-to-speech powered by Alibaba Cloud CosyVoice.

## Capabilities

| Mode | Model | Description |
|------|-------|-------------|
| **Voice Cloning** | cosyvoice-v3.5-plus | Clone a voice from 10-20 second audio sample |
| **Voice Design** | cosyvoice-v3.5-plus | Design a voice from text description |
| **TTS Synthesis** | cosyvoice-v3.5-plus/flash | Generate speech with any voice |

## Usage

### Clone Voice from Audio
```
/voice-clone <audio_file> --name myvoice
```
Upload a 10-20 second clear speech recording. Returns a `voice_id`.

### Design Voice from Description
```
/voice-design "沉稳的中年男性播音员，音色低沉浑厚，富有磁性" --preview "大家好，欢迎收听"
```

### Generate Speech
```
/speak <text> --voice <voice_id>
/speak "你好，这是用我的声音生成的语音" --voice myvoice_xxx
```

### List Saved Voices
```
/voice-list
```

## Voice Config Storage

Voices are saved to `voice-clone/voices.json`:
```json
{
  "default": "myvoice_xxx",
  "voices": {
    "myvoice_xxx": {
      "voice_id": "myvoice_xxx",
      "name": "我的声音",
      "target_model": "cosyvoice-v3.5-plus",
      "created_at": "2026-04-04"
    }
  }
}
```

## Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--name` | Voice name for cloning | auto-generated |
| `--voice` | Voice ID for TTS | default from config |
| `--model` | TTS model | cosyvoice-v3.5-plus |
| `--format` | Audio format | mp3 |
| `--speed` | Speech speed | 1.0 |
| `--preview TEXT` | Preview text for voice design | 大家好，欢迎收听 |

## API Details

- **Provider**: Alibaba Cloud Bailian (DashScope)
- **Models**: cosyvoice-v3.5-plus, cosyvoice-v3.5-flash
- **API Key**: From bailian auth profile
- **Base URL**: https://dashscope.aliyuncs.com

## Notes

- Voice cloning requires clear speech audio (10-20 seconds minimum)
- Audio should be in a supported language (Chinese, English, etc.)
- Voice IDs are persistent and can be reused
- Audio output is MP3 format by default
