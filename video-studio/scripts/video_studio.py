#!/usr/bin/env python3
"""
Video Studio - AI video generation with Alibaba Cloud Wan 2.6/2.7

Modes:
  t2v  - Text-to-Video (wan2.7-t2v, wan2.6-t2v)
  i2v  - Image-to-Video, first frame or first+last frame (wan2.6-i2v)
  r2v  - Reference-to-Video, multi-character/multi-shot (wan2.7-r2v, wan2.6-r2v)

All modes are asynchronous: submit → poll → download.
"""

import argparse
import base64
import json
import os
import sys
import time
import requests

# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

# Configuration
BASE_URL = "https://dashscope.aliyuncs.com"
DASHSCOPE_API_KEY = os.environ.get("DASHSCOPE_API_KEY", "")
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)


def get_api_key():
    """Get API key from environment or .env file."""
    if DASHSCOPE_API_KEY:
        return DASHSCOPE_API_KEY
    env_path = os.path.expanduser("~/.openclaw/.env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("DASHSCOPE_API_KEY="):
                    return line.split("=", 1)[1].strip()
    return ""


def resolve_media_path(media_str):
    """
    Resolve media to URL or base64.
    - If starts with http/https/oss:// → return as-is
    - If local file → encode to base64 data URI
    """
    if not media_str:
        return None
    if media_str.startswith(("http://", "https://", "oss://")):
        return media_str
    if os.path.isfile(media_str):
        with open(media_str, "rb") as f:
            img_data = f.read()
        b64 = base64.b64encode(img_data).decode("utf-8")
        ext = os.path.splitext(media_str)[1].lower()
        mime_map = {
            ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
            ".png": "image/png", ".bmp": "image/bmp",
            ".webp": "image/webp",
            ".mp4": "video/mp4", ".mov": "video/quicktime",
            ".mp3": "audio/mpeg", ".wav": "audio/wav",
        }
        mime = mime_map.get(ext, "application/octet-stream")
        return f"data:{mime};base64,{b64}"
    return media_str  # Assume it's a URL


def is_video_path(path):
    """Check if path is a video file."""
    if not path:
        return False
    ext = os.path.splitext(path)[1].lower()
    return ext in (".mp4", ".mov", ".avi", ".mkv")


def is_audio_path(path):
    """Check if path is an audio file."""
    if not path:
        return False
    ext = os.path.splitext(path)[1].lower()
    return ext in (".mp3", ".wav", ".ogg", ".flac", ".aac")


def is_image_path(path):
    """Check if path is an image file."""
    if not path:
        return False
    ext = os.path.splitext(path)[1].lower()
    return ext in (".jpg", ".jpeg", ".png", ".bmp", ".webp", ".gif")


def get_resolution_size(resolution, ratio):
    """Map resolution + ratio to actual pixel dimensions for wan2.6 models."""
    size_map = {
        ("1080P", "16:9"): "1920*1080",
        ("1080P", "9:16"): "1080*1920",
        ("1080P", "1:1"): "1440*1440",
        ("1080P", "4:3"): "1632*1248",
        ("1080P", "3:4"): "1248*1632",
        ("720P", "16:9"): "1280*720",
        ("720P", "9:16"): "720*1280",
        ("720P", "1:1"): "960*960",
        ("720P", "4:3"): "1088*832",
        ("720P", "3:4"): "832*1088",
        ("480P", "16:9"): "832*480",
        ("480P", "9:16"): "480*832",
    }
    return size_map.get((resolution, ratio), "1280*720")


# =============================================================================
# Text-to-Video
# =============================================================================

def create_t2v_task(prompt, model="wan2.6-t2v", audio_url=None,
                    resolution="720P", ratio="16:9", duration=5,
                    negative_prompt="", prompt_extend=True, watermark=False, seed=None):
    """Create text-to-video async task."""
    api_key = get_api_key()
    if not api_key:
        return {"error": "No API key found. Set DASHSCOPE_API_KEY."}

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "X-DashScope-Async": "enable",
    }

    input_data = {"prompt": prompt}
    if audio_url:
        input_data["audio_url"] = resolve_media_path(audio_url)

    if "wan2.7" in model:
        # wan2.7 uses new protocol with resolution
        parameters = {
            "resolution": resolution,
            "ratio": ratio,
            "duration": duration,
            "prompt_extend": prompt_extend,
            "watermark": watermark,
        }
    else:
        # wan2.6 and earlier use size
        size = get_resolution_size(resolution, ratio)
        parameters = {
            "size": size,
            "ratio": ratio,
            "duration": duration,
            "prompt_extend": prompt_extend,
            "watermark": watermark,
        }

    if negative_prompt:
        parameters["negative_prompt"] = negative_prompt
    if seed is not None:
        parameters["seed"] = seed

    payload = {
        "model": model,
        "input": input_data,
        "parameters": parameters,
    }

    endpoint = f"{BASE_URL}/api/v1/services/aigc/video-generation/video-synthesis"
    try:
        response = requests.post(endpoint, headers=headers, json=payload, timeout=60)
        return response.json()
    except Exception as e:
        return {"error": f"Request failed: {str(e)}"}


# =============================================================================
# Image-to-Video
# =============================================================================

def create_i2v_task(prompt, model="wan2.6-i2v", image=None,
                    first_image=None, last_image=None,
                    resolution="720P", ratio="16:9", duration=5,
                    negative_prompt="", prompt_extend=True, watermark=False, seed=None):
    """Create image-to-video async task."""
    api_key = get_api_key()
    if not api_key:
        return {"error": "No API key found. Set DASHSCOPE_API_KEY."}

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "X-DashScope-Async": "enable",
    }

    first = image or first_image
    if not first:
        return {"error": "Image-to-video requires --image or --first parameter."}

    first_resolved = resolve_media_path(first)

    if "wan2.7" in model:
        # wan2.7 uses multimodal messages
        content = [{"text": prompt}]
        if first_resolved:
            content.append({"image": first_resolved})
        if last_image:
            content.append({"image": resolve_media_path(last_image)})

        parameters = {
            "resolution": resolution,
            "ratio": ratio,
            "duration": duration,
            "prompt_extend": prompt_extend,
            "watermark": watermark,
        }
        if seed is not None:
            parameters["seed"] = seed

        payload = {
            "model": model,
            "input": {"messages": [{"role": "user", "content": content}]},
            "parameters": parameters,
        }
    else:
        # wan2.6 uses img_url + last_frame_url
        size = get_resolution_size(resolution, ratio)
        input_data = {"prompt": prompt, "img_url": first_resolved}
        if last_image:
            input_data["last_frame_url"] = resolve_media_path(last_image)

        parameters = {
            "size": size,
            "ratio": ratio,
            "duration": duration,
            "prompt_extend": prompt_extend,
            "watermark": watermark,
        }
        if negative_prompt:
            parameters["negative_prompt"] = negative_prompt
        if seed is not None:
            parameters["seed"] = seed

        payload = {
            "model": model,
            "input": input_data,
            "parameters": parameters,
        }

    endpoint = f"{BASE_URL}/api/v1/services/aigc/video-generation/video-synthesis"
    try:
        response = requests.post(endpoint, headers=headers, json=payload, timeout=60)
        return response.json()
    except Exception as e:
        return {"error": f"Request failed: {str(e)}"}


# =============================================================================
# Reference-to-Video
# =============================================================================

def create_r2v_task(prompt, model="wan2.6-r2v",
                    refs=None, first_frame=None,
                    audio_url=None, reference_voice=None,
                    resolution="720P", ratio="16:9", duration=5,
                    shot_type="single", audio_enabled=True,
                    negative_prompt="", prompt_extend=True, watermark=False, seed=None):
    """
    Create reference-to-video async task.

    refs: list of media paths/URLs (images and videos)
    first_frame: optional first frame image for r2v
    """
    api_key = get_api_key()
    if not api_key:
        return {"error": "No API key found. Set DASHSCOPE_API_KEY."}

    if not refs or len(refs) == 0:
        return {"error": "Reference-to-video requires at least one --ref parameter."}

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "X-DashScope-Async": "enable",
    }

    if "wan2.7" in model:
        # ===== wan2.7 protocol: media array =====
        media = []
        video_count = 0
        image_count = 0

        for ref in refs:
            resolved = resolve_media_path(ref)
            if not resolved:
                continue

            # Determine type from path/URL
            if is_video_path(ref):
                media.append({"type": "reference_video", "url": resolved})
                video_count += 1
            elif is_image_path(ref):
                media.append({"type": "reference_image", "url": resolved})
                image_count += 1
            else:
                # Assume video if can't determine
                media.append({"type": "reference_video", "url": resolved})
                video_count += 1

        # Add first frame if provided
        if first_frame:
            resolved_first = resolve_media_path(first_frame)
            if resolved_first:
                media.append({"type": "first_frame", "url": resolved_first})

        # Validate limits
        if video_count > 3:
            return {"error": f"Too many reference videos ({video_count}). Maximum is 3 for wan2.7-r2v."}
        if image_count + video_count > 5:
            return {"error": f"Too many references ({image_count + video_count}). Maximum is 5 total for wan2.7-r2v."}

        input_data = {"prompt": prompt, "media": media}
        if audio_url:
            input_data["audio_url"] = resolve_media_path(audio_url)
        if reference_voice:
            input_data["reference_voice"] = resolve_media_path(reference_voice)

        parameters = {
            "resolution": resolution,
            "ratio": ratio,
            "duration": duration,
            "prompt_extend": prompt_extend,
            "watermark": watermark,
        }
        if negative_prompt:
            parameters["negative_prompt"] = negative_prompt
        if seed is not None:
            parameters["seed"] = seed

    else:
        # ===== wan2.6 protocol: reference_urls =====
        resolved_refs = []
        video_count = 0
        image_count = 0

        for ref in refs:
            resolved = resolve_media_path(ref)
            if resolved:
                resolved_refs.append(resolved)
                if is_video_path(ref):
                    video_count += 1
                else:
                    image_count += 1

        # Validate limits
        if video_count > 3:
            return {"error": f"Too many reference videos ({video_count}). Maximum is 3 for wan2.6-r2v."}
        if image_count + video_count > 5:
            return {"error": f"Too many references ({image_count + video_count}). Maximum is 5 total for wan2.6-r2v."}

        size = get_resolution_size(resolution, ratio)
        input_data = {"prompt": prompt, "reference_urls": resolved_refs}
        if audio_url:
            input_data["audio_url"] = resolve_media_path(audio_url)

        parameters = {
            "size": size,
            "duration": duration,
            "prompt_extend": prompt_extend,
            "watermark": watermark,
            "shot_type": shot_type,
        }
        if not audio_enabled:
            parameters["audio"] = False
        if negative_prompt:
            parameters["negative_prompt"] = negative_prompt
        if seed is not None:
            parameters["seed"] = seed

    payload = {
        "model": model,
        "input": input_data,
        "parameters": parameters,
    }

    endpoint = f"{BASE_URL}/api/v1/services/aigc/video-generation/video-synthesis"
    try:
        response = requests.post(endpoint, headers=headers, json=payload, timeout=60)
        return response.json()
    except Exception as e:
        return {"error": f"Request failed: {str(e)}"}


# =============================================================================
# Task Polling & Download
# =============================================================================

def get_task_result(task_id, max_retries=120, interval=15):
    """Poll task result until completion."""
    api_key = get_api_key()
    if not api_key:
        return {"error": "No API key found."}

    headers = {"Authorization": f"Bearer {api_key}"}
    start_time = time.time()

    for i in range(max_retries):
        try:
            url = f"{BASE_URL}/api/v1/tasks/{task_id}"
            response = requests.get(url, headers=headers, timeout=30)
            result = response.json()

            output = result.get("output", {})
            status = output.get("task_status", "UNKNOWN")

            if status == "SUCCEEDED":
                return result
            elif status == "FAILED":
                return result
            elif status in ("PENDING", "RUNNING"):
                elapsed = int(time.time() - start_time)
                if i % 4 == 0:
                    print(f"⏳ Generating video... ({elapsed}s) Status: {status}", file=sys.stderr)
                time.sleep(interval)
            else:
                return {"error": f"Unknown task status: {status}"}

        except Exception as e:
            return {"error": f"Failed to get task result: {str(e)}"}

    return {"error": f"Task timed out after {max_retries * interval} seconds."}


def download_video(result, output_dir=None):
    """Download video from URL in result."""
    output = result.get("output", {})
    video_url = output.get("video_url", "")

    if not video_url:
        return None

    if output_dir is None:
        output_dir = os.path.join(SKILL_DIR, "output")

    os.makedirs(output_dir, exist_ok=True)

    try:
        resp = requests.get(video_url, timeout=180)
        if resp.status_code == 200:
            filename = f"video_{int(time.time())}.mp4"
            filepath = os.path.join(output_dir, filename)
            with open(filepath, "wb") as f:
                f.write(resp.content)
            return filepath
    except Exception as e:
        print(f"Failed to download video: {e}", file=sys.stderr)

    return video_url


# =============================================================================
# Main CLI
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Video Studio - AI video generation with Alibaba Cloud Wan 2.6/2.7",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Text to video
  video_studio.py t2v "A cat running in the garden" --duration 10

  # Image to video (first frame)
  video_studio.py i2v "cinematic camera pan" --image start.jpg

  # Image to video (first + last frame)
  video_studio.py i2v "smooth transition" --first start.jpg --last end.jpg

  # Reference to video (single character)
  video_studio.py r2v "character1 dancing in the rain" --ref person.mp4

  # Reference to video (multi-character)
  video_studio.py r2v "视频1和图3在咖啡厅对话" --ref char1.mp4 --ref char2.mp4 --ref cafe.jpg

  # Reference to video (multi-shot)
  video_studio.py r2v "adventure story" --ref storyboard.png --shot-type multi

  # Poll task
  video_studio.py poll <task_id>
        """
    )
    parser.add_argument("mode", nargs="?", choices=["t2v", "i2v", "r2v", "poll"],
                        help="Generation mode")
    parser.add_argument("prompt", nargs="?", default=None, help="Video description prompt")

    # Image-to-Video parameters
    parser.add_argument("--image", default=None, help="First frame image (i2v mode)")
    parser.add_argument("--first", default=None, help="First frame image (alias for --image)")
    parser.add_argument("--last", default=None, help="Last frame image (i2v mode)")

    # Reference-to-Video parameters
    parser.add_argument("--ref", action="append", dest="refs", default=[],
                        help="Reference video/image URL or local path (r2v mode, repeatable)")
    parser.add_argument("--first-frame", default=None, help="First frame image for r2v mode")
    parser.add_argument("--reference-voice", default=None, help="Audio URL for voice reference (r2v wan2.7)")

    # Common parameters
    parser.add_argument("--model", default=None, help="Override model name")
    parser.add_argument("--audio", default=None, help="Audio file URL for video soundtrack")
    parser.add_argument("--duration", type=int, default=None, help="Duration in seconds")
    parser.add_argument("--resolution", default="720P", help="Resolution: 480P, 720P, 1080P")
    parser.add_argument("--ratio", default="16:9", help="Aspect ratio: 16:9, 9:16, 1:1, 4:3, 3:4")
    parser.add_argument("--shot-type", default="single", choices=["single", "multi"],
                        help="Shot type: single or multi (r2v wan2.6)")
    parser.add_argument("--no-audio", action="store_true", help="Generate silent video (r2v wan2.6-flash)")
    parser.add_argument("--seed", type=int, default=None, help="Random seed")
    parser.add_argument("--negative", default="", help="Negative prompt")
    parser.add_argument("--no-prompt-extend", action="store_true", help="Disable prompt enhancement")
    parser.add_argument("--watermark", action="store_true", help="Add AI watermark")
    parser.add_argument("--task-id", default=None, help="Task ID to check status")
    parser.add_argument("--poll", action="store_true", help="Poll task until completion")
    parser.add_argument("--output-dir", default=None, help="Output directory")

    args = parser.parse_args()

    # Handle task polling
    if args.mode == "poll" or args.task_id:
        task_id = args.task_id or args.prompt
        if not task_id:
            print("❌ Please provide a task ID")
            return
        print(f"🔍 Checking task: {task_id}", file=sys.stderr)
        result = get_task_result(task_id)
        if "error" in result:
            print(f"❌ {result['error']}")
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return

        output = result.get("output", {})
        status = output.get("task_status", "UNKNOWN")

        if status == "SUCCEEDED":
            video_file = download_video(result, args.output_dir)
            if video_file and not video_file.startswith("http"):
                print(f"🎬 Video saved: {video_file}")
            elif video_file:
                print(f"🎬 Video URL (download within 24h): {video_file}")
        elif status == "FAILED":
            print(f"❌ Failed: {output.get('code', '')} - {output.get('message', '')}")
        else:
            print(f"Status: {status}")

        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    # Validate mode and prompt
    if not args.mode or not args.prompt:
        print("❌ Usage: video_studio.py <mode> <prompt> [options]")
        print("   Modes: t2v, i2v, r2v")
        print("   Poll:  video_studio.py poll <task_id>")
        parser.print_help()
        return

    # Determine model
    model = args.model
    if not model:
        if args.mode == "t2v":
            model = "wan2.6-t2v"
        elif args.mode == "i2v":
            model = "wan2.6-i2v"
        elif args.mode == "r2v":
            model = "wan2.6-r2v"

    # Determine duration defaults
    duration = args.duration
    if duration is None:
        if "wan2.7" in model:
            duration = 5
        else:
            duration = 5

    prompt_extend = not args.no_prompt_extend

    # Print info
    print(f"🎬 Starting video generation...", file=sys.stderr)
    print(f"   Mode: {args.mode}", file=sys.stderr)
    print(f"   Model: {model}", file=sys.stderr)
    print(f"   Prompt: {args.prompt[:100]}{'...' if len(args.prompt) > 100 else ''}", file=sys.stderr)
    print(f"   Duration: {duration}s | Resolution: {args.resolution} ({args.ratio})", file=sys.stderr)
    if args.refs:
        print(f"   References: {len(args.refs)} files", file=sys.stderr)
    if args.shot_type == "multi":
        print(f"   Shot type: multi (多镜头)", file=sys.stderr)

    # Create task based on mode
    if args.mode == "t2v":
        result = create_t2v_task(
            prompt=args.prompt, model=model,
            audio_url=args.audio,
            resolution=args.resolution, ratio=args.ratio,
            duration=duration, negative_prompt=args.negative,
            prompt_extend=prompt_extend, watermark=args.watermark,
            seed=args.seed,
        )
    elif args.mode == "i2v":
        result = create_i2v_task(
            prompt=args.prompt, model=model,
            image=args.image, first_image=args.first,
            last_image=args.last,
            resolution=args.resolution, ratio=args.ratio,
            duration=duration, negative_prompt=args.negative,
            prompt_extend=prompt_extend, watermark=args.watermark,
            seed=args.seed,
        )
    elif args.mode == "r2v":
        result = create_r2v_task(
            prompt=args.prompt, model=model,
            refs=args.refs, first_frame=args.first_frame,
            audio_url=args.audio, reference_voice=args.reference_voice,
            resolution=args.resolution, ratio=args.ratio,
            duration=duration, shot_type=args.shot_type,
            audio_enabled=not args.no_audio,
            negative_prompt=args.negative,
            prompt_extend=prompt_extend, watermark=args.watermark,
            seed=args.seed,
        )
    else:
        print(f"❌ Unknown mode: {args.mode}")
        return

    # Handle result
    if "error" in result:
        print(f"❌ Error: {result['error']}")
        sys.exit(1)

    task_id = result.get("output", {}).get("task_id")
    if task_id:
        print(f"📋 Task ID: {task_id}")
        print(f"   Status: {result.get('output', {}).get('task_status', 'PENDING')}")
        print(f"   Poll with: python video_studio.py poll {task_id}")

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
