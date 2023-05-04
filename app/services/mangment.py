from services.reddit import get_reddits_with_comments
from emotion_classfication_model.emotion_classfication_model import  get_emotion



def get_all_classfied_data(query, fromDate='', toDate='', subreddit='all',post_limit = 100):
    
    reddit_posts_list,reddit_comments_list=get_reddits_with_comments(query, fromDate='', toDate='', subreddit='all',post_limit = 100)


    return reddit_posts_list,reddit_comments_list