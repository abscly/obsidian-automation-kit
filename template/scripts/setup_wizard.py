#!/usr/bin/env python3
"""
OAK セットアップウィザード
===========================
対話形式でconfig.jsonを生成し、必要な依存関係をチェック。

使い方:
    python setup_wizard.py           # 対話形式でセットアップ
    python setup_wizard.py --check   # 環境チェックのみ
    python setup_wizard.py --reset   # config.jsonをリセット
"""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
CONFIG_PATH = SCRIPT_DIR / "config.json"

# デフォルト設定テンプレート
DEFAULT_CONFIG = {
    "vault_path": "",
    "gemini_api_key": "",
    "gemini_model": "gemini-2.0-flash",
    "discord_webhook_url": "",
    "x_api": {
        "api_key": "",
        "api_secret": "",
        "access_token": "",
        "access_secret": ""
    },
    "github": {
        "username": "",
        "repo": "obsidian-automation-kit",
        "pages_url": ""
    },
    "scheduler": {
        "enabled": False,
        "daily_note": {
            "time": "00:05",
            "enabled": True
        },
        "git_backup": {
            "interval_minutes": 60,
            "enabled": True
        },
        "weekly_review": {
            "day_of_week": "Sunday",
            "time": "23:30",
            "enabled": True
        },
        "monthly_review": {
            "day_of_month": 1,
            "time": "23:45",
            "enabled": True
        }
    },
    "features": {
        "daily_note": True,
        "weekly_review": True,
        "monthly_review": True,
        "git_backup": True,
        "vault_health": True,
        "ai_reporter": False,
        "discord_notify": False,
        "semantic_search": False,
        "tts_reporter": False,
        "bigquery_logging": False,
        "x_auto_post": False
    }
}


def check_environment():
    """環境チェック"""
    print("\n🔍 Environment Check\n")
    checks = []

    # Python version
    ver = sys.version_info
    ok = ver >= (3, 10)
    checks.append(("Python 3.10+", ok, f"{ver.major}.{ver.minor}.{ver.micro}"))

    # Git
    git_ok = shutil.which("git") is not None
    checks.append(("Git", git_ok, "installed" if git_ok else "NOT FOUND"))

    # pip packages
    packages = {
        "google-generativeai": "AI機能（日報/検索/コンテンツ生成）",
        "tweepy": "X (Twitter) 自動投稿",
        "markdown": "Markdown→HTML変換",
    }
    for pkg, desc in packages.items():
        try:
            __import__(pkg.replace("-", "_").split(".")[0] if "-" in pkg else pkg)
            checks.append((f"pip: {pkg}", True, desc))
        except ImportError:
            checks.append((f"pip: {pkg}", False, f"pip install {pkg}"))

    # 結果表示
    for name, ok, detail in checks:
        status = "✅" if ok else "❌"
        print(f"  {status} {name:<30} {detail}")

    all_ok = all(ok for _, ok, _ in checks)
    if not all_ok:
        print("\n  ⚠️  Some requirements are missing.")
        missing = [name for name, ok, _ in checks if not ok]
        print(f"  Missing: {', '.join(missing)}")
    else:
        print("\n  🎉 All checks passed!")

    return all_ok


def interactive_setup():
    """対話形式でconfig.jsonを生成"""
    print("\n🧙 OAK Setup Wizard\n")
    print("  対話形式でconfig.jsonを生成します。")
    print("  空のままEnterでスキップ（後から設定可能）\n")

    config = DEFAULT_CONFIG.copy()

    # Step 1: Vault
    print("─── Step 1/6: Obsidian Vault ───")
    vault = input("  Vault のパス (例: C:\\Users\\you\\Obsidian): ").strip()
    if vault:
        config["vault_path"] = vault

    # Step 2: Gemini API
    print("\n─── Step 2/6: Gemini API ───")
    print("  取得先: https://aistudio.google.com/apikey")
    api_key = input("  Gemini API Key (skippable): ").strip()
    if api_key:
        config["gemini_api_key"] = api_key
        config["features"]["ai_reporter"] = True

    # Step 3: Discord
    print("\n─── Step 3/6: Discord Webhook ───")
    print("  設定 → 連携サービス → ウェブフック → URL取得")
    webhook = input("  Discord Webhook URL (skippable): ").strip()
    if webhook:
        config["discord_webhook_url"] = webhook
        config["features"]["discord_notify"] = True

    # Step 4: X (Twitter) API
    print("\n─── Step 4/6: X (Twitter) API ───")
    print("  https://developer.twitter.com/ で取得")
    x_key = input("  X API Key (skippable): ").strip()
    if x_key:
        config["x_api"]["api_key"] = x_key
        config["x_api"]["api_secret"] = input("  X API Secret: ").strip()
        config["x_api"]["access_token"] = input("  X Access Token: ").strip()
        config["x_api"]["access_secret"] = input("  X Access Secret: ").strip()
        config["features"]["x_auto_post"] = True

    # Step 5: GitHub
    print("\n─── Step 5/6: GitHub ───")
    username = input("  GitHub Username (skippable): ").strip()
    if username:
        config["github"]["username"] = username
        config["github"]["pages_url"] = f"https://{username}.github.io/obsidian-automation-kit"

    # Step 6: Scheduler
    print("\n─── Step 6/6: 内蔵スケジューラー ───")
    print("  OSのタスクスケジューラを使わず、Pythonを常駐させて自動実行しますか？")
    use_scheduler = input("  スケジューラーを有効にする (y/N): ").strip().lower()
    if use_scheduler == 'y':
        config["scheduler"]["enabled"] = True
        
        # Git Backup Interval
        interval = input("  Gitバックアップの間隔（分、デフォルト: 60）: ").strip()
        if interval.isdigit():
            config["scheduler"]["git_backup"]["interval_minutes"] = int(interval)
            
        # Daily Note Time
        d_time = input("  Daily Noteの生成時刻（HH:MM、デフォルト: 00:05）: ").strip()
        if d_time:
            config["scheduler"]["daily_note"]["time"] = d_time

    # 保存
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

    # 有効化された機能の表示
    enabled = [k for k, v in config["features"].items() if v]
    disabled = [k for k, v in config["features"].items() if not v]

    print(f"\n{'='*50}")
    print(f"  ✅ config.json saved!")
    print(f"{'='*50}")
    print(f"\n  Enabled features ({len(enabled)}):")
    for f_name in enabled:
        print(f"    ✅ {f_name}")
    print(f"\n  Disabled features ({len(disabled)}):")
    for f_name in disabled:
        print(f"    ⬜ {f_name} (後から有効化可能)")
    print(f"\n  📁 Config: {CONFIG_PATH}")
    print(f"  📋 次: python master.py")


def verify_setup():
    """セットアップ検証"""
    print("\n🔍 Setup Verification\n")

    # config.json チェック
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            config = json.load(f)
        print(f"  ✅ config.json exists")

        vault = config.get("vault_path", "")
        if vault and Path(vault).exists():
            print(f"  ✅ Vault path valid: {vault}")
        elif vault:
            print(f"  ❌ Vault path not found: {vault}")
        else:
            print(f"  ⬜ Vault path not configured")

        if config.get("gemini_api_key"):
            print(f"  ✅ Gemini API key configured")
        else:
            print(f"  ⬜ Gemini API key not configured (AI features disabled)")

        if config.get("discord_webhook_url"):
            print(f"  ✅ Discord webhook configured")
        else:
            print(f"  ⬜ Discord webhook not configured")

        x_api = config.get("x_api", {})
        if x_api.get("api_key"):
            print(f"  ✅ X API configured")
        else:
            print(f"  ⬜ X API not configured (auto-posting disabled)")

    else:
        print(f"  ❌ config.json not found")
        print(f"  Run: python setup_wizard.py")

    # ディレクトリチェック
    dirs_to_check = [
        ("blog/articles", "ブログ記事"),
        ("tools", "無料ツール"),
        ("sns", "SNSスクリプト"),
        ("template", "テンプレート"),
        (".github/workflows", "GitHub Actions"),
    ]
    print(f"\n  Directory Structure:")
    for dir_path, desc in dirs_to_check:
        full_path = PROJECT_ROOT / dir_path
        if full_path.exists():
            count = len(list(full_path.iterdir()))
            print(f"    ✅ {dir_path}/ ({count} items) — {desc}")
        else:
            print(f"    ❌ {dir_path}/ — {desc}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description='OAK Setup Wizard')
    parser.add_argument('--check', action='store_true', help='Check environment only')
    parser.add_argument('--verify', action='store_true', help='Verify setup')
    parser.add_argument('--reset', action='store_true', help='Reset config.json')
    args = parser.parse_args()

    if args.check:
        check_environment()
    elif args.verify:
        check_environment()
        verify_setup()
    elif args.reset:
        if CONFIG_PATH.exists():
            CONFIG_PATH.unlink()
            print("✅ config.json deleted")
        interactive_setup()
    else:
        check_environment()
        interactive_setup()


if __name__ == '__main__':
    main()
