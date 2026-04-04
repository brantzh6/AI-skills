#!/usr/bin/env python3
"""
Creative Studio Research - Source Monitor & Updater

Monitors key resources for new prompt techniques and updates the knowledge base.

Usage:
  python research_update.py check     # Check all sources for updates
  python research_update.py research  # Full research cycle
  python research_update.py add --category portrait "prompt text"  # Add new prompt
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

# Configuration
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
STATE_FILE = os.path.join(SKILL_DIR, "research-state.json")
UPDATE_LOG = os.path.join(SKILL_DIR, "docs", "update-log.md")

# Sources to monitor
SOURCES = [
    {
        "name": "阿里云万相文生图 API",
        "url": "https://help.aliyun.com/zh/model-studio/text-to-image-v2-api-reference",
        "type": "official_doc",
        "check_interval_days": 7,
    },
    {
        "name": "阿里云万相文生视频 API",
        "url": "https://help.aliyun.com/zh/model-studio/text-to-video-api-reference",
        "type": "official_doc",
        "check_interval_days": 7,
    },
    {
        "name": "阿里云万相参考生视频 API",
        "url": "https://help.aliyun.com/zh/model-studio/wan-video-to-video-api-reference",
        "type": "official_doc",
        "check_interval_days": 7,
    },
    {
        "name": "Apatero Prompt Guide",
        "url": "https://apatero.com/blog/ai-image-prompts-engineering-guide-2026",
        "type": "tutorial",
        "check_interval_days": 14,
    },
    {
        "name": "Runway Prompt Guide",
        "url": "https://runwayml.com/resources/ai-video-prompting-guide",
        "type": "official_guide",
        "check_interval_days": 14,
    },
    {
        "name": "Awesome AI Video Prompts",
        "url": "https://github.com/geekjourneyx/awesome-ai-video-prompts",
        "type": "github_repo",
        "check_interval_days": 14,
    },
    {
        "name": "阿里云 Wan 2.6 Guide",
        "url": "https://apatero.com/blog/wan-2-6-complete-guide-multi-shot-video-generation-2025",
        "type": "tutorial",
        "check_interval_days": 14,
    },
]


def load_state():
    """Load research state."""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"sources": {}, "prompts_added": 0, "scenes_added": 0, "last_full_research": None}


def save_state(state):
    """Save research state."""
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def fetch_url(url):
    """Fetch URL content."""
    try:
        import requests
        response = requests.get(url, timeout=30, headers={
            "User-Agent": "Mozilla/5.0 Creative-Studio-Research/1.0"
        })
        return response.status_code == 200, response.text
    except Exception as e:
        return False, str(e)


def check_sources():
    """Check all sources for updates."""
    state = load_state()
    now = datetime.now()
    updates = []

    for source in SOURCES:
        name = source["name"]
        url = source["url"]
        interval = source["check_interval_days"]

        last_check = state["sources"].get(name, {}).get("last_check")
        if last_check:
            last_date = datetime.fromisoformat(last_check)
            days_since = (now - last_date).days
            if days_since < interval:
                print(f"⏭️  {name}: Last checked {days_since}d ago (interval: {interval}d)")
                continue

        print(f"🔍 Checking: {name}...")
        success, content = fetch_url(url)

        if success:
            # Simple hash-based change detection
            import hashlib
            content_hash = hashlib.md5(content[:10000].encode()).hexdigest()
            prev_hash = state["sources"].get(name, {}).get("content_hash", "")

            if content_hash != prev_hash:
                updates.append({
                    "source": name,
                    "url": url,
                    "status": "UPDATED",
                    "checked_at": now.isoformat(),
                })
                print(f"  📝 {name}: Content changed!")
                state["sources"][name] = {
                    "last_check": now.isoformat(),
                    "content_hash": content_hash,
                    "last_updated": now.isoformat(),
                }
            else:
                print(f"  ✅ {name}: No changes")
                state["sources"][name] = {
                    "last_check": now.isoformat(),
                    "content_hash": content_hash,
                }
        else:
            print(f"  ❌ {name}: Fetch failed - {content}")
            state["sources"][name] = {
                "last_check": now.isoformat(),
                "error": content,
            }

    save_state(state)

    if updates:
        print(f"\n📊 Summary: {len(updates)} source(s) updated")
        for u in updates:
            print(f"  - {u['source']}: {u['status']}")
    else:
        print("\n✅ All sources up to date")

    return updates


def add_prompt(category, prompt_text, model="wan2.6-t2i", rating=4, notes=""):
    """Add a new prompt to the library."""
    prompt_file = os.path.join(SKILL_DIR, "prompts", f"{category}.md")

    if not os.path.exists(prompt_file):
        # Create new prompt file
        with open(prompt_file, "w", encoding="utf-8") as f:
            f.write(f"# {category.title()} Prompt Library\n\n> Auto-generated\n\n")

    # Read existing content
    with open(prompt_file, "r", encoding="utf-8") as f:
        existing = f.read()

    # Count existing prompts
    count = existing.count("### ") + 1

    # Generate entry
    stars = "⭐" * rating
    entry = f"""
### {count}. New Prompt ({stars})

```
{prompt_text}
```

**参数：** `--n 1`
**模型：** {model}
**备注：** {notes}

"""

    # Append to file
    with open(prompt_file, "a", encoding="utf-8") as f:
        f.write(entry)

    # Update state
    state = load_state()
    state["prompts_added"] = state.get("prompts_added", 0) + 1
    save_state(state)

    print(f"✅ Prompt added to prompts/{category}.md (#{count})")
    return count


def generate_report():
    """Generate research summary report."""
    state = load_state()

    # Count files
    prompts_dir = os.path.join(SKILL_DIR, "prompts")
    scenes_dir = os.path.join(SKILL_DIR, "scenes")

    prompt_files = list(Path(prompts_dir).glob("*.md")) if os.path.exists(prompts_dir) else []
    scene_files = list(Path(scenes_dir).glob("*.md")) if os.path.exists(scenes_dir) else []

    report = f"""
# Creative Studio Research Report

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}

## Knowledge Base Status

| Category | Files | Total Items |
|----------|-------|-------------|
| Prompt Libraries | {len(prompt_files)} | {state.get('prompts_added', 0)} |
| Scene Libraries | {len(scene_files)} | {state.get('scenes_added', 0)} |

## Source Monitoring

| Source | Last Checked | Status |
|--------|-------------|--------|
"""

    for source in SOURCES:
        name = source["name"]
        info = state.get("sources", {}).get(name, {})
        last = info.get("last_check", "Never")
        if last and last != "Never":
            last = last[:10]
        status = "⚠️ Error" if "error" in info else "✅ OK"
        report += f"| {name} | {last} | {status} |\n"

    report += f"""
## Next Scheduled Check

Sources are checked every {min(s['check_interval_days'] for s in SOURCES)}-{max(s['check_interval_days'] for s in SOURCES)} days.

## Actions Needed

"""

    # Check which sources need attention
    now = datetime.now()
    for source in SOURCES:
        name = source["name"]
        info = state.get("sources", {}).get(name, {})
        last = info.get("last_check")
        if not last:
            report += f"- [ ] Initial check: {name}\n"
        else:
            days = (now - datetime.fromisoformat(last)).days
            if days >= source["check_interval_days"]:
                report += f"- [ ] Overdue check ({days}d): {name}\n"

    return report


def main():
    parser = argparse.ArgumentParser(description="Creative Studio Research Update")
    parser.add_argument("action", choices=["check", "report", "add"], help="Action to perform")
    parser.add_argument("--category", default=None, help="Prompt category (for add)")
    parser.add_argument("--prompt", default=None, help="Prompt text (for add)")
    parser.add_argument("--model", default="wan2.6-t2i", help="Model name (for add)")
    parser.add_argument("--rating", type=int, default=4, help="Rating 1-5 (for add)")
    parser.add_argument("--notes", default="", help="Notes (for add)")

    args = parser.parse_args()

    if args.action == "check":
        check_sources()
    elif args.action == "report":
        print(generate_report())
    elif args.action == "add":
        if not args.category or not args.prompt:
            print("❌ --category and --prompt required for add action")
            return
        add_prompt(args.category, args.prompt, args.model, args.rating, args.notes)


if __name__ == "__main__":
    main()
