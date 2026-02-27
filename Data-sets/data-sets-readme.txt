The current folder contains the main datasets being used in the project. For tests that are conducted on these datasets a prepared version of the respective tests are cloned and placed in the scripts folder. This version of datasets are primarily to understand the scope and params within it 

----------------------------------------------------------------------------------------------------------

* annual_income_and_hours.csv

Source
https://data.worldbank.org/indicator/NY.GDP.MKTP.CD

Contains the data of wages and PPI(purchasing power index) used to identify the pay disparity, sanitized and formatted. missing certain entries

* piracy_search_geo.csv

Source
https://trends.google.com/trends/explore?date=2015-01-01%202025-12-31&q=game%20torrents%20%2B%20games%20repacks%20%2B%20games%20pirated&hl=en-US

Contains interest by region volume for piracy game searches for various regions supported by google trends. sanitized and formatted.

----------------------------------------------------------------------------------------------------------

* streaming_fragmentation_analytics.csv

Source
Parrot Analytics Global Streaming Market Share Data (2018-2023) https://www.parrotanalytics.com/insights/category/whitepapers/

Contains global demand share percentages for major streaming platforms (Netflix, Amazon Prime, Hulu, Disney+, Apple TV+, HBO Max, Paramount+, and aggregated Others). Used to calculate the Herfindahl-Hirschman Index (HHI) to quantify market concentration and fragmentation over time. Data represents worldwide streaming audience demand distribution.


* streaming_analytics_sandvine.csv

Source
Sandvine Global Internet Phenomena Reports (2011-2024) https://www.applogicnetworks.com/resources?filter=.casestudies

Contains North American/US streaming traffic share data extracted from Sandvine's biannual reports. Includes market share percentages for Netflix, Amazon Prime Video, Hulu, HBO GO/Max, and Disney+ measured as percentage of downstream internet traffic during peak periods (2011-2016) and total daily traffic (2018-2024). Used to establish temporal precedence showing fragmentation began 7 years before global piracy measurement became available. Note: Methodology changed between reporting periods - Peak Period measurement (2011-2016) vs Total Traffic measurement (2018+).

* streaming_analytics_sandvine.csv

Source
https://trends.google.com/trends/explore?date=2018-01-01%202024-12-31&q=putlocker%20%2B%20watch%20movies%20free%20%2B%20watch%20series%20free%20%2B%20123movies%20%2B%20fmovies&hl=en&legacy

Contains worldwide search interest data for piracy-related composite index: "putlocker + watch movies free + watch series free + 123movies + fmovies" spanning 2018-2024 (monthly granularity).


--------------------------------------------------------------------------------------------------------

* list_of_delisted_games.csv 

Source
https://steam-tracker.com/

Contains a list of 7k+ delisted games (Not available to purchase on steam anymore) the list is a sanitized, formatted version of the data taken from the source. There is error within the data which are minimal and also rectified  