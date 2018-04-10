import numpy as np
import pandas as pd
import get_weather_ndawn as nd
import wunderground_parser_nd as wup
import wunderground_scraper_nd as wus
import os

##Edit variables after the 'if __name__ == "__main__" statement##
##
##


def main(begin_date, end_date, weather='ndawn'):
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
        stations = range(1,103)
        df = nd.get_weather(stations,begin_date,end_date)
        df.to_csv("./weather_data/ndawn/"+begin_date+"-"+end_date+".csv", encoding = "utf-8",index=False)
    elif weather == "wund":
        stations = ["KBIS","KFAR", "KGFK", "KDVL", "KJMS", "KMOT", "KISN"]
        wus.scrape(stations, begin_date, end_date)
        wup.parse(stations, begin_date, end_date)
    else:
        print("no weather specified")
        

if __name__ == "__main__":
    ##Edit the variables here##
    
    #choose noaa, ndawn, or wund for "weather"
    #noaa gets weather from noaa.gov
    #wund gets weather from wunderground.com
    #ndawn gets weather from ndawn.ndsu.nodak.edu
    weather = 'wund'
    
    #Edit begining and end dates for span of weather data
    #ndawn exists from approx 1993 to present
    #NOAA and Wunderground are approx 1890 (or so). Check their respective websites for earliest data

    #dates use fmt YYYY-mm-dd
    begin_date = '2018-01-01'
    end_date = '2018-02-01'

    df = main(begin_date, end_date, weather)
    
