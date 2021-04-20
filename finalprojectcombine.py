#Yelp API Data

import json
import requests
import sqlite3
import os


#sets up the finalproject database
def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn
    
apiKey = 'kP35wj7sg11cJpUJDjT11YnTc_zqbIyoLmOcb0z98mWud37ESt5qV2d5InA2BGMe-XEceQ4M8n3D8zcLraN6qjRUEiWDcNEK9pWnFnLwCxZHpDbiXnzfLHql0GZ4YHYx'

#getting data from the Yelp API
def dataFromYelp(apiKey, locationList):
    information = [] 
    for location in locationList: 
        baseURL = 'https://api.yelp.com/v3/businesses/search'
        headers = {'Authorization': 'Bearer %s' % apiKey}
        p = {'term' : 'restaurant', 'location' : location, 'sort_by' : 'review_count', 'sort_by' : 'rating', 'limit' : 50}

        requestURL = requests.get(baseURL, headers = headers, params = p)
        data = json.loads(requestURL.text)
        yelpData = data['businesses']
        for i in yelpData: 
            # if i['id'] not in information: 
            information.append((i['name'], i.get('price', ''), i['rating'], i['location']['zip_code'], i['location']['city']))  
    return information


# Create a function called CreateYelpDatabase to insert the values of the list into the table called YelpData
def CreateYelpDatabase(data, cur, conn):
    cur.execute('CREATE TABLE IF NOT EXISTS YelpData (RestaurantName TEXT, Price TEXT, Rating FLOAT, zipCode TEXT, CityID INTEGER)')


    count = 0 
    for tup in data: 
        if count == 25: 
            break #break because cannot be 25 so exit for loop and go to line 90
        if cur.execute('SELECT RestaurantName FROM YelpData WHERE RestaurantName = ?', (tup[0],)).fetchone() == None: #making sure no duplicate data 
            cur.execute('SELECT ID FROM RestaurantCities WHERE Cities == ?', (tup[4],)) 
            cityID = cur.fetchone()[0]
            cur.execute('INSERT INTO YelpData (RestaurantName, Price, Rating, zipCode, CityID) VALUES (?, ?, ?, ?, ?)', (tup[0], tup[1], tup[2], tup[3], cityID))
            count += 1 #controlling for 25 items adding to database at time
    
    conn.commit()

#CreateCities table 
def setUpCitiesTable(data, cur, conn): 
    cur.execute('CREATE TABLE IF NOT EXISTS RestaurantCities (ID INTEGER PRIMARY KEY, Cities TEXT)')
    count = 0 
   # print(data)
    for tup in data: 
        if count == 25: 
            break #break because cannot be 25 so exit for loop and go to line 90
        if cur.execute('SELECT Cities FROM RestaurantCities WHERE Cities = ?', (tup[4],)).fetchone() == None: #making sure no duplicate data 
            cur.execute('INSERT INTO RestaurantCities (Cities) VALUES (?)', (tup[4],))
            count += 1 #controlling for 25 items adding to database at time
    
    conn.commit()

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


def weather_data(API_KEY, latitude, longitude, start_date):
    '''This function calls the requests.get() method on the OpenWeather 
    link and creates a list of tuples containing the temperature, forecast, 
    humidity, and weather conditions for each citiy at a given unix time.'''
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
    '''This function creates the WeatherData table and inserts the 
    sorted information from both cities to the table.'''

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
    cur, conn = setUpDatabase('finalproject.db')
    start_date = 1618358400
    
    AA = weather_data(API_KEY, annarbor_latitude, annarbor_longitude, start_date)
    LA = weather_data(API_KEY, la_latitude, la_longitude, start_date)
    CHI = weather_data(API_KEY, chi_latitude, chi_longitude, start_date)
    DET = weather_data(API_KEY, det_latitude, det_longitude, start_date)
    NYC = weather_data(API_KEY, nyc_latitude, nyc_latitude, start_date)
    
    create_table(cur, conn, AA)
    create_table(cur, conn, LA)
    create_table(cur, conn, CHI)
    create_table(cur, conn, DET)
    create_table(cur, conn, NYC)

    setUpCitiesTable(dataFromYelp(apiKey, ['Ann Arbor', 'Los Angeles', 'Chicago', 'Detroit', 'New York']), cur, conn)
    CreateYelpDatabase(dataFromYelp(apiKey, ['Ann Arbor', 'Los Angeles', 'Chicago', 'Detroit', 'New York']), cur, conn)

if __name__ == "__main__":
    main()


