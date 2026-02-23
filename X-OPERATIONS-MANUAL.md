# 🐦 X (Twitter) 運用マニュアル — 完全版

> 「`python x_ops.py daily` — 毎日これだけ」

---

## ⚡ クイックリファレンス

```bash
# 1つのコマンドで全部やる
python sns/x_ops.py daily

# 細かく実行する場合
python sns/x_ops.py post          # 投稿
python sns/x_ops.py thread tips   # スレッド生成
python sns/x_ops.py analytics     # ダッシュボード更新
python sns/x_ops.py hashtags AI   # ハッシュタグ提案
python sns/x_ops.py content       # 1週間のコンテンツ生成
python sns/x_ops.py report        # 週次レポート
```

---

## 📊 スクリプト一覧

| スクリプト | 用途 | 使用頻度 |
|:---|:---|:---|
| `x_ops.py` | **統合CLI（全部ここから）** | 毎日 |
| `x_auto_poster.py` | 投稿キュー管理・自動投稿 | 自動(Actions) |
| `x_analytics.py` | パフォーマンス分析・ダッシュボード | 毎日(自動) |
| `x_thread_generator.py` | スレッド生成（4タイプ+AI） | 週1 |
| `x_hashtag_analyzer.py` | ハッシュタグ分析・提案 | 投稿前に確認 |
| `x_reply_templates.py` | リプライテンプレート | リプ時 |
| `x_follower_tracker.py` | フォロワー成長追跡 | 週1 |
| `x_engagement_content.py` | エンゲージメントコンテンツDB | 自動 |

---

## 📅 デイリールーティン（5分）

### 朝（5分）
1. `python sns/x_ops.py daily` を実行
2. Xアプリで通知チェック
3. 3件リプライ返信（テンプレ使用OK）

### やらなくていいこと（自動化済み）
- ❌ 投稿作成 → **自動生成+自動投稿**
- ❌ ハッシュタグ選び → **自動最適化**
- ❌ 分析 → **ダッシュボード自動更新**

---

## 📅 週次ルーティン（15分）

### 毎週日曜
1. `python sns/x_ops.py report` — 週次レポート生成
2. `python sns/x_follower_tracker.py --log XXX` — フォロワー数記録
3. ダッシュボード(`tools/x-analytics-dashboard.html`)を確認
4. 最も ER が高かったコンテンツタイプを確認 → 来週増やす

---

## 🧵 スレッド活用

### テンプレートタイプ
| タイプ | ER傾向 | おすすめ頻度 |
|:---|:---|:---|
| Tips | ★★★★☆ | 週1 |
| Story (Before/After) | ★★★★★ | 月2 |
| Comparison | ★★★★☆ | 月1 |
| Tutorial | ★★★☆☆ | 月1 |

### 生成例
```bash
python sns/x_thread_generator.py --type story    # ストーリー型
python sns/x_thread_generator.py --ai "Gemini API"  # AIでカスタム
```

---

## 🏷️ ハッシュタグ戦略

### コアタグ（毎回1-2個）
- `#Obsidian` — ER 1.4x boost
- `#個人開発` — ER 1.6x boost

### 高ERタグ
- `#GeminiAPI` — ER **1.8x** boost（ニッチで効果大）
- `#自動化` — ER 1.5x boost
- `#Chrome拡張` — ER 1.6x boost

### 避けるべき
- `#相互フォロー` → スパム判定リスク
- 5個以上のタグ → ウザく見える

---

## 📊 KPI目標

| 指標 | Month 1 | Month 3 | Month 6 |
|:---|:---|:---|:---|
| フォロワー | 100 | 300 | 500 |
| 月間Imp | 10,000 | 30,000 | 50,000 |
| 平均ER | 2% | 3% | 3.5% |

---

## 🔧 初期セットアップ

### 1. X API 取得
1. https://developer.twitter.com/ でアカウント作成
2. Project → App 作成
3. Keys から API Key/Secret、Access Token/Secret を取得

### 2. GitHub Secrets に登録
```
X_API_KEY
X_API_SECRET
X_ACCESS_TOKEN
X_ACCESS_SECRET
```

### 3. 最初のコンテンツ生成
```bash
python sns/x_auto_poster.py --generate
python sns/x_auto_poster.py --preview
```

### 4. テスト投稿
```bash
python sns/x_auto_poster.py --post
```

---

## 💡 エンゲージメント Tips

1. **質問で終える** — リプライ誘発
2. **具体的な数字** — 「月3万円」「11ステップ」
3. **Before/After** — 最もRT率が高い
4. **朝9時 or 夜20時** — ER最高の時間帯
5. **画像付き** — ER 1.5x（端末スクショが効果的）
