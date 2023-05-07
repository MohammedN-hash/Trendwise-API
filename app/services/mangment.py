from services.reddit import get_reddits_with_comments
from emotion_classfication_model.emotion_classfication_model import  get_emotion



def get_all_classfied_data(query, fromDate, toDate, subreddit,post_limit,comment_limit):
    
    reddit_posts_list,reddit_comments_list=get_reddits_with_comments(query, fromDate=fromDate, toDate=toDate, subreddit=subreddit,post_limit =post_limit,comment_limit=comment_limit)


    return reddit_posts_list,reddit_comments_list