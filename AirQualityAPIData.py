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

def airqualitydata(API_KEY, country, state, city):
    baseurl = 'http://api.airvisual.com/v2/city?city={{}}&state={{}}&country={{}}&key={{}}'.format(city, state, country, API_KEY)
    r = requests.get(baseurl)
    response = json.loads(r.text)
    aqi = []

    print(response['data']['city'])
    print(response['data']['forecasts'][0]['pollution'])
    try:
        for elem in response['data']['forecasts']['current']['pollution']:
            print(elem)
            city = response['data']['city']
            air_quality = response['pollution']['aquis']
            pollutant_concentration = ['pollution']['p1']['conc']
            aqi.append((city, air_quality, pollutant_concentration))
    except:
        print('ERROR')
    return aqi

def create_table(cur, conn, data):
    '''This function creates the WeatherData table and inserts the sorted information from all of the cities cities to the table and
    ensures there is no duplicate data in the tables.'''

    cur.execute("CREATE TABLE IF NOT EXISTS AirQualityData (ID INTEGER, City STRING, AirQuality INTEGER, PollutantConcentration INTEGER)")
    cur.execute("SELECT * FROM AirQualityData")
    num = len(cur.fetchall())
    count = 0
    for elem in data:
        if count == 5:
            break
        if cur.execute("SELECT City FROM WeatherData WHERE City = ?", (elem[0],)).fetchone() == None:
            cur.execute("SELECT ID FROM RestaurantCities WHERE Cities = ?", (elem[0],))
            cityID = cur.fetchone()[0]
            cur.execute("INSERT INTO AirQualityData (ID, City, AirQuality, PollutantConcentration) VALUES (?, ?, ?, ?)", (cityID, elem[0], elem[1], elem[2]))
            num = num + 1
            count = count + 1
    conn.commit()

def main():
    cur, conn = setUpDatabase('AirQuality.db')
    LA = airqualitydata(API_KEY, 'USA', 'California', 'Los Angeles')
    create_table(cur, conn, LA)

if __name__ == '__main__':
    main()
