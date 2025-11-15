"""
RSSフィードからニュース記事を収集
"""

import feedparser
import requests
from datetime import datetime, timedelta
from typing import List, Dict
import pytz
from bs4 import BeautifulSoup
import logging

from news_sources import NEWS_SOURCES, AI_KEYWORDS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FeedCollector:
    def __init__(self, timezone: str = "Asia/Tokyo", hours_lookback: int = 24):
        """
        Args:
            timezone: タイムゾーン (例: "Asia/Tokyo")
            hours_lookback: 何時間前までの記事を取得するか
        """
        self.timezone = pytz.timezone(timezone)
        self.hours_lookback = hours_lookback
        self.cutoff_time = datetime.now(self.timezone) - timedelta(hours=hours_lookback)

    def collect_all_feeds(self) -> List[Dict]:
        """
        全ソースからフィードを収集

        Returns:
            記事のリスト
        """
        all_articles = []

        # 英語ソース
        for source in NEWS_SOURCES["english"]:
            articles = self._collect_from_source(source)
            all_articles.extend(articles)
            logger.info(f"Collected {len(articles)} articles from {source['name']}")

        # 日本語ソース
        for source in NEWS_SOURCES["japanese"]:
            articles = self._collect_from_source(source)
            all_articles.extend(articles)
            logger.info(f"Collected {len(articles)} articles from {source['name']}")

        # 時刻でフィルタリング
        recent_articles = self._filter_by_time(all_articles)
        logger.info(f"Total recent articles (last {self.hours_lookback}h): {len(recent_articles)}")

        # 重複削除（URLベース）
        unique_articles = self._remove_duplicates(recent_articles)
        logger.info(f"Unique articles after deduplication: {len(unique_articles)}")

        return unique_articles

    def _collect_from_source(self, source: Dict) -> List[Dict]:
        """
        単一ソースから記事を収集

        Args:
            source: ソース情報 (name, url, language)

        Returns:
            記事のリスト
        """
        articles = []

        try:
            # RSSフィードを取得
            feed = feedparser.parse(source["url"])

            for entry in feed.entries:
                # 必須フィールドの存在確認
                if not hasattr(entry, 'title') or not hasattr(entry, 'link'):
                    continue

                # 公開日時を取得
                published_date = self._parse_date(entry)
                if not published_date:
                    # 日時が取得できない場合は現在時刻とする
                    published_date = datetime.now(self.timezone)

                # 要約/説明を取得
                summary = ""
                if hasattr(entry, 'summary'):
                    summary = self._clean_html(entry.summary)
                elif hasattr(entry, 'description'):
                    summary = self._clean_html(entry.description)

                article = {
                    "title": entry.title,
                    "link": entry.link,
                    "published": published_date,
                    "summary": summary,
                    "source": source["name"],
                    "language": source["language"]
                }

                articles.append(article)

        except Exception as e:
            logger.error(f"Error collecting from {source['name']}: {str(e)}")

        return articles

    def _parse_date(self, entry) -> datetime:
        """
        RSSエントリから日時を解析

        Args:
            entry: feedparserのエントリ

        Returns:
            datetime オブジェクト（タイムゾーン付き）
        """
        # published_parsed または updated_parsed を使用
        date_tuple = None
        if hasattr(entry, 'published_parsed') and entry.published_parsed:
            date_tuple = entry.published_parsed
        elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
            date_tuple = entry.updated_parsed

        if date_tuple:
            # time.struct_time から datetime に変換
            dt = datetime(*date_tuple[:6])
            # UTCとして解釈し、指定タイムゾーンに変換
            dt_utc = pytz.utc.localize(dt)
            return dt_utc.astimezone(self.timezone)

        return None

    def _clean_html(self, html_text: str) -> str:
        """
        HTMLタグを除去してプレーンテキストに変換

        Args:
            html_text: HTML文字列

        Returns:
            プレーンテキスト
        """
        if not html_text:
            return ""

        soup = BeautifulSoup(html_text, 'lxml')
        text = soup.get_text(separator=' ', strip=True)
        return text[:500]  # 最大500文字

    def _filter_by_time(self, articles: List[Dict]) -> List[Dict]:
        """
        指定時間内の記事のみをフィルタリング

        Args:
            articles: 記事のリスト

        Returns:
            フィルタリングされた記事のリスト
        """
        return [
            article for article in articles
            if article["published"] >= self.cutoff_time
        ]

    def _remove_duplicates(self, articles: List[Dict]) -> List[Dict]:
        """
        URLベースで重複記事を除去

        Args:
            articles: 記事のリスト

        Returns:
            重複除去後の記事のリスト
        """
        seen_urls = set()
        unique_articles = []

        for article in articles:
            if article["link"] not in seen_urls:
                seen_urls.add(article["link"])
                unique_articles.append(article)

        return unique_articles

    def is_ai_related(self, article: Dict) -> bool:
        """
        記事がAI関連かどうかを判定

        Args:
            article: 記事

        Returns:
            AI関連ならTrue
        """
        text = f"{article['title']} {article['summary']}".lower()

        for keyword in AI_KEYWORDS:
            if keyword.lower() in text:
                return True

        return False
