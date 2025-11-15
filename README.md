# AI News Analyzer (完全無料版)

完全自動化されたAIニュース収集・分析システム。直近24時間で最もサプライズ度が高いAIニュースを自動選定し、GitHub Issueにレポートを投稿します。

## ✨ 特徴

- **完全自動化**: GitHub Actionsで毎日定時実行
- **高精度分析**: Claude Code (Groq LLaMA 3.1 70B) によるサプライズ度スコアリング
- **X統合**: Nitter + RSSHub で X (Twitter) の有用な投稿も収集
- **完全無料**: すべて無料サービスのみで運用可能（API料金ゼロ）
- **履歴管理**: GitHub Issuesで分析レポートを自動保存

## 🏗️ アーキテクチャ

```
┌─────────────────────┐
│  GitHub Actions     │  ← 毎日定時実行 (cron)
│  (daily-analysis)   │
└──────────┬──────────┘
           │
           ↓
┌─────────────────────────────────┐
│  Python Script                  │
│  - RSS収集 (複数メディア)       │
│  - X検索 (Nitter)                │
│  - X監視 (RSSHub)                │
│  - Claude Code分析 (Groq)        │
└────────────┬────────────────────┘
             │
             ↓
┌─────────────────────┐
│  GitHub Issue       │  ← レポート自動投稿
│  (分析結果保存)      │
└─────────────────────┘
```

## 📦 収集ソース

### RSS Feeds
- TechCrunch AI / VentureBeat AI / The Verge AI
- MIT Technology Review / OpenAI Blog
- Google AI Blog / Anthropic News
- Hugging Face Blog / DeepMind Blog
- ITmedia AI+ / AINOW / Ledge.ai

### X (Twitter)
#### Nitter検索（キーワード）
- ChatGPT, GPT-4, Claude, Gemini
- OpenAI, Anthropic, Google AI
- AI breakthrough, LLM 等

#### RSSHub監視（アカウント）
- @OpenAI, @AnthropicAI, @GoogleDeepMind
- @sama (Sam Altman), @ylecun (Yann LeCun)
- @karpathy, @DrJimFan 等

## 🚀 セットアップ

### 1. 必要なAPIキー

**Groq API のみ（完全無料）**

1. https://console.groq.com/ にアクセス
2. サインアップ（GitHubアカウントでログイン可能）
3. 「Create API Key」をクリック
4. APIキーをコピー

**無料枠**:
- LLaMA 3.1 70B: 30リクエスト/分
- 月間制限なし
- クレジットカード不要

### 2. GitHub Secretsの設定

リポジトリの `Settings` → `Secrets and variables` → `Actions` で以下を追加:

| Name | Value |
|------|-------|
| `GROQ_API_KEY` | Groq APIキー |

これだけで完了です！

### 3. 実行スケジュールの設定

`.github/workflows/daily-analysis.yml` の `cron` を編集:

```yaml
schedule:
  - cron: '0 0 * * *'  # UTC 0:00 = JST 9:00
```

日本時間で実行したい時刻から9時間引いた値を設定してください。

## 💻 ローカル実行

```bash
# 依存関係のインストール
pip install -r requirements.txt

# 環境変数の設定
cp .env.example .env
# .env ファイルを編集してGroq APIキーを設定

# 実行
python src/analyzer.py
```

## 📊 サプライズ度評価基準

Claude Code (Groq LLaMA 3.1 70B) が以下の4つの観点で評価:

1. **インパクト**: 性能・価格・規模の桁違い感
2. **新規性**: 既存技術との非連続性
3. **現実性**: 利用可能性・具体的ロードマップ
4. **信頼性**: 一次情報の裏付け

## 📝 出力例

GitHub Issueに以下のような形式でレポートが投稿されます:

```markdown
# AIニュース分析レポート

## 🚀 選定されたニュース

### タイトル
OpenAI、GPT-5を予想外の価格で一般公開

### URL
https://openai.com/blog/gpt-5-release

## ⚡ なぜサプライズか

1. **従来比10倍の性能向上**
2. **月額$20→$5に値下げ**
3. **今日から全ユーザー利用可能**

## 💡 インパクト分析

### 💻 エンジニア視点
...

### 💼 ビジネス視点
...

## 📊 サプライズスコア
**92 / 100**
```

## 🛠️ 技術スタック

| 項目 | 技術 | コスト |
|------|------|--------|
| **LLM分析** | Groq LLaMA 3.1 70B | 無料 |
| **X収集** | Nitter + RSSHub | 無料 |
| **RSS収集** | feedparser | 無料 |
| **自動化** | GitHub Actions | 無料 |
| **レポート保存** | GitHub Issues | 無料 |

**月額コスト: $0**

## 📚 ドキュメント

- [QUICKSTART.md](QUICKSTART.md) - 5分でセットアップ
- [SETUP.md](SETUP.md) - 詳細セットアップガイド

## 🔧 カスタマイズ

### X監視アカウントの追加

[src/news_sources.py](src/news_sources.py) の `X_ACCOUNTS` に追加:

```python
X_ACCOUNTS = [
    "OpenAI",
    "your_favorite_account",  # 追加
]
```

### 検索キーワードの追加

[src/news_sources.py](src/news_sources.py) の `X_SEARCH_KEYWORDS` に追加:

```python
X_SEARCH_KEYWORDS = [
    "ChatGPT",
    "your_keyword",  # 追加
]
```

## ⚠️ 注意事項

- **Nitter**: 公開データのスクレイピングです。利用規約を確認してください。
- **RSSHub**: 公開RSSサービスです。レート制限に注意してください。
- **安定性**: 無料サービスのため、時々エラーが発生する可能性があります。

## 📄 ライセンス

MIT License

## 👥 作成者

AI News Analyzer Team
