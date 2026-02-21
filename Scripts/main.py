import extractor as ex
import searcher as ser
import sampler as sam
import cleaner as cl
import infofilter as fl

keyword = []
timeframe = []

#----STEP 1 : Sample the data randomly-----
sam.sample_from('data/delisted_games_data.csv', 150)

#----STEP 2 : Exract necessary data from sampled data-----
keyword = ex.extract_column('output/sampled_delisted.csv', 0)
time_start = ex.extract_column('output/sampled_delisted.csv', 2)
time_end = ex.extract_column('output/sampled_delisted.csv', 3)
timeframe = ex.build_timeframe(time_start, time_end)

#----STEP 3 : build the payload and query trends-----
ser.deploy_payload(keyword, timeframe)

#----STEP 4 : Clean the recieved results-----
cleaned_dataframe = cl.clean_csv("data/delisted_trends_output.csv")
cl.interpolate_info(cleaned_dataframe)

#----STEP 5 : Filter the recieved results-----
fl.filter_data('data/interpolated_infomation.csv')