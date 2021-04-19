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
    # p = {'term' : 'restaurant', 'location' : location, 'sort_by' : 'review_count', 'sort_by' : 'rating', 'limit' : 50}
    p = {'term' : 'restaurant', 'location' : location, 'sort_by' : 'review_count', 'sort_by' : 'rating', 'limit' : 25}

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

def getRestaurantInfo(rest_info):
    #print(rest_info)
    #print('&**&&**&**&*&')
    restaurantName = [] 
    restaurantPrice = []
    restaurantRating = [] 
    restaurantZip = [] 
    for item in rest_info: 
        restaurantName.append(item[0])
        restaurantPrice.append(item[1])
        restaurantRating.append(item[2])
        restaurantZip.append(item[3])
    tupList = []
    x = 0 
    for x in range(len(restaurantName)): 
        tupList.append((restaurantName[x], restaurantPrice[x], restaurantRating[x], restaurantZip[x]))
        x+=1 
    #print(tupList)
    return tupList



# Create a function called CreateYelpDatabase to insert the values of the list into the table called YelpData
def CreateYelpDatabase(L):
    cur, conn = setUpDatabase('YelpData.db')
    cur.execute('DROP TABLE IF EXISTS YelpData') #REMEMBER TO DELETE BEFORE SUBMITTING!!!!
    cur.execute('CREATE TABLE IF NOT EXISTS YelpData (CounterID INTEGER PRIMARY KEY, RestaurantName TEXT, Price TEXT, Rating FLOAT, zipCode TEXT)')
    
    try:

        restaurantName = [] #HOW DO I DO THIS SO I DONT HAVE TO REPEAT ALL OF THIS BECAUSE I HAVE IN FUNCTION ABOVE
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
        AllYelpelpInformation = getRestaurantInfo(L)
        cur.execute('SELECT RestaurantName FROM YelpData') #selects restaurant name from YelpData table 
        res_name_list = cur.fetchall() #trying to get the restaurant names already added to databae so we know what we can't repeat
    
           
        counter = 1
        # count = len(res_name_list)
        for i in range(25): #HOW DO I MAKE IT DO THIS 4 TIMES SO THAT I GET 100 ROWS???? 
            #print(restaurantName)
            cur.execute('INSERT INTO YelpData (CounterID, RestaurantName, Price, Rating, zipCode) VALUES (?, ?, ?, ?, ?)', (counter, restaurantName[i], restaurantPrice[i], restaurantRating[i], restaurantZip[i],))
            counter += 1
            conn.commit()
        cur.close()

    except: 
        print('not working')

# def fillYelpDatabase(cur, conn): 
#     RestaurantList = CreateYelpDatabase()

    
        
    

# data = dataFromYelp(apiKey, 'Ann Arbor')[0:20]
# YelpDatabase(data)
getRestaurantInfo(dataFromYelp(apiKey, 'Ann Arbor'))
CreateYelpDatabase(dataFromYelp(apiKey, 'Ann Arbor'))
# setUpDatabase('YelpData.db')
    






    