#Yelp API Data

import json
import requests
import sqlite3
import os
import csv


'''––––––––––––––––––––––––––––––––––––––––––––––––––––-––––– Global data being used to run functions ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––'''
YELP_KEY = 'kP35wj7sg11cJpUJDjT11YnTc_zqbIyoLmOcb0z98mWud37ESt5qV2d5InA2BGMe-XEceQ4M8n3D8zcLraN6qjRUEiWDcNEK9pWnFnLwCxZHpDbiXnzfLHql0GZ4YHYx'

'''Data to run the Yelp API and set up YelpData and RestaurantCities tables with.'''
yelp_cities = ['Ann Arbor', 'Los Angeles', 'Chicago', 'Detroit', 'New York', 'Indianapolis', 'Nashville', 'Grand Rapids', 'Lancaster']



'''––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– DB: Function to set up a database –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––'''
def setUpDatabase(db_name):
    '''This function will create a database named after the string input into the function.'''

    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn



'''–––––––––––––––––––– YELP API: Pulling data from the Yelp API and putting it into the YelpData table and RestaurantCities Table ––––––––––––––––––––––––––––––'''
def dataFromYelp(apiKey, locationList):
    '''This function pulls data from the Yelp API given a certain list of cities and stores it in a list of tuples containing a restaurant's name, 
    price, rating, zip code and city.'''
    
    information = [] 
    for location in locationList: 
        baseURL = 'https://api.yelp.com/v3/businesses/search'
        headers = {'Authorization': 'Bearer %s' % apiKey}
        p = {'term' : 'restaurant', 'location' : location, 'sort_by' : 'review_count', 'sort_by' : 'rating', 'limit' : 50}

        requestURL = requests.get(baseURL, headers = headers, params = p)
        data = json.loads(requestURL.text)
        yelpData = data['businesses']
        for i in yelpData: 
            information.append((i['name'], i.get('price', ''), i['rating'], i['location']['zip_code'], i['location']['city']))  
    return information


def CreateYelpTable(data, cur, conn):
    '''This function creates the Yelp Table and inserts the all the values in the list of tuples into the respective columns.'''

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


def setUpRestaurantCitiesTable(data, cur, conn): 
    '''This function creates the RestaurantCities Table with the cities pulled from the list of tuples and creates the integer IDs for each city to be
    used later on when joining the data.'''

    cur.execute('CREATE TABLE IF NOT EXISTS RestaurantCities (ID INTEGER PRIMARY KEY, Cities TEXT)')
    count = 0 
    for tup in data: 
        if count == 25: 
            break #break because cannot be 25 so exit for loop and go to line 90
        if cur.execute('SELECT Cities FROM RestaurantCities WHERE Cities = ?', (tup[4],)).fetchone() == None: #making sure no duplicate data 
            cur.execute('INSERT INTO RestaurantCities (Cities) VALUES (?)', (tup[4],))
            count += 1 #controlling for 25 items adding to database at time
    conn.commit()





'''–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– MAIN –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––'''
def main():
    '''The main function calls the function to set up the database, sets up the YelpData table, and RestaurantCities table.'''
    cur, conn = setUpDatabase('finalprojectdatabase.db')
    

    '''Calling the dataFromYelp function, setUpRestaurantCitiesTable function, and CreateYelpTable function on the given list of cities 
    and setting up the YelpData table and RestaurantCities table with the information from those cities.'''
    setUpRestaurantCitiesTable(dataFromYelp(YELP_KEY, yelp_cities), cur, conn)
    CreateYelpTable(dataFromYelp(YELP_KEY, yelp_cities), cur, conn)


    cur.close()


if __name__ == "__main__":
    main()

