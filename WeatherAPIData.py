#Weather API Data

import json
import requests
import sqlite3
import os

API_KEY = '2c4debeef933141f65cb3c162b82970d'

annarbor_latitude = 42.280826
annarbor_longitude = -83.743038

la_latitude = 34.052234
la_longitude = -118.243685

start_date = 1614574800
end_date = 1617249599

def setUpDatabase(db_name):
    '''This function will create a database named after the string 
    input into the function.'''
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def weather_data(API_KEY, latitude, longitude):
    '''This function calls the requests.get() method on the OpenWeather 
    link and creates a list of all the data for both cities.'''
    baseurl = "http://history.openweathermap.org/data/2.5/history/city?lat={}&lon={}&type=hour&start={}&end={}&appid={}".format(latitude, longitude, start_date, end_date, API_KEY)
    r = requests.get(baseurl)
    response = json.loads(r.text)
    data = []

    for i in response:
        data.append(response[])
    return data

def sort_by_city(API_KEY, latitude, longitude):
    '''This function sorts all the data based on which city is input and
    returns a list containing the weather data from one city.'''
    city = weather_data(API_KEY, latitude, longitude)
    city_sort = []

    for elem in city:
        if city['latitude'] == annarbor_latitude:
            city_sort.append('AA')
        if city['latitude'] == la_latitude:
            city_sort.append('LA')
    return city_sort

def create_table():
    '''This function creates the WeatherData table and inserts the 
    sorted information from both cities to the table.'''
    cur.execute("CREATE TABLE IF NOT EXISTS Weather Data (city TEXT PRIMARY KEY, date INTEGER, temperature FLOAT, forecast TEXT)")

def main():
    cur, conn = setUpDatabase('weather_data.db')
    weather_data(API_KEY, annarbor_latitude, annarbor_longitude)

if __name__ == "__main__":
    main()
