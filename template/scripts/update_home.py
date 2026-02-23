"""
🏠 Home.md Auto-Updater

Automatically updates the Home.md dashboard with current vault statistics,
project list, and recent activity.

Usage:
  python update_home.py
"""

import re
from datetime import datetime
from pathlib import Path

VAULT_DIR = Path(__file__).parent.parent
HOME_PATH = VAULT_DIR / "Home.md"
DAILY_DIR = VAULT_DIR / "Daily"
PROJECTS_DIR = VAULT_DIR / "Projects"
IGNORE_DIRS = {".git", ".obsidian", "node_modules", "__pycache__", "scripts", ".github", "exports"}


def get_vault_stats():
    """Get vault statistics"""
    note_count = 0
    total_size = 0
    for md in VAULT_DIR.rglob("*.md"):
        if any(part in IGNORE_DIRS for part in md.parts):
            continue
        note_count += 1
        total_size += md.stat().st_size
    return note_count, total_size


def get_recent_dailies(count=5):
    """Get recent daily notes"""
    if not DAILY_DIR.exists():
        return []
    dailies = sorted(DAILY_DIR.glob("*.md"), reverse=True)[:count]
    results = []
    for d in dailies:
        content = d.read_text(encoding="utf-8", errors="ignore")
        # Extract first meaningful content line
        lines = [l.strip() for l in content.split("\n") 
                 if l.strip() and not l.startswith("#") and not l.startswith("---") 
                 and not l.startswith(">") and not l.startswith("tags:") 
                 and "type/" not in l and "created:" not in l]
        summary = lines[0][:60] if lines else "—"
        results.append({"date": d.stem, "summary": summary})
    return results


def get_projects():
    """Get list of projects from Projects directory"""
    if not PROJECTS_DIR.exists():
        return []
    projects = []
    for proj_dir in sorted(PROJECTS_DIR.iterdir()):
        if proj_dir.is_dir():
            main_file = proj_dir / f"{proj_dir.name}.md"
            status = "🟡 Unknown"
            if main_file.exists():
                content = main_file.read_text(encoding="utf-8", errors="ignore")
                if "#status/active" in content:
                    status = "🟢 Active"
                elif "#status/completed" in content:
                    status = "✅ Done"
                elif "#status/paused" in content:
                    status = "⏸️ Paused"
            projects.append({"name": proj_dir.name, "status": status})
    return projects


def update_home():
    """Update Home.md with current data"""
    if not HOME_PATH.exists():
        print("  ⚠️ Home.md not found")
        return False
    
    content = HOME_PATH.read_text(encoding="utf-8")
    note_count, total_size = get_vault_stats()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    size_kb = total_size // 1024
    
    # Update stats line
    content = re.sub(
        r'> 📊 更新:.*',
        f'> 📊 更新: {now} | ノート数: {note_count} | サイズ: {size_kb} KB',
        content
    )
    
    # Update recent activity
    dailies = get_recent_dailies(5)
    if dailies:
        activity_lines = []
        for d in dailies:
            activity_lines.append(f"| [[{d['date']}]] | {d['summary']} |")
        
        activity_table = "| 日付 | 内容 |\n|:---|:---|\n" + "\n".join(activity_lines)
        content = re.sub(
            r'\| 日付 \| 内容 \|.*?(?=\n---|\n##)',
            activity_table + "\n",
            content,
            flags=re.DOTALL
        )
    
    HOME_PATH.write_text(content, encoding="utf-8")
    print(f"  ✅ Home.md updated (notes: {note_count}, size: {size_kb}KB)")
    return True


def main():
    return update_home()


if __name__ == "__main__":
    main()
