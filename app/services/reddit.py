import pandas as pd
from services.util import is_english
import praw
import datetime as dt
from emotion_classfication_model.emotion_classfication_model import  get_emotion

#Reddit Authentication

CLIENT_ID='mLBpma4aso8gX60SizAjjA'
SECRET_TOKEN ='TkUYeICJW0X3aEuRch-jFwkLkYO10w'
username='moanwereryani'
password='5ubSTC5bwAndYbW'
base_url = 'https://www.reddit.com/'
user_agent='EmoMetrics0.1'

def get_reddits_with_comments(query, fromDate='', toDate='', subreddit='all',post_limit = 100):
    # set up your Reddit API credentials
    reddit = praw.Reddit(client_id=CLIENT_ID,
                        client_secret=SECRET_TOKEN,
                        user_agent=user_agent,
                        check_for_async=False)

    # set up the search query
    query = query
    # specify a specific subreddit
    subreddit = subreddit  

    # set up the time range for the search
    last_week = int((dt.datetime.now() - dt.timedelta(days=7)).timestamp())
    start_epoch = int(dt.datetime.timestamp(dt.datetime.strptime(fromDate, '%Y-%m-%d'))) if fromDate != '' else last_week   
    end_epoch = int(dt.datetime.timestamp(dt.datetime.strptime(toDate, '%Y-%m-%d'))) if toDate != '' else int(dt.datetime.now().timestamp())

    comment_limit = 500

    # perform the search
    # create an empty list to store the data
    posts = []
    comments  = []
    i=0
    for post in reddit.subreddit(subreddit).search(query, sort='new',
                                                  limit=post_limit, params={'after': start_epoch, 'before': end_epoch}):
        i=0
        if is_english(post.title): 
          posts.append({'id': post.id,
                      'title': post.title,
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
                              'body': comment.body,
                              'ups': comment.ups,
                              'downs': comment.downs,
                              'emotion':get_emotion(comment.body)})
    # create Pandas DataFrame from the collected data
    return  pd.DataFrame(posts).values.tolist(), pd.DataFrame(comments).values.tolist()
