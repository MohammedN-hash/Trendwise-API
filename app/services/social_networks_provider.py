import pandas as pd
from services.utilities  import is_english
import praw
from datetime import datetime, timedelta
from emotion_classfication_model.emotion_classfication_model import  get_emotion

#Reddit Authentication
CLIENT_ID='mLBpma4aso8gX60SizAjjA'
SECRET_TOKEN ='TkUYeICJW0X3aEuRch-jFwkLkYO10w'
username='moanwereryani'
password='5ubSTC5bwAndYbW'
base_url = 'https://www.reddit.com/'
user_agent='EmoMetrics0.1'

def get_reddits_with_comments(query, fromDate='', toDate='', subreddit='all',post_limit = 50,comment_limit=50):
    # set up  Reddit API credentials
    reddit = praw.Reddit(client_id=CLIENT_ID,
                        client_secret=SECRET_TOKEN,
                        user_agent=user_agent,
                        check_for_async=False)

    post_limit = max(5, min(50, post_limit))  # Set the limit within the range of 5 to 50
    comment_limit = max(5, min(50, comment_limit))  # Set the limit within the range of 5 to 50
    
    
    # set up default time if not selected bu user
    last_week = datetime.now() - timedelta(days=7)

    start_epoch = fromDate if fromDate != '' else last_week
    end_epoch = toDate if toDate != '' else datetime.now()




    # create an empty list to store the data
    posts = []
    comments  = []
    i=0
    # perform the search
    for post in reddit.subreddit(subreddit).search(query, sort='new',
                                                  limit=post_limit, params={'after': start_epoch, 'before': end_epoch}):
        i=0
        if is_english(post.title): 
          posts.append({'id': post.id,
                      'text': post.title,
                      'author': post.author.name if post.author else '[deleted]',
                      'created_utc': post.created_utc,
                      'num_comments': post.num_comments,
                      'permalink': f"https://www.reddit.com{post.permalink}",
                      'score': post.score,
                      'emotion':get_emotion(post.title)})
      # iterate over the search results and extract the desired data
          for comment in post.comments.list():
              if i == comment_limit:
                break  
              if isinstance(comment, praw.models.MoreComments):
                # skip over any MoreComments objects in the loop, which should prevent the code from trying to access the author attribute of those objects.
                continue
              if is_english(comment.body):  
                comments.append({'post_id': post.id,
                              'id': comment.id,
                              'author': comment.author.name if comment.author else '[deleted]',
                              'created_utc': comment.created_utc,
                              'text': comment.body,
                              'ups': comment.ups,
                              'downs': comment.downs,
                              'emotion':get_emotion(comment.body)})
    return  posts, comments
