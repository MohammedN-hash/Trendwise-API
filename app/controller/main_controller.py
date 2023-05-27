
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder

from services.mangment import get_classfied_social_networks,get_classfied_news
from services.google_trends_provider import get_trends



router = APIRouter(
    responses={404: {"description": "Not found"}},

)





@router.get('/social-networks')
async def get_social_networks(query, from_date, to_date, subreddit,post_limit,comment_limit):

    reddit_posts_list,reddit_comments_list=get_classfied_social_networks(query, from_date, to_date, subreddit,post_limit,comment_limit)
    # convert the results to a JSON-serializable format using jsonable_encoder
    results = {
        "posts": jsonable_encoder(reddit_posts_list),
        "comments": jsonable_encoder(reddit_comments_list)
    }
    
    # return the results as JSON
    return results

@router.get('/google-trend')
async def get_google_trend(query,region, resolution, from_date, to_date):

    return get_trends(query, region=region, resolution=resolution, from_date=from_date, to_date=to_date,language='en-US' )


@router.get('/get-news')
async def get_news(query, from_date, to_date,limit):

    # Get data
    googleNews,techcrunchNews,wired_news=get_classfied_news(query, from_date, to_date,limit)
                                                 
    # convert the results to a JSON-serializable format using jsonable_encoder
    results = {
        "googleNews": jsonable_encoder(googleNews),
        "techcrunchNews": jsonable_encoder(techcrunchNews),
        "wired_news": jsonable_encoder(wired_news)
    }
    

    return results