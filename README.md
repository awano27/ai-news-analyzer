# AI News Analyzer

完全自動化されたAIニュース収集・分析システム。直近24時間で最もサプライズ度が高いAIニュースを自動選定し、X (Twitter) に投稿します。

## 特徴

- **完全自動化**: GitHub Actionsで毎日定時実行
- **高精度分析**: Claude Codeによるサプライズ度スコアリング（Groq API - 無料）
- **自動投稿**: X (Twitter) APIで分析結果を自動ポスト
- **履歴管理**: GitHub Issues/Discussionsでレポート保存
- **完全無料**: Groq APIの無料枠で運用可能

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
│  - Claude Code分析  │  ← サプライズ度スコアリング (Groq LLaMA 3.1 70B)
│  - X API投稿        │  ← 結果を自動ツイート
└─────────────────────┘
```

## セットアップ

### 1. 必要なAPIキー

以下のAPIキーを取得してください：

#### Groq API（完全無料）
1. https://console.groq.com/ にアクセス
2. サインアップ（GitHubアカウントでログイン可能）
3. 「Create API Key」をクリック
4. APIキーをコピー
5. GitHub Secretsに `GROQ_API_KEY` として保存

**無料枠**: 
- LLaMA 3.1 70B: 30リクエスト/分
- 月間制限なし
- 高速推論（Claudeより速い）

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

- `GROQ_API_KEY`: Groq APIキー（無料）
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
- Hugging Face Blog
- DeepMind Blog

### 日本語メディア
- ITmedia AI+
- AINOW
- Ledge.ai

## サプライズ度評価基準

Claude Code（Groq LLaMA 3.1 70B）が以下の4つの観点で評価:

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

## 技術スタック

- **LLM**: Groq LLaMA 3.1 70B（無料）
- **自動化**: GitHub Actions
- **言語**: Python 3.11+
- **ライブラリ**: feedparser, groq, tweepy, pytz

## ライセンス

MIT License

## 作成者

AI News Analyzer Team
