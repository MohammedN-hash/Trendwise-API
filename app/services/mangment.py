from services.reddit import get_reddits_with_comments
from services.news import search_google_news,search_techcrunch,search_wired_articles
import time



def get_classfied_social_networks(query, fromDate, toDate, subreddit,post_limit,comment_limit):

    post_limit = int(post_limit)  # Convert limit to an integer
    comment_limit = int(comment_limit)  # Convert limit to an integer
    fromDate=time.strptime(fromDate, '%Y-%m-%d')
    toDate=time.strptime(toDate, '%Y-%m-%d')

    reddit_posts_list,reddit_comments_list=get_reddits_with_comments(query, fromDate=fromDate, toDate=toDate, subreddit=subreddit,post_limit =post_limit,comment_limit=comment_limit)

    return reddit_posts_list,reddit_comments_list


def get_classfied_news(query, fromDate, toDate,limit):
   
    limit = int(limit)  # Convert limit to an integer
    fromDate=time.strptime(fromDate, '%Y-%m-%d')
    toDate=time.strptime(toDate, '%Y-%m-%d')

    google_news=search_google_news(query,fromDate, toDate,limit)
    techcrunch_news=search_techcrunch(query,fromDate, toDate,limit)
    wired_news=search_wired_articles(query,fromDate, toDate,limit)

    return google_news,techcrunch_news,wired_news