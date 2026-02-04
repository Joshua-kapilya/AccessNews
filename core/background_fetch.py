import threading
import time
import feedparser
from django.db import IntegrityError
from .models import Article
from .utils import rewrite_article, fetch_full_article

RSS_FEEDS = [
    "https://www.lusakatimes.com/feed/",
    "https://www.daily-mail.co.zm/feed/",
    "https://www.zambiareports.com/feed/"
]

FETCH_INTERVAL = 60 * 5  # every 5 minutes
DAILY_MAIL_LOGO = "/static/images/logo.png"

# 🔹 Keyword lists per category
CATEGORY_KEYWORDS = {
    "Politics": ["politics", "government", "president", "minister", "election", "parliament"],
    "Business": ["business", "market", "stock", "economy", "investment", "finance"],
    "Sports": ["sport", "football", "soccer", "basketball", "tennis", "rugby", "match", "league"],
    "Technology": ["tech", "technology", "software", "app", "ai", "artificial intelligence", "gadget"],
    "Entertainment": ["entertainment", "movie", "music", "celebrity", "film", "tv", "show"],
    "Health": ["health", "disease", "covid", "virus", "medicine", "hospital", "fitness"],
}


def assign_category(title, content):
    """
    Assign a category based on keywords in title + content.
    Returns a string category or 'Other'.
    """
    text_lower = (title + " " + content).lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword in text_lower for keyword in keywords):
            return category
    return "Other"


def fetch_articles():
    while True:
        for feed_url in RSS_FEEDS:
            feed = feedparser.parse(feed_url)

            for entry in feed.entries[:10]:
                url = entry.link
                if not url or Article.objects.filter(source_url=url).exists():
                    continue

                title = entry.title

                # Fetch full content + image
                full_content, image_url = fetch_full_article(url)

                # 🔧 Daily Mail → force OUR logo
                if "daily-mail.co.zm" in url:
                    image_url = DAILY_MAIL_LOGO

                # Rewrite content
                rewritten_title, rewritten_description, rewritten_content = rewrite_article(
                    title, full_content
                )

                # 🔹 Assign category
                category = assign_category(title, full_content)

                try:
                    Article.objects.create(
                        title_original=title,
                        title_rewritten=rewritten_title,
                        description_original=full_content,
                        description_rewritten=rewritten_description,
                        content_rewritten=rewritten_content,
                        image_url=image_url,
                        source=feed.feed.get("title", "Unknown Source"),
                        source_url=url,
                        category=category  # ← new field
                    )
                except IntegrityError:
                    pass

        time.sleep(FETCH_INTERVAL)


def start_background_fetch():
    thread = threading.Thread(target=fetch_articles, daemon=True)
    thread.start()
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     