'''
Modified from wunderground_scraper.py from fivethirtyeight.com
forked from https://github.com/fivethirtyeight/data/tree/master/us-weather-history
Scrapes wunderground weather data from specified weather stations
Modifications made can be found in the README.md file on github
This script functions with make_weather.py and wunderground_parser_nd.py and does nothing if run from the 
command line
'''

from datetime import datetime, timedelta
from urllib.request import urlopen
import os


def scrape_station(station, begin_date, end_date):
    current_date = datetime.strptime(begin_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")+timedelta(days=1) #add one to make loop end on the end date
    '''
    This function scrapes the weather data web pages from wunderground.com
    for the station you provide it.

    You can look up your city's weather station by performing a search for
    it on wunderground.com then clicking on the "History" section.
    The 4-letter name of the station will appear on that page.
    '''
    # Make sure a directory exists for the station web pages
    if not os.path.isdir("wund_html"):
        os.mkdir('wund_html')
    if not os.path.isdir('wund_html/'+station):
        os.mkdir('wund_html/'+station)

        # Use .format(station, YYYY, M, D)
    lookup_URL = 'http://www.wunderground.com/history/airport/{}/{}/{}/{}/DailyHistory.html'


    while current_date != end_date:

        if current_date.day == 1:
            print(str(current_date)+" "+str(station))

        formatted_lookup_URL = lookup_URL.format(station,
                                                 current_date.year,
                                                 current_date.month,
                                                 current_date.day)
        html = urlopen(formatted_lookup_URL).read().decode('utf-8')

        out_file_name = 'wund_html/{}/{}-{}-{}.html'.format(station, current_date.year,
                                                  current_date.month,
                                                  current_date.day)

        with open(out_file_name, 'w') as out_file:
            out_file.write(html)

        current_date += timedelta(days=1)


# Scrape the stations 
def scrape(stations, begin_date, end_date):
    for station in stations:
        scrape_station(station, begin_date, end_date)
