#!/usr/bin/env python
# -*- coding: utf-8 -*-

import feedparser

rss_url = "http://weather.yahooapis.com/forecastrss?w=615702&u=c"

feed_dict = feedparser.parse(rss_url)

#for key, value in feed_dict.items():
#    print key, ':', value

location_dict   = feed_dict.feed.yweather_location   # contains the locations dictionary
atmosphere_dict = feed_dict.feed.yweather_atmosphere # contains the atmospheric conditions dictionary (pressure/humidity)
astronomy_dict  = feed_dict.feed.yweather_astronomy  # contains the astronomy dictionary (sunset/sunrise hours)

#print location_dict
#print atmosphere_dict
#print astronomy_dict

city = location_dict['city']
humidity = atmosphere_dict['humidity']
pressure = atmosphere_dict['pressure']
sunrise = astronomy_dict['sunrise']
sunset = astronomy_dict['sunset']

#print feed_dict.entries[0].summary

summary_list = feed_dict.entries[0].summary.splitlines()

weather_pic = summary_list[0].split("<br />")[0].split("\"")[1]
current_conditions = summary_list[2].split("<br />")[0][:-2]
today_forecast, today_forecast_temp = summary_list[4].split("<br />")[0].split(" - ")[1].split(". ")

print city
print "humidity", humidity
print "pressure", pressure
print "sunrise", sunrise
print "sunset", sunset

print weather_pic
print current_conditions
print today_forecast
print today_forecast_temp

