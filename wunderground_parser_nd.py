'''
Modified from wunderground_parser.py from fivethirtyeight.com
forked from https://github.com/fivethirtyeight/data/tree/master/us-weather-history
Parses wunderground weather data from specified weather stations
Modifications made can be found in the README.md file on github
This script functions with make_weather.py and wunderground_scraper_nd.py and does nothing if run from the
command line
'''


from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from urllib.request import urlopen


def parse_station(station, current_date, end_date, out_file):

    '''
    This function parses the web pages downloaded from wunderground.com
    into a flat CSV file for the station you provide it.

    Make sure to run the wunderground scraper first so you have the web
    pages downloaded.
    '''
    
        
    while current_date != end_date:
        #try_again will allow script to download html data if an error occurs
        #already_tried only allows one attempt to redownload data before skipping that date
        try_again = False
        already_tried = False

        with open('wund_html/{}/{}-{}-{}.html'.format(station,
                                                current_date.year,
                                                current_date.month,
                                                current_date.day)) as in_file:
            soup = BeautifulSoup(in_file.read(), 'html.parser')

            weather_data = soup.find(id='historyTable').find_all('span', class_='wx-value')
            weather_data_units = soup.find(id='historyTable').find_all('td')

            try:
                actual_mean_temp = weather_data[0].text
                actual_max_temp = weather_data[2].text
                average_max_temp = weather_data[3].text
                record_max_temp = weather_data[4].text
                actual_min_temp = weather_data[5].text
                average_min_temp = weather_data[6].text
                record_min_temp = weather_data[7].text
                record_max_temp_year = weather_data_units[
                            9].text.split('(')[-1].strip(')')
                record_min_temp_year = weather_data_units[
                            13].text.split('(')[-1].strip(')')

                actual_precipitation = weather_data[9].text
                if actual_precipitation == 'T':
                    actual_precipitation = '0.0'
                average_precipitation = weather_data[10].text
                record_precipitation = weather_data[11].text

                # Verify that the parsed data is valid
                if (record_max_temp_year == '-1' or record_min_temp_year == '-1' or
                            int(record_max_temp) < max(int(actual_max_temp), int(average_max_temp)) or
                            int(record_min_temp) > min(int(actual_min_temp), int(average_min_temp)) or
                            float(actual_precipitation) > float(record_precipitation) or
                            float(average_precipitation) > float(record_precipitation)):
                    raise Exception

                out_file.write('{}-{}-{},'.format(current_date.year, current_date.month, current_date.day))
                out_file.write(','.join([station, actual_mean_temp, actual_min_temp, actual_max_temp,
                                             average_min_temp, average_max_temp,
                                             record_min_temp, record_max_temp,
                                             record_min_temp_year, record_max_temp_year,
                                             actual_precipitation, average_precipitation,
                                             record_precipitation]))
                out_file.write('\n')
                current_date += timedelta(days=1)
            except:
                # If the web page is formatted improperly, signal that the page may need
                # to be downloaded again.
                try_again = True

            # If the web page needs to be downloaded again, re-download it from
            # wunderground.com

            # If the parser gets stuck on a certain date, you may need to investigate
            # the page to find out what is going on. Sometimes data is missing, in
            # which case the  parser will skip this day.

        if try_again and not already_tried:
            print('Error with date {}'.format(current_date)+" "+str(station))

            lookup_URL = 'http://www.wunderground.com/history/airport/{}/{}/{}/{}/DailyHistory.html'
            formatted_lookup_URL = lookup_URL.format(station,
                                                         current_date.year,
                                                         current_date.month,
                                                         current_date.day)
            html = urlopen(formatted_lookup_URL).read().decode('utf-8')

            out_file_name = 'wund_html/{}/{}-{}-{}.html'.format(station,
                                                          current_date.year,
                                                          current_date.month,
                                                          current_date.day)

            with open(out_file_name, 'w') as out_file:
                out_file.write(html)
                
            #Only allow parser to try again once, then move on. You can modifiy this with a counter to allow it to
            #try multiple times, but usually if it does not work after the first attempt, the data is missing or 
            #in a different format
            already_tried = True
            
        if already_tried:
            current_date += timedelta(days=1)


def parse(stations, begin_date, end_date):
    current_date = datetime.strptime(begin_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")+timedelta(days=1) #add one to make loop end on the end date
    
    with open('weather_data/wund/{}-{}-{}-{}-{}-{}.csv'.format(current_date.year, current_date.month, current_date.day, end_date.year, end_date.month, end_date.day), 'w') as out_file:
        out_file.write('date,station,actual_mean_temp,actual_min_temp,actual_max_temp,'
                       'average_min_temp,average_max_temp,'
                       'record_min_temp,record_max_temp,'
                       'record_min_temp_year,record_max_temp_year,'
                       'actual_precipitation,average_precipitation,'
                       'record_precipitation\n')
        for station in stations:
            parse_station(station, current_date, end_date, out_file)
