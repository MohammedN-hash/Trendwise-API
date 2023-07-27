
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder

from services.mangment import get_classfied_social_networks,get_classfied_news
from services.google_trends_provider import get_trends

from services.latest_news import latest_news


router = APIRouter(
    responses={404: {"description": "Not found"}},

)





@router.get('/social_networks')
async def get_social_networks(query, from_date, to_date, subreddit,post_limit,comment_limit):

    reddit_posts_list,reddit_comments_list=await get_classfied_social_networks(query, from_date, to_date, subreddit,post_limit,comment_limit)
    # convert the results to a JSON-serializable format using jsonable_encoder
    results = {
        "posts": jsonable_encoder(reddit_posts_list),
        "comments": jsonable_encoder(reddit_comments_list)
    }
    
    # return the results as JSON
    return results

@router.get('/google_trend')
async def get_google_trend(query,region, resolution, from_date, to_date):

    return get_trends(query, region=region, resolution=resolution, from_date=from_date, to_date=to_date,language='en-US' )


@router.get('/get_news')
async def get_news(query, from_date, to_date,limit):

    # Get data
    google_news,techcrunch_news,wired_news= await get_classfied_news(query, from_date, to_date,limit)
                                                 
    # convert the results to a JSON-serializable format using jsonable_encoder
        # Convert the results to a JSON-serializable format using jsonable_encoder
    results = {
        "google_news": jsonable_encoder(await google_news),
        "techcrunch_news": jsonable_encoder(await techcrunch_news),
        "wired_news": jsonable_encoder(await wired_news)
    }
    

    return results



@router.get("/latest-news/")
async def get_latest_news(genre: str = 'news'):
    """
    Get the latest news without a specific topic.

    Args:
        genre (str): Genre of the news articles. (Optional, default: 'news')

    Returns:
        List of article objects, where each object contains the following fields:
        - title (str)
        - link (str)
        - content (str)
        - published (datetime)
        - genre (str)
    """
    return await latest_news(genre)