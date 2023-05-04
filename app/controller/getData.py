
from fastapi import APIRouter
from services.mangment import get_all_classfied_data
from services.google_trends import get_interest



router = APIRouter(
    responses={404: {"description": "Not found"}},

)





@router.get('/getAnalysis')
async def get_analysis(query):

    return get_all_classfied_data(query, fromDate='', toDate='', subreddit='all',post_limit = 100)

@router.get('/getInterest')
async def get_analysis(query,region, resolution, from_date, to_date):

    return get_interest(query, region=region, resolution=resolution, from_date=from_date, to_date=to_date,language='en-US' )


 