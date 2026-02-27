import time
from pytrends.request import TrendReq
from pytrends.exceptions import ResponseError
from requests.exceptions import HTTPError
import pandas as pd
import random


# proxy format proxies=["http://username:password@ip:port"]
proxies = []

def set_proxies(proxy_list):
    global proxies
    proxies = proxy_list
    print("Proxies set successfully...")

pytrends = TrendReq(hl='en-US', tz=360, proxies=proxies)

successful=0
failed=0

def reset_counter():
    global successful, failed
    successful = 0
    failed = 0

def rng():
    return random.randint(5, 15)

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

