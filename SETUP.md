# セットアップガイド

このガイドでは、AI News Analyzerを完全自動化するための手順を説明します。

## 前提条件

- GitHubアカウント
- Groq API アカウント（Anthropic）
- X (Twitter) Developer アカウント

## ステップ1: リポジトリの作成

### 1.1 GitHubで新しいリポジトリを作成

1. https://github.com/new にアクセス
2. リポジトリ名: `ai-news-analyzer` (任意)
3. 公開/プライベートを選択
4. **「Add a README file」のチェックは外す**（既にREADME.mdがあるため）
5. 「Create repository」をクリック

### 1.2 ローカルリポジトリをプッシュ

```bash
cd /d/ai-news-analyzer

# リモートリポジトリを追加（YOUR_USERNAMEを置き換え）
git remote add origin https://github.com/YOUR_USERNAME/ai-news-analyzer.git

# 初回コミット
git add .
git commit -m "Initial commit: AI News Analyzer"

# プッシュ
git branch -M main
git push -u origin main
```

## ステップ2: APIキーの取得

### 2.1 Groq API キー

1. https://console.groq.com/ にアクセス
2. サインアップ/ログイン
3. 左メニューの「API Keys」をクリック
4. 「Create Key」をクリック
5. キーをコピーして安全に保存

### 2.2 X (Twitter) API キー

#### Developer Accountの作成

1. https://developer.twitter.com/ にアクセス
2. 「Sign up」または「Apply」をクリック
3. 利用目的を記入（例: "Automated AI news analysis and posting"）
4. 承認を待つ（通常数分〜数時間）

#### アプリケーションの作成

1. Developer Portal: https://developer.twitter.com/en/portal/dashboard
2. 「Projects & Apps」 → 「Create Project」
3. プロジェクト名を入力（例: "AI News Analyzer"）
4. Use caseを選択（例: "Making a bot"）
5. 「Create App」をクリック
6. アプリ名を入力（例: "ai-news-bot"）

#### APIキーの取得

1. アプリの「Keys and tokens」タブに移動
2. **API Key and Secret**:
   - 「Regenerate」をクリック
   - `API Key` と `API Key Secret` をコピー
3. **Access Token and Secret**:
   - 「Generate」をクリック
   - `Access Token` と `Access Token Secret` をコピー

#### 権限の設定

1. アプリの「Settings」タブに移動
2. 「User authentication settings」 → 「Set up」
3. **App permissions**: 「Read and Write」を選択
4. 「Save」をクリック

## ステップ3: GitHub Secretsの設定

1. GitHubリポジトリページにアクセス
2. 「Settings」タブをクリック
3. 左メニューの「Secrets and variables」 → 「Actions」をクリック
4. 「New repository secret」をクリック

以下の5つのSecretを追加:

| Name | Value |
|------|-------|
| `GROQ_API_KEY` | Groq APIキー |
| `TWITTER_API_KEY` | Twitter API Key |
| `TWITTER_API_SECRET` | Twitter API Key Secret |
| `TWITTER_ACCESS_TOKEN` | Twitter Access Token |
| `TWITTER_ACCESS_TOKEN_SECRET` | Twitter Access Token Secret |

## ステップ4: GitHub Actionsの有効化

1. リポジトリの「Actions」タブをクリック
2. 「I understand my workflows, go ahead and enable them」をクリック
3. ワークフロー「Daily AI News Analysis」が表示されることを確認

## ステップ5: 初回テスト実行

### 手動実行でテスト

1. 「Actions」タブ → 「Daily AI News Analysis」を選択
2. 「Run workflow」をクリック
3. 「Run workflow」ボタンを再度クリック
4. 実行結果を確認

### ローカルでテスト（オプション）

```bash
# .envファイルを作成
cp .env.example .env

# .envファイルを編集してAPIキーを設定
nano .env  # または任意のエディタ

# 依存関係のインストール
pip install -r requirements.txt

# テスト実行
python src/analyzer.py
```

## ステップ6: 実行スケジュールの調整

デフォルトでは毎日JST 9:00（UTC 0:00）に実行されます。

変更する場合は `.github/workflows/daily-analysis.yml` を編集:

```yaml
schedule:
  - cron: '0 0 * * *'  # UTC時刻で指定
```

### cron式の例

- `0 0 * * *` - 毎日 UTC 0:00（JST 9:00）
- `0 3 * * *` - 毎日 UTC 3:00（JST 12:00）
- `0 12 * * *` - 毎日 UTC 12:00（JST 21:00）
- `0 */6 * * *` - 6時間ごと

## トラブルシューティング

### エラー: "Missing required environment variables"

→ GitHub Secretsが正しく設定されているか確認

### エラー: "403 Forbidden" (Twitter)

→ アプリの権限が「Read and Write」になっているか確認

### ニュースが見つからない

→ `HOURS_LOOKBACK` を増やす（24 → 48など）

### Groq APIエラー

→ APIキーが有効か、クレジットが残っているか確認

## カスタマイズ

### ニュースソースの追加

[src/news_sources.py](src/news_sources.py) の `NEWS_SOURCES` に追加:

```python
{
    "name": "Your News Source",
    "url": "https://example.com/rss.xml",
    "language": "ja"
}
```

### ツイートフォーマットの変更

[src/twitter_poster.py](src/twitter_poster.py) の `_format_tweet()` メソッドを編集

### サプライズ度評価基準の変更

[src/surprise_analyzer.py](src/surprise_analyzer.py) の `_create_analysis_prompt()` メソッドを編集

## サポート

- Issue: https://github.com/YOUR_USERNAME/ai-news-analyzer/issues
- Pull Requests大歓迎！

## 次のステップ

完全自動化が成功したら、以下も検討してみてください:

- [ ] Slack/Discord通知の追加
- [ ] ダッシュボードの構築（GitHub Pages）
- [ ] 複数言語対応
- [ ] 週次/月次サマリーレポート
