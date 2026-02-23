"""
🔔 Discord Webhook Notification

Sends pipeline results to a Discord channel via webhook.

Usage:
  python discord_notify.py
"""

import json
from datetime import datetime
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent
CONFIG_PATH = SCRIPTS_DIR / "config.json"


def load_config():
    if CONFIG_PATH.exists():
        return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    return {}


def notify(message=None, results=None):
    """Send a notification to Discord webhook"""
    import requests
    
    config = load_config()
    webhook_url = config.get("discord_webhook_url", "")
    
    if not webhook_url:
        print("  ⚠️ Discord webhook URL not configured")
        return False
    
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    if results:
        # Build pipeline result embed
        active = [k for k, v in results.items() if v is not None and v is not False]
        skipped = [k for k, v in results.items() if v is None or v is False]
        
        fields = []
        if active:
            fields.append({
                "name": "✅ Executed",
                "value": ", ".join(active),
                "inline": False
            })
        if skipped:
            fields.append({
                "name": "⏭️ Skipped",
                "value": ", ".join(skipped),
                "inline": False
            })
        
        embed = {
            "title": "🚀 Obsidian Pipeline Complete",
            "description": f"Automated pipeline finished at {now}",
            "color": 0x00d4aa,  # Teal
            "fields": fields,
            "footer": {"text": "Obsidian Automation Kit"},
            "timestamp": datetime.utcnow().isoformat()
        }
        
        payload = {"embeds": [embed]}
    else:
        payload = {
            "embeds": [{
                "title": "📝 Obsidian Update",
                "description": message or "Vault updated",
                "color": 0x7c3aed,
                "timestamp": datetime.utcnow().isoformat()
            }]
        }
    
    try:
        response = requests.post(webhook_url, json=payload, timeout=10)
        if response.status_code in (200, 204):
            print("  ✅ Discord notification sent")
            return True
        else:
            print(f"  ⚠️ Discord webhook error: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ⚠️ Discord notification failed: {e}")
        return False


def main():
    notify(message="Manual test notification")


if __name__ == "__main__":
    main()
