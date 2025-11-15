"""
メインスクリプト: ニュース収集・分析を実行（完全無料版）
"""

import os
import sys
import json
import logging
from datetime import datetime
from dotenv import load_dotenv

from feed_collector import FeedCollector
from surprise_analyzer import SurpriseAnalyzer
from x_collector import XCollector
from news_sources import X_SEARCH_KEYWORDS, X_ACCOUNTS

# ロギング設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """
    メイン処理
    """
    # 環境変数読み込み
    load_dotenv()

    # 必須環境変数チェック
    required_vars = [
        'GROQ_API_KEY',
    ]

    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        sys.exit(1)

    # 設定
    timezone = os.getenv('TIMEZONE', 'Asia/Tokyo')
    hours_lookback = int(os.getenv('HOURS_LOOKBACK', '24'))

    logger.info("=== AI News Analyzer Started (Free Edition) ===")
    logger.info(f"Timezone: {timezone}")
    logger.info(f"Lookback period: {hours_lookback} hours")

    # ステップ1: ニュース収集（RSS + X）
    logger.info("\n[STEP 1] Collecting news from multiple sources...")

    # 1-1: RSSフィードから収集
    logger.info("[STEP 1-1] Collecting from RSS feeds...")
    collector = FeedCollector(timezone=timezone, hours_lookback=hours_lookback)
    rss_articles = collector.collect_all_feeds()
    logger.info(f"RSS articles collected: {len(rss_articles)}")

    # 1-2: Xから収集
    logger.info("[STEP 1-2] Collecting from X (Twitter)...")
    x_collector = XCollector(timezone=timezone, hours_lookback=hours_lookback)

    # Nitter検索
    x_search_articles = x_collector.collect_from_search(X_SEARCH_KEYWORDS, max_tweets=50)
    logger.info(f"X search articles collected: {len(x_search_articles)}")

    # RSSHub（特定アカウント）
    x_account_articles = x_collector.collect_from_rsshub(X_ACCOUNTS)
    logger.info(f"X account articles collected: {len(x_account_articles)}")

    # 全記事を統合
    all_articles = rss_articles + x_search_articles + x_account_articles
    logger.info(f"Total articles collected: {len(all_articles)}")

    if not all_articles:
        logger.warning("No articles found in the specified time range")
        sys.exit(0)

    # AI関連記事のみフィルタリング
    ai_articles = [article for article in all_articles if collector.is_ai_related(article)]
    logger.info(f"AI-related articles: {len(ai_articles)} out of {len(all_articles)}")

    if not ai_articles:
        logger.warning("No AI-related articles found")
        sys.exit(0)

    # ステップ2: サプライズ度分析
    logger.info("\n[STEP 2] Analyzing articles with Claude Code (Groq LLaMA 3.1 70B)...")
    analyzer = SurpriseAnalyzer(api_key=os.getenv('GROQ_API_KEY'))
    result = analyzer.analyze_articles(ai_articles)

    if not result:
        logger.error("Analysis failed")
        sys.exit(1)

    # 結果をログ出力
    logger.info("\n=== Analysis Result ===")
    logger.info(f"Selected article: {result['article']['title']}")
    logger.info(f"Source: {result['article']['source']}")
    logger.info(f"URL: {result['article']['link']}")
    logger.info(f"Surprise score: {result['analysis'].get('surprise_score', 'N/A')}")

    # 結果をJSONファイルに保存
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = os.path.join(output_dir, f"analysis_{timestamp}.json")

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2, default=str)
    logger.info(f"Result saved to: {output_file}")

    # ステップ3: レポート生成（Markdown形式）
    logger.info("\n[STEP 3] Generating detailed report...")
    report_file = os.path.join(output_dir, f"report_{timestamp}.md")
    generate_report(result, report_file)
    logger.info(f"Report saved to: {report_file}")

    logger.info("\n=== AI News Analyzer Completed ===")
    logger.info("Report will be posted to GitHub Issues by Actions workflow")


def generate_report(result: Dict, output_file: str):
    """
    詳細レポートをMarkdown形式で生成

    Args:
        result: 分析結果
        output_file: 出力ファイルパス
    """
    article = result['article']
    analysis = result['analysis']

    report = f"""# AIニュース分析レポート

生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 🚀 選定されたニュース

### タイトル
{analysis.get('title_ja', article['title'])}

### ソース
{article['source']} ({article['language']})

### URL
{article['link']}

### 公開日時
{article['published'].strftime('%Y-%m-%d %H:%M %Z')}

---

## 📝 概要

{analysis.get('summary', article['summary'])}

---

## ⚡ なぜサプライズか

"""

    # サプライズ理由
    reasons = analysis.get('surprise_reasons', [])
    for i, reason in enumerate(reasons, 1):
        report += f"{i}. **{reason}**\n"

    report += f"""
---

## 💡 インパクト分析

### 💻 エンジニア視点

{analysis.get('engineer_impact', 'N/A')}

### 💼 ビジネス視点

{analysis.get('business_impact', 'N/A')}

---

## 📊 サプライズスコア

**{analysis.get('surprise_score', 'N/A')} / 100**

---

## 🔍 他候補との比較

{analysis.get('other_candidates_comparison', 'N/A')}

---

## 📋 全候補リスト

"""

    # 全候補を列挙
    all_candidates = result.get('all_candidates', [])
    for i, candidate in enumerate(all_candidates, 1):
        report += f"""
### 候補{i}: {candidate['title'][:80]}
- **ソース**: {candidate['source']}
- **URL**: {candidate['link']}
- **公開日時**: {candidate['published'].strftime('%Y-%m-%d %H:%M %Z')}
- **予備スコア**: {candidate.get('preliminary_score', 0)}

"""

    report += f"""
---

## 🔧 メタデータ

- **分析に使用したモデル**: Claude Code (Groq LLaMA 3.1 70B)
- **フォールバックモード**: {'はい' if result.get('fallback') else 'いいえ'}
- **候補数**: {len(all_candidates)}
- **収集ソース**: RSS, X (Nitter), X (RSSHub)
"""

    # ファイルに書き込み
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)


if __name__ == "__main__":
    main()
