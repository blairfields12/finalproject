#Weather API Data

import json
import requests
import sqlite3

API_KEY = '2c4debeef933141f65cb3c162b82970d'

annarbor_latitude = '42.280826'
annarbor_longitude = '-83.743038'

la_latitude = '34.052234'
la_longitude = '-118.243685'

def weather_data(API_KEY, latitude, longitude):
    baseurl = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&appid={}'.format(latitude, longitude, API_KEY)
    r = requests.get(baseurl)
    response = json.loads(r.text)
    data = []

    for i in range():
        data.append(response[''])
    
    return data