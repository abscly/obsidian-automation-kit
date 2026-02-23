"""
📊 Project Timeline Auto-Updater

Automatically generates a Mermaid Gantt chart timeline
from project creation dates and activity.

Usage:
  python auto_timeline.py
"""

import re
from datetime import datetime
from pathlib import Path

VAULT_DIR = Path(__file__).parent.parent
PROJECTS_DIR = VAULT_DIR / "Projects"
TIMELINE_PATH = VAULT_DIR / "プロジェクトタイムライン.md"


def get_project_dates():
    """Extract project names and dates"""
    projects = []
    
    if not PROJECTS_DIR.exists():
        return projects
    
    for proj_dir in sorted(PROJECTS_DIR.iterdir()):
        if not proj_dir.is_dir():
            continue
        
        main_file = proj_dir / f"{proj_dir.name}.md"
        if not main_file.exists():
            continue
        
        content = main_file.read_text(encoding="utf-8", errors="ignore")
        
        # Extract created date
        match = re.search(r'created:\s*(\d{4}-\d{2}-\d{2})', content)
        created = match.group(1) if match else None
        
        # Determine status
        status = "active"
        if "#status/completed" in content:
            status = "done"
        elif "#status/paused" in content:
            status = "paused"
        
        # Get last modified
        log_file = proj_dir / f"{proj_dir.name} ログ.md"
        last_modified = None
        if log_file.exists():
            dates = re.findall(r'(\d{4}-\d{2}-\d{2})', log_file.read_text(encoding="utf-8", errors="ignore"))
            if dates:
                last_modified = max(dates)
        
        if not last_modified:
            last_modified = datetime.now().strftime("%Y-%m-%d")
        
        projects.append({
            "name": proj_dir.name,
            "created": created or "2025-01-01",
            "last_modified": last_modified,
            "status": status
        })
    
    return projects


def generate_timeline():
    """Generate Mermaid Gantt chart"""
    projects = get_project_dates()
    
    if not projects:
        print("  ⚠️ No projects found")
        return False
    
    # Build Mermaid chart
    mermaid_lines = [
        "```mermaid",
        "gantt",
        "    title Project Timeline",
        "    dateFormat YYYY-MM-DD",
        "    axisFormat %Y-%m",
        ""
    ]
    
    # Group by status
    for status_label, status_key in [("Active", "active"), ("Completed", "done"), ("Paused", "paused")]:
        group_projects = [p for p in projects if p["status"] == status_key]
        if group_projects:
            mermaid_lines.append(f"    section {status_label}")
            for p in group_projects:
                status_suffix = "" if status_key == "active" else f", {status_key}"
                mermaid_lines.append(f"    {p['name']}    :{status_suffix} {p['created']}, {p['last_modified']}")
    
    mermaid_lines.append("```")
    
    content = f"""---
tags:
  - type/可視化
updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
---

# 📊 プロジェクトタイムライン

> 自動生成: {datetime.now().strftime('%Y-%m-%d %H:%M')} | プロジェクト数: {len(projects)}

{chr(10).join(mermaid_lines)}

## 📋 プロジェクト一覧

| プロジェクト | 開始日 | 最終更新 | 状態 |
|:---|:---|:---|:---|
""" + "\n".join(f"| {p['name']} | {p['created']} | {p['last_modified']} | {p['status']} |" for p in projects)
    
    TIMELINE_PATH.write_text(content, encoding="utf-8")
    print(f"  ✅ Timeline updated ({len(projects)} projects)")
    return True


def main():
    return generate_timeline()


if __name__ == "__main__":
    main()
