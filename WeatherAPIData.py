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

chi_latitude = 41.8781
chi_longitude = 87.6298

det_latitude = 42.3314
det_longitude = 83.0458

nyc_latitude = 40.7128
nyc_longitude = 74.0060


def setUpDatabase(db_name):
    '''This function will create a database named after the string input into the function.'''
    
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn


def weather_data(API_KEY, latitude, longitude, start_date):
    '''This function calls the requests.get() method on the OpenWeather link and creates a list of tuples containing the unix time (when the
    data is retrieved from), city name, temperature, forecast, and humidity for each city filtered and sorted by the latitudes.'''
    
    baseurl = "https://api.openweathermap.org/data/2.5/onecall/timemachine?lat={}&lon={}&dt={}&appid={}".format(latitude, longitude, start_date, API_KEY)
    r = requests.get(baseurl)
    response = json.loads(r.text)
    data = []
    position = 0
   
    try:
        for elem in response['hourly']:
            time = response['hourly'][position]['dt']
            city = response['lat']
            if city == 42.2808:
                city_name = 'Ann Arbor'
                temp = response['hourly'][position]['temp']
                forecast = response['hourly'][position]['weather'][0]['description']
                humidity = response['hourly'][position]['humidity']
            if city == 34.0522:
                city_name = 'Los Angeles'
                temp = response['hourly'][position]['temp']
                forecast = response['hourly'][position]['weather'][0]['description']
                humidity = response['hourly'][position]['humidity']
            if city == 41.8781:
                city_name = 'Chicago'
                temp = response['hourly'][position]['temp']
                forecast = response['hourly'][position]['weather'][0]['description']
                humidity = response['hourly'][position]['humidity']
            if city == 42.3314:
                city_name = 'Detroit'
                temp = response['hourly'][position]['temp']
                forecast = response['hourly'][position]['weather'][0]['description']
                humidity = response['hourly'][position]['humidity']
            if city == 40.7128:
                city_name = 'New York City'
                temp = response['hourly'][position]['temp']
                forecast = response['hourly'][position]['weather'][0]['description']
                humidity = response['hourly'][position]['humidity']
            data.append((time, city_name, temp, forecast, humidity))
            position = position + 1
    except:
        print('Error')
    return data


def create_table(cur, conn, data):
    '''This function creates the WeatherData table and inserts the sorted information from all of the cities cities to the table and
    ensures there is no duplicate data in the tables.'''

    cur.execute("CREATE TABLE IF NOT EXISTS WeatherData (ID INTEGER PRIMARY KEY, Time INTEGER, City TEXT, Temperature FLOAT, Forecast TEXT, Humidity_Percentage FLOAT)")
    cur.execute("SELECT * FROM WeatherData")
    num = len(cur.fetchall())
    count = 0
    for elem in data:
        if count == 5:
            break
        if cur.execute("SELECT Time, City FROM WeatherData WHERE Time = ? and City = ?", (elem[0], elem[1],)).fetchone() == None:
            cur.execute("INSERT INTO WeatherData (ID, Time, City, Temperature, Forecast, Humidity_Percentage) VALUES (?, ?, ?, ?, ?, ?)", (num, elem[0], elem[1], elem[2], elem[3], elem[4]))
            num = num + 1
            count = count + 1
    conn.commit()


def main():
    '''The main function calls the function to set up the database, calls the weather_data function with the respective data for each city and
    inserts all of the information into a table called WeatherData.'''
    cur, conn = setUpDatabase('finalprojectdatabase.db')
    start_date = 1619323200
    
    AA = weather_data(API_KEY, annarbor_latitude, annarbor_longitude, start_date)
    LA = weather_data(API_KEY, la_latitude, la_longitude, start_date)
    CHI = weather_data(API_KEY, chi_latitude, chi_longitude, start_date)
    DET = weather_data(API_KEY, det_latitude, det_longitude, start_date)
    NYC = weather_data(API_KEY, nyc_latitude, nyc_longitude, start_date)
    
    create_table(cur, conn, AA)
    create_table(cur, conn, LA)
    create_table(cur, conn, CHI)
    create_table(cur, conn, DET)
    create_table(cur, conn, NYC)


if __name__ == "__main__":
    main()
