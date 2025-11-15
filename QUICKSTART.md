# クイックスタート（完全無料版）

最速でAI News Analyzerを動かすための簡易版です。

## ⚡ 3ステップで完了

### 1. Groq APIキーを取得

**https://console.groq.com/**
1. Sign up（GitHubアカウントでOK）
2. API Keys → Create Key
3. キーをコピー

### 2. GitHub Secretsを設定

**https://github.com/awano27/ai-news-analyzer/settings/secrets/actions**

New repository secret をクリック:

```
Name: GROQ_API_KEY
Secret: gsk_xxxxx（コピーしたキー）
```

### 3. テスト実行

**https://github.com/awano27/ai-news-analyzer/actions/workflows/daily-analysis.yml**

Run workflow → Run workflow

以上！

## 💻 ローカルで試す場合

```bash
# 依存関係インストール
pip install -r requirements.txt

# .env作成
cp .env.example .env
# .envファイルを編集してGroq APIキーを設定

# 実行
python src/analyzer.py
```

## 📊 結果の確認

- **GitHub Issues**: 分析レポートが自動投稿されます
- **GitHub Actions**: 実行ログで詳細を確認できます

## ❓ トラブルシューティング

### エラー: "Missing required environment variables"
→ GitHub Secretsに `GROQ_API_KEY` が設定されているか確認

### Nitterエラー
→ 正常です。Nitterインスタンスが一時的に使えない場合があります

### ニュースが見つからない
→ 正常です。24時間以内にAIニュースがない日もあります

## 🔗 次に読むドキュメント

- [README.md](README.md) - 詳細な機能説明
- [SETUP.md](SETUP.md) - カスタマイズ方法

## 💰 コスト

**$0 / 月**

すべて無料サービスで動作します！
