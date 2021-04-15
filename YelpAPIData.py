#Yelp API Data

import json
import requests
import sqlite3

apiKey = 'mq7UhVeyQ6mG3od9DRFjZQ'

def dataFromYelp(apiKey, location):
    baseURL = 'https://api.yelp.com/v3/businesses/search'
    headers = {'Authorization': 'Bearer %s' % apiKey}
    p = {'term' : 'restaurant', 'location' : location, 'sort_by' : 'review_count', 'sort_by' : 'rating', 'limit' : 50}
    requestURL = requests.get(baseURL, headers = headers, params = p)
    

