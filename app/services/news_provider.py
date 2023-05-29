
import requests
import json
import re
from bs4 import BeautifulSoup
import feedparser

from datetime import datetime, timedelta,timezone

from emotion_classfication_model.emotion_classfication_model import get_emotion


async def search_google_news(topic, from_date=None, to_date=None, limit=10):
    try:
        # Set the API endpoint and parameters
        endpoint = 'https://news.google.com/rss/search?q=' + \
            topic + '&hl=en-US&gl=US&ceid=US:en'
        # Set the limit within the range of 5 to 50
        limit = max(5, min(50, limit))  
        # set up default time if not selected bu user
        last_week = datetime.now() - timedelta(days=7)
        from_date = from_date if from_date != '' else last_week
        to_date = to_date if to_date != '' else datetime.now()


        # Parse the RSS feed from the API
        feed = feedparser.parse(endpoint)

        # Extract the articles from the feed
        articles = []
        for i, entry in enumerate(feed.entries):

            # Format date
            published_date = entry.published_parsed
            published_date =datetime(*published_date[:6])
            # check date range is between the selected intervel
            check_date = from_date <= published_date <= to_date

            if check_date:

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
    except Exception as e:
        print(f"An error occurred: {e}")
        return articles


async def search_techcrunch(query, from_date=None, to_date=None, limit=10):
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
    print('---------------------------2')

    try:
        API_ENDPOINT = "https://techcrunch.com/wp-json/wp/v2/posts"
        # Set the limit within the range of 5 to 50
        limit = max(5, min(50, limit))  
        # set up default time if not selected bu user
        last_week = datetime.now() - timedelta(days=7)
        from_date = from_date if from_date != '' else last_week
        to_date = to_date if to_date != '' else datetime.now()


        query_params = {"search": query, "per_page": limit}

        response = requests.get(API_ENDPOINT, params=query_params)
        artical_list = []
        if response.ok:
            articles = response.json()
            if len(articles) >= 0:

                for article in articles:

                    # Format date
                    published_date = article["date"]
                    date_format = '%Y-%m-%dT%H:%M:%S'
                    published_date = datetime.strptime(published_date, date_format)
                    # check date range is between the selected intervel
                    check_date = from_date <= published_date <= to_date
                    if check_date:

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
                print("No articles found.")

        else:
            print(f"Request failed with status code {response.status_code}")


        return artical_list
    except Exception as e:
        print(f"An error occurred: {e}")
        return artical_list

async def search_wired_articles(topic, from_date, to_date, limit=10):
    try:
        # Set the API endpoint and parameters
        api_key = "27fa7d69a2ba4aed8bc11abacae6afcf"
        limit = max(5, min(50, limit))  # Set the limit within the range of 5 to 50

        endpoint = f"https://newsapi.org/v2/everything?q={topic}&apiKey={api_key}"

        # Send the GET request to the API
        response = requests.get(endpoint)
        from_date=from_date.replace(tzinfo=timezone.utc)
        to_date=to_date.replace(tzinfo=timezone.utc)
        # Check if the request was successful (status code 200)
        results = []
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            articles = data["articles"]

            # Loop through the articles and process the desired fields
            for article in articles:
                published_date = article["publishedAt"]
                published_date = datetime.fromisoformat(published_date.replace("Z", "+00:00")).replace(tzinfo=None)

                # Convert published date to UTC
                published_date = published_date.replace(tzinfo=timezone.utc)


                # Check if the published date is within the selected interval
                if from_date <= published_date <= to_date:
                    title = article["title"]
                    link = article["url"]
                    content = article.get("content", "")
                    title_emotion = get_emotion(title),
                    content_emotion = get_emotion(content)

                    results.append({
                        'title': title,
                        'link': link,
                        'content': content,
                        'published': published_date,
                        'title_emotion': title_emotion,
                        'content_emotion': content_emotion
                    })

                    # Break the loop if the desired limit is reached
                    if len(results) >= limit:
                        break

        return results

    except requests.exceptions.RequestException as e:
        print("An error occurred while making the request:", str(e))
        return []
    except (KeyError, ValueError, TypeError) as e:
        print("An error occurred while processing the response:", str(e))
        return []
    

def clean(content):

    soup = BeautifulSoup(content, 'html.parser')
    content = soup.get_text()  # extract text from HTML tags
    content = re.sub(r'\s+', ' ', content)
    content = re.sub(r'<a\s+href=[^>]+>([^<]+)<\/a>', r'\1', content)

    return content
