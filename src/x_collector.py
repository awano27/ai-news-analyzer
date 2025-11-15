"""
X (Twitter) からAI関連の投稿を収集
Nitter + RSSHub を使用した無料統合
"""

from ntscraper import Nitter
import requests
import logging
from datetime import datetime, timedelta
from typing import List, Dict
import pytz
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class XCollector:
    def __init__(self, timezone: str = "Asia/Tokyo", hours_lookback: int = 24):
        """
        Args:
            timezone: タイムゾーン
            hours_lookback: 何時間前までの投稿を取得するか
        """
        self.timezone = pytz.timezone(timezone)
        self.hours_lookback = hours_lookback
        self.cutoff_time = datetime.now(self.timezone) - timedelta(hours=hours_lookback)

        # Nitterインスタンス（X検索用）
        try:
            self.scraper = Nitter(log_level=1, skip_instance_check=False)
        except Exception as e:
            logger.warning(f"Nitter initialization failed: {e}")
            self.scraper = None

    def collect_from_search(self, keywords: List[str], max_tweets: int = 50) -> List[Dict]:
        """
        Nitter経由でX検索から投稿を収集

        Args:
            keywords: 検索キーワードリスト
            max_tweets: 最大取得数

        Returns:
            投稿のリスト
        """
        if not self.scraper:
            logger.warning("Nitter scraper not available, skipping X search")
            return []

        articles = []

        # キーワードをOR検索クエリに変換
        query = " OR ".join(keywords)

        try:
            logger.info(f"Searching X for: {query}")

            # Nitterで検索
            tweets = self.scraper.get_tweets(query, mode='term', number=max_tweets)

            for tweet in tweets.get('tweets', []):
                # 投稿日時を解析
                published_date = self._parse_tweet_date(tweet.get('date'))

                if not published_date or published_date < self.cutoff_time:
                    continue

                # リンクを抽出
                link = tweet.get('link', '')
                if not link:
                    continue

                article = {
                    'title': tweet.get('text', '')[:100],  # 最初の100文字をタイトルとして使用
                    'link': link,
                    'published': published_date,
                    'summary': tweet.get('text', ''),
                    'source': f"X (@{tweet.get('user', {}).get('name', 'unknown')})",
                    'language': 'en' if self._is_english(tweet.get('text', '')) else 'ja'
                }

                articles.append(article)

            logger.info(f"Collected {len(articles)} tweets from X search")

        except Exception as e:
            logger.error(f"Error collecting from X search: {str(e)}")

        return articles

    def collect_from_rsshub(self, accounts: List[str]) -> List[Dict]:
        """
        RSSHub経由で特定アカウントの投稿を収集

        Args:
            accounts: Xアカウント名のリスト（@なし）

        Returns:
            投稿のリスト
        """
        articles = []

        # 公開RSSHubインスタンス
        rsshub_base = "https://rsshub.app/twitter/user"

        for account in accounts:
            try:
                url = f"{rsshub_base}/{account}"
                logger.info(f"Fetching RSS from RSSHub: {account}")

                response = requests.get(url, timeout=10)

                if response.status_code != 200:
                    logger.warning(f"Failed to fetch RSS for @{account}: {response.status_code}")
                    continue

                # RSSフィードを解析
                import feedparser
                feed = feedparser.parse(response.content)

                for entry in feed.entries:
                    # 公開日時を取得
                    published_date = self._parse_date(entry)

                    if not published_date or published_date < self.cutoff_time:
                        continue

                    # 要約を取得
                    summary = ""
                    if hasattr(entry, 'summary'):
                        summary = self._clean_html(entry.summary)
                    elif hasattr(entry, 'description'):
                        summary = self._clean_html(entry.description)

                    article = {
                        'title': entry.title if hasattr(entry, 'title') else summary[:100],
                        'link': entry.link if hasattr(entry, 'link') else '',
                        'published': published_date,
                        'summary': summary,
                        'source': f"X (@{account})",
                        'language': 'en' if self._is_english(summary) else 'ja'
                    }

                    articles.append(article)

                logger.info(f"Collected {len([a for a in articles if a['source'] == f'X (@{account})'])} tweets from @{account}")

            except Exception as e:
                logger.error(f"Error collecting from @{account}: {str(e)}")

        return articles

    def _parse_tweet_date(self, date_str: str) -> datetime:
        """
        ツイートの日時文字列を解析

        Args:
            date_str: 日時文字列

        Returns:
            datetime オブジェクト
        """
        if not date_str:
            return None

        try:
            # Nitterのフォーマット: "Jan 1, 2025 · 12:00 PM UTC"
            # 簡略化のため、現在時刻を使用（より正確な解析は必要に応じて実装）
            return datetime.now(self.timezone)
        except Exception as e:
            logger.warning(f"Failed to parse date: {date_str}, error: {e}")
            return None

    def _parse_date(self, entry) -> datetime:
        """
        RSSエントリから日時を解析

        Args:
            entry: feedparserのエントリ

        Returns:
            datetime オブジェクト
        """
        date_tuple = None
        if hasattr(entry, 'published_parsed') and entry.published_parsed:
            date_tuple = entry.published_parsed
        elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
            date_tuple = entry.updated_parsed

        if date_tuple:
            dt = datetime(*date_tuple[:6])
            dt_utc = pytz.utc.localize(dt)
            return dt_utc.astimezone(self.timezone)

        return None

    def _clean_html(self, html_text: str) -> str:
        """
        HTMLタグを除去

        Args:
            html_text: HTML文字列

        Returns:
            プレーンテキスト
        """
        if not html_text:
            return ""

        soup = BeautifulSoup(html_text, 'lxml')
        text = soup.get_text(separator=' ', strip=True)
        return text[:500]

    def _is_english(self, text: str) -> bool:
        """
        テキストが英語かどうかを判定

        Args:
            text: テキスト

        Returns:
            英語ならTrue
        """
        if not text:
            return True

        # 簡易判定: ASCIIが70%以上なら英語
        ascii_chars = sum(1 for c in text if ord(c) < 128)
        return (ascii_chars / len(text)) > 0.7
