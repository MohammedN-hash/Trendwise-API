import requests
from bs4 import BeautifulSoup
import feedparser
from typing import List

# Function to clean HTML content
def clean(content):
    soup = BeautifulSoup(content, 'html.parser')
    return soup.get_text()

# Function to search Google News
async def search_google_news(category='', limit=10):
    try:
        # Set the API endpoint and parameters
        if not category:

            endpoint = f'https://news.google.com/rss?&hl=en-US&gl=US&ceid=US:en'
        else:
            endpoint = f'https://news.google.com/rss/search?q={category}&hl=en-US&gl=US&ceid=US:en'

        # Parse the RSS feed from the API
        feed = feedparser.parse(endpoint)

        # Extract the articles from the feed
        articles = []
        for entry in feed.entries:
            articles.append({
                'source': 'google',
                'title': clean(entry.title),
                'link': entry.link,
                'content': clean(entry.description),
                'published': entry.published,
            })
            # Break the loop if the desired limit is reached
            if len(articles) >= limit:
                break

        return articles

    except Exception as e:
        print(f"An error occurred while searching Google News: {e}")
        return []

# Function to search TechCrunch articles
async def search_techcrunch(category='', limit=10):
    try:
        API_ENDPOINT = "https://techcrunch.com/wp-json/wp/v2/posts"

        # Set the limit within the range of 5 to 50
        limit = max(5, min(50, limit))

        query_params = {"categories": category, "per_page": limit}
        response = requests.get(API_ENDPOINT, params=query_params)

        articles = []
        if response.ok:
            articles_data = response.json()
            for article in articles_data:
                articles.append({
                    'source': 'techcrunch',
                    'title': clean(article["title"]["rendered"]),
                    'link': article["link"],
                    'content': clean(article['content']['rendered'][:500]),
                    'published': article["date"],
                })
                # Break the loop if the desired limit is reached
                if len(articles) >= limit:
                    break
        else:
            print(f"Request to TechCrunch API failed with status code {response.status_code}")

        return articles

    except Exception as e:
        print(f"An error occurred while searching TechCrunch: {e}")
        return []

# Function to search Wired articles
async def news_api(category='', limit=10):
    try:
        api_key = "27fa7d69a2ba4aed8bc11abacae6afcf"
        limit = max(5, min(50, limit))  # Set the limit within the range of 5 to 50

        if not category:
            endpoint = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
        else:
            endpoint = f"https://newsapi.org/v2/top-headlines/sources?category={category}&apiKey={api_key}"
        

        # Send the GET request to the API
        response = requests.get(endpoint)

        articles = []
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            articles_data = data.get("articles", [])

            for article in articles_data:
                articles.append({
                    'source': 'wired',
                    'title': clean(article["title"]),
                    'link': article["url"],
                    'content': clean(article.get("description", "")),
                    'published': article.get("publishedAt"),
                })
                # Break the loop if the desired limit is reached
                if len(articles) >= limit:
                    break
        else:
            print(f"Request to Wired API failed with status code {response.status_code}")

        return articles

    except Exception as e:
        print(f"An error occurred while searching Wired articles: {e}")
        return []

async def latest_news(category: str = '', limit: int = 10) -> List[dict]:
    """
    Get the latest news based on the category.

    Args:
        category (str): Category of the news articles. (Optional, default: '')
                        If no category is provided, retrieve the latest news from all sources.
        limit (int): Maximum number of articles to retrieve. (Optional, default: 10)

    Returns:
        List of article objects, where each object contains the following fields:
        - source (str): Source of the news articles.
        - title (str)
        - link (str)
        - content (str)
        - published (str)
    """
    articles = []
    genre_articles = await search_google_news(category=category,limit=limit)
    articles.extend(genre_articles)
    genre_articles = await search_techcrunch(category=category, limit=limit)
    articles.extend(genre_articles)
    genre_articles = await news_api(category=category, limit=limit)
    articles.extend(genre_articles)

        # Add other news sources based on the category if needed

    if not articles:
        # No news articles found for the selected category
        return []

    return articles
