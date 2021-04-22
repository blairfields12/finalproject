#HUDAPI data
import json
import requests
import sqlite3
import os
import csv


apiKey = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjkwNDI4NmI0ZjYyNDhhNjJjMWE3N2U0MjVjMWQwYzQ2ODFjOWNhYTI0NWEwMjllMjQ2ZmM0ZDE1ZWRkOWUyNjkyOWI3ODE5ZWRhMWY5MWZlIn0.eyJhdWQiOiI2IiwianRpIjoiOTA0Mjg2YjRmNjI0OGE2MmMxYTc3ZTQyNWMxZDBjNDY4MWM5Y2FhMjQ1YTAyOWUyNDZmYzRkMTVlZGQ5ZTI2OTI5Yjc4MTllZGExZjkxZmUiLCJpYXQiOjE2MTkxMTU2NDMsIm5iZiI6MTYxOTExNTY0MywiZXhwIjoxOTM0NjQ4NDQzLCJzdWIiOiIxNjk5OSIsInNjb3BlcyI6W119.ktqThUDKE8lPYQrZqupweLKzO4Mu_xfCBZkiWPwuq3pBM05AzPOEFmYlRdiIsMrnVW3WuwxsfOS6Op49fwGcQg'

def dataFromHUD(apiKey, locationList):
    '''This function will create a database named after the string input into the function.'''

    information = [] 
    for location in locationList: 
        baseURL = 'https://www.huduser.gov/hudapi/public/il/'
        param = {'county_name': location}
        requestURL = requests.get(baseURL, params = param)
        data = json.loads(requestURL.text)
        print(data)
    #     for i in yelpData: 
    #         # if i['id'] not in information: 
    #         information.append((i['name'], i.get('price', ''), i['rating'], i['location']['zip_code'], i['location']['city']))  
    # return information

dataFromHUD(apiKey, ['Ann Arbor', 'Los Angeles', 'Chicago', 'Detroit', 'New York'])



