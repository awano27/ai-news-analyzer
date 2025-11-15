"""
AIニュースソースの定義
"""

# RSS/Atomフィードを提供する主要AIニュースソース
NEWS_SOURCES = {
    "english": [
        {
            "name": "TechCrunch AI",
            "url": "https://techcrunch.com/category/artificial-intelligence/feed/",
            "language": "en"
        },
        {
            "name": "VentureBeat AI",
            "url": "https://venturebeat.com/category/ai/feed/",
            "language": "en"
        },
        {
            "name": "The Verge AI",
            "url": "https://www.theverge.com/ai-artificial-intelligence/rss/index.xml",
            "language": "en"
        },
        {
            "name": "MIT Technology Review AI",
            "url": "https://www.technologyreview.com/topic/artificial-intelligence/feed",
            "language": "en"
        },
        {
            "name": "OpenAI Blog",
            "url": "https://openai.com/blog/rss.xml",
            "language": "en"
        },
        {
            "name": "Google AI Blog",
            "url": "https://ai.googleblog.com/feeds/posts/default",
            "language": "en"
        },
        {
            "name": "Anthropic News",
            "url": "https://www.anthropic.com/news/rss.xml",
            "language": "en"
        },
        {
            "name": "Hugging Face Blog",
            "url": "https://huggingface.co/blog/feed.xml",
            "language": "en"
        },
        {
            "name": "DeepMind Blog",
            "url": "https://deepmind.google/blog/rss.xml",
            "language": "en"
        }
    ],
    "japanese": [
        {
            "name": "ITmedia AI+",
            "url": "https://rss.itmedia.co.jp/rss/2.0/aiplus.xml",
            "language": "ja"
        },
        {
            "name": "AINOW",
            "url": "https://ainow.ai/feed/",
            "language": "ja"
        },
        {
            "name": "Ledge.ai",
            "url": "https://ledge.ai/feed/",
            "language": "ja"
        }
    ]
}

# AI関連キーワード（フィルタリング用）
AI_KEYWORDS = [
    # 基本
    "AI", "artificial intelligence", "machine learning", "deep learning",
    "neural network", "transformer", "LLM", "large language model",

    # モデル・技術
    "GPT", "Claude", "Gemini", "Llama", "Mistral", "ChatGPT",
    "diffusion", "GAN", "reinforcement learning", "AGI",

    # 企業
    "OpenAI", "Anthropic", "Google AI", "DeepMind", "Meta AI",
    "Microsoft AI", "Amazon AI", "NVIDIA",

    # アプリケーション
    "generative AI", "computer vision", "NLP", "natural language",
    "image generation", "text-to-image", "voice synthesis",

    # 日本語
    "人工知能", "機械学習", "深層学習", "生成AI", "対話AI",
    "言語モデル", "画像生成", "音声合成"
]

# サプライズ度の高いキーワード（スコアリング用）
SURPRISE_KEYWORDS = {
    "breakthrough": 3,
    "revolutionary": 3,
    "unprecedented": 3,
    "world first": 3,
    "record-breaking": 3,

    "launches": 2,
    "announces": 2,
    "releases": 2,
    "unveils": 2,
    "open source": 2,
    "available now": 2,

    "新発表": 3,
    "世界初": 3,
    "画期的": 3,
    "驚異的": 3,

    "発表": 2,
    "リリース": 2,
    "公開": 2,
    "提供開始": 2,
    "オープンソース": 2
}
