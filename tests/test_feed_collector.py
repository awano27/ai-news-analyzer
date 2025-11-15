"""
FeedCollectorのテスト
"""

import sys
import os

# srcディレクトリをパスに追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from feed_collector import FeedCollector


def test_collect_feeds():
    """
    フィード収集のテスト（実際のRSSフィードから取得）
    """
    collector = FeedCollector(timezone="Asia/Tokyo", hours_lookback=168)  # 1週間分

    print("Collecting feeds...")
    articles = collector.collect_all_feeds()

    print(f"\nTotal articles collected: {len(articles)}")

    if articles:
        print("\n=== Sample Articles ===")
        for i, article in enumerate(articles[:5], 1):
            print(f"\n{i}. {article['title']}")
            print(f"   Source: {article['source']}")
            print(f"   Published: {article['published']}")
            print(f"   URL: {article['link']}")
            print(f"   Summary: {article['summary'][:100]}...")

    # AI関連フィルタリングのテスト
    ai_articles = [article for article in articles if collector.is_ai_related(article)]
    print(f"\n\nAI-related articles: {len(ai_articles)} out of {len(articles)}")


if __name__ == "__main__":
    test_collect_feeds()
