import datetime as dt
from pytrends.request import TrendReq
from fastapi import APIRouter
router = APIRouter()


def get_trends(query, region='', resolution='WORLD', from_date='', to_date='',language='en-US' ):

    if not from_date:
        from_date = (dt.datetime.now() - dt.timedelta(days=30)).strftime('%Y-%m-%d')
    if not to_date:
        to_date = dt.datetime.now().strftime('%Y-%m-%d')
    print(from_date,to_date)

    pytrend = TrendReq(hl=language)

    pytrend.build_payload(kw_list=[query], geo=region, timeframe=f'{from_date} {to_date}')

    interest_df = pytrend.interest_by_region(resolution=resolution, inc_low_vol=False, inc_geo_code=True)


    print(interest_df)
    return interest_df.values.tolist()