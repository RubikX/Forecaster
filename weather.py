# Author: Edison Suen
# Description: Scrape "The Weather Network" to extract the 7 day forecast

# -*- coding: utf-8 -*-
import requests
import pandas as pd
import re
from bs4 import BeautifulSoup


country = raw_input("CAD or US?: ")
province = raw_input("Please enter a province: ")
province = province.replace(' ', '-').lower()
city = raw_input("Please enter a city: ")
city = city.replace(' ', '-').lower()
units = raw_input("Metric or Imperial? ")
units = units.title()
print("\n")

if country.upper() == "CAD":
	base_url = "https://www.theweathernetwork.com/ca/weather/"

elif country.upper() == "US":
	base_url = "https://www.theweathernetwork.com/us/weather/"

headers = {'User-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
website = requests.get((base_url+"{}"+"/"+"{}").format(province,city),headers=headers)
soup = BeautifulSoup(website.content, 'html.parser')

###### FOR TESTING PURPOSES ######
forecast = soup.find(id="seven-days-only")
items = forecast.find_all(class_="seven-day-column")
column = items[0]
period = column.find(class_ ="day_title").get_text()
outlook = column.find(class_="day_outlook").get_text()
feels_celcius = (column.find_all("span"))[4]
feels_feh = (column.find_all("span"))[5]
temp_celcius = column.find(class_="chart-daily-temp seven_days_metric seven_days_metric_c").get_text()
temp_feh = column.find(class_="chart-daily-temp seven_days_imperial seven_days_imperial_f").get_text()
night_celcius = column.find(class_="chart-daily-temp-low seven_days_metric seven_days_metric_c").get_text()
night_feh = column.find(class_="chart-daily-temp-low seven_days_imperial seven_days_imperial_f").get_text()
rain_metric = column.find(class_="fx-details seven_days_metric rain seven_days_metric_kmh").get_text()
rain_imperial = column.find(class_="fx-details seven_days_imperial rain seven_days_imperial_mph").get_text()
wind_metric = column.find(class_="fx-details seven_days_metric seven_days_metric_kmh wind")
wind_imperial = column.find(class_="fx-details seven_days_imperial seven_days_imperial_mph wind")

###### END TEST VARIABLES ######

###### CONDITIONALS ######
if units== "Metric":

	days = [dt.get_text() for dt in forecast.select(".seven-day-column .day_title")]
	temp = [t.get_text() for t in forecast.select(".seven-day-column .chart-daily-temp.seven_days_metric.seven_days_metric_c")]
	temp_night = [tn.get_text() for tn in forecast.select(".seven-day-column .chart-daily-temp-low.seven_days_metric.seven_days_metric_c")]
	rain = [r.get_text() for r in forecast.select(".seven-day-column .fx-details.seven_days_metric.rain.seven_days_metric_kmh")]
	feels_arr = []
	for feels in items: 
		feels_like = (feels.find_all("span"))[4]
		feels_arr.append(feels_like)

	for i in range(7):
		feels_arr[i] = str(feels_arr[i])
		feels_arr[i] = feels_arr[i]

elif units == "Imperial":
	days = [dt.get_text() for dt in forecast.select(".seven-day-column .day_title")]
	temp = [t.get_text() for t in forecast.select(".seven-day-column .chart-daily-temp.seven_days_imperial.seven_days_imperial_f")]
	temp_night = [tn.get_text() for tn in forecast.select(".seven-day-column .chart-daily-temp-low.seven_days_imperial.seven_days_imperial_f")]
	rain = [r.get_text() for r in forecast.select(".seven-day-column .fx-details.seven_days_imperial.rain.seven_days_imperial_mph")]
	feels_arr = []
	for feels in items: 
		feels_like = (feels.find_all("span"))[5]
		feels_arr.append(feels_like)

	for i in range(7):
		feels_arr[i] = str(feels_arr[i])
		feels_arr[i] = feels_arr[i]

###### END CONDITIONALS ######

###### DATA FRAME ######
weather = pd.DataFrame({
	"Days": days,
	"Temp": temp,
	"Night": temp_night,
	"Rain   ": rain,
	"    Feels like": feels_arr
	})

weather = weather[["Days", "Temp", "Night", "Rain   ", "    Feels like"]]
weather.index += 1

weather["Days"] = weather["Days"].map(lambda x: x.lstrip('\t'))
weather["Temp"] = weather["Temp"].map(lambda x: x.lstrip('\t'))
if units == "Metric":
	weather["Night"] = weather["Night"].map(lambda x: x.lstrip('\t') + "C")
else:
	weather["Night"] = weather["Night"].map(lambda x: x.lstrip('\t') + "F")

weather["Rain   "] = weather["Rain   "].map(lambda x: x.lstrip('\t').rstrip('\t'))
if units == "Metric":
	weather["    Feels like"] = weather["    Feels like"].map(lambda x: x.lstrip("<span>").rstrip("</span>")+u"\u00b0 " + "C")
else:
	weather["    Feels like"] = weather["    Feels like"].map(lambda x: x.lstrip("<span>").rstrip("</span>")+u"\u00b0" + "F")
###### END DATA FRAME ######

###### RUN ######
print(weather)
###### END RUN ######


