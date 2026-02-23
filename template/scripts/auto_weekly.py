"""
📊 Weekly Review Auto-Generator

Automatically generates a weekly review from Daily Notes.

Usage:
  python auto_weekly.py
"""

from datetime import datetime, timedelta
from pathlib import Path

VAULT_DIR = Path(__file__).parent.parent
DAILY_DIR = VAULT_DIR / "Daily"
WEEKLY_DIR = VAULT_DIR / "Weekly"
TEMPLATE_PATH = VAULT_DIR / "Templates" / "Weekly テンプレート.md"


def get_week_range(date=None):
    """Get the start (Monday) and end (Sunday) of the week"""
    if date is None:
        date = datetime.now()
    start = date - timedelta(days=date.weekday())
    end = start + timedelta(days=6)
    return start, end


def collect_daily_highlights(start_date, end_date):
    """Collect highlights from Daily Notes in the date range"""
    highlights = []
    current = start_date
    while current <= end_date:
        daily_path = DAILY_DIR / f"{current.strftime('%Y-%m-%d')}.md"
        if daily_path.exists():
            content = daily_path.read_text(encoding="utf-8")
            # Extract tasks and highlights
            lines = content.split("\n")
            for line in lines:
                stripped = line.strip()
                if stripped.startswith("- [x]"):
                    highlights.append(f"✅ {stripped[5:].strip()} ({current.strftime('%m/%d')})")
                elif stripped.startswith("- [/]"):
                    highlights.append(f"🔄 {stripped[5:].strip()} ({current.strftime('%m/%d')})")
        current += timedelta(days=1)
    return highlights


def generate_weekly(date=None):
    """Generate a weekly review"""
    if date is None:
        date = datetime.now()
    
    start, end = get_week_range(date)
    week_num = start.isocalendar()[1]
    
    filename = f"Week {week_num} ({start.strftime('%Y-%m-%d')}).md"
    weekly_path = WEEKLY_DIR / filename
    
    if weekly_path.exists():
        return {"created": False, "message": f"{filename} already exists"}
    
    WEEKLY_DIR.mkdir(parents=True, exist_ok=True)
    
    # Collect data
    highlights = collect_daily_highlights(start, end)
    daily_count = sum(1 for d in range(7) if (DAILY_DIR / f"{(start + timedelta(days=d)).strftime('%Y-%m-%d')}.md").exists())
    
    highlight_text = "\n".join(f"- {h}" for h in highlights) if highlights else "- (記録なし)"
    
    content = f"""---
tags:
  - type/週次
created: {datetime.now().strftime('%Y-%m-%d')}
week: {week_num}
---

# Week {week_num} ({start.strftime('%Y-%m-%d')} 〜 {end.strftime('%Y-%m-%d')}) 週次レビュー

> 📊 期間: {start.strftime('%m/%d')} ({['月','火','水','木','金','土','日'][start.weekday()]}) — {end.strftime('%m/%d')} ({['月','火','水','木','金','土','日'][end.weekday()]})

---

## 📋 今週のハイライト

{highlight_text}

## 📊 統計

| 指標 | 値 |
|:---|:---|
| 作業日数 | {daily_count}/7 |
| 完了タスク | {len([h for h in highlights if h.startswith('✅')])} |
| 進行中タスク | {len([h for h in highlights if h.startswith('🔄')])} |

## 💡 学び・振り返り

- 

## ➡️ 来週の予定

- [ ] 
"""
    
    weekly_path.write_text(content, encoding="utf-8")
    return {"created": True, "message": f"Created {filename}"}


def main():
    result = generate_weekly()
    if result["created"]:
        print(f"✅ {result['message']}")
    else:
        print(f"📋 {result['message']}")
    return result


if __name__ == "__main__":
    main()
