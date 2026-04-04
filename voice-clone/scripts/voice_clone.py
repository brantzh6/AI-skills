#!/usr/bin/env python3
"""
Voice Clone - AI voice cloning and TTS with Alibaba Cloud CosyVoice
Supports: voice cloning from audio, voice design from text, TTS synthesis
"""

import argparse
import base64
import json
import os
import sys
import time
import requests

# Configuration
BASE_URL = "https://dashscope.aliyuncs.com"
DASHSCOPE_API_KEY = os.environ.get("DASHSCOPE_API_KEY", "")
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
VOICES_FILE = os.path.join(SKILL_DIR, "voices.json")


def get_api_key():
    """Get API key from environment or config."""
    if DASHSCOPE_API_KEY:
        return DASHSCOPE_API_KEY
    env_path = os.path.expanduser("~/.openclaw/.env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("DASHSCOPE_API_KEY="):
                    return line.split("=", 1)[1].strip()
    return ""


def load_voices():
    """Load saved voices config."""
    if os.path.exists(VOICES_FILE):
        with open(VOICES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"default": None, "voices": {}}


def save_voices(config):
    """Save voices config."""
    with open(VOICES_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


def create_voice_clone(audio_url, prefix=None, target_model="cosyvoice-v3.5-plus"):
    """Create a voice clone from audio URL."""
    api_key = get_api_key()
    if not api_key:
        return {"error": "No API key found. Set DASHSCOPE_API_KEY."}

    if prefix is None:
        prefix = f"voice_{int(time.time())}"

    # Import SDK
    try:
        import dashscope
        from dashscope.audio.tts_v2 import VoiceEnrollmentService

        dashscope.api_key = api_key
        dashscope.base_http_api_url = f"{BASE_URL}/api/v1"

        service = VoiceEnrollmentService()
        voice_id = service.create_voice(
            target_model=target_model,
            prefix=prefix,
            url=audio_url,
        )
        return {
            "voice_id": voice_id,
            "status": "DEPLOYING",
            "target_model": target_model,
        }
    except ImportError:
        # Fallback to HTTP API
        return create_voice_clone_http(audio_url, prefix, target_model, api_key)


def create_voice_clone_http(audio_url, prefix, target_model, api_key):
    """HTTP fallback for voice cloning."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    data = {
        "model": "voice-enrollment",
        "input": {
            "action": "create_voice",
            "target_model": target_model,
            "url": audio_url,
            "prefix": prefix,
        },
    }

    url = f"{BASE_URL}/api/v1/services/audio/tts/customization"
    try:
        response = requests.post(url, headers=headers, json=data, timeout=60)
        result = response.json()
        if response.status_code == 200:
            return {
                "voice_id": result["output"]["voice_id"],
                "status": "DEPLOYING",
                "target_model": target_model,
            }
        return {"error": result.get("message", "Unknown error")}
    except Exception as e:
        return {"error": f"Request failed: {str(e)}"}


def create_voice_design(voice_prompt, preview_text="大家好，欢迎收听", prefix=None, target_model="cosyvoice-v3.5-plus"):
    """Design a voice from text description."""
    api_key = get_api_key()
    if not api_key:
        return {"error": "No API key found. Set DASHSCOPE_API_KEY."}

    if prefix is None:
        prefix = f"voice_{int(time.time())}"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    data = {
        "model": "voice-enrollment",
        "input": {
            "action": "create_voice",
            "target_model": target_model,
            "voice_prompt": voice_prompt,
            "preview_text": preview_text,
            "prefix": prefix,
        },
        "parameters": {
            "sample_rate": 24000,
            "response_format": "wav",
        },
    }

    url = f"{BASE_URL}/api/v1/services/audio/tts/customization"
    try:
        response = requests.post(url, headers=headers, json=data, timeout=120)
        result = response.json()

        if response.status_code == 200:
            output = result.get("output", {})
            voice_id = output.get("voice_id", "")

            # Save preview audio
            preview_audio = output.get("preview_audio", {})
            base64_audio = preview_audio.get("data", "")
            if base64_audio:
                audio_bytes = base64.b64decode(base64_audio)
                output_dir = os.path.join(SKILL_DIR, "output")
                os.makedirs(output_dir, exist_ok=True)
                preview_file = os.path.join(output_dir, f"{voice_id}_preview.wav")
                with open(preview_file, "wb") as f:
                    f.write(audio_bytes)

                return {
                    "voice_id": voice_id,
                    "status": "OK",
                    "target_model": target_model,
                    "preview_file": preview_file,
                }

            return {"voice_id": voice_id, "status": "DEPLOYING", "target_model": target_model}
        else:
            return {"error": result.get("message", "Unknown error")}
    except Exception as e:
        return {"error": f"Request failed: {str(e)}"}


def poll_voice_status(voice_id, target_model="cosyvoice-v3.5-plus", max_retries=60, interval=10):
    """Poll voice enrollment status until ready."""
    api_key = get_api_key()
    if not api_key:
        return {"error": "No API key found."}

    try:
        import dashscope
        from dashscope.audio.tts_v2 import VoiceEnrollmentService

        dashscope.api_key = api_key
        dashscope.base_http_api_url = f"{BASE_URL}/api/v1"

        service = VoiceEnrollmentService()
        for attempt in range(max_retries):
            try:
                voice_info = service.query_voice(voice_id=voice_id)
                status = voice_info.get("status")
                print(f"⏳ Voice status: {status} (attempt {attempt+1}/{max_retries})", file=sys.stderr)

                if status == "OK":
                    return {"voice_id": voice_id, "status": "OK", "target_model": target_model}
                elif status == "UNDEPLOYED":
                    return {"voice_id": voice_id, "status": "UNDEPLOYED", "error": "Voice processing failed"}

                time.sleep(interval)
            except Exception as e:
                time.sleep(interval)

        return {"voice_id": voice_id, "status": "TIMEOUT", "error": "Polling timed out"}
    except ImportError:
        return {"voice_id": voice_id, "status": "UNKNOWN", "note": "SDK not available, use HTTP API"}


def synthesize_speech(text, voice_id, model="cosyvoice-v3.5-plus", output_file=None):
    """Generate speech with the specified voice."""
    api_key = get_api_key()
    if not api_key:
        return {"error": "No API key found."}

    try:
        import dashscope
        from dashscope.audio.tts_v2 import SpeechSynthesizer

        dashscope.api_key = api_key
        dashscope.base_websocket_api_url = f"wss://dashscope.aliyuncs.com/api-ws/v1/inference"

        synthesizer = SpeechSynthesizer(model=model, voice=voice_id)
        audio_data = synthesizer.call(text)

        if output_file is None:
            output_dir = os.path.join(SKILL_DIR, "output")
            os.makedirs(output_dir, exist_ok=True)
            output_file = os.path.join(output_dir, f"speech_{int(time.time())}.mp3")

        with open(output_file, "wb") as f:
            f.write(audio_data)

        return {
            "status": "OK",
            "output_file": output_file,
            "voice_id": voice_id,
            "model": model,
            "request_id": synthesizer.get_last_request_id(),
        }
    except ImportError:
        return {"error": "DashScope SDK not installed. Install with: pip install dashscope"}
    except Exception as e:
        return {"error": f"Synthesis failed: {str(e)}"}


def main():
    parser = argparse.ArgumentParser(description="Voice Clone - AI voice cloning and TTS")
    parser.add_argument("mode", nargs="?", choices=["clone", "design", "speak", "poll", "list", "set-default"],
                        help="Mode: clone, design, speak, poll, list, set-default")
    parser.add_argument("input", nargs="?", default=None,
                        help="Input: audio URL (clone), description (design), text (speak), voice_id (poll)")

    parser.add_argument("--name", "--prefix", default=None, help="Voice name/prefix")
    parser.add_argument("--voice", default=None, help="Voice ID for TTS")
    parser.add_argument("--model", default="cosyvoice-v3.5-plus", help="TTS model")
    parser.add_argument("--preview", default="大家好，欢迎收听", help="Preview text for voice design")
    parser.add_argument("--output", default=None, help="Output file path")
    parser.add_argument("--save", action="store_true", help="Save voice to config")

    args = parser.parse_args()

    if not args.mode:
        parser.print_help()
        return

    if args.mode == "list":
        config = load_voices()
        print(f"📋 Saved Voices:")
        print(f"   Default: {config.get('default', 'None')}")
        for vid, info in config.get("voices", {}).items():
            default_marker = " ★" if vid == config.get("default") else ""
            print(f"   - {info.get('name', vid)}{default_marker}")
            print(f"     ID: {vid}")
            print(f"     Model: {info.get('target_model', 'N/A')}")
            print(f"     Created: {info.get('created_at', 'N/A')}")
        return

    if args.mode == "set-default":
        if args.input:
            config = load_voices()
            config["default"] = args.input
            save_voices(config)
            print(f"✅ Default voice set to: {args.input}")
        else:
            print("❌ Please provide a voice ID")
        return

    if args.mode == "poll":
        voice_id = args.input
        if not voice_id:
            print("❌ Please provide a voice ID")
            return
        result = poll_voice_status(voice_id, args.model)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        if result.get("status") == "OK" and args.save:
            config = load_voices()
            name = args.name or voice_id
            config["voices"][voice_id] = {
                "voice_id": voice_id,
                "name": name,
                "target_model": args.model,
                "created_at": time.strftime("%Y-%m-%d"),
            }
            config["default"] = voice_id
            save_voices(config)
            print(f"✅ Voice saved to config")
        return

    if args.mode == "clone":
        if not args.input:
            print("❌ Please provide an audio URL")
            return
        result = create_voice_clone(args.input, args.name, args.model)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        if "error" not in result and args.save:
            config = load_voices()
            name = args.name or result.get("voice_id", "unknown")
            config["voices"][result["voice_id"]] = {
                "voice_id": result["voice_id"],
                "name": name,
                "target_model": args.model,
                "created_at": time.strftime("%Y-%m-%d"),
            }
            config["default"] = result["voice_id"]
            save_voices(config)
            print(f"✅ Voice saved to config")
        return

    if args.mode == "design":
        if not args.input:
            print("❌ Please provide a voice description")
            return
        print(f"🎙️ Designing voice...", file=sys.stderr)
        print(f"   Description: {args.input[:80]}...", file=sys.stderr)
        result = create_voice_design(args.input, args.preview, args.name, args.model)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        if "error" not in result and args.save:
            config = load_voices()
            name = args.name or result.get("voice_id", "unknown")
            config["voices"][result["voice_id"]] = {
                "voice_id": result["voice_id"],
                "name": name,
                "target_model": args.model,
                "created_at": time.strftime("%Y-%m-%d"),
            }
            config["default"] = result["voice_id"]
            save_voices(config)
            print(f"✅ Voice saved to config")
        return

    if args.mode == "speak":
        if not args.input:
            print("❌ Please provide text to synthesize")
            return

        config = load_voices()
        voice_id = args.voice or config.get("default")
        if not voice_id:
            print("❌ No voice ID specified. Use --voice <id> or set a default with: set-default <id>")
            return

        print(f"🔊 Synthesizing speech...", file=sys.stderr)
        print(f"   Voice: {voice_id}", file=sys.stderr)
        print(f"   Text: {args.input[:80]}...", file=sys.stderr)

        result = synthesize_speech(args.input, voice_id, args.model, args.output)
        if "error" in result:
            print(f"❌ {result['error']}")
            sys.exit(1)
        else:
            print(f"✅ Speech saved to: {result['output_file']}")
            print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
