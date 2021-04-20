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

    print(response.get('data'))

    base = response['data']['current']['pollution']['conc']

    try:
        for elem in base:
            city = response['data']['city']
            air_quality = base['aquis']
            atmospheric_pressure = base['pr']
            aqi.append((city, air_quality, atmospheric_pressure))
    except:
        print('ERROR')
    return aqi

def create_table(cur, conn, data):
    '''This function creates the WeatherData table and inserts the sorted information from all of the cities cities to the table and
    ensures there is no duplicate data in the tables.'''

    cur.execute("CREATE TABLE IF NOT EXISTS AirQualityData (ID INTEGER, City STRING, AirQuality INTEGER, AtmosphericPressure INTEGER)")
    cur.execute("SELECT * FROM AirQualityData")
    num = len(cur.fetchall())
    count = 0
    for elem in data:
        if count == 5:
            break
        if cur.execute("SELECT City FROM WeatherData WHERE City = ?", (elem[0],)).fetchone() == None:
            cur.execute("SELECT ID FROM RestaurantCities WHERE Cities = ?", (elem[0],))
            cityID = cur.fetchone()[0]
            cur.execute("INSERT INTO AirQualityData (ID, City, AirQuality, AtmosphericPressure) VALUES (?, ?, ?, ?)", (cityID, elem[0], elem[1], elem[2]))
            num = num + 1
            count = count + 1
    conn.commit()

def main():
    cur, conn = setUpDatabase('AirQuality.db')
    
    AA = airqualitydata(API_KEY, 'Ann Arbor', 'Michigan', 'USA')
    LA = airqualitydata(API_KEY, 'Los Angeles', 'California', 'USA')
    CHI = airqualitydata(API_KEY, 'Chicago', 'Illinois', 'USA')
    DET = airqualitydata(API_KEY, 'Detroit', 'Michigan', 'USA')
    NYC = airqualitydata(API_KEY, 'New York', 'New York', 'USA')

    create_table(cur, conn, AA)
    create_table(cur, conn, LA)
    create_table(cur, conn, CHI)
    create_table(cur, conn, DET)
    create_table(cur, conn, NYC)

if __name__ == '__main__':
    main()
