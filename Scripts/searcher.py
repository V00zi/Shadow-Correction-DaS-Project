import time
from pytrends.request import TrendReq
from pytrends.exceptions import ResponseError
from requests.exceptions import HTTPError
import pandas as pd

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

successful=0
failed=0

def get_trends(kw_list, tf, proxy_list):
    global successful, failed
    retries = 5
   
    for i in range(retries):
        try:
            pytrends = TrendReq(hl='en-US', tz=360, proxies=proxy_list)
            pytrends.build_payload(kw_list, timeframe=tf)
            successful+=1

            print(f"Successful Fetch:{successful}, Failed Fetch:{failed}, Fetching trends for: {kw_list[0]}")
            return pytrends.interest_over_time()

        except ResponseError as re:
            failed+=1
            successful-=1
            print(f"Invalid request for keyword:{kw_list[0]}, Error: {re}")
            return None

        except HTTPError as he:
            if he.response.status_code == 429:
                sleep_time = 60 ** i
                print(f"HTTP Error: {he}, Adjusting Backoff: {sleep_time}s")
                time.sleep(sleep_time)
            else:
                raise he

    print(f"Max retries exceeded for keyword '{kw_list[0]}'. Skipping.")
    return None

def deploy_payload(keyword, timeframe):
    dfs = []

    for kw, tf in zip(keyword, timeframe):
        kw_tags = f"{kw} torrent +{kw} repack"
        df = get_trends([kw_tags], tf, proxies)
        
        if df is not None and not df.empty:
            if 'isPartial' in df.columns:
                df = df.drop(columns=['isPartial'])
            df.rename(columns={kw_tags: kw}, inplace=True)
            dfs.append(df)

            result_df = pd.concat(dfs, axis=1, sort=True)
            result_df.to_csv("output/delisted_trends_output.csv")

        time.sleep(5)    
    return None