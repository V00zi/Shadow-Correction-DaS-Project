import extractor as ex
import searcher as ser
import sampler as sam
import cleaner as cl
import infofilter as fl


countries_list=[]
keyword = []
timeframe = []

# MANDATORY STEP NOTICE ME........................

# Initalize your proxies: atleast 10 static proxies
# proxy format proxies=["http://username:password@ip:port"]

my_proxies=[

] 

ser.set_proxies(my_proxies)


############################################################################################


#----STEP 1 A : Extract the country codes from the data set randomly-----
countries_list = ex.extract_column('data/piracy_search_geo.csv', 1)

#----STEP 2 A : build the payload and query trends country wise-----
ser.deploy_payload_countries(countries_list)

#----STEP 3 A : Normalize the recieved results on the basis or region search ranks-----
fl.normalize_data('output/p2/countries_piracy_searches.csv')



#############################################################################################



# #----STEP 1 B : Sample the data randomly-----
# sam.sample_from('data/delisted_games_data.csv', 150)

# #----STEP 2 B : Exract necessary data from sampled data-----
# keyword = ex.extract_column('output/sampled_delisted.csv', 0)
# time_start = ex.extract_column('output/sampled_delisted.csv', 2)
# time_end = ex.extract_column('output/sampled_delisted.csv', 3)
# timeframe = ex.build_timeframe(time_start, time_end)

# #----STEP 3 B : build the payload and query trends-----
# ser.deploy_payload(keyword, timeframe)

# #----STEP 4 B : Clean the recieved results-----
# cleaned_dataframe = cl.clean_data("output/p3/delisted_trends_output.csv")
# cl.interpolate_info(cleaned_dataframe)

# #----STEP 5 B : Filter the recieved results-----
# fl.filter_data('output/p3/interpolated_infomation.csv')