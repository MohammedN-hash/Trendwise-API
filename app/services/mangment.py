from services.social_networks_provider import get_reddits_with_comments
from services.news_provider import search_google_news,search_techcrunch,search_wired_articles
import datetime

async def get_classfied_social_networks(query, from_date, to_date, subreddit, post_limit, comment_limit): 
    try:
        # Convert limits to an integer
        post_limit = int(post_limit)  
        comment_limit = int(comment_limit)  
       
        # Format dates 
        to_date = datetime.datetime.strptime(to_date,'%Y-%m-%d') if to_date != '' else None
        from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d') if from_date != '' else None

        reddit_posts_list, reddit_comments_list = get_reddits_with_comments(
            query, from_date=from_date, to_date=to_date, subreddit=subreddit, post_limit=post_limit, comment_limit=comment_limit
        )

        return reddit_posts_list, reddit_comments_list 
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None


async def get_classfied_news(query, from_date, to_date, limit):
    try:
        # Convert limit to an integer
        limit = int(limit)  
        to_date = datetime.datetime.strptime(to_date, '%Y-%m-%d')  if to_date != '' else None
        from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d')  if from_date != '' else None

        google_news = search_google_news(query, from_date, to_date, limit)
        techcrunch_news = search_techcrunch(query, from_date, to_date, limit)
        wired_news = search_wired_articles(query, from_date, to_date, limit)

        return google_news, techcrunch_news, wired_news
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None, None
