# AI News Analyzer

完全自動化されたAIニュース収集・分析システム。直近24時間で最もサプライズ度が高いAIニュースを自動選定し、X (Twitter) に投稿します。

## 特徴

- **完全自動化**: GitHub Actionsで毎日定時実行
- **高精度分析**: Claude APIによるサプライズ度スコアリング
- **自動投稿**: X (Twitter) APIで分析結果を自動ポスト
- **履歴管理**: GitHub Issues/Discussionsでレポート保存

## アーキテクチャ

```
┌─────────────────────┐
│  GitHub Actions     │  ← 毎日定時実行 (cron)
│  (daily-analysis)   │
└──────────┬──────────┘
           │
           ↓
┌─────────────────────┐
│  Python Script      │
│  - RSS収集          │  ← 複数のAIメディアから取得
│  - Claude API分析   │  ← サプライズ度スコアリング
│  - X API投稿        │  ← 結果を自動ツイート
└─────────────────────┘
```

## セットアップ

### 1. 必要なAPIキー

以下のAPIキーを取得してください：

#### Claude API
1. https://console.anthropic.com/ にアクセス
2. API Keyを発行
3. GitHub Secretsに `ANTHROPIC_API_KEY` として保存

#### X (Twitter) API
1. https://developer.twitter.com/ でDeveloper Accountを作成
2. プロジェクト作成 → App作成
3. 以下の権限を有効化:
   - Read and Write permissions
4. Keys and Tokensから以下を取得:
   - API Key → `TWITTER_API_KEY`
   - API Secret Key → `TWITTER_API_SECRET`
   - Access Token → `TWITTER_ACCESS_TOKEN`
   - Access Token Secret → `TWITTER_ACCESS_TOKEN_SECRET`
5. すべてGitHub Secretsに保存

### 2. GitHub Secretsの設定

リポジトリの `Settings` → `Secrets and variables` → `Actions` で以下を追加:

- `ANTHROPIC_API_KEY`: Claude APIキー
- `TWITTER_API_KEY`: X API Key
- `TWITTER_API_SECRET`: X API Secret Key
- `TWITTER_ACCESS_TOKEN`: X Access Token
- `TWITTER_ACCESS_TOKEN_SECRET`: X Access Token Secret

### 3. 実行スケジュールの設定

`.github/workflows/daily-analysis.yml` の `cron` を編集:

```yaml
schedule:
  - cron: '0 0 * * *'  # UTC 0:00 = JST 9:00
```

日本時間で実行したい時刻から9時間引いた値を設定してください。

## ローカル実行

```bash
# 依存関係のインストール
pip install -r requirements.txt

# 環境変数の設定
cp .env.example .env
# .env ファイルを編集してAPIキーを設定

# 実行
python src/analyzer.py
```

## 対応ニュースソース

### 英語メディア
- TechCrunch AI
- VentureBeat AI
- The Verge AI
- MIT Technology Review
- OpenAI Blog
- Google AI Blog
- Anthropic News

### 日本語メディア
- ITmedia AI+
- AINOW
- AI Database
- Ledge.ai

## サプライズ度評価基準

Claude APIが以下の4つの観点で評価:

1. **インパクト**: 性能・価格・規模の桁違い感
2. **新規性**: 既存技術との非連続性
3. **現実性**: 利用可能性・具体的ロードマップ
4. **信頼性**: 一次情報の裏付け

## 出力例

X投稿フォーマット:

```
🚀 本日のAIサプライズニュース

【タイトル】
OpenAI、GPT-5を予想外の価格で一般公開

【なぜサプライズ?】
✨ 従来比10倍の性能向上
✨ 月額$20→$5に値下げ
✨ 今日から全ユーザー利用可能

📊 詳細分析: [GitHub Issue Link]

#AI #MachineLearning #OpenAI
```

## ライセンス

MIT License

## 作成者

AI News Analyzer Team
