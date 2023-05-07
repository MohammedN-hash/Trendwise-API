
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder

from services.mangment import get_all_classfied_data
from services.google_trends import get_interest



router = APIRouter(
    responses={404: {"description": "Not found"}},

)





@router.get('/getAnalysis')
async def get_analysis(query,post_limit,comment_limit):

    reddit_posts_list,reddit_comments_list=get_all_classfied_data(query, fromDate='', toDate='', subreddit='all',post_limit = post_limit,comment_limit=comment_limit)
    # convert the results to a JSON-serializable format using jsonable_encoder
    results = {"posts": jsonable_encoder(reddit_posts_list), "comments": jsonable_encoder(reddit_comments_list)}
    
    # return the results as JSON
    return results

@router.get('/getInterest')
async def get_analysis(query,region, resolution, from_date, to_date):

    return get_interest(query, region=region, resolution=resolution, from_date=from_date, to_date=to_date,language='en-US' )


 