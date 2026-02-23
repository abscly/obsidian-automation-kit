#!/usr/bin/env python3
"""
OAK Launch Day 自動チェック
============================
ローンチ日に必要な全ステップを自動チェック。
省略可能なものと必須のものを区別。

使い方:
    python launch_checklist.py              # チェックリスト表示
    python launch_checklist.py --auto       # 自動チェック
"""

import json
import shutil
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent


def check_item(name, check_fn, required=True):
    """チェック項目を実行"""
    try:
        result = check_fn()
        status = "✅" if result else ("❌" if required else "⬜")
        return {"name": name, "status": status, "ok": result, "required": required}
    except Exception as e:
        status = "❌" if required else "⬜"
        return {"name": name, "status": status, "ok": False, "required": required, "error": str(e)}


def auto_check():
    """自動ランチチェック"""
    print("\n🚀 OAK Launch Day Checklist\n")

    results = []

    # === 必須チェック ===
    results.append(check_item(
        "README.md exists",
        lambda: (PROJECT_ROOT / "README.md").exists()
    ))
    results.append(check_item(
        "LICENSE exists",
        lambda: (PROJECT_ROOT / "LICENSE").exists()
    ))
    results.append(check_item(
        ".gitignore exists",
        lambda: (PROJECT_ROOT / ".gitignore").exists()
    ))
    results.append(check_item(
        "index.html exists",
        lambda: (PROJECT_ROOT / "index.html").exists()
    ))
    results.append(check_item(
        "sitemap.xml exists",
        lambda: (PROJECT_ROOT / "sitemap.xml").exists()
    ))
    results.append(check_item(
        "Blog articles (≥5)",
        lambda: len(list((PROJECT_ROOT / "blog" / "articles").glob("*.html"))) >= 5
    ))
    results.append(check_item(
        "Landing page exists",
        lambda: (PROJECT_ROOT / "landing-page" / "index.html").exists()
    ))
    results.append(check_item(
        "Portfolio exists",
        lambda: (PROJECT_ROOT / "portfolio" / "index.html").exists()
    ))
    results.append(check_item(
        "Free tools (≥3)",
        lambda: len(list((PROJECT_ROOT / "tools").glob("*.html"))) >= 3
    ))
    results.append(check_item(
        "GitHub Actions (≥2)",
        lambda: len(list((PROJECT_ROOT / ".github" / "workflows").glob("*.yml"))) >= 2
    ))
    results.append(check_item(
        "SNS scripts (≥8)",
        lambda: len(list((PROJECT_ROOT / "sns").glob("*.py"))) >= 8
    ))

    # === オプショナルチェック ===
    results.append(check_item(
        "config.json configured",
        lambda: (PROJECT_ROOT / "sns" / "config.json").exists(),
        required=False
    ))
    results.append(check_item(
        "X post queue ready",
        lambda: (PROJECT_ROOT / "content" / "x_post_queue.json").exists(),
        required=False
    ))
    results.append(check_item(
        "Zenn articles (≥5)",
        lambda: len(list((PROJECT_ROOT / "zenn" / "articles").glob("*.md"))) >= 5,
        required=False
    ))
    results.append(check_item(
        "Git initialized",
        lambda: shutil.which("git") is not None,
        required=False
    ))

    # 結果表示
    print("  Required:")
    for r in results:
        if r["required"]:
            print(f"    {r['status']} {r['name']}")

    print("\n  Optional:")
    for r in results:
        if not r["required"]:
            print(f"    {r['status']} {r['name']}")

    # サマリー
    required_ok = sum(1 for r in results if r["required"] and r["ok"])
    required_total = sum(1 for r in results if r["required"])
    optional_ok = sum(1 for r in results if not r["required"] and r["ok"])
    optional_total = sum(1 for r in results if not r["required"])

    print(f"\n  Required: {required_ok}/{required_total}")
    print(f"  Optional: {optional_ok}/{optional_total}")

    if required_ok == required_total:
        print(f"\n  🎉 Ready to launch!")
    else:
        failed = [r["name"] for r in results if r["required"] and not r["ok"]]
        print(f"\n  ⚠️ Fix these before launch: {', '.join(failed)}")


def show_manual_checklist():
    """手動チェックリスト表示"""
    print("\n📋 Manual Launch Checklist\n")
    checklist = [
        ("GitHub", [
            "[ ] リポジトリ作成 (Public)",
            "[ ] Secrets設定 (GEMINI_API_KEY, X_API_*)",
            "[ ] GitHub Pages 有効化",
            "[ ] About セクション更新",
        ]),
        ("Gumroad/BOOTH", [
            "[ ] Free版アップロード",
            "[ ] Pro版アップロード",
            "[ ] 商品説明設定",
            "[ ] 価格設定",
        ]),
        ("SNS", [
            "[ ] X プロフィール更新",
            "[ ] 固定ツイート設定",
            "[ ] 最初の投稿",
            "[ ] Zenn記事公開 (5本)",
        ]),
        ("モニタリング", [
            "[ ] Google Analytics設定",
            "[ ] UptimeRobot設定",
            "[ ] GitHub Star数チェック",
        ]),
    ]

    for category, items in checklist:
        print(f"  📂 {category}")
        for item in items:
            print(f"    {item}")
        print()


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Launch Checklist')
    parser.add_argument('--auto', action='store_true')
    args = parser.parse_args()

    if args.auto:
        auto_check()
    else:
        auto_check()
        show_manual_checklist()


if __name__ == '__main__':
    main()
