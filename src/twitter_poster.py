"""
X (Twitter) APIを使用して分析結果を投稿
"""

import tweepy
import logging
from typing import Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TwitterPoster:
    def __init__(self, api_key: str, api_secret: str, access_token: str, access_token_secret: str):
        """
        Args:
            api_key: Twitter API Key
            api_secret: Twitter API Secret Key
            access_token: Twitter Access Token
            access_token_secret: Twitter Access Token Secret
        """
        # Twitter API v2 Client
        self.client = tweepy.Client(
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_token_secret
        )

    def post_analysis(self, result: Dict, issue_url: str = None) -> bool:
        """
        分析結果をツイート

        Args:
            result: 分析結果
            issue_url: GitHub IssueのURL（詳細レポートへのリンク）

        Returns:
            成功したらTrue
        """
        if not result or not result.get('article'):
            logger.error("No valid result to post")
            return False

        # ツイート文を生成
        tweet_text = self._format_tweet(result, issue_url)

        try:
            # ツイート投稿
            response = self.client.create_tweet(text=tweet_text)
            logger.info(f"Tweet posted successfully: {response.data['id']}")
            return True

        except Exception as e:
            logger.error(f"Error posting tweet: {str(e)}")
            return False

    def _format_tweet(self, result: Dict, issue_url: str = None) -> str:
        """
        ツイート用のテキストを整形

        Args:
            result: 分析結果
            issue_url: GitHub IssueのURL

        Returns:
            ツイート文（280文字以内）
        """
        article = result['article']
        analysis = result['analysis']

        # 基本フォーマット
        tweet_parts = [
            "🚀 本日のAIサプライズニュース",
            "",
            f"【{analysis.get('title_ja', article['title'][:50])}】",
            ""
        ]

        # サプライズ理由（3つ、各60文字以内）
        reasons = analysis.get('surprise_reasons', [])
        if reasons:
            tweet_parts.append("なぜサプライズ?")
            for i, reason in enumerate(reasons[:3], 1):
                # 60文字以内に切り詰め
                short_reason = reason[:57] + "..." if len(reason) > 60 else reason
                tweet_parts.append(f"✨ {short_reason}")
            tweet_parts.append("")

        # リンク
        tweet_parts.append(f"🔗 {article['link']}")

        # GitHub Issue（詳細レポート）
        if issue_url:
            tweet_parts.append(f"📊 詳細: {issue_url}")

        # ハッシュタグ
        tweet_parts.append("")
        tweet_parts.append("#AI #人工知能 #MachineLearning")

        # 結合
        tweet_text = "\n".join(tweet_parts)

        # 280文字制限チェック
        if len(tweet_text) > 280:
            # 長すぎる場合は削減
            tweet_text = self._shorten_tweet(result, issue_url)

        return tweet_text

    def _shorten_tweet(self, result: Dict, issue_url: str = None) -> str:
        """
        280文字以内に収まるようツイートを短縮

        Args:
            result: 分析結果
            issue_url: GitHub IssueのURL

        Returns:
            短縮されたツイート文
        """
        article = result['article']
        analysis = result['analysis']

        # 短縮版フォーマット
        tweet_parts = [
            "🚀 本日のAIサプライズニュース",
            "",
            f"{analysis.get('title_ja', article['title'][:40])}",
            ""
        ]

        # サプライズ理由を1つだけ
        reasons = analysis.get('surprise_reasons', [])
        if reasons:
            short_reason = reasons[0][:50] + "..." if len(reasons[0]) > 50 else reasons[0]
            tweet_parts.append(f"✨ {short_reason}")
            tweet_parts.append("")

        # リンク
        tweet_parts.append(f"🔗 {article['link']}")

        # GitHub Issue
        if issue_url:
            tweet_parts.append(f"📊 {issue_url}")

        tweet_parts.append("")
        tweet_parts.append("#AI #MachineLearning")

        tweet_text = "\n".join(tweet_parts)

        # さらに長い場合は理由を削除
        if len(tweet_text) > 280:
            tweet_parts = [
                "🚀 本日のAIサプライズニュース",
                "",
                f"{analysis.get('title_ja', article['title'][:60])}",
                "",
                f"🔗 {article['link']}",
                "",
                "#AI"
            ]
            if issue_url:
                tweet_parts.insert(-2, f"📊 {issue_url}")

            tweet_text = "\n".join(tweet_parts)

        return tweet_text[:280]  # 確実に280文字以内

    def post_thread(self, result: Dict, issue_url: str = None) -> bool:
        """
        スレッド形式で詳細を投稿（オプション機能）

        Args:
            result: 分析結果
            issue_url: GitHub IssueのURL

        Returns:
            成功したらTrue
        """
        try:
            # 1つ目のツイート（概要）
            first_tweet_text = self._format_tweet(result, issue_url)
            first_response = self.client.create_tweet(text=first_tweet_text)
            first_tweet_id = first_response.data['id']
            logger.info(f"First tweet posted: {first_tweet_id}")

            # 2つ目のツイート（エンジニア視点）
            analysis = result['analysis']
            engineer_impact = analysis.get('engineer_impact', '')
            if engineer_impact and engineer_impact != 'N/A':
                second_tweet = f"💻 エンジニア視点:\n{engineer_impact[:250]}"
                self.client.create_tweet(
                    text=second_tweet,
                    in_reply_to_tweet_id=first_tweet_id
                )
                logger.info("Second tweet (engineer) posted")

            # 3つ目のツイート（ビジネス視点）
            business_impact = analysis.get('business_impact', '')
            if business_impact and business_impact != 'N/A':
                third_tweet = f"💼 ビジネス視点:\n{business_impact[:250]}"
                self.client.create_tweet(
                    text=third_tweet,
                    in_reply_to_tweet_id=first_tweet_id
                )
                logger.info("Third tweet (business) posted")

            return True

        except Exception as e:
            logger.error(f"Error posting thread: {str(e)}")
            return False
