# 🚀 クイックスタートガイド — 全自動マネタイズを70分で始める

## 必要なもの

- GitHub アカウント（無料）
- Google アカウント（Gemini API用、無料）
- BMC / Ko-fi アカウント（寄付受け取り、無料）
- Gumroad または BOOTH アカウント（商品販売、無料）

---

## Step 1: GitHubリポジトリ作成（10分）

### 1.1 新しいリポジトリを作成
1. [github.com/new](https://github.com/new) へアクセス
2. リポジトリ名: `obsidian-automation-kit`
3. Public を選択
4. 「Create repository」をクリック

### 1.2 コードをpush
```bash
cd obsidian-automation-kit
git init
git add -A
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/obsidian-automation-kit.git
git push -u origin main
```

### 1.3 GitHub Pages を有効化
1. Settings → Pages
2. Source: Deploy from a branch
3. Branch: main / root
4. Save

### 1.4 API キーを設定
1. Settings → Secrets and variables → Actions
2. 「New repository secret」をクリック
3. Name: `GEMINI_API_KEY`
4. Value: [Google AI Studio](https://aistudio.google.com/) で取得したAPIキー

→ **これで記事自動生成ワークフローが稼働開始！**

---

## Step 2: BMC / Ko-fi アカウント作成（10分）

### Buy Me a Coffee
1. [buymeacoffee.com](https://buymeacoffee.com/) でアカウント作成
2. プロフィールを設定（アイコン、説明文）
3. ページURLをメモ（例: `buymeacoffee.com/abscl`）

### Ko-fi（オプション）
1. [ko-fi.com](https://ko-fi.com/) でアカウント作成
2. 決済設定（PayPal or Stripe）

### FUNDING.yml を更新
```yaml
# .github/FUNDING.yml
buy_me_a_coffee: YOUR_USERNAME
ko_fi: YOUR_USERNAME
```

→ **リポジトリに「Sponsor」ボタンが自動表示！**

---

## Step 3: Gumroad / BOOTH 出品（30分）

### Gumroad
1. [gumroad.com](https://gumroad.com/) でアカウント作成
2. 「New product」→ Digital product
3. 商品名: 「Obsidian Automation Kit Pro」
4. 説明文: `content/gumroad-listing.md` からコピペ
5. 価格: ¥2,980
6. ZIPファイルをアップロード
7. Publish

### BOOTH（日本市場向け）
1. [booth.pm](https://booth.pm/) でアカウント作成
2. 「商品管理」→「商品登録」
3. 商品名: 「Obsidian 完全自動化キット Pro」
4. 説明文: `content/booth-listing.md` からコピペ
5. 価格: ¥2,980
6. ZIPファイルをアップロード
7. 公開

### ZIPファイルの作成
```bash
cd template
# Free版
zip -r oak-free.zip scripts/auto_daily.py scripts/auto_weekly.py \
  scripts/auto_monthly.py scripts/git_backup.py scripts/vault_health.py \
  scripts/auto_timeline.py scripts/master.py scripts/config.template.json \
  Templates/ README.md

# Pro版
zip -r oak-pro.zip scripts/ Templates/ README.md
```

---

## Step 4: コンテンツ投稿（10分）

### Zenn（GitHub連携）
1. [zenn.dev](https://zenn.dev/) にログイン
2. 設定 → GitHub連携
3. `zenn/` ディレクトリ内の記事が自動公開される

### note
1. [note.com](https://note.com/) にログイン
2. 「投稿」→ テキスト
3. `content/note-article-draft.md` からコピペ
4. 価格設定: ¥300
5. 公開

### X ローンチスレッド
1. [x.com](https://x.com/) にログイン
2. `content/x-threads-template.md` のパターン1をコピペ
3. スレッドとして投稿

---

## Step 5: X Developer Account（5分 + 審査待ち）

> ⚠️ 自動投稿には Developer Account が必要。審査に数日かかる場合あり。

1. [developer.x.com](https://developer.x.com/) でアプリケーション作成
2. Free tier を選択
3. API Keys を取得
4. GitHub Secrets に設定:
   - `X_API_KEY`
   - `X_API_SECRET`
   - `X_ACCESS_TOKEN`
   - `X_ACCESS_SECRET`

→ **審査通過後、毎日朝夜の自動投稿が開始！**

---

## 完了！ 🎉

### 自動で動き続けること
| 何が | いつ | どこで |
|:---|:---|:---|
| ブログ記事生成 | 週2回 | GitHub Actions |
| X投稿 | 毎日2回 | GitHub Actions |
| コンテンツ生成 | 毎週月曜 | GitHub Actions |
| GitHub Pages更新 | push時 | 自動 |
| 商品販売 | 24/7 | Gumroad/BOOTH |
| 寄付受け取り | 24/7 | BMC/Ko-fi |

### 手動でやること（週30分程度）
- [ ] Xのリプ・引用RT（5分/日）
- [ ] 週次の数値チェック（5分/週）
- [ ] コンテンツの品質チェック（10分/週）

### トラブルシューティング
| 問題 | 対策 |
|:---|:---|
| Actions が動かない | Settings → Actions → Allow all actions |
| 記事生成失敗 | GEMINI_API_KEY を確認 |
| X投稿失敗 | API Keys を確認 |
| Pages非公開 | Settings → Pages → Branch を確認 |
