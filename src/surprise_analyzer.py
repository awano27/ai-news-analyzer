"""
Claude APIを使用してニュースのサプライズ度を分析
"""

import anthropic
import json
import logging
from typing import List, Dict, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SurpriseAnalyzer:
    def __init__(self, api_key: str):
        """
        Args:
            api_key: Anthropic APIキー
        """
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = "claude-3-5-sonnet-20241022"

    def analyze_articles(self, articles: List[Dict]) -> Dict:
        """
        複数の記事を分析し、最もサプライズ度が高いものを選定

        Args:
            articles: 記事のリスト

        Returns:
            分析結果（最もサプライズ度が高いニュース + スコア）
        """
        if not articles:
            logger.warning("No articles to analyze")
            return None

        # 候補を2-5件に絞る（APIコスト削減のため）
        candidates = self._select_candidates(articles)
        logger.info(f"Selected {len(candidates)} candidates for detailed analysis")

        # Claude APIで詳細分析
        analysis_result = self._analyze_with_claude(candidates)

        return analysis_result

    def _select_candidates(self, articles: List[Dict], max_candidates: int = 5) -> List[Dict]:
        """
        候補記事を選定（単純なキーワードスコアリング）

        Args:
            articles: 記事のリスト
            max_candidates: 最大候補数

        Returns:
            候補記事のリスト
        """
        from news_sources import SURPRISE_KEYWORDS

        # 各記事にスコアを付与
        for article in articles:
            score = 0
            text = f"{article['title']} {article['summary']}".lower()

            for keyword, points in SURPRISE_KEYWORDS.items():
                if keyword.lower() in text:
                    score += points

            article['preliminary_score'] = score

        # スコアでソートして上位を取得
        sorted_articles = sorted(articles, key=lambda x: x['preliminary_score'], reverse=True)
        return sorted_articles[:max_candidates]

    def _analyze_with_claude(self, candidates: List[Dict]) -> Dict:
        """
        Claude APIで候補記事を詳細分析

        Args:
            candidates: 候補記事のリスト

        Returns:
            分析結果
        """
        # 候補記事をテキスト形式に整形
        candidates_text = self._format_candidates(candidates)

        # プロンプト作成
        prompt = self._create_analysis_prompt(candidates_text)

        try:
            # Claude APIを呼び出し
            message = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                temperature=0.3,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            # レスポンスをパース
            response_text = message.content[0].text
            logger.info(f"Claude API response received: {len(response_text)} chars")

            # JSON形式で結果を抽出
            result = self._parse_claude_response(response_text, candidates)

            return result

        except Exception as e:
            logger.error(f"Error calling Claude API: {str(e)}")
            # エラー時はフォールバック（最も preliminary_score が高いものを返す）
            return self._fallback_selection(candidates)

    def _format_candidates(self, candidates: List[Dict]) -> str:
        """
        候補記事を分析用のテキストに整形

        Args:
            candidates: 候補記事のリスト

        Returns:
            整形されたテキスト
        """
        formatted = []

        for i, article in enumerate(candidates, 1):
            formatted.append(f"""
候補{i}:
タイトル: {article['title']}
ソース: {article['source']}
URL: {article['link']}
公開日時: {article['published'].strftime('%Y-%m-%d %H:%M %Z')}
要約: {article['summary'][:300]}
""")

        return "\n---\n".join(formatted)

    def _create_analysis_prompt(self, candidates_text: str) -> str:
        """
        Claude API用のプロンプトを作成

        Args:
            candidates_text: 候補記事のテキスト

        Returns:
            プロンプト文字列
        """
        return f"""あなたはAIニュース特化のリサーチャー兼アナリストです。

以下の候補ニュースの中から、**サプライズ度が最も高いAI関連ニュースを1件だけ**選び、分析してください。

## 評価基準（サプライズ度）

1. **インパクト**: 性能・価格・ユーザー数・ビジネスインパクトが"桁違い"と言えるか
2. **新規性**: 既存の延長線ではなく、発想・仕組み・スケールが非連続的か
3. **現実性**: すでに利用可能、もしくは具体的な提供開始時期や実動デモが提示されているか
4. **信頼性**: 企業や研究機関などの公式発表、または信頼できる一次情報に裏付けられているか

## 候補ニュース

{candidates_text}

## 出力形式

以下のJSON形式で出力してください:

```json
{{
  "selected_index": 1,
  "title_ja": "日本語タイトル",
  "summary": "3-5行の概要（誰が何を発表し、どのような特徴があり、いつ利用可能か）",
  "surprise_reasons": [
    "インパクト面での驚き（具体的に）",
    "新規性（従来との違い）",
    "現実性（使える/具体的ロードマップ）"
  ],
  "engineer_impact": "エンジニア視点での意味（開発・運用・アーキテクチャへの影響）",
  "business_impact": "ビジネス視点での意味（コスト・収益・戦略への影響）",
  "surprise_score": 85,
  "other_candidates_comparison": "他候補と比較してなぜこれが最もサプライズか"
}}
```

必ずJSONのみを出力してください。
"""

    def _parse_claude_response(self, response_text: str, candidates: List[Dict]) -> Dict:
        """
        Claudeのレスポンスをパースして構造化

        Args:
            response_text: Claudeのレスポンステキスト
            candidates: 候補記事のリスト

        Returns:
            構造化された分析結果
        """
        try:
            # JSONブロックを抽出
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1

            if json_start == -1 or json_end == 0:
                raise ValueError("No JSON found in response")

            json_text = response_text[json_start:json_end]
            analysis = json.loads(json_text)

            # 選択された記事を取得
            selected_index = analysis.get('selected_index', 1) - 1  # 0-indexed
            if selected_index < 0 or selected_index >= len(candidates):
                selected_index = 0

            selected_article = candidates[selected_index]

            # 結果を統合
            result = {
                "article": selected_article,
                "analysis": analysis,
                "all_candidates": candidates
            }

            return result

        except Exception as e:
            logger.error(f"Error parsing Claude response: {str(e)}")
            return self._fallback_selection(candidates)

    def _fallback_selection(self, candidates: List[Dict]) -> Dict:
        """
        Claude API失敗時のフォールバック選択

        Args:
            candidates: 候補記事のリスト

        Returns:
            フォールバック結果
        """
        # preliminary_scoreが最も高いものを選択
        selected = candidates[0] if candidates else None

        return {
            "article": selected,
            "analysis": {
                "selected_index": 1,
                "title_ja": selected['title'] if selected else "",
                "summary": selected['summary'] if selected else "",
                "surprise_reasons": [
                    "（自動分析失敗のため、キーワードスコアで選択）"
                ],
                "engineer_impact": "N/A",
                "business_impact": "N/A",
                "surprise_score": selected.get('preliminary_score', 0) if selected else 0,
                "other_candidates_comparison": "N/A"
            },
            "all_candidates": candidates,
            "fallback": True
        }
