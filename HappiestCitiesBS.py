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
        city_id = tag.find('h2', class_="slide-title-text").text[2:].replace(".", "").strip()  
        best_cities.append((city_id, int(p), int(salary), float(quality)))
    return best_cities
    #print(best_cities)
            

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn


def setUpCitiesTable(data, cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS CitiesData (City_Name TEXT PRIMARY KEY, Population INTEGER, Average_annual_salary INTEGER, Quality_of_life FLOAT)")
    cur.execute("SELECT * FROM CitiesData")
    num = len(cur.fetchall())
    count = 0
    for elem in data:
        if count == 25:
            break
        if cur.execute("SELECT City_Name FROM CitiesData WHERE City_Name = ?", (elem[0],)).fetchone() == None:
            #cur.execute("SELECT ID FROM RestaurantCities WHERE Cities = ?", (data[0]))
            cur.execute('INSERT INTO CitiesData (City_Name, Population, Average_annual_salary, Quality_of_life) VALUES (?, ?, ?, ?)', (elem[0], elem[1], elem[2], elem[3]))
            num = num + 1
            count = count + 1

    conn.commit()



def main():
    cur, conn = setUpDatabase('finalprojectdatabase.db')
    data = getTags()
    setUpCitiesTable(data, cur, conn)


if __name__ == "__main__":
    main()

