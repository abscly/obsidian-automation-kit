#!/usr/bin/env python3
"""
⏰ OAK Built-in Scheduler
========================
config.json の設定に基づいて自動化タスクをバックグラウンドで定期実行します。
OSのタスクスケジューラ（cron等）なしで運用可能です。

使い方:
    python scheduler.py
"""

import time
import json
import logging
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("OAK_Scheduler")

SCRIPT_DIR = Path(__file__).parent
CONFIG_PATH = SCRIPT_DIR / "config.json"
MASTER_SCRIPT = SCRIPT_DIR / "master.py"

# State tracking to avoid duplicate runs
state = {
    "last_git_backup": datetime.min,
    "last_daily_note_date": None,
    "last_weekly_review_date": None,
    "last_monthly_review_date": None,
    "last_config_mtime": 0
}

current_config = {}

def load_config():
    """Reload config.json if modified (Hot Reload)"""
    global current_config
    if not CONFIG_PATH.exists():
        return False
    
    mtime = CONFIG_PATH.stat().st_mtime
    if mtime > state["last_config_mtime"]:
        try:
            with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
                current_config = json.load(f)
            state["last_config_mtime"] = mtime
            logger.info("🔧 Config reloaded.")
            return True
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
    return True

def run_script(args, name):
    """Execute a python script as a subprocess"""
    logger.info(f"🚀 Starting task: {name}")
    try:
        cmd = [str(Path(sys.executable)), str(MASTER_SCRIPT)] + args
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        logger.info(f"✅ Task complete: {name}")
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Task failed: {name}\n{e.stderr}")
    except Exception as e:
        logger.error(f"❌ Execution error: {e}")

def check_schedule():
    """Evaluate current time against config schedule"""
    now = datetime.now()
    today_str = now.strftime('%Y-%m-%d')
    current_time_str = now.strftime('%H:%M')
    current_day_of_week = now.strftime('%A')
    current_day_of_month = now.day

    sched = current_config.get("scheduler", {})
    if not sched.get("enabled", False):
        return

    # 1. Daily Note
    dn_conf = sched.get("daily_note", {})
    if dn_conf.get("enabled", False):
        if current_time_str == dn_conf.get("time", "00:05"):
            if state["last_daily_note_date"] != today_str:
                state["last_daily_note_date"] = today_str
                import sys
                cmd = [sys.executable, str(SCRIPT_DIR / "auto_daily.py")]
                subprocess.run(cmd, capture_output=True)
                logger.info("✅ Daily Note task executed")

    # 2. Git Backup
    git_conf = sched.get("git_backup", {})
    if git_conf.get("enabled", False):
        interval_min = git_conf.get("interval_minutes", 60)
        if now - state["last_git_backup"] >= timedelta(minutes=interval_min):
            state["last_git_backup"] = now
            import sys
            cmd = [sys.executable, str(SCRIPT_DIR / "git_backup.py")]
            subprocess.run(cmd, capture_output=True)
            logger.info("✅ Git Backup task executed")

    # 3. Weekly Review
    wk_conf = sched.get("weekly_review", {})
    if wk_conf.get("enabled", False):
        if current_day_of_week == wk_conf.get("day_of_week", "Sunday") and current_time_str == wk_conf.get("time", "23:30"):
            if state["last_weekly_review_date"] != today_str:
                state["last_weekly_review_date"] = today_str
                import sys
                cmd = [sys.executable, str(SCRIPT_DIR / "auto_weekly.py")]
                subprocess.run(cmd, capture_output=True)
                logger.info("✅ Weekly Review task executed")

    # 4. Monthly Review
    mo_conf = sched.get("monthly_review", {})
    if mo_conf.get("enabled", False):
        if current_day_of_month == mo_conf.get("day_of_month", 1) and current_time_str == mo_conf.get("time", "23:45"):
            if state["last_monthly_review_date"] != today_str:
                state["last_monthly_review_date"] = today_str
                import sys
                cmd = [sys.executable, str(SCRIPT_DIR / "auto_monthly.py")]
                subprocess.run(cmd, capture_output=True)
                logger.info("✅ Monthly Review task executed")


def main():
    print("==================================================")
    print("  ⏰ OAK Built-in Scheduler is starting...")
    print("  Leave this terminal open to keep it running.")
    print("  Press Ctrl+C to stop.")
    print("==================================================\n")
    
    if not load_config():
        logger.warning("config.json not found. Waiting for it to be created...")

    try:
        import sys
        while True:
            load_config()
            
            if current_config.get("scheduler", {}).get("enabled", False):
                check_schedule()
            
            # Sleep for a bit before checking again (aligns with minute boundaries reasonably well)
            time.sleep(30)
            
    except KeyboardInterrupt:
        print("\n⏹️ Scheduler stopped by user.")


if __name__ == "__main__":
    main()
