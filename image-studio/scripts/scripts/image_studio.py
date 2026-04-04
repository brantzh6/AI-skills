#!/usr/bin/env python3
"""
Image Studio - AI image generation and editing with Alibaba Cloud Wan 2.6
Supports: text-to-image, image editing, style transfer
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

# Common size presets
SIZE_PRESETS = {
    "1:1": "1280*1280",
    "3:4": "1104*1472",
    "4:3": "1472*1104",
    "16:9": "1696*960",
    "9:16": "960*1696",
    "21:9": "1344*576",
}


def get_api_key():
    """Get API key from environment or config."""
    if DASHSCOPE_API_KEY:
        return DASHSCOPE_API_KEY
    # Try reading from .env
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
    # Determine MIME type
    ext = os.path.splitext(image_path)[1].lower()
    mime_map = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".bmp": "image/bmp",
        ".webp": "image/webp",
    }
    mime = mime_map.get(ext, "image/jpeg")
    return f"data:{mime};base64,{b64}"


def resolve_size(size_str):
    """Resolve size string to actual dimensions."""
    if size_str in SIZE_PRESETS:
        return SIZE_PRESETS[size_str]
    # Check if it's already in W*H format
    if "*" in size_str:
        return size_str
    return size_str


def upload_image_to_oss(image_path):
    """Upload image to a temporary location and return URL.
    
    For local images, we use base64 encoding instead.
    For URL images, we return as-is.
    """
    if image_path.startswith(("http://", "https://")):
        return image_path
    # Use base64 for local files
    return encode_image_to_base64(image_path)


def create_image_async(mode, prompt, images=None, negative_prompt="", size="1280*1280", n=1, seed=None, prompt_extend=True, watermark=False):
    """Create an async image generation task."""
    api_key = get_api_key()
    if not api_key:
        return {"error": "No API key found. Set DASHSCOPE_API_KEY environment variable."}

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "X-DashScope-Async": "enable",
    }

    if mode == "t2i":
        model = "wan2.6-t2i"
        endpoint = f"{BASE_URL}/api/v1/services/aigc/image-generation/generation"
        
        payload = {
            "model": model,
            "input": {
                "messages": [
                    {
                        "role": "user",
                        "content": [{"text": prompt}],
                    }
                ]
            },
            "parameters": {
                "size": size,
                "n": n,
                "prompt_extend": prompt_extend,
                "watermark": watermark,
            },
        }
        
        if negative_prompt:
            payload["parameters"]["negative_prompt"] = negative_prompt
        if seed is not None:
            payload["parameters"]["seed"] = seed
            
    elif mode == "edit":
        model = "wan2.6-image"
        endpoint = f"{BASE_URL}/api/v1/services/aigc/image-generation/generation"
        
        content = [{"text": prompt}]
        if images:
            for img in images:
                img_ref = upload_image_to_oss(img)
                content.append({"image": img_ref})
        
        payload = {
            "model": model,
            "input": {
                "messages": [
                    {
                        "role": "user",
                        "content": content,
                    }
                ]
            },
            "parameters": {
                "size": size,
                "n": n,
                "prompt_extend": prompt_extend,
                "watermark": watermark,
                "enable_interleave": False,
            },
        }
        
        if negative_prompt:
            payload["parameters"]["negative_prompt"] = negative_prompt
        if seed is not None:
            payload["parameters"]["seed"] = seed
    else:
        return {"error": f"Unknown mode: {mode}. Use 't2i' or 'edit'."}

    try:
        response = requests.post(endpoint, headers=headers, json=payload, timeout=30)
        return response.json()
    except Exception as e:
        return {"error": f"Request failed: {str(e)}"}


def get_task_result(task_id, max_retries=60, interval=5):
    """Poll task result until completion."""
    api_key = get_api_key()
    if not api_key:
        return {"error": "No API key found."}

    headers = {
        "Authorization": f"Bearer {api_key}",
    }

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
                if i % 6 == 0:  # Print progress every ~30 seconds
                    elapsed = (i + 1) * interval
                    print(f"⏳ Generating... ({elapsed}s) Status: {status}", file=sys.stderr)
                time.sleep(interval)
            else:
                return {"error": f"Unknown task status: {status}"}
                
        except Exception as e:
            return {"error": f"Failed to get task result: {str(e)}"}
    
    return {"error": "Task timed out after maximum retries."}


def download_images(result, output_dir=None):
    """Download images from URLs in result."""
    output = result.get("output", {})
    images = []
    
    # Handle sync response format (wan2.6-t2i sync)
    choices = output.get("choices", [])
    if choices:
        for choice in choices:
            message = choice.get("message", {})
            content = message.get("content", [])
            for item in content:
                if "image" in item:
                    images.append(item["image"])
    
    # Handle async response format
    if not images:
        results_list = output.get("results", [])
        for item in results_list:
            if "url" in item:
                images.append(item["url"])
    
    if not images:
        return []
    
    # Default output dir: same directory as this script / output
    if output_dir is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_dir = os.path.join(script_dir, "output")
    
    os.makedirs(output_dir, exist_ok=True)
    
    downloaded = []
    for idx, img_url in enumerate(images):
        try:
            resp = requests.get(img_url, timeout=60)
            if resp.status_code == 200:
                filename = f"image_{int(time.time())}_{idx}.png"
                filepath = os.path.join(output_dir, filename)
                with open(filepath, "wb") as f:
                    f.write(resp.content)
                downloaded.append(filepath)
        except Exception as e:
            print(f"Failed to download image {idx}: {e}", file=sys.stderr)
            downloaded.append(img_url)  # Keep URL if download fails
    
    return downloaded


def main():
    parser = argparse.ArgumentParser(description="Image Studio - AI image generation and editing")
    parser.add_argument("mode", nargs="?", choices=["t2i", "edit", "t2i-sync", "edit-sync"], 
                        help="Mode: t2i (text-to-image async), edit (image editing async), t2i-sync, edit-sync")
    parser.add_argument("prompt", nargs="?", default=None, help="Image description prompt")
    parser.add_argument("--image", action="append", help="Reference image path or URL (for edit mode)")
    parser.add_argument("--size", default="1280*1280", help="Image size (e.g., 1280*1280, 16:9)")
    parser.add_argument("--n", type=int, default=1, help="Number of images (1-4)")
    parser.add_argument("--seed", type=int, default=None, help="Random seed")
    parser.add_argument("--negative", default="", help="Negative prompt")
    parser.add_argument("--no-prompt-extend", action="store_true", help="Disable prompt extension")
    parser.add_argument("--watermark", action="store_true", help="Add AI watermark")
    parser.add_argument("--task-id", help="Task ID to check status")
    parser.add_argument("--poll", action="store_true", help="Poll task until completion")
    parser.add_argument("--output-dir", default=None, help="Output directory (default: <skill_dir>/output)")
    
    args = parser.parse_args()
    
    # Handle task polling
    if args.task_id:
        result = get_task_result(args.task_id)
        if "error" in result:
            print(json.dumps(result, ensure_ascii=False, indent=2))
            sys.exit(1)
        
        # Check status
        output = result.get("output", {})
        status = output.get("task_status", "UNKNOWN")
        
        if status == "SUCCEEDED":
            downloaded = download_images(result, args.output_dir)
            print(f"\n✅ Generation complete! {len(downloaded)} image(s) saved to {args.output_dir}/")
            for fp in downloaded:
                print(f"  📷 {fp}")
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"Task status: {status}")
            if status == "FAILED":
                print(f"Error: {output.get('code', '')} - {output.get('message', '')}")
            print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    
    # Resolve size
    size = resolve_size(args.size)
    
    # Create task
    mode = args.mode.replace("-sync", "")  # Strip -sync suffix
    prompt_extend = not args.no_prompt_extend
    
    print(f"🎨 Starting image generation...", file=sys.stderr)
    print(f"   Mode: {mode}", file=sys.stderr)
    print(f"   Prompt: {args.prompt[:80]}{'...' if len(args.prompt) > 80 else ''}", file=sys.stderr)
    print(f"   Size: {size}", file=sys.stderr)
    print(f"   Count: {args.n}", file=sys.stderr)
    
    result = create_image_async(
        mode=mode,
        prompt=args.prompt,
        images=args.image,
        negative_prompt=args.negative,
        size=size,
        n=args.n,
        seed=args.seed,
        prompt_extend=prompt_extend,
        watermark=args.watermark,
    )
    
    if "error" in result:
        print(f"❌ Error: {result['error']}")
        sys.exit(1)
    
    task_id = result.get("output", {}).get("task_id")
    if task_id:
        print(f"📋 Task ID: {task_id}")
        print(f"   Status: {result.get('output', {}).get('task_status', 'PENDING')}")
        print(f"   Poll with: --task-id {task_id} --poll")
    
    # If sync mode, poll immediately
    if "-sync" in args.mode and task_id:
        print(f"\n⏳ Waiting for generation to complete...", file=sys.stderr)
        poll_result = get_task_result(task_id)
        
        if "error" in poll_result:
            print(f"❌ {poll_result['error']}")
            sys.exit(1)
        
        output = poll_result.get("output", {})
        status = output.get("task_status", "UNKNOWN")
        
        if status == "SUCCEEDED":
            downloaded = download_images(poll_result, args.output_dir)
            print(f"\n✅ Generation complete! {len(downloaded)} image(s) saved to {args.output_dir}/")
            for fp in downloaded:
                print(f"  📷 {fp}")
        elif status == "FAILED":
            print(f"❌ Generation failed: {output.get('code', '')} - {output.get('message', '')}")
            sys.exit(1)
        
        print(json.dumps(poll_result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
