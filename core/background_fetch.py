import threading
import time
import feedparser
from .models import Article
from .utils import rewrite_article, fetch_full_article

RSS_FEEDS = [
    "https://www.lusakatimes.com/feed/",
    "https://www.daily-mail.co.zm/feed/",
    "https://www.zambiareports.com/feed/"
]

FETCH_INTERVAL = 60 * 5  # every 5 minutes


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

                # 🔧 FIX: remove Daily Mail logo images
                if "daily-mail.co.zm" in url:
                    if not image_url or "logo" in image_url.lower():
                        image_url = None

                # Rewrite content
                rewritten_title, rewritten_description, rewritten_content = rewrite_article(
                    title, full_content
                )

                Article.objects.create(
                    title_original=title,
                    title_rewritten=rewritten_title,
                    description_original=full_content,
                    description_rewritten=rewritten_description,
                    content_rewritten=rewritten_content,
                    image_url=image_url,
                    source=feed.feed.get("title", "Unknown Source"),
                    source_url=url
                )

        time.sleep(FETCH_INTERVAL)


def start_background_fetch():
    thread = threading.Thread(target=fetch_articles, daemon=True)
    thread.start()
