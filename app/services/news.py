
import requests
import json
import re
from bs4 import BeautifulSoup
import feedparser
import time

from emotion_classfication_model.emotion_classfication_model import get_emotion


def search_google_news(topic, from_date=None, to_date=None, limit=10):
    # Set the API endpoint and parameters
    endpoint = 'https://news.google.com/rss/search?q=' + \
        topic + '&hl=en-US&gl=US&ceid=US:en'
    limit = max(5, min(50, limit))  # Set the limit within the range of 5 to 50

    # Parse the RSS feed from the API
    feed = feedparser.parse(endpoint)

    # Extract the articles from the feed
    articles = []
    for i, entry in enumerate(feed.entries):

        published_date = entry.published_parsed
        if published_date >= from_date:
            continue
        if published_date <= to_date:
            continue


        if i == limit:
            break
        content = clean(entry.description)
        if i == limit:
            break
        article = {
            'title': entry.title,
            'link': entry.link,
            'content': content,
            'published': entry.published,
            'title_emotion': get_emotion(entry.title),
            'content_emotion': get_emotion(content)

        }
        articles.append(article)

    return articles


def search_techcrunch(query, from_date=None, to_date=None, limit=10):
    """
    Search for TechCrunch articles based on a query and a date range.

    Args:
        query (str): Search query.
        limit (int): Maximum number of articles to retrieve.

    Returns:
        List of article objects, where each object contains the following fields:
        - title (str)
        - link (str)
        - date (str)
    """

    API_ENDPOINT = "https://techcrunch.com/wp-json/wp/v2/posts"
    limit = max(5, min(50, limit))  # Set the limit within the range of 5 to 50

    query_params = {"search": query, "per_page": limit}

    response = requests.get(API_ENDPOINT, params=query_params)
    artical_list = []
    if response.ok:
        articles = response.json()
        if len(articles) == 0:
            print("No articles found.")
        else:
            for article in articles:

                published_date = article["date"]
                published_date=time.strptime(published_date, '%Y-%m-%dT%H:%M:%S')
                if published_date >= from_date:
                    continue
                if published_date <= to_date:
                    continue

                title = article["title"]["rendered"]
                link = article["link"]
                date = article["date"]
                content = clean(article['content']['rendered'][:500])
                title_emotion = get_emotion(title),
                content_emotion = get_emotion(content)

                artical_list.append({
                    'title': title,
                    'link': link,
                    'content': content,
                    'published': date,
                    'title_emotion': title_emotion,
                    'content_emotion': content_emotion
                })
    else:
        print(f"Request failed with status code {response.status_code}")
        print(response.content)

    return artical_list


def search_wired_articles(topic, from_date=None, to_date=None, limit=10):
    # Set the API endpoint and parameters
    endpoint = 'https://www.wired.com/wp-json/wp/v2/posts'
    limit = max(5, min(50, limit))  # Set the limit within the range of 5 to 50

    params = {
        'per_page': limit,     # Number of articles to fetch
        'orderby': 'date',  # Order by publish date
        'search': topic    # Search for articles on this topic
    }

    # Send the GET request to the API
    response = requests.get(endpoint, params=params)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        articles = json.loads(response.content)

        # Create a list to store the article titles and links
        results = []

        # Loop through the articles and add their titles and links to the list
        for article in articles:

            published_date=article["date"]
            published_date=time.strptime(published_date,'%Y-%m-%dT%H:%M:%S')
            if published_date >= from_date:
                continue
            if published_date <= to_date:
                continue

            title = article['title']['rendered']
            link = article['link']
            content = clean(article['content']['rendered'][:500])
            date = article["date"]
            title_emotion = get_emotion(title),
            content_emotion = get_emotion(content)

            results.append({
                'title': title,
                'link': link,
                'content': content,
                'published': date,
                'title_emotion': title_emotion,
                'content_emotion': content_emotion

            })

        # Return the list of results
        return results
    else:
        print('Error: Failed to fetch articles')


def clean(content):

    soup = BeautifulSoup(content, 'html.parser')
    content = soup.get_text()  # extract text from HTML tags
    content = re.sub(r'\s+', ' ', content)
    content = re.sub(r'<a\s+href=[^>]+>([^<]+)<\/a>', r'\1', content)

    return content
