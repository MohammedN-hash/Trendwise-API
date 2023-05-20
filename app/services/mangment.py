from services.reddit import get_reddits_with_comments
from services.news import search_google_news,search_techcrunch,search_wired_articles
import datetime

def get_classfied_social_networks(query, fromDate, toDate, subreddit, post_limit, comment_limit): 
    try:
        # Convert limits to an integer
        post_limit = int(post_limit)  
        comment_limit = int(comment_limit)  
       
        # Format dates 
        toDate = datetime.strptime(toDate, '%Y-%m-%d') if toDate != '' else None
        fromDate = datetime.strptime(fromDate, '%Y-%m-%d') if fromDate != '' else None

        reddit_posts_list, reddit_comments_list = get_reddits_with_comments(
            query, fromDate=fromDate, toDate=toDate, subreddit=subreddit, post_limit=post_limit, comment_limit=comment_limit
        )

        return reddit_posts_list, reddit_comments_list 
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None


def get_classfied_news(query, fromDate, toDate, limit):
    try:
        # Convert limit to an integer
        limit = int(limit)  
        toDate = datetime.datetime.strptime(toDate, '%Y/%m/%d')  if toDate != '' else None
        fromDate = datetime.datetime.strptime(fromDate, '%Y/%m/%d')  if fromDate != '' else None
            
        google_news = search_google_news(query, fromDate, toDate, limit)
        techcrunch_news = search_techcrunch(query, fromDate, toDate, limit)
        wired_news = search_wired_articles(query, fromDate, toDate, limit)

        return google_news, techcrunch_news, wired_news
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None, None
