"""
📅 Daily Note Auto-Generator

Automatically creates today's Daily Note from template if it doesn't exist.

Usage:
  python auto_daily.py
"""

from datetime import datetime
from pathlib import Path

VAULT_DIR = Path(__file__).parent.parent
DAILY_DIR = VAULT_DIR / "Daily"
TEMPLATE_PATH = VAULT_DIR / "Templates" / "Daily テンプレート.md"


def create_daily(date=None):
    """Create today's Daily Note if it doesn't exist"""
    if date is None:
        date = datetime.now()
    
    date_str = date.strftime("%Y-%m-%d")
    daily_path = DAILY_DIR / f"{date_str}.md"
    
    if daily_path.exists():
        return {"created": False, "message": f"{date_str}.md already exists", "path": str(daily_path)}
    
    # Ensure Daily directory exists
    DAILY_DIR.mkdir(parents=True, exist_ok=True)
    
    # Load template or use default
    if TEMPLATE_PATH.exists():
        content = TEMPLATE_PATH.read_text(encoding="utf-8")
        # Replace template variables
        content = content.replace("{{date:YYYY-MM-DD}}", date_str)
        content = content.replace("{{date}}", date_str)
    else:
        weekday_names = ["月", "火", "水", "木", "金", "土", "日"]
        weekday = weekday_names[date.weekday()]
        content = f"""---
tags:
  - type/日報
created: {date_str}
---

# {date_str} ({weekday}) 作業ログ

> 📊 作業時間: `未記録` | 関連プロジェクト: 

---

## 📋 今日のタスク

- [ ] 

## 🔨 作業内容

### 🏗️ プロジェクト: 

**やったこと:**
- 

**変更ファイル:**
- 

### 🐛 問題と解決

| 問題 | 原因 | 解決方法 |
|:---|:---|:---|
|  |  |  |

## 💡 気づき・アイデア

- 

## ➡️ 次回やること

- [ ] 
"""
    
    daily_path.write_text(content, encoding="utf-8")
    return {"created": True, "message": f"Created {date_str}.md", "path": str(daily_path)}


def main():
    result = create_daily()
    if result["created"]:
        print(f"✅ {result['message']}")
    else:
        print(f"📋 {result['message']}")
    return result


if __name__ == "__main__":
    main()
