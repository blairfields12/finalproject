#Cities Beautiful Soup

import json
import requests
import sqlite3
import os
import csv
from bs4 import BeautifulSoup

'''––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– DB: Function to set up a database –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––'''
def setUpDatabase(db_name):
    '''This function will create a database named after the string input into the function.'''

    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn




'''––––––––––––––––– CITIES BEAUTIFUL SOUP: Pulling data from Business Insider using Beautiful Soup and putting it into the CitiesData table ––––––––––––––––––––'''
def getTags():
    '''This function pulls data from Business Insider using Beautiful Soup and returns a list of tuples containing 50 cities and their population, 
    average annual salary, and quality of life rating.'''
    url = 'https://www.businessinsider.com/us-news-best-places-to-live-in-america-2016-3'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    best_cities = []
    tags = soup.find_all('div', class_="slide-layout clearfix")
    p = 0
    salary = 0
    quality = 0
    

    for tag in tags:
        for content in tag.find_all('p'):
            if content.text.startswith("Population:"):
                p = content.text.replace("Population:", "").strip()
                p = p.replace(",", '')   
         
            if content.text.startswith("Average annual salary:"):
                salary = content.text.replace("Average annual salary:", "").strip()[1:]
                salary = salary.replace(",", '')   

            if content.text.startswith("Quality of life:"):
                quality = content.text.replace("Quality of life:", "").strip()
        cit = tag.find('h2', class_="slide-title-text").text[2:].replace(".", "").strip()  
        city = cit.split(',')
        city_id = city[0]
        state = city[1]
        best_cities.append((city_id, state, int(p), int(salary), float(quality)))
    return best_cities


def setUpCitiesTable(data, cur, conn):
    '''This function creates the CitiesData Table with the cities pulled from the list of tuples and sorts the data into the respective columns.'''
    cur.execute("CREATE TABLE IF NOT EXISTS CitiesData (City_Name TEXT PRIMARY KEY, State_Name TEXT, Population INTEGER, Average_Annual_Salary INTEGER, Quality_of_Life FLOAT)")
    cur.execute("SELECT * FROM CitiesData")
    num = len(cur.fetchall())
    count = 0
    for elem in data:
        if count == 25:
            break
        if cur.execute("SELECT City_Name FROM CitiesData WHERE City_Name = ?", (elem[0],)).fetchone() == None:
            cur.execute('INSERT INTO CitiesData (City_Name, State_Name, Population, Average_annual_salary, Quality_of_life) VALUES (?, ?, ?, ?, ?)', (elem[0], elem[1], elem[2], elem[3], elem[4]))
            num = num + 1
            count = count + 1
    conn.commit()




'''–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– MAIN –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––'''
def main():
    '''The main function calls the function to set up the database, sets up the YelpData table, RestaurantCities table, WeatherData table, 
    and CitiesData Table. It calls all the visualization functions and calculation functions, as well as the JOIN statement.'''
    cur, conn = setUpDatabase('finalprojectdatabase.db')
    


    '''Calling the getTags function and setUpCitiesTable using Beautiful Soup on Business Insider to get the data about the 50 cities and put
    them into a table.'''
    data = getTags()
    setUpCitiesTable(data, cur, conn)


    cur.close()


if __name__ == "__main__":
    main()