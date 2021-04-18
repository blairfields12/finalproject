#Yelp API Data

import json
import requests
import sqlite3
import os


apiKey = 'kP35wj7sg11cJpUJDjT11YnTc_zqbIyoLmOcb0z98mWud37ESt5qV2d5InA2BGMe-XEceQ4M8n3D8zcLraN6qjRUEiWDcNEK9pWnFnLwCxZHpDbiXnzfLHql0GZ4YHYx'

#getting data from the Yelp API
def dataFromYelp(apiKey, location):
    baseURL = 'https://api.yelp.com/v3/businesses/search'
    headers = {'Authorization': 'Bearer %s' % apiKey}
    p = {'term' : 'restaurant', 'location' : location, 'sort_by' : 'review_count', 'sort_by' : 'rating', 'limit' : 50}
    requestURL = requests.get(baseURL, headers = headers, params = p)
    data = json.loads(requestURL.text)
    yelpData = data['businesses']
    information = [] 
    for i in yelpData: 
        if i['id'] not in information: 
            information.append((i['name'], i.get('price', ''), i['rating'], i['location']['zip_code']))  
    # print(information)
    return information

#sets up the database
def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

# Create a function called YelpDatabase to insert the values of the list into the table called YelpData
def YelpDatabase(L):
    cur, conn = setUpDatabase('YelpData.db')
    cur.execute('DROP TABLE IF EXISTS YelpData')
    cur.execute('CREATE TABLE IF NOT EXISTS YelpData (CounterID PRIMARY KEY, RestaurantName TEXT, Price TEXT, Rating FLOAT, zipCode TEXT)')
    
    try:
        restaurantName = [] 
        restaurantPrice = []
        restaurantRating = [] 
        restaurantZip = [] 
        for item in L: 
            restaurantName.append(item[0])
            restaurantPrice.append(item[1])
            restaurantRating.append(item[2])
            restaurantZip.append(item[3])
        # print(restaurantName)
        # print(restaurantPrice)
        counter = 1
        for i in range(25): 
            print(restaurantName)
            cur.execute('INSERT INTO YelpData (CounterID, RestaurantName, Price, Rating, zipCode) VALUES (?, ?, ?, ?, ?)', (counter, restaurantName[i], restaurantPrice[i], restaurantRating[i], restaurantZip[i]))
        counter += 1
        conn.commit()

    except: 
        print('not working')
    

YelpDatabase(dataFromYelp(apiKey, 'Ann Arbor'))
# setUpDatabase('YelpData.db')
    