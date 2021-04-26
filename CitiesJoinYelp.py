#JOIN Statement between Cities and Yelp Tables
import sqlite3
import os


def joinCitiesData():
    base_dir = os.path.dirname(os.path.realpath(__file__))
    conn = sqlite3.connect(base_dir + '/finalprojectdatabase.db')
    cur = conn.cursor()
    # cur.execute("SELECT CitiesData.Quality_of_Life, CitiesData.Average_Annual_Salary, CitiesData.Population FROM CitiesData LEFT JOIN RestaurantCities ON RestaurantCities.ID = CitiesData.CityID")
    cur.execute("SELECT Quality_of_Life, Average_Annual_Salary, Population FROM CitiesData JOIN RestaurantCities ON trim(CitiesData.CityID) = trim(RestaurantCities.ID)")
    conn.commit()
    joined = cur.fetchall()
    for x in joined: 
        print(x)
    #make a new column and execute x into it 
    cur.close()

joinCitiesData()