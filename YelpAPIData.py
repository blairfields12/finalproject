#Yelp API Data

import json
import requests
import sqlite3
<<<<<<< HEAD
=======
import os


apiKey = 'kP35wj7sg11cJpUJDjT11YnTc_zqbIyoLmOcb0z98mWud37ESt5qV2d5InA2BGMe-XEceQ4M8n3D8zcLraN6qjRUEiWDcNEK9pWnFnLwCxZHpDbiXnzfLHql0GZ4YHYx'

#getting data from the Yelp API
def dataFromYelp(apiKey, locationList):
    for location in locationList: 

        baseURL = 'https://api.yelp.com/v3/businesses/search'
        headers = {'Authorization': 'Bearer %s' % apiKey}
        # p = {'term' : 'restaurant', 'location' : location, 'sort_by' : 'review_count', 'sort_by' : 'rating', 'limit' : 50}
        p = {'term' : 'restaurant', 'location' : location, 'sort_by' : 'review_count', 'sort_by' : 'rating', 'limit' : 50}

        requestURL = requests.get(baseURL, headers = headers, params = p)
        data = json.loads(requestURL.text)
        yelpData = data['businesses']
        # print(yelpData)
        information = [] 
        for i in yelpData: 
            if i['id'] not in information: 
                information.append((i['name'], i.get('price', ''), i['rating'], i['location']['zip_code'], i['location']['city']))  
        # print(information)
    return information

#sets up the database
def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

# def getRestaurantInfo(rest_info):
#     #print(rest_info)
#     #print('&**&&**&**&*&')
#     restaurantName = [] 
#     restaurantPrice = []
#     restaurantRating = [] 
#     restaurantZip = [] 
#     for item in rest_info: 
#         restaurantName.append(item[0])
#         restaurantPrice.append(item[1])
#         restaurantRating.append(item[2])
#         restaurantZip.append(item[3])
#     tupList = []
#     x = 0 
#     for x in range(len(restaurantName)): 
#         tupList.append((restaurantName[x], restaurantPrice[x], restaurantRating[x], restaurantZip[x]))
#         x+=1 
#     #print(tupList)
#     return tupList
   

# Create a function called CreateYelpDatabase to insert the values of the list into the table called YelpData
def CreateYelpDatabase(data, cur, conn):
    cur.execute('CREATE TABLE IF NOT EXISTS YelpData (RestaurantName TEXT, Price TEXT, Rating FLOAT, zipCode TEXT, CityID INTEGER)')

    # restaurantName = [] #HOW DO I DO THIS SO I DONT HAVE TO REPEAT ALL OF THIS BECAUSE I HAVE IN FUNCTION ABOVE
    # restaurantPrice = []
    # restaurantRating = [] 
    # restaurantZip = [] 
    # for item in L: 
    #     restaurantName.append(item[0])
    #     restaurantPrice.append(item[1])
    #     restaurantRating.append(item[2])
    #     restaurantZip.append(item[3])
    # print(restaurantName)
    # print(restaurantPrice)
    # cur.execute('SELECT RestaurantName FROM YelpData') #selects restaurant name from YelpData table 
    # res_name_list = cur.fetchall() #trying to get the restaurant names already added to databae so we know what we can't repeat

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
    print(data)
    for tup in data: 
        if count == 25: 
            break #break because cannot be 25 so exit for loop and go to line 90
        if cur.execute('SELECT Cities FROM RestaurantCities WHERE Cities = ?', (tup[4],)).fetchone() == None: #making sure no duplicate data 
            cur.execute('INSERT INTO RestaurantCities (Cities) VALUES (?)', (tup[4],))
            count += 1 #controlling for 25 items adding to database at time
    
    conn.commit()
#zipcodeID connects this table to yelp table - strings of zipcodes takes up more space than numbers so  beneficial for repeating zipcodes


    
        
    

# data = dataFromYelp(apiKey, 'Ann Arbor')[0:20]
# YelpDatabase(data)
# getRestaurantInfo(dataFromYelp(apiKey, ['Ann Arbor', 'Los Angeles', 'Chicago']))
cur, conn = setUpDatabase('YelpData.db')
setUpCitiesTable(dataFromYelp(apiKey, ['Ann Arbor', 'Los Angeles', 'Chicago', 'Detroit', 'New York']), cur, conn)
CreateYelpDatabase(dataFromYelp(apiKey, ['Ann Arbor', 'Los Angeles', 'Chicago', 'Detroit', 'New York']), cur, conn)
# setUpDatabase('YelpData.db')

conn.close()
    


>>>>>>> e1aa0f94cb7ad0ff48911aa51ddd10f96d653e95
