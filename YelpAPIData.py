#Yelp API Data

import json
import requests
import sqlite3

apiKey = 'kP35wj7sg11cJpUJDjT11YnTc_zqbIyoLmOcb0z98mWud37ESt5qV2d5InA2BGMe-XEceQ4M8n3D8zcLraN6qjRUEiWDcNEK9pWnFnLwCxZHpDbiXnzfLHql0GZ4YHYx'

def dataFromYelp(apiKey, location):
    baseURL = 'https://api.yelp.com/v3/businesses/search'
    headers = {'Authorization': 'Bearer %s' % apiKey}
    p = {'term' : 'restaurant', 'location' : location, 'sort_by' : 'review_count', 'sort_by' : 'rating', 'limit' : 50}
    requestURL = requests.get(baseURL, headers = headers, params = p)
    data = json.loads(requestURL.text)
    print(data)
    yelpData = data['businesses']
    #print(yelpData)
    information = [] 
    for i in yelpData: 
        if i['id'] not in information: 
            information.append((i['name']))
    #print(information)

dataFromYelp(apiKey, 'Ann Arbor')
    

