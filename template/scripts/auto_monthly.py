"""
📊 Monthly Review Auto-Generator

Automatically generates a monthly review from Daily and Weekly Notes.

Usage:
  python auto_monthly.py
"""

from datetime import datetime, timedelta
from pathlib import Path
import calendar

VAULT_DIR = Path(__file__).parent.parent
DAILY_DIR = VAULT_DIR / "Daily"
WEEKLY_DIR = VAULT_DIR / "Weekly"
MONTHLY_DIR = VAULT_DIR / "Monthly"


def generate_monthly(date=None):
    """Generate a monthly review"""
    if date is None:
        date = datetime.now()
    
    # Review previous month
    if date.month == 1:
        target_year, target_month = date.year - 1, 12
    else:
        target_year, target_month = date.year, date.month - 1
    
    month_str = f"{target_year}-{target_month:02d}"
    filename = f"{month_str}.md"
    monthly_path = MONTHLY_DIR / filename
    
    if monthly_path.exists():
        return {"created": False, "message": f"{filename} already exists"}
    
    MONTHLY_DIR.mkdir(parents=True, exist_ok=True)
    
    # Count daily notes in the month
    days_in_month = calendar.monthrange(target_year, target_month)[1]
    daily_count = 0
    completed_tasks = 0
    
    for day in range(1, days_in_month + 1):
        daily_path = DAILY_DIR / f"{target_year}-{target_month:02d}-{day:02d}.md"
        if daily_path.exists():
            daily_count += 1
            content = daily_path.read_text(encoding="utf-8")
            completed_tasks += content.count("- [x]")
    
    # Count weekly reviews
    weekly_count = len(list(WEEKLY_DIR.glob(f"Week * ({target_year}-{target_month:02d}*).md"))) if WEEKLY_DIR.exists() else 0
    
    month_names_jp = ["", "1月", "2月", "3月", "4月", "5月", "6月", 
                      "7月", "8月", "9月", "10月", "11月", "12月"]
    
    content = f"""---
tags:
  - type/月次
created: {datetime.now().strftime('%Y-%m-%d')}
month: {month_str}
---

# {target_year}年 {month_names_jp[target_month]} 月次レビュー

> 📊 期間: {month_str}-01 〜 {month_str}-{days_in_month}

---

## 📊 統計

| 指標 | 値 |
|:---|:---|
| 作業日数 | {daily_count}/{days_in_month} |
| 完了タスク | {completed_tasks} |
| 週次レビュー | {weekly_count} |

## 📋 今月のハイライト

- 

## 🏆 成果

- 

## 📈 成長・学び

- 

## ⚠️ 課題・反省

- 

## ➡️ 来月の目標

- [ ] 
"""
    
    monthly_path.write_text(content, encoding="utf-8")
    return {"created": True, "message": f"Created {filename}"}


def main():
    result = generate_monthly()
    if result["created"]:
        print(f"✅ {result['message']}")
    else:
        print(f"📋 {result['message']}")
    return result


if __name__ == "__main__":
    main()
