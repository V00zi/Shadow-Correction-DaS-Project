import time
from pytrends.request import TrendReq
from pytrends.exceptions import ResponseError
from requests.exceptions import HTTPError
import pandas as pd
import random

proxies = [
"http://iweber02:qp9dQbDM@31.131.11.187:29842",
"http://iweber02:qp9dQbDM@172.81.23.200:29842",
"http://iweber02:qp9dQbDM@107.166.116.67:29842",
"http://iweber02:qp9dQbDM@31.131.9.22:29842",
"http://iweber02:qp9dQbDM@172.81.21.41:29842",
"http://iweber02:qp9dQbDM@172.81.20.69:29842",
"http://iweber02:qp9dQbDM@162.218.13.126:29842",
"http://iweber02:qp9dQbDM@52.128.216.28:29842",
"http://iweber02:qp9dQbDM@31.131.8.161:29842",
"http://iweber02:qp9dQbDM@23.226.24.128:29842"
]

pytrends = TrendReq(hl='en-US', tz=360, proxies=proxies)

successful=0
failed=0

def reset_counter():
    global successful, failed
    successful = 0
    failed = 0

def rng():
    return random.randint(5, 15)

def get_trends_countries(kw, cn, tf):
    global successful, failed

    try:
        time.sleep(rng())
        pytrends.build_payload(kw, timeframe=tf, geo=cn)
        successful+=1

        print(f"Successful Fetch:{successful}, Failed Fetch:{failed}, Fetching trends in {cn}")
        return pytrends.interest_over_time()
        
    except ResponseError as e:

        if e.response.status_code == 429:
            print(f"Timed out: {e}\nExiting...")
            exit()

        elif e.response.status_code == 400:
            failed+=1
            successful-=1
            print(f"Invalid request for country: {cn}, Error: {e}\nSkipping...")
            return None

        else:
            print(f"An unexpected error occurred: {e}.\nRetrying in 10 seconds...")
            time.sleep(10)

    print(f"Max retries exceeded Skipping...")
    return None


def get_trends(kw_list, tf):
    global successful, failed

    try:
        time.sleep(rng())
        pytrends.build_payload(kw_list, timeframe=tf)
        successful+=1
        
        print(f"Successful Fetch:{successful}, Failed Fetch:{failed}, Fetching trends for: {kw_list[0]}")
        return pytrends.interest_over_time()

    except ResponseError as e:
        if e.response.status_code == 429:
            print(f"Timed out: {e}\nExiting...")
            exit()           

        elif e.response.status_code == 400:
            failed+=1
            successful-=1
            print(f"Invalid request: {kw_list[0]}, Error: {e}\nSkipping...")
            return None

        else:
            print(f"An unexpected error occurred: {e}.\nRetrying in 10 seconds...")
            time.sleep(10)

    print(f"Max retries exceeded Skipping...")
    return None

def deploy_payload(keyword, timeframe):
    print(f"building payload for delisted games trend search...")
    reset_counter()
    dfs = []

    for kw, tf in zip(keyword, timeframe):
        kw_tags = f"{kw} torrent +{kw} repack"
        df = get_trends([kw_tags], tf)
        
        if df is not None and not df.empty:
            if 'isPartial' in df.columns:
                df = df.drop(columns=['isPartial'])
            df.rename(columns={kw_tags: kw}, inplace=True)
            dfs.append(df)

            result_df = pd.concat(dfs, axis=1, sort=True)
            result_df.to_csv("output/p3/delisted_trends_output.csv")
    return None

def deploy_payload_countries(countries):
    print(f"building payload for country-wise trend search...")
    reset_counter()
    dfs = []

    keyword = 'game torrents + game repacks + games pirated'
    timeframe = '2015-01-01 2025-12-31'

    for country in countries:
        
        df = get_trends_countries([keyword], country, timeframe) 
        
        if df is not None and not df.empty:
            if 'isPartial' in df.columns:
                df = df.drop(columns=['isPartial'])
            df.rename(columns={keyword: country}, inplace=True)
            dfs.append(df)

            result_df = pd.concat(dfs, axis=1)
            result_df.to_csv("output/p2/countries_piracy_searches.csv")

    return None
