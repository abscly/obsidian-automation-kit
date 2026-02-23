"""
🚀 Obsidian Master Orchestrator

Run all automation scripts in sequence with a single command.

Usage:
  python master.py           # Full pipeline
  python master.py --quick   # Export + NLM upload only
  python master.py --weekly  # Weekly review generation
  python master.py --monthly # Monthly review generation
"""

import sys
import importlib
import traceback
import json
from datetime import datetime
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent
VAULT_DIR = SCRIPTS_DIR.parent
CONFIG_PATH = SCRIPTS_DIR / "config.json"


def load_config():
    """Load configuration from config.json"""
    if CONFIG_PATH.exists():
        return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    print("⚠️  config.json not found. Copy config.template.json to config.json and configure it.")
    return {}


def run_step(name: str, func, *args, **kwargs):
    """Run a step safely (continue even if errors occur)"""
    try:
        print(f"\n{'─'*50}")
        print(f"  ▶ {name}")
        result = func(*args, **kwargs)
        print(f"  ✅ {name} complete")
        return result
    except BaseException as e:
        print(f"  ⚠️ {name} error: {type(e).__name__}: {e}")
        return None


def run_full():
    """Full pipeline execution"""
    config = load_config()
    
    print("🚀 Obsidian Automation Kit — Full Pipeline")
    print("=" * 50)
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {}
    
    # 1. Weekly Review (Sunday only)
    if datetime.now().weekday() == 6:
        from auto_weekly import main as weekly_main
        results["weekly"] = run_step("Weekly Review", weekly_main)
    
    # 2. Monthly Review (first 3 days of month)
    if datetime.now().day <= 3:
        from auto_monthly import main as monthly_main
        results["monthly"] = run_step("Monthly Review", monthly_main)
    
    # 3. Daily Note generation
    try:
        from auto_daily import create_daily
        result = create_daily()
        if result["created"]:
            print(f"  ✅ {result['message']}")
        else:
            print(f"  📋 {result['message']}")
        results["daily"] = True
    except Exception as e:
        print(f"  ⏭️ Daily generation skipped: {e}")
    
    # 4. Timeline update
    try:
        from auto_timeline import main as timeline_main
        results["timeline"] = run_step("Timeline Update", timeline_main)
    except Exception as e:
        print(f"  ⏭️ Timeline skipped: {e}")
    
    # 5. Home.md update
    try:
        from update_home import main as home_main
        results["home"] = run_step("Home.md Update", home_main)
    except ImportError:
        print("  ⏭️ update_home.py not available")
    
    # 6. Knowledge organization
    try:
        from knowledge_organizer import main as knowledge_main
        results["knowledge"] = run_step("Knowledge Organization", knowledge_main)
    except ImportError:
        print("  ⏭️ knowledge_organizer.py not available")
    
    # 7. NotebookLM export (if configured)
    if config.get("auto_nlm_upload", False):
        try:
            from export_to_notebooklm import main as export_main
            results["export"] = run_step("NLM Export", export_main)
            
            from upload_to_notebooklm import main as upload_main
            results["upload"] = run_step("NLM Upload", upload_main)
        except ImportError:
            print("  ⏭️ NotebookLM dependencies not installed")
    
    # 8. Git backup (if configured)
    if config.get("auto_git_backup", True):
        try:
            from git_backup import main as git_main
            results["git"] = run_step("Git Backup", git_main)
        except Exception as e:
            print(f"  ⏭️ Git backup skipped: {e}")
    
    # 9. Discord notification (if configured)
    if config.get("auto_discord_notify", False) and config.get("discord_webhook_url"):
        try:
            from discord_notify import notify
            results["discord"] = run_step("Discord Notification", lambda: notify(results=results))
        except Exception as e:
            print(f"  ⏭️ Discord notification skipped: {e}")
    
    # 10. AI Reporter (if configured)
    if config.get("auto_ai_reporter", False) and config.get("gemini_api_key"):
        try:
            from ai_reporter import enrich_daily
            results["ai_report"] = run_step(f"AI Report ({config.get('gemini_model', 'gemini-2.0-flash')})", enrich_daily)
        except Exception as e:
            print(f"  ⏭️ AI Reporter skipped: {e}")
    
    # 11. Semantic Search index update
    try:
        from vault_search import build_index
        results["search_index"] = run_step("Search Index Update", build_index)
    except Exception as e:
        print(f"  ⏭️ Search index skipped: {e}")
    
    # Summary
    print(f"\n{'='*50}")
    print(f"✅ Pipeline complete ({datetime.now().strftime('%H:%M:%S')})")
    active = [k for k, v in results.items() if v is not None and v is not False]
    skipped = [k for k, v in results.items() if v is None or v is False]
    if active:
        print(f"  Executed: {', '.join(active)}")
    if skipped:
        print(f"  Skipped: {', '.join(skipped)}")


def run_quick():
    """Export + NLM upload only"""
    print("⚡ Quick Sync")
    try:
        from export_to_notebooklm import main as export_main
        run_step("NLM Export", export_main)
        from upload_to_notebooklm import main as upload_main
        run_step("NLM Upload", upload_main)
    except ImportError:
        print("  ⏭️ NotebookLM dependencies not installed")


def run_weekly():
    """Weekly review only"""
    from auto_weekly import main as weekly_main
    weekly_main()


def run_monthly():
    """Monthly review only"""
    from auto_monthly import main as monthly_main
    monthly_main()


def main():
    if "--quick" in sys.argv:
        run_quick()
    elif "--weekly" in sys.argv:
        run_weekly()
    elif "--monthly" in sys.argv:
        run_monthly()
    else:
        run_full()


if __name__ == "__main__":
    main()
