#Weather API Data

import json
import requests
import sqlite3

API_KEY = '2c4debeef933141f65cb3c162b82970d'

annarbor_latitude = 42.280826
annarbor_longitude = -83.743038

la_latitude = 34.052234
la_longitude = -118.243685

start_date = 1614574800
end_date = 1617249599

def weather_data(API_KEY, latitude, longitude):
    baseurl = "http://history.openweathermap.org/data/2.5/history/city?lat={}&lon={}&type=hour&start={}&end={}&appid={}".format(latitude, longitude, start_date, end_date, API_KEY)
    r = requests.get(baseurl)
    response = json.loads(r.text)
    data = []

    print(response)

def main():
    weather_data(API_KEY, annarbor_latitude, annarbor_longitude)

if __name__ == "__main__":
    main()