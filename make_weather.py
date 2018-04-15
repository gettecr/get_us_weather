import numpy as np
import pandas as pd
import get_weather_ndawn as nd
import get_weather_noaa as noaa
import wunderground_parser_nd as wup
import wunderground_scraper_nd as wus
import os

##Edit the variables here##
    
#choose noaa, ndawn, or wund for "weather"
#noaa gets weather from noaa.gov
#wund gets weather from wunderground.com
#ndawn gets weather from ndawn.ndsu.nodak.edu

weather = 'ndawn'
    
#Edit begining and end dates for span of weather data
#ndawn exists from approx 1993 to present
#NOAA and Wunderground are approx 1890 (or so). Check their respective websites for earliest data

#dates use fmt YYYY-mm-dd
begin_date = '2018-01-01'
end_date = '2018-01-01'

stations = ["KBIS","KFAR", "KGFK", "KDVL", "KJMS", "KMOT", "KISN"] #stations in North Dakota. Required for Wunderground data
locationid='FIPS:38' #location id for North Dakota. Required for NOAA data

#API token from NOAA
mytoken = ''


##
##


def main():
    # Make sure a directory exists for the weather data
    if not os.path.isdir("weather_data"):
        os.mkdir('weather_data')
    if not os.path.isdir('weather_data/ndawn'):
        os.mkdir('weather_data/ndawn')
    if not os.path.isdir('weather_data/wund'):
        os.mkdir('weather_data/wund')
    if not os.path.isdir('weather_data/noaa'):
        os.mkdir('weather_data/noaa')
    
    #Choose which station to get data depending on parameters entered below
    if weather == "ndawn":
        print('Retrieving weather from ndawn.ndsu.nodak.edu')
        stationnums = range(1,103)
        df = nd.get_weather(stationnums,begin_date,end_date)
        df.to_csv("./weather_data/ndawn/"+begin_date+"-"+end_date+".csv", encoding = "utf-8",index=False)
    elif weather == "wund":
        print('Retrieving weather from Wunderground')
        print(str(stations[1]))
        wus.scrape(stations, begin_date, end_date)
        wup.parse(stations, begin_date, end_date)
    elif weather == "noaa":
        print('Retrieving weather from NOAA')
        df= noaa.make_weather(locationid, begin_date,end_date, mytoken)
        df.to_csv("./weather_data/noaa/"+begin_date+"-"+end_date+".csv", encoding = "utf-8",index=False)
    else:
        print("no weather specified")
        

if __name__ == "__main__":
   
    main()
    
