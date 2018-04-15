Get Weather Data
==============================

**WORK IN PROGRESS** 
To Do:
- [x]  Finish scripts to retrieve weather data from NOAA or Wunderground (using API)
- [x]  Modify make_weather to include new script
- [ ] Add description and details to README

Project Organization
------------

    ├── LICENSE
    ├─ README.md			   <- The top-level README 
    ├── make_weather.py      	 	   <- Execute this to get data
    ├── wunderground_parser_nd.py  	   <- parses .html weather data from wunderground
    ├── wunderground_scraper_nd.py	   <- scrapes wunderground for .html weather data
    ├── get_weather_ndawn.py		   <- requests data from ndawn.ndsu.nodak.edu via API
    ├── weather_data
    |	├── ndawn			   <- contains .csv data from ndawn
    |	├── noaa			   <- contains .csv data from noaa
    |	├── wund 			   <- contains .csv data from wunderground
    ├──{station}			   <- .html data from wunderground for each station

--------


