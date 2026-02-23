#!/usr/bin/env python3
"""
OAK 全体ヘルスチェック
======================
プロジェクト全体の状態を一括チェック。

使い方:
    python health_check.py
"""

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
SNS_DIR = PROJECT_ROOT / "sns"
BLOG_DIR = PROJECT_ROOT / "blog"
TOOLS_DIR = PROJECT_ROOT / "tools"


def check_files():
    """重要ファイルの存在チェック"""
    critical = [
        ("README.md", "プロジェクトREADME"),
        ("OPERATOR-MANUAL.md", "運用マニュアル"),
        ("X-OPERATIONS-MANUAL.md", "X運用マニュアル"),
        ("index.html", "ルートページ"),
        ("sitemap.xml", "サイトマップ"),
        (".gitignore", "Git除外設定"),
        ("LICENSE", "ライセンス"),
    ]

    print("\n📁 Critical Files")
    for filepath, desc in critical:
        full = PROJECT_ROOT / filepath
        status = "✅" if full.exists() else "❌"
        size = f"({full.stat().st_size:,} bytes)" if full.exists() else ""
        print(f"  {status} {filepath:<35} {desc} {size}")


def check_scripts():
    """スクリプトの存在と構文チェック"""
    scripts = list(SNS_DIR.glob("*.py")) + list((BLOG_DIR / "scripts").glob("*.py"))
    print(f"\n🐍 Python Scripts ({len(scripts)})")

    errors = []
    for script in sorted(scripts):
        try:
            compile(script.read_text(encoding='utf-8'), str(script), 'exec')
            print(f"  ✅ {script.relative_to(PROJECT_ROOT)}")
        except SyntaxError as e:
            print(f"  ❌ {script.relative_to(PROJECT_ROOT)} — Syntax Error: {e.msg}")
            errors.append(script)

    return errors


def check_html():
    """HTMLファイルのチェック"""
    html_files = list(PROJECT_ROOT.rglob("*.html"))
    html_files = [f for f in html_files if "node_modules" not in str(f)]
    print(f"\n🌐 HTML Pages ({len(html_files)})")

    for html in sorted(html_files):
        size = html.stat().st_size
        content = html.read_text(encoding='utf-8', errors='replace')
        has_title = '<title>' in content
        has_meta = '<meta ' in content
        status = "✅" if has_title else "⚠️"
        print(f"  {status} {html.relative_to(PROJECT_ROOT)} ({size:,}b)")


def check_data():
    """データファイルのチェック"""
    data_files = [
        (SNS_DIR / "x_analytics_data.json", "X Analytics"),
        (BLOG_DIR / "articles.json", "Blog Articles"),
        (PROJECT_ROOT / "content" / "x_post_queue.json", "Post Queue"),
    ]

    print(f"\n📊 Data Files")
    for filepath, desc in data_files:
        if filepath.exists():
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                if isinstance(data, list):
                    print(f"  ✅ {filepath.name:<30} {desc} ({len(data)} items)")
                elif isinstance(data, dict):
                    items = sum(1 for _ in data.values() if isinstance(_, list))
                    print(f"  ✅ {filepath.name:<30} {desc} ({items} lists)")
                else:
                    print(f"  ✅ {filepath.name:<30} {desc}")
            except json.JSONDecodeError:
                print(f"  ❌ {filepath.name:<30} {desc} (INVALID JSON)")
        else:
            print(f"  ⬜ {filepath.name:<30} {desc} (not yet created)")


def check_workflows():
    """GitHub Actionsチェック"""
    wf_dir = PROJECT_ROOT / ".github" / "workflows"
    if not wf_dir.exists():
        print(f"\n⚙️ GitHub Actions: Directory not found")
        return

    workflows = list(wf_dir.glob("*.yml"))
    print(f"\n⚙️ GitHub Actions ({len(workflows)})")
    for wf in sorted(workflows):
        print(f"  ✅ {wf.name}")


def summary():
    """サマリー"""
    total_py = len(list(SNS_DIR.glob("*.py"))) + len(list((BLOG_DIR / "scripts").glob("*.py")))
    total_html = len([f for f in PROJECT_ROOT.rglob("*.html") if "node_modules" not in str(f)])
    total_md = len(list(PROJECT_ROOT.rglob("*.md")))
    total_files = len(list(PROJECT_ROOT.rglob("*")))

    print(f"\n{'='*50}")
    print(f"  📊 Project Summary")
    print(f"{'='*50}")
    print(f"  Python scripts:  {total_py}")
    print(f"  HTML pages:      {total_html}")
    print(f"  Markdown docs:   {total_md}")
    print(f"  Total files:     {total_files}")
    print(f"{'='*50}\n")


def main():
    print(f"\n{'='*50}")
    print(f"  🏥 OAK Health Check")
    print(f"{'='*50}")

    check_files()
    errors = check_scripts()
    check_html()
    check_data()
    check_workflows()
    summary()

    if errors:
        print(f"⚠️  {len(errors)} scripts with syntax errors!")
        sys.exit(1)
    else:
        print(f"✅ All checks passed!")


if __name__ == '__main__':
    main()
