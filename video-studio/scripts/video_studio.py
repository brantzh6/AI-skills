#!/usr/bin/env python3
"""
Video Studio - AI video generation with Alibaba Cloud Wan 2.6/2.7
Supports: text-to-video, image-to-video, reference video generation
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

# Model to endpoint mapping
MODEL_ENDPOINTS = {
    "wan2.7-t2v": "video-synthesis",
    "wan2.6-t2v": "video-synthesis",
    "wan2.5-t2v-preview": "video-synthesis",
    "wan2.2-t2v-plus": "video-synthesis",
    "wanx2.1-t2v-turbo": "video-synthesis",
    "wan2.6-i2v": "image-to-video",
    "wan2.5-i2v-preview": "image-to-video",
    "wan2.6-r2v": "reference-to-video",
}


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


def encode_image_to_base64(image_path):
    """Encode local image file to base64 data URI."""
    with open(image_path, "rb") as f:
        img_data = f.read()
    b64 = base64.b64encode(img_data).decode("utf-8")
    ext = os.path.splitext(image_path)[1].lower()
    mime_map = {
        ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
        ".png": "image/png", ".bmp": "image/bmp", ".webp": "image/webp",
    }
    mime = mime_map.get(ext, "image/jpeg")
    return f"data:{mime};base64,{b64}"


def get_model_type(model):
    """Determine model type from model name."""
    if "i2v" in model:
        return "i2v"
    elif "r2v" in model:
        return "r2v"
    else:
        return "t2v"


def create_video_task(prompt, model="wan2.6-t2v", image=None, first_image=None,
                      last_image=None, ref_video=None, audio_url=None,
                      resolution="720P", ratio="16:9", duration=5,
                      negative_prompt="", prompt_extend=True, watermark=False, seed=None):
    """Create an async video generation task."""
    api_key = get_api_key()
    if not api_key:
        return {"error": "No API key found. Set DASHSCOPE_API_KEY."}

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "X-DashScope-Async": "enable",
    }

    model_type = get_model_type(model)

    if model_type == "t2v":
        # Text-to-video
        input_data = {"prompt": prompt}
        if audio_url:
            input_data["audio_url"] = audio_url

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

        # For wan2.6, use size instead of resolution
        if "wan2.6" in model or "wan2.5" in model or "wan2.2" in model or "wanx2.1" in model:
            size_map = {
                ("720P", "16:9"): "1280*720",
                ("720P", "9:16"): "720*1280",
                ("720P", "1:1"): "960*960",
                ("480P", "16:9"): "832*480",
                ("480P", "9:16"): "480*832",
            }
            size = size_map.get((resolution, ratio), "832*480")
            parameters["size"] = size
            del parameters["resolution"]

        payload = {
            "model": model,
            "input": input_data,
            "parameters": parameters,
        }

    elif model_type == "i2v":
        # Image-to-video
        content = [{"text": prompt}]

        if first_image and last_image:
            # First + Last frame mode
            for img_path in [first_image, last_image]:
                if img_path.startswith(("http://", "https://")):
                    content.append({"image": img_path})
                else:
                    content.append({"image": encode_image_to_base64(img_path)})
        elif image:
            # Single first frame mode
            if image.startswith(("http://", "https://")):
                content.append({"image": image})
            else:
                content.append({"image": encode_image_to_base64(image)})
        else:
            return {"error": "Image-to-video mode requires --image or --first parameter."}

        input_data = {"prompt": prompt, "img_url": content[-1]["image"]}
        if last_image:
            input_data["last_frame"] = content[-1]["image"] if last_image.startswith(("http://", "https://")) else encode_image_to_base64(last_image)

        # Check if this is the new multimodal API format
        if "wan2.7" in model:
            payload = {
                "model": model,
                "input": {
                    "messages": [{"role": "user", "content": content}]
                },
                "parameters": {
                    "resolution": resolution,
                    "ratio": ratio,
                    "duration": duration,
                    "prompt_extend": prompt_extend,
                    "watermark": watermark,
                },
            }
        else:
            # Old API format for wan2.6 and earlier
            size_map = {
                ("720P", "16:9"): "1280*720",
                ("720P", "9:16"): "720*1280",
                ("480P", "16:9"): "832*480",
                ("480P", "9:16"): "480*832",
            }
            size = size_map.get((resolution, ratio), "832*480")
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

    elif model_type == "r2v":
        # Reference-to-video
        if not ref_video:
            return {"error": "Reference video mode requires --ref parameter."}

        ref_urls = []
        if isinstance(ref_video, list):
            ref_urls = ref_video
        else:
            ref_urls = [ref_video]

        input_data = {"prompt": prompt, "ref_video_urls": ref_urls}

        size_map = {
            ("720P", "16:9"): "1280*720",
            ("720P", "9:16"): "720*1280",
            ("480P", "16:9"): "832*480",
        }
        size = size_map.get((resolution, ratio), "832*480")

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
    else:
        return {"error": f"Unknown model type: {model_type}"}

    endpoint = f"{BASE_URL}/api/v1/services/aigc/video-generation/video-synthesis"

    try:
        response = requests.post(endpoint, headers=headers, json=payload, timeout=60)
        return response.json()
    except Exception as e:
        return {"error": f"Request failed: {str(e)}"}


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
                if i % 4 == 0:  # Print progress every ~60 seconds
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
        resp = requests.get(video_url, timeout=120)
        if resp.status_code == 200:
            filename = f"video_{int(time.time())}.mp4"
            filepath = os.path.join(output_dir, filename)
            with open(filepath, "wb") as f:
                f.write(resp.content)
            return filepath
    except Exception as e:
        print(f"Failed to download video: {e}", file=sys.stderr)

    return video_url  # Return URL if download fails


def main():
    parser = argparse.ArgumentParser(description="Video Studio - AI video generation")
    parser.add_argument("mode", nargs="?", choices=["t2v", "i2v", "r2v", "poll"],
                        help="Mode: t2v (text-to-video), i2v (image-to-video), r2v (reference-to-video), poll")
    parser.add_argument("prompt", nargs="?", default=None, help="Video description prompt")

    parser.add_argument("--image", default=None, help="Input image for i2v (first frame)")
    parser.add_argument("--first", default=None, help="First frame image for i2v")
    parser.add_argument("--last", default=None, help="Last frame image for i2v")
    parser.add_argument("--ref", action="append", help="Reference video URL(s) for r2v")
    parser.add_argument("--audio", default=None, help="Audio file URL for video soundtrack")

    parser.add_argument("--model", default="wan2.6-t2v", help="Model name")
    parser.add_argument("--duration", type=int, default=5, help="Video duration in seconds (2-15)")
    parser.add_argument("--resolution", default="720P", help="Resolution: 480P, 720P, 1080P")
    parser.add_argument("--ratio", default="16:9", help="Aspect ratio: 16:9, 9:16, 1:1, 4:3, 3:4")
    parser.add_argument("--seed", type=int, default=None, help="Random seed")
    parser.add_argument("--negative", default="", help="Negative prompt")
    parser.add_argument("--no-prompt-extend", action="store_true", help="Disable prompt extension")
    parser.add_argument("--watermark", action="store_true", help="Add AI watermark")
    parser.add_argument("--task-id", help="Task ID to check status")
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
            if video_file and video_file.startswith("http"):
                print(f"🎬 Video generated! Download within 24h:")
                print(f"  {video_file}")
            elif video_file:
                print(f"🎬 Video saved to: {video_file}")
        elif status == "FAILED":
            print(f"❌ Video generation failed: {output.get('code', '')} - {output.get('message', '')}")
        else:
            print(f"Task status: {status}")

        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    # Validate required params
    if not args.mode or not args.prompt:
        print("❌ Usage: video_studio.py <mode> <prompt> [options]")
        print("   Modes: t2v, i2v, r2v")
        print("   Poll:  video_studio.py poll <task_id>")
        return

    prompt_extend = not args.no_prompt_extend

    print(f"🎬 Starting video generation...", file=sys.stderr)
    print(f"   Mode: {args.mode}", file=sys.stderr)
    print(f"   Model: {args.model}", file=sys.stderr)
    print(f"   Prompt: {args.prompt[:80]}{'...' if len(args.prompt) > 80 else ''}", file=sys.stderr)
    print(f"   Duration: {args.duration}s", file=sys.stderr)
    print(f"   Resolution: {args.resolution} ({args.ratio})", file=sys.stderr)

    result = create_video_task(
        prompt=args.prompt,
        model=args.model,
        image=args.image,
        first_image=args.first,
        last_image=args.last,
        ref_video=args.ref,
        audio_url=args.audio,
        resolution=args.resolution,
        ratio=args.ratio,
        duration=args.duration,
        negative_prompt=args.negative,
        prompt_extend=prompt_extend,
        watermark=args.watermark,
        seed=args.seed,
    )

    if "error" in result:
        print(f"❌ Error: {result['error']}")
        sys.exit(1)

    task_id = result.get("output", {}).get("task_id")
    if task_id:
        print(f"📋 Task ID: {task_id}")
        print(f"   Status: {result.get('output', {}).get('task_status', 'PENDING')}")
        print(f"   Poll with: --task-id {task_id} --poll")

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
