#Yelp API Data

import json
import requests
import sqlite3
import os


apiKey = 'kP35wj7sg11cJpUJDjT11YnTc_zqbIyoLmOcb0z98mWud37ESt5qV2d5InA2BGMe-XEceQ4M8n3D8zcLraN6qjRUEiWDcNEK9pWnFnLwCxZHpDbiXnzfLHql0GZ4YHYx'

def dataFromYelp(apiKey, location):
    baseURL = 'https://api.yelp.com/v3/businesses/search'
    headers = {'Authorization': 'Bearer %s' % apiKey}
    p = {'term' : 'restaurant', 'location' : location, 'sort_by' : 'review_count', 'sort_by' : 'rating', 'limit' : 50}
    requestURL = requests.get(baseURL, headers = headers, params = p)
    data = json.loads(requestURL.text)
    # print(data)
    yelpData = data['businesses']
    # print(yelpData)
    information = [] 
    for i in yelpData: 
        if i['id'] not in information: 
            information.append((i['name'], i.get('price', ''), i['rating'], i['location']['zip_code']))  
    # print(information)
    return information

# def yelpData(): 
#     conn = sqlite3.connect(path+'/'+db_name) #NEED HELP 
#     cur = conn.cursor()
    # cur.execute("CREATE TABLE YelpData (RestaurantName TEXT, Price TEXT, Rating FLOAT, zipCode TEXT)")

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

# Create a function called YelpDatabase to insert the values of the dictionary into the table called YelpData
def YelpDatabase(L):
    cur, conn = setUpDatabase('YelpData.db')
    cur.execute('DROP TABLE IF EXISTS YelpData')
    cur.execute('CREATE TABLE IF NOT EXISTS YelpData (CounterID PRIMARY KEY, RestaurantName TEXT, Price TEXT, Rating FLOAT, zipCode TEXT)')
    counter = 1
    for item in L: 
        cur.execute('INSERT INTO YelpData (CounterID, RestaurantName, Price, Rating, zipCode) VALUES (?, ?, ?, ?, ?)', (counter, item[0], item[1], item[2], item[3]))
        counter += 1
    
    conn.commit()
    

# def yelpDatabase(info): 
#     try:
#         restaurantName = [] 
#         restaurantPrice = []
#         restaurantRating = [] 
#         restaurantZip = [] 
#         for i in info: 
#            # print(i)
#     except: 
#         print('not working')
    

YelpDatabase(dataFromYelp(apiKey, 'Ann Arbor'))
# setUpDatabase('YelpData.db')
    