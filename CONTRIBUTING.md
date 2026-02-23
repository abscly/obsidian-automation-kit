# 🤝 Contributing

OAKへのコントリビューションを歓迎します！

## 開発環境セットアップ

```bash
git clone https://github.com/YOUR_USERNAME/obsidian-automation-kit.git
cd obsidian-automation-kit
pip install -r template/scripts/requirements.txt
```

## プロジェクト構成

```
├── blog/               ← 技術ブログ（HTML, JSON）
│   ├── articles/       ← 記事HTML
│   ├── scripts/        ← 自動化スクリプト
│   └── articles.json   ← 記事メタデータ
├── content/            ← マーケティング素材
├── landing-page/       ← LP
├── portfolio/          ← ポートフォリオ
├── products/           ← 販売商品（Bot テンプレ等）
├── sns/                ← SNS自動化スクリプト
├── template/           ← OAK本体（Free/Pro）
├── tools/              ← 無料ツール（HTML）
└── zenn/               ← Zenn記事
```

## コントリビューション方法

### バグ報告
1. Issue を作成
2. 再現手順を記載
3. 環境情報（OS, Python バージョン）を明記

### 機能提案
1. Issue で提案
2. ユースケースを説明
3. 実装案があれば記載

### Pull Request
1. Fork → ブランチ作成
2. 変更を実装
3. テスト確認
4. PR 送信

## コーディング規約

- Python: PEP 8 準拠
- HTML: セマンティックタグ使用
- CSS: CSS Custom Properties (var()) 使用
- コミットメッセージ: `type: message` (fix, feat, docs, style)

## ライセンス

MIT License — 自由に使ってください！
