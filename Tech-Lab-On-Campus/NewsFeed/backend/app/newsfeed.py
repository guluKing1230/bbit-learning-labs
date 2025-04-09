"""Module for retrieving newsfeed information."""

from dataclasses import dataclass
from datetime import datetime

from app.utils.redis import REDIS_CLIENT

@dataclass
class Article:
    """Dataclass for an article."""

    author: str
    title: str
    body: str
    publish_date: datetime
    image_url: str
    url: str


def format_article(entry):
    return Article(
        author = entry["author"],
        title = entry["title"],
        body = entry["text"],
        publish_date = datetime.fromisoformat(entry["published"]),
        image_url = entry["thread"]["main_image"],
        url = entry["url"]
    )

def get_all_news() -> list[Article]:
    """Get all news articles from the datastore."""
    # 1. Use Redis client to fetch all articles
    # 2. Format the data into articles
    # 3. Return a list of the articles formatted 
    res = []
    all_articles: list[dict] = REDIS_CLIENT.get_entry("all_articles")

    if all_articles is None:
        return res

    for article in all_articles:
        res.append(format_article(article))
    return res


def get_featured_news() -> Article | None:
    """Get the featured news article from the datastore."""
    # 1. Get all the articles
    # 2. Return as a list of articles sorted by most recent date
    all_articles = get_all_news()
    if not all_articles:
        return None
    else:
        return sorted(all_articles, key=lambda article: article.publish_date, reverse=True)[0]
