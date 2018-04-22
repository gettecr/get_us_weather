Get Weather Data
==============================

This project retrieves weather data with python in one of three ways: Using an API
from NOAA, web scraping and parsing from Wunderground, or from NDAWN.

Note: NDAWN is limited to North Dakota data only (and a few stations
in northern Minnesota)

Getting Started
--------------------------

Clone the repo and navigate to the `make_weather.py` file. Open the
file and edit the
`weather`,
`begin_date`, and
`end_date`
variables. The `weather` variable can be `noaa` for retrieving data
from NOAA.gov, `wund` for wunderground data, or `ndawn` for NDAWN
data. The begin and end dates are the dates between which you want the
data.

If using `wund`:

You need to look up and provide a list of the `stations` to look
up. The provided stations are from cities in North Dakota.

If using `noaa`:

You need to get a unique API key from NOAA and paste it in `mytoken =
''`. You must also find what the location id is called for the area
you want to sample. For example `FIPS:38` is the location id for North Dakota.

Once you have provided the above information, run

`make_weather.py`

and it will retrieve the data.


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


