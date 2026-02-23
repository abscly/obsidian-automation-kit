# 🚀 Obsidian Automation Kit

> AI-Powered Knowledge Management — ナレッジを自動で整理・分析・バックアップ

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Obsidian](https://img.shields.io/badge/Obsidian-v1.5+-purple.svg)](https://obsidian.md)
[![Python](https://img.shields.io/badge/Python-3.10+-green.svg)](https://python.org)

## ✨ 特徴

🤖 **AI日報補完** — Gemini ProがDaily Noteを自動で要約・分析  
📊 **全自動パイプライン** — 1コマンドで11ステップの処理を実行  
🔄 **Git自動バックアップ** — 変更を自動検知してpull + commit + push  
📅 **日報/週報/月報の自動生成** — テンプレートベースで定期生成  
🔔 **Discord Webhook通知** — パイプライン結果をリアルタイム通知  
🔍 **セマンティック検索** — Gemini Embeddingでノートを自然言語検索  
🗣️ **TTS日報読み上げ** — Cloud TTSでDaily Noteを音声化  
📈 **BigQueryロギング** — 作業データを蓄積してパターン分析  
📱 **Google Calendar/Tasks連携** — TODOとスケジュールを同期  
📤 **NotebookLMエクスポート** — AI分析のために自動エクスポート  
🏥 **Vault健康診断** — 壊れたリンクや孤立ノートを検出  
⏰ **Windows タスクスケジューラ** — 全自動化を簡単セットアップ

## 📂 フォルダ構成

```
YourVault/
├── Home.md                    ← ダッシュボード（自動更新）
├── Daily/                     ← 日報ノート（自動生成）
├── Weekly/                    ← 週次レビュー（自動生成）
├── Monthly/                   ← 月次レビュー（自動生成）
├── Projects/                  ← プロジェクト管理
│   └── {ProjectName}/
│       ├── {ProjectName}.md   ← 概要・TODO
│       ├── {ProjectName} 設計.md ← アーキテクチャ
│       └── {ProjectName} ログ.md ← 作業ログ
├── Knowledge/                 ← 技術知見の蓄積
├── MOC/                       ← Map of Content（知識の地図）
├── Templates/                 ← テンプレート集
│   ├── Daily テンプレート.md
│   ├── Weekly テンプレート.md
│   ├── Project テンプレート.md
│   └── Quick Capture.md
└── scripts/                   ← 自動化スクリプト
    ├── master.py              ← 統合オーケストレーター
    ├── config.json            ← 設定ファイル
    ├── auto_daily.py          ← Daily Note自動生成
    ├── auto_weekly.py         ← 週次レビュー生成
    ├── auto_monthly.py        ← 月次レビュー生成
    ├── auto_timeline.py       ← タイムライン自動更新
    ├── ai_reporter.py         ← AI日報補完（Gemini）
    ├── git_backup.py          ← Git自動バックアップ
    ├── discord_notify.py      ← Discord Webhook通知
    ├── vault_search.py        ← セマンティック検索
    ├── vault_health.py        ← Vault健康診断
    ├── update_home.py         ← Home.md自動更新
    ├── knowledge_organizer.py ← Knowledge整理
    ├── export_to_notebooklm.py ← NLMエクスポート
    └── setup_scheduler.ps1    ← タスクスケジューラ設定
```

## 🚀 クイックスタート

### 1. ダウンロードと配置

```bash
# このフォルダをObsidian Vaultのルートに配置
# または既存のVaultにコピー
```

### 2. 設定ファイルの編集

```bash
# scripts/config.json を編集
cp scripts/config.template.json scripts/config.json
```

`config.json` を開いて、以下を設定:

```json
{
    "discord_webhook_url": "YOUR_DISCORD_WEBHOOK_URL",
    "gemini_api_key": "YOUR_GEMINI_API_KEY",
    "gemini_model": "gemini-2.0-flash",
    "auto_weekly": true,
    "auto_monthly": true,
    "auto_git_backup": true,
    "auto_discord_notify": true,
    "auto_ai_reporter": true
}
```

### 3. 依存パッケージのインストール

```bash
pip install -r scripts/requirements.txt
```

### 4. 実行

```bash
# 全自動パイプライン
python scripts/master.py

# クイック同期だけ
python scripts/master.py --quick

# 週次レビュー生成
python scripts/master.py --weekly
```

### 5. 自動化（オプション）

```powershell
# Windows: タスクスケジューラに登録（管理者権限）
powershell -ExecutionPolicy Bypass -File scripts/setup_scheduler.ps1
```

## 📋 API キーの取得方法

| サービス | 取得先 | 必須 |
|:---|:---|:---|
| Gemini API | [Google AI Studio](https://aistudio.google.com/) | ⭐ 推奨 |
| Discord Webhook | サーバー設定 > 連携サービス > Webhook | オプション |
| Google Calendar | [Google Cloud Console](https://console.cloud.google.com/) | オプション |

## 🏷️ タグ体系

| カテゴリ | タグ例 |
|:---|:---|
| 種別 | `#type/project` `#type/設計` `#type/ログ` `#type/日報` |
| 状態 | `#status/active` `#status/completed` `#status/paused` |
| 技術 | `#tech/python` `#tech/javascript` `#tech/react` |

## 📖 詳細ドキュメント

- [セットアップガイド](docs/setup.md)
- [スクリプト一覧](docs/scripts.md)
- [カスタマイズガイド](docs/customization.md)
- [FAQ](docs/faq.md)

## 💰 ティアプラン

| 機能 | Free | Pro |
|:---|:---|:---|
| Vault テンプレート | ✅ | ✅ |
| テンプレートファイル | ✅ | ✅ |
| master.py（基本） | ✅ | ✅ |
| auto_daily / weekly / monthly | ✅ | ✅ |
| git_backup | ✅ | ✅ |
| AI日報補完（Gemini） | ❌ | ✅ |
| Discord Webhook通知 | ❌ | ✅ |
| セマンティック検索 | ❌ | ✅ |
| TTS読み上げ | ❌ | ✅ |
| BigQueryロギング | ❌ | ✅ |
| Google Calendar連携 | ❌ | ✅ |
| NotebookLMエクスポート | ❌ | ✅ |
| Dashboard（PWA） | ❌ | ✅ |
| タスクスケジューラ設定 | ❌ | ✅ |
| 優先サポート | ❌ | ✅ |

## 📝 License

MIT License — 商用利用・改変・再配布自由

---

Made with 🚀 Antigravity + Obsidian
