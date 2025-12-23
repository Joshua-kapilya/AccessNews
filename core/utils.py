import re
from newspaper import Article as NewsPaperArticle

def rewrite_text(text):
    if not text:
        return ""

    # Normalize spaces first
    text = re.sub(r'\s+', ' ', text).strip()

    # Light rewrite (sentence-safe)
    replacements = {
        "said that": "said",
        "according to": "as reported by",
        "reported that": "reported",
        "has been": "was",
        "is said to be": "is believed to be",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    # ✅ FORCE PARAGRAPHS (KEY FIX)
    # Break into readable paragraphs every 2–3 sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)

    paragraphs = []
    chunk = []

    for sentence in sentences:
        chunk.append(sentence)
        if len(chunk) >= 3:
            paragraphs.append(" ".join(chunk))
            chunk = []

    if chunk:
        paragraphs.append(" ".join(chunk))

    return "\n\n".join(paragraphs)


def rewrite_article(title, content):
    """
    Returns:
    1️⃣ rewritten_title
    2️⃣ rewritten_description (short teaser, first 2 sentences)
    3️⃣ rewritten_content (full rewritten content)
    """
    rewritten_title = rewrite_text(title)
    rewritten_content = rewrite_text(content)

    # Short teaser = first 2 sentences ONLY (no paragraphs)
    flat_text = re.sub(r'\s+', ' ', rewritten_content)
    sentences = re.split(r'(?<=[.!?])\s+', flat_text)
    rewritten_description = " ".join(sentences[:2])

    return rewritten_title, rewritten_description, rewritten_content


def fetch_full_article(url):
    """
    Scrape full article content and top image from a URL.
    Returns (content, image_url)
    """
    try:
        article = NewsPaperArticle(url)
        article.download()
        article.parse()

        content = article.text.strip()
        image_url = article.top_image if article.top_image else ""

        return content, image_url
    except:
        return "", ""
