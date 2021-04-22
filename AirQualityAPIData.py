#Air Quality in Various Cities in America

import json
import requests
import sqlite3
import os

API_KEY = 'd453a8e1-1b40-4d25-b3fe-2133555dcb6c'

def setUpDatabase(db_name):
    '''This function will create a database named after the string input into the function.'''
    
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def airqualitydata(API_KEY, city, state, country):
    baseurl = 'http://api.airvisual.com/v2/city?city={}&state={}&country={}&key={}'.format(city, state, country, API_KEY)
    r = requests.get(baseurl)
    response = json.loads(r.text)
    aqi = []

    base = response.get('data')['current']['pollution']

    try:
        for elem in response:
            city = response['data']['city']
            air_quality = base['aqius']
            weather_temp = response['data']['current']['weather']['tp']
            aqi.append((city, air_quality, weather_temp))
    except:
        print('ERROR')
    return aqi

def create_table(cur, conn, data):
    '''This function creates the WeatherData table and inserts the sorted information from all of the cities cities to the table and
    ensures there is no duplicate data in the tables.'''

    cur.execute("CREATE TABLE IF NOT EXISTS AirQualityData (ID INTEGER, City STRING, AirQuality INTEGER, WeatherTemperature INTEGER)")
    cur.execute("SELECT * FROM AirQualityData")
    num = len(cur.fetchall())
    count = 0
    for elem in data:
        if count == 5:
            break
        print(elem[0])
        if cur.execute("SELECT City FROM AirQualityData WHERE City = ?", (elem[0],)).fetchone() == None:
            cur.execute("SELECT ID FROM RestaurantCities WHERE Cities = ?", (elem[0],))
            # cur.execute('SELECT * FROM RestaurantCities')
            # y = cur.fetchall()
            cityID = cur.fetchone()[0]
            print(cityID)
            cur.execute("INSERT INTO AirQualityData (City, AirQuality, WeatherTemperature) VALUES (?, ?, ?)", (cityID, elem[1], elem[2]))
            num = num + 1
            count = count + 1
    conn.commit()


def main():
    cur, conn = setUpDatabase('finalprojectdatabase.db')

    
    AA = airqualitydata(API_KEY, 'Ann Arbor', 'Michigan', 'USA')
    LA = airqualitydata(API_KEY, 'Los Angeles', 'California', 'USA')
    CHI = airqualitydata(API_KEY, 'Chicago', 'Illinois', 'USA')
    DET = airqualitydata(API_KEY, 'Detroit', 'Michigan', 'USA')
    NYC = airqualitydata(API_KEY, 'New York City', 'New%20York', 'USA')

    create_table(cur, conn, AA)
    create_table(cur, conn, LA)
    create_table(cur, conn, CHI)
    create_table(cur, conn, DET)
    create_table(cur, conn, NYC)

if __name__ == '__main__':
    main()

