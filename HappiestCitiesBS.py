#50 best places to live in America ranked

from bs4 import BeautifulSoup
import requests
import sqlite3
import os



def getTags():
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
        city_name = tag.find('h2', class_="slide-title-text").text[2:].replace(".", "").strip()  
        best_cities.append((city_name, int(p), int(salary), float(quality)))
    return best_cities
    #print(best_cities)
            


def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn


def setUpCitiesTable(data, cur, conn):
    cur.execute("DROP TABLE IF EXISTS CitiesData")
    cur.execute("CREATE TABLE CitiesData (cities_id INTEGER PRIMARY KEY, population INTEGER, average_annual_salary INTEGER, quality_of_life FLOAT)")
    cur.execute("SELECT * FROM CitiesData")
    num = len(cur.fetchall())
    count = 0
    for elem in data:
        if count == 25:
            break
        if cur.execute("SELECT cities_id FROM CitiesData WHERE cities_id = ?", (city_id,)).fetchone() == None:
            cur.execute("SELECT ID FROM FROM RestaurantCities WHERE Cities = ?", (data[0]))
            cur.execute('INSERT INTO CitiesData (CityName, Population, Average_annual_salary, Quality_of_life) VALUES (?, ?, ?, ?)', (city_id, data[1], data[2], data[3]))
            num = num + 1
            count = count + 1

    conn.commit()


def main():
    cur, conn = setUpDatabase(getTags)
    data = getTags()
    setUpCitiesTable(data, cur, conn)


    


if __name__ == "__main__":
    main()

