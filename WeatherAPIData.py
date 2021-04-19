#Weather API Data

import json
import requests
import sqlite3
import os

API_KEY = '2c4debeef933141f65cb3c162b82970d'

annarbor_latitude = 42.2808
annarbor_longitude = -83.7430

la_latitude = 34.0522
la_longitude = -118.2437

start_date = 1618358400


def setUpDatabase(db_name):
    '''This function will create a database named after the string 
    input into the function.'''
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def weather_data(API_KEY, latitude, longitude, start_date):
    '''This function calls the requests.get() method on the OpenWeather 
    link and creates a list of tuples containing the temperature, forecast, 
    humidity, and weather conditions for each citiy at a given unix time.'''
    baseurl = "https://api.openweathermap.org/data/2.5/onecall/timemachine?lat={}&lon={}&dt={}&appid={}".format(latitude, longitude, start_date, API_KEY)
    r = requests.get(baseurl)
    response = json.loads(r.text)
    data = []

    for elem in response:
        city = response['lat']
        if city == 42.2808:
            city_name = 'Ann Arbor'
        if city == 34.0522:
            city_name = 'Los Angeles'
        temp = response['current']['temp']
        forecast = response['current']['weather'][0]['description']
        humidity = response['current']['humidity']
        data.append((city_name, temp, forecast, humidity))

    return data


def create_table(cur, conn, data):
    '''This function creates the WeatherData table and inserts the 
    sorted information from both cities to the table.'''

    cur.execute("DROP TABLE IF EXISTS WeatherData")
    cur.execute("CREATE TABLE IF NOT EXISTS WeatherData (city TEXT PRIMARY KEY, temperature FLOAT, forecast TEXT, humidity_percentage FLOAT)")
    for elem in data:
        print(elem)
        cur.execute("INSERT INTO WeatherData (city, temperature, forecast, humidity_percentage) VALUES (?, ?, ?, ?)", (elem[0], elem[1], elem[2], elem[3]))
    conn.commit()

def main():
    cur, conn = setUpDatabase('weather_data.db')
    AA1 = weather_data(API_KEY, annarbor_latitude, annarbor_longitude, start_date)
    create_table(cur, conn, AA1)
    # for i in range(100):
    #     start_date = start_date + 3,600

if __name__ == "__main__":
    main()





# def sort_by_city(API_KEY, latitude, longitude, start_date):
#     '''This function sorts all the data based on which city is input and
#     returns a list containing the weather data from one city.'''
#     city = weather_data(API_KEY, latitude, longitude, start_date)
#     city_sort = []

#     for elem in city:
#         temp = city['current']['temp']
#         forecast = city['current']['weather'][0]['description']
#         humidity = city['current']['humidity']

#         if city['lat'] == annarbor_latitude:
#             city_sort.append(('AA', temp, forecast, humidity))
#         if city['lat'] == la_latitude:
#             city_sort.append(('LA', temp, forecast, humidity))
#     print(city_sort)
#     return city_sort
