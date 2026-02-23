# 🚀 Obsidian Automation Kit (OAK)

> `python master.py` — たった1コマンドでObsidianの11ステップを完全自動化

[![License: MIT](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)

## ✨ 特徴

Obsidianの運用で面倒な「日次/週次の手動処理」「バックアップ」「分析」を、Pythonスクリプト1発ですべて自動化するツールキットです。

| 機能 | 内容 |
|:---|:---|
| **Daily Note 自動生成** | 毎朝の白紙ノートを前日のタスクと共に自動生成 |
| **Weekly/Monthly 自動生成** | 振り返りテンプレートを日曜/月末に自動生成 |
| **Git 自動バックアップ** | `git pull -> commit -> push` を全自動化 |
| **Vault 健康診断** | リンク切れやサイズ肥大化をチェックし警告 |
| **プロジェクトタイムライン** | Obsidian内のMarkdownタスクからMermaid Gantt作成 |
| **NotebookLM 自動同期** | Vaultのノート差分を検知しNotebookLMへアップロード |

## 🚀 クイックスタート

```bash
git clone https://github.com/YOUR_USERNAME/obsidian-automation-kit.git
cd obsidian-automation-kit

# セットアップウィザード（対話形式）
python template/scripts/setup_wizard.py

# または手動
cp template/scripts/config.template.json template/scripts/config.json
# config.json を編集 → python template/scripts/master.py に登録
```

## 📦 プロジェクト構成

```
obsidian-automation-kit/
├── template/scripts/           ← Obsidian自動化コア
│   ├── master.py               ← 🎯 全自動オーケストレーター
│   ├── setup_wizard.py         ← セットアップウィザード
│   ├── health_check.py         ← ヘルスチェック
│   ├── auto_daily.py           ← Daily Note 生成
│   ├── auto_weekly.py          ← 週次レビュー
│   ├── auto_monthly.py         ← 月次レビュー
│   ├── auto_timeline.py        ← Mermaid Gantt 生成
│   ├── git_backup.py           ← Git バックアップ
│   └── vault_health.py         ← 健康診断
├── template/Templates/         ← Obsidian カスタムテンプレート群
└── README.md
```

## ⏰ 内蔵スケジューラー (常駐自動化)

OSのタスクスケジューラや `cron` の設定は不要です。`config.json` に指定したタイミングや間隔（ウィザードで設定可能）に従い、バックグラウンドで自動実行します。

```bash
# スケジューラーを起動（立ち上げっぱなしにするだけ）
python template/scripts/scheduler.py
```

実行中に `config.json` のバックアップ間隔や時間を変更しても、再起動なしで即座に反映（ホットリロード）されます。

| デフォルト設定例 | 内容 |
|:---|:---|
| **毎日 00:05** | `auto_daily.py` (Dailyノート生成) |
| **60分ごと** | `git_backup.py` (自動バックアップ) |
| **日曜 23:30** | `auto_weekly.py` (週次レビュー用) |
| **1日 23:45** | `auto_monthly.py` (月次レビュー用) |

## 🛠️ 要件

- Python 3.10+
- Obsidian (バージョン問わず)
- Git (バックアップ機能を使用する場合)

## ☕ サポート

このプロジェクトが役に立ったら、サポートをお願いします:

- ⭐ GitHubでStarをつける

## 📄 ライセンス

MIT License
