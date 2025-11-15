# クイックスタート

このガイドは、最速でAI News Analyzerを動かすための簡易版です。

詳細なセットアップは [SETUP.md](SETUP.md) を参照してください。

## 5分で完了する最小セットアップ

### 1. GitHubリポジトリを作成

```bash
# GitHubで新規リポジトリ作成後
cd /d/ai-news-analyzer
git remote add origin https://github.com/YOUR_USERNAME/ai-news-analyzer.git
git push -u origin main
```

### 2. APIキーを取得

#### Claude API
- https://console.anthropic.com/ → API Keys → Create Key

#### Twitter API
- https://developer.twitter.com/en/portal/dashboard
- Project作成 → App作成 → Keys取得
- **重要**: App Permissions を「Read and Write」に設定

### 3. GitHub Secretsを設定

リポジトリの Settings → Secrets and variables → Actions で以下を追加:

```
ANTHROPIC_API_KEY=sk-ant-xxxxx
TWITTER_API_KEY=xxxxx
TWITTER_API_SECRET=xxxxx
TWITTER_ACCESS_TOKEN=xxxxx
TWITTER_ACCESS_TOKEN_SECRET=xxxxx
```

### 4. テスト実行

Actions タブ → Daily AI News Analysis → Run workflow

以上！

## ローカルで試す場合

```bash
# 依存関係インストール
pip install -r requirements.txt

# .env作成
cp .env.example .env
# .envファイルを編集してAPIキーを設定

# 実行
python src/analyzer.py
```

## 実行スケジュール変更

[.github/workflows/daily-analysis.yml](.github/workflows/daily-analysis.yml) の cron を編集:

```yaml
# 毎日JST 21:00に実行したい場合
cron: '0 12 * * *'  # UTC 12:00 = JST 21:00
```

## トラブルシューティング

### Twitter投稿できない
→ App Permissions が「Read and Write」になっているか確認

### ニュースが見つからない
→ 正常です。実際にAIニュースが少ない日もあります

### Claude APIエラー
→ APIキーが正しいか、クレジットが残っているか確認

## 次に読むドキュメント

- 📖 [README.md](README.md) - プロジェクト概要
- 🔧 [SETUP.md](SETUP.md) - 詳細セットアップガイド
- 💻 [src/](src/) - ソースコードの説明

## サポート

問題があれば Issue を作成してください！
