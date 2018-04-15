#Script uses API requests to get historical weather data from NOAA stations
#Can be modified to get data from other regions
#This script functions in tandem with make_weather.py, however if run from the
#command line it will retrieve this day last year's weather data for given stations


import requests
import datetime
import numpy as np
import pandas as pd
import os
import sys

def get_weather(locationid, begin_date, end_date, mytoken):
    token = {'token': mytoken}

    #passing as string instead of dict because NOAA API does not like percent encoding
    params = 'datasetid=GHCND'+'&locationid='+str(locationid)+'&startdate='+str(begin_date)+'&enddate='+str(end_date)+'&limit=25'+'&units=standard'
                     
    base_url = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/data'
    
    r = requests.get(base_url, params = params, headers=token)
    print("Request status code: "+str(r.status_code))

    try:
        #results comes in json form. Convert to dataframe
        df = pd.DataFrame.from_dict(r.json()['results'])
        print("Successfully retrieved "+str(len(df['station'].unique()))+" stations")
        dates = pd.to_datetime(df['date'])
        print("Last date retrieved: "+str(dates.iloc[-1]))

        if df.count().max()==1000:
            print('WARNING: Maximum data limit was reached (limit = 1000)')
            print('Consider breaking your request into smaller pieces')
            
        return df

    #Catch all exceptions for a bad request or missing data
    except:
        print("Error converting weather data to dataframe. Missing data?")
        

def get_station_info(locationid, mytoken):
    token = {'token': mytoken}

    #passing as string instead of dict because NOAA API does not like percent encoding
    
    stations = 'locationid='+str(locationid)+'&datasetid=GHCND'+'&units=standard'+'&limit=1000'
    base_url = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/stations'
    r = requests.get(base_url, headers = token, params=stations)
    print("Request status code: "+str(r.status_code))

    try:
        #results comes in json form. Convert to dataframe
        df = pd.DataFrame.from_dict(r.json()['results'])
        print("Successfully retrieved "+str(len(df['id'].unique()))+" stations")
        
        if df.count().max() >= 1000:
            print('WARNING: Maximum data limit was reached (limit = 1000)')
            print('Consider breaking your request into smaller pieces')
 
        return df
    #Catch all exceptions for a bad request or missing data
    except:
        print("Error converting station data to dataframe. Missing data?")


def make_weather(locationid, begin_date, end_date, mytoken):

    df_weather =  get_weather(locationid, begin_date, end_date, mytoken)
    df_stations = get_station_info(locationid, mytoken)
    try:
        df = df_weather.merge(df_stations, left_on = 'station', right_on = 'id', how='inner')

        #Check for missing overlap between station weather info and location info
    
        location_ismissing = df_weather[~df_weather['station'].isin(df_stations['id'])]
        loc_miss_count = len(location_ismissing['station'].unique())
        if loc_miss_count != 0:
            print("Missing location data for "+str(loc_miss_count)+" stations")

        weather_ismissing = df_stations[~df_stations['id'].isin(df_weather['station'])]
        weath_miss_count = len(weather_ismissing['id'].unique())
        if weath_miss_count != 0:
            print("Missing weather data for "+str(weath_miss_count)+" stations")
        return df
        
    except:
        print('An error occured. Unable to generate weather data.')
 
if __name__ == '__main__':

    #If running script directly from command line, just retrieve this day last year's weather
    #This can be modified to replace 'lastyear' with any date with the format 'YYYY-mm-dd'

    #Put your API token from NOAA here
    mytoken = ''

    if mytoken == '':
        sys.exit('Missing API token. Open get_weather_noaa and provide your unique token!')
        
    #Location key for the region you are interested in (can be found on NOAA or requested as a different API as well)
    locationid = 'FIPS:38' #location id for North Dakota

   
    lastyear = datetime.datetime.now()-datetime.timedelta(days=365)

    #Modify begin_date and end_date with format "YYYY-mm-dd"
    #begin_date = 'YYYY-mm-dd' #uncomment this line and replace date with your own for testing
    #end_date = 'YYYY-mm-dd' #this line too
    
    begin_date = lastyear.strftime("%Y-%m-%d")
    end_date = lastyear.strftime("%Y-%m-%d")

    df = make_weather(locationid, begin_date, end_date, mytoken)
        
    #save as flattened csv
    df.to_csv('./weather_data/weather_lastyear_noaa.csv', encoding='utf-8', index=False)
