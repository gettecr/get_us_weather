'''
Script uses API requests to get historical weather data from all available weather stations
from ndawn stations in North Dakota
Not intended to get data from other regions
This script functions in tandem with make_weather.py, however if run from the
command line it will retrieve yesterday's weather data for all available stations

Author: Cody R. Gette
'''

import requests
import datetime
import numpy as np
import pandas as pd
import os

def get_weather(stations, begin_date, end_date):
    #Stations 2-102
    count = 0
    for station in stations:
        
        params = {'station': station, 'begin_date': begin_date,'end_date': end_date, 'ttype': "daily", 'quick_pick':''}
        
    ##'ddmxt' = max temp; 'ddmnt'= min temp; 'ddavt' = average temp; 'ddbst' = bare soil temp; 
    ##'ddtst' = turf soil temp; 'ddws' = average wind speed; 'ddmxws' = max wind speed; 'ddsr' = solar radiation; 
    ##'ddr' = rain fall; 'dddp'= dew point; 'ddwc' = wind chill
 
        more_params={'variable':[ 'ddmxt','ddmnt','ddavt','ddbst','ddtst','ddws','ddmxws','ddsr','ddr','dddp','ddwc']}
        params_all = {**params,**more_params}

        r = requests.get('https://ndawn.ndsu.nodak.edu/table.csv', params = params_all)
        print("Request status code from Station #"+str(station)+': '+str(r.status_code))

        try:
            #output content of request and read back into dataframe
            #Possibly a more elegant way to accomplish this -- for future updates
            with open("Output.csv", "w") as text_file:
                text_file.write(r.content.decode('utf-8'))

            tmp = pd.read_csv('Output.csv', header=[0,1],skiprows=3)

        #Column names to keep as they come from the csv file. Skipping some of the "Flag" columns. 

            tmp=tmp[[('Station Name', 'Unnamed: 0_level_1'),
                       ('Latitude', 'deg'),
                       ('Longitude', 'deg'),
                       ('Elevation', 'ft'),
                       ('Year', 'Unnamed: 4_level_1'),
                       ('Month', 'Unnamed: 5_level_1'),
                       ('Day', 'Unnamed: 6_level_1'),
                       ('Max Temp', 'Degrees F'),
                       ('Min Temp', 'Degrees F'),
                       ('Avg Temp', 'Degrees F'),
                       ('Avg Bare Soil Temp', 'Degrees F'),
                       ('Avg Turf Soil Temp', 'Degrees F'),
                       ('Avg Wind Speed', 'mph'),
                       ('Max Wind Speed', 'mph'),
                       ('Total Solar Rad', 'Lys'),
                       ('Rainfall', 'inch'),
                       ('Dew Point', 'Degrees F'),
                       ('Wind Chill', 'Degrees F'),]]

        #Rename the columns in one line instead of two
            tmp.columns = ['Station Name', 'Latitude (deg)', 'Longitute (deg)', 'Elevation (ft)', 'Year', 'Month','Day', 'Max Temp (F)',
                              'Min Temp (F)', 'Avg Temp (F)', 'Avg Bare Soil Temp (F)','Avg Turf Soil Temp (F)',
                              'Avg Wind Speed (mph)','Max Wind Speed (mph)', 'Total Solar Rad (Lys)',
                              'Rainfall (in)', 'Dew Point', 'Wind Chill' ]
            #Assign tmp to new dataframe if the first time through the loop; otherwise combine data
            if count == 0:
                df = tmp
            else:
                df = pd.concat([df,tmp], ignore_index=True)
            count+=1

        #Catch all exceptions for a bad request or missing data
        except:
            print("Error converting Station #"+str(station)+" to csv. Missing?")

    print("Successfully retrieved "+str(count+1)+" stations")
    print("Data exists from "+str(len(df['Station Name'].unique())+1)+" stations")
    os.remove('Output.csv')
    return df

        
if __name__ == '__main__':

    #If running script directly from command line, just retrieve yesterday's weather
    #This can be modified to replace 'yesterday' with any date with the format 'YYYY-mm-dd'

    yesterday = datetime.datetime.now()-datetime.timedelta(days=1)
    stations = range(1,103)
    df =  get_weather(stations, yesterday.strftime("%Y-%m-%d"), yesterday.strftime("%Y-%m-%d"))
    df.to_csv('./weather_data/weather_yesterday.csv', encoding='utf-8', index=False)
        
