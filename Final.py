#SI 206 Final Project
#By Blair Fields, Mia Schaftel, and Savy Dardashti

import json
import requests
import sqlite3
import os
from bs4 import BeautifulSoup
import csv
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
from numpy import genfromtxt
import plotly.express as px
import pandas as pd 



'''––––––––––––––––––––––––––––––––––––––––––––––––––––-––––– Global data being used to run functions ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––'''
YELP_KEY = 'kP35wj7sg11cJpUJDjT11YnTc_zqbIyoLmOcb0z98mWud37ESt5qV2d5InA2BGMe-XEceQ4M8n3D8zcLraN6qjRUEiWDcNEK9pWnFnLwCxZHpDbiXnzfLHql0GZ4YHYx'
WEATHER_KEY = '2c4debeef933141f65cb3c162b82970d'

'''Data to run the OpenWeather API and set up the WeatherData table with.'''
annarbor_latitude = 42.2808
annarbor_longitude = -83.7430
la_latitude = 34.0522
la_longitude = -118.2437
chi_latitude = 41.8781
chi_longitude = 87.6298
det_latitude = 42.3314
det_longitude = 83.0458
nyc_latitude = 40.7128
nyc_longitude = 74.0060
start_date = 1619323200

'''Data to run the Yelp API and set up YelpData and RestaurantCities tables with.'''
yelp_cities = ['Ann Arbor', 'Los Angeles', 'Chicago', 'Detroit', 'New York', 'Indianapolis', 'Nashville', 'Grand Rapids', 'Lancaster']



'''––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– DB: Function to set up a database –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––'''
def setUpDatabase(db_name):
    '''This function will create a database named after the string input into the function.'''

    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn



'''––––––––––––––––––––––––––––––––– WEATHER API: Pulling data from the OpenWeather API and putting it into the WeatherData table ––––––––––––––––––––––––––––––'''
def weather_data(API_KEY, latitude, longitude, start_date):
    '''This function calls the requests.get() method on the OpenWeather link and creates a list of tuples containing the unix time (when the
    data is retrieved from), city name, temperature, forecast, and humidity for each city filtered and sorted by the latitudes.'''
    
    baseurl = "https://api.openweathermap.org/data/2.5/onecall/timemachine?lat={}&lon={}&dt={}&appid={}".format(latitude, longitude, start_date, API_KEY)
    r = requests.get(baseurl)
    response = json.loads(r.text)
    data = []
    position = 0
   
    try:
        for elem in response['hourly']:
            time = response['hourly'][position]['dt']
            city = response['lat']
            if city == 42.2808:
                city_name = 'Ann Arbor'
                temp = response['hourly'][position]['temp']
                forecast = response['hourly'][position]['weather'][0]['description']
                humidity = response['hourly'][position]['humidity']
            if city == 34.0522:
                city_name = 'Los Angeles'
                temp = response['hourly'][position]['temp']
                forecast = response['hourly'][position]['weather'][0]['description']
                humidity = response['hourly'][position]['humidity']
            if city == 41.8781:
                city_name = 'Chicago'
                temp = response['hourly'][position]['temp']
                forecast = response['hourly'][position]['weather'][0]['description']
                humidity = response['hourly'][position]['humidity']
            if city == 42.3314:
                city_name = 'Detroit'
                temp = response['hourly'][position]['temp']
                forecast = response['hourly'][position]['weather'][0]['description']
                humidity = response['hourly'][position]['humidity']
            if city == 40.7128:
                city_name = 'New York City'
                temp = response['hourly'][position]['temp']
                forecast = response['hourly'][position]['weather'][0]['description']
                humidity = response['hourly'][position]['humidity']
            data.append((time, city_name, temp, forecast, humidity))
            position = position + 1
    except:
        print('Error')
    return data


def weather_table(cur, conn, data):
    '''This function creates the WeatherData table and inserts the sorted information from all of the cities cities to the table and
    ensures there is no duplicate data in the tables.'''

    cur.execute("CREATE TABLE IF NOT EXISTS WeatherData (ID INTEGER PRIMARY KEY, Time INTEGER, City TEXT, Temperature FLOAT, Forecast TEXT, Humidity_Percentage FLOAT)")
    cur.execute("SELECT * FROM WeatherData")
    num = len(cur.fetchall())
    count = 0
    for elem in data:
        if count == 5:
            break
        if cur.execute("SELECT Time, City FROM WeatherData WHERE Time = ? and City = ?", (elem[0], elem[1],)).fetchone() == None:
            cur.execute("INSERT INTO WeatherData (ID, Time, City, Temperature, Forecast, Humidity_Percentage) VALUES (?, ?, ?, ?, ?, ?)", (num, elem[0], elem[1], elem[2], elem[3], elem[4]))
            num = num + 1
            count = count + 1
    conn.commit()



'''–––––––––––––––––––– YELP API: Pulling data from the Yelp API and putting it into the YelpData table and RestaurantCities Table ––––––––––––––––––––––––––––––'''
def dataFromYelp(apiKey, locationList):
    '''This function pulls data from the Yelp API given a certain list of cities and stores it in a list of tuples containing a restaurant's name, 
    price, rating, zip code and city.'''
    
    information = [] 
    for location in locationList: 
        baseURL = 'https://api.yelp.com/v3/businesses/search'
        headers = {'Authorization': 'Bearer %s' % apiKey}
        p = {'term' : 'restaurant', 'location' : location, 'sort_by' : 'review_count', 'sort_by' : 'rating', 'limit' : 50}

        requestURL = requests.get(baseURL, headers = headers, params = p)
        data = json.loads(requestURL.text)
        yelpData = data['businesses']
        for i in yelpData: 
            # if i['id'] not in information: 
            information.append((i['name'], i.get('price', ''), i['rating'], i['location']['zip_code'], i['location']['city']))  
    return information


def CreateYelpTable(data, cur, conn):
    '''This function creates the Yelp Table and inserts the all the values in the list of tuples into the respective columns.'''

    cur.execute('CREATE TABLE IF NOT EXISTS YelpData (RestaurantName TEXT, Price TEXT, Rating FLOAT, zipCode TEXT, CityID INTEGER)')
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


def setUpRestaurantCitiesTable(data, cur, conn): 
    '''This function creates the RestaurantCities Table with the cities pulled from the list of tuples and creates the integer IDs for each city to be
    used later on when joining the data.'''

    cur.execute('CREATE TABLE IF NOT EXISTS RestaurantCities (ID INTEGER PRIMARY KEY, Cities TEXT)')
    count = 0 
    for tup in data: 
        if count == 25: 
            break #break because cannot be 25 so exit for loop and go to line 90
        if cur.execute('SELECT Cities FROM RestaurantCities WHERE Cities = ?', (tup[4],)).fetchone() == None: #making sure no duplicate data 
            cur.execute('INSERT INTO RestaurantCities (Cities) VALUES (?)', (tup[4],))
            count += 1 #controlling for 25 items adding to database at time
    conn.commit()



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
        best_cities.append((city_id, int(p), int(salary), float(quality)))
    return best_cities


def setUpCitiesTable(data, cur, conn):
    '''This function creates the CitiesData Table with the cities pulled from the list of tuples and sorts the data into the respective columns.'''
    cur.execute("CREATE TABLE IF NOT EXISTS CitiesData (City_Name TEXT PRIMARY KEY, Population INTEGER, Average_Annual_Salary INTEGER, Quality_of_Life FLOAT, CityID INTEGER)")
    cur.execute("SELECT * FROM CitiesData")
    num = len(cur.fetchall())
    count = 0
    for elem in data:
        if count == 25:
            break
        if cur.execute("SELECT City_Name FROM CitiesData WHERE City_Name = ?", (elem[0],)).fetchone() == None:
            try: 
                cur.execute('SELECT ID FROM RestaurantCities WHERE Cities = ?', (elem[0],)) 
                cityID = cur.fetchone()[0]
                cur.execute('INSERT INTO CitiesData (City_Name, Population, Average_annual_salary, Quality_of_life, CityID) VALUES (?, ?, ?, ?, ?)', (elem[0], elem[1], elem[2], elem[3], cityID))
                num = num + 1
                count = count + 1
            except: 
                cur.execute('INSERT INTO CitiesData (City_Name, Population, Average_annual_salary, Quality_of_life) VALUES (?, ?, ?, ?)', (elem[0], elem[1], elem[2], elem[3]))
    conn.commit()



'''–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– CALCULATIONS ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––'''
def convertFromKelvinToCelsiusAndFahrenheit(cur, conn, filepath):
    '''Converting the Kelvin input temperature to Celsius and Fahrenheit and ouputting the results into a CSV file.'''
    cur.execute('SELECT WeatherData.Temperature FROM WeatherData')
    data = cur.fetchall()
    conn.commit()

    kelvinTemp = []
    for tup in data: 
        for i in tup: 
            kelvinTemp.append(i)

    celsiusTemp = []
    for i in kelvinTemp:
        c = i - 273.15
        celsiusTemp.append((c))

    '''Converting temperatures in degrees Celsius to Fahrenheit, multiply by 1.8 (or 9/5) and add 32.'''
    FahrenheitTemp = [] 
    for i in celsiusTemp:
        F = (1.8 * i) + 32
        FahrenheitTemp.append((F))

    with open(filepath, 'w', newline = '', encoding= 'utf-8') as f: 
        f = csv.writer(f, delimiter = ',')
        f.writerow(['Temp in Kelvin', 'Temp in Celsius', 'Temp in Fahrenheit'])
        count = 0
        for i in kelvinTemp:
            temps = (kelvinTemp[count], celsiusTemp[count], FahrenheitTemp[count])
            count += 1
            f.writerow(temps)


def PricesPerCityCount(cur, con, filepath): 
    '''Calculating the number of restaurants with each price ($, $$, $$$, $$$) in two zip codes and outputting the results into a CSV file.'''
    data = cur.execute('SELECT Price,cityID FROM YelpData').fetchall()
    conn.commit()

    with open(filepath, 'w', newline = '', encoding= 'utf-8') as f: 
        f = csv.writer(f, delimiter = ',')

        annArborprice1 = 0
        NewYorkprice1 = 0 
        annArborprice2 = 0 
        NewYorkprice2 = 0 
        annArborprice3 = 0 
        NewYorkprice3 = 0 
        annArborprice4 = 0 
        NewYorkprice4 = 0 

        for tup in data: 
            if tup[0] == '$':
                if tup[1] == 2:
                    annArborprice1 += 1 
                if tup[1] == 42: 
                    NewYorkprice1 += 1 
            if tup[0] == '$$':
                if tup[1] == 2:
                    annArborprice2 += 1 
                if tup[1] == 42: 
                    NewYorkprice2 += 1 

            if tup[0] == '$$$':
                if tup[1] == 2:
                    annArborprice3 += 1 
                if tup[1] == 42: 
                    NewYorkprice3 += 1 
            
            if tup[0] == '$$$$':
                if tup[1] == 2:
                    annArborprice4 += 1 
                if tup[1] == 42:
                    NewYorkprice4 += 1
        

        priceCityData = (annArborprice1, NewYorkprice1, annArborprice2, NewYorkprice2, annArborprice3, NewYorkprice3, annArborprice4, NewYorkprice4)
        f.writerow(['Ann Arbor $', 'New York $', 'Ann Arbor $$', 'New York $$', 'Ann Arbor $$$', 'New York $$$', 'Ann Arbor $$$$', 'New York $$$$'])
        f.writerow(priceCityData)


def salary_quality(cur, conn, filepath):
    '''Calculating the socioeconomic status for each city to see if restaurants that are pricer have more wealthy people in that city.'''
    cur.execute('SELECT * FROM CitiesData')
    data = cur.fetchall()
    conn.commit()

    cityNames = []
    income = []
    qualityOfLife = []
    population = [] 
    for tup in data: 
        # print(tup)
        cityNames.append(tup[0])
        population.append(tup[1])
        income.append(tup[2])
        qualityOfLife.append(tup[3])


    """Trying to calculate if there is a relationship between each cities income and their quality of life rating."""
    relationships = []
    for i in range(len(income)): 
        calc = income[i]/qualityOfLife[i]
        relationships.append([cityNames[i], calc])


    with open(filepath, 'w', newline = '', encoding= 'utf-8') as f: 
        f = csv.writer(f, delimiter = ',')
        f.writerow(['City Name', 'Populations', 'Avg Income', 'Quality of Life', 'Avg Income / Quality of Life'])
        count = 0
        for i in population:
            headers = (cityNames[count], population[count], income[count], qualityOfLife[count], relationships[count][1])
            count += 1
            f.writerow(headers)



'''–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– VISUALIZATION ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––'''
def weather_visualization():
    with sqlite3.connect(path) as weather_data:
        cur = weather_data.cursor()
        data = cur.execute("SELECT * FROM WeatherData").fetchall()

        AA_data = []
        for item in data: 
            if 'Ann Arbor' in item: 
                AA_data.append(item)

        LA_data = []
        for item in data: 
            if "Los Angeles" in item: 
                LA_data.append(item)
        
        Chi_data = []
        for item in data: 
            if "Chicago" in item: 
                Chi_data.append(item)

        Det_data = []
        for item in data: 
            if "Detroit" in item: 
                Det_data.append(item)

        NYC_data = []
        for item in data: 
            if "New York City" in item: 
                NYC_data.append(item)
        
        aa_temperature = []
        la_temperature = []
        chi_temperature = []
        det_temperature = []
        nyc_temperature = []
        aa_time = []
        la_time = [] 
        chi_time = [] 
        det_time = [] 
        nyc_time = [] 

        for i in AA_data: 
            aa_temperature.append(i[3])
            aa_time.append(i[1])

        for i in LA_data: 
            la_temperature.append(i[3])
            la_time.append(i[1])

        for i in Chi_data: 
            chi_temperature.append(i[3])
            chi_time.append(i[1])

        for i in Det_data: 
            det_temperature.append(i[3])
            det_time.append(i[1])
        
        for i in NYC_data: 
            nyc_temperature.append(i[3])
            nyc_time.append(i[1])


    '''Plotting the data'''

    time2 = aa_time[1]
    time3 = aa_time[2]
    time4 = aa_time[3]
    time5 = aa_time[4]
    time6 = aa_time[5]

    f, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5)
    f.suptitle('Temperature Values for Ann Arbor vs. Los Angeles vs. Chicago \n vs. Detroit vs. NYC Over a 25 Hour Period', fontsize= 10)

    x = np.arange(1,5)

    ax1.plot(aa_time, aa_temperature, 'y', label = 'Ann Arbor, MI')

    ax1.tick_params(axis='x', labelsize=6)
    ax1.tick_params(axis='y', labelsize=6)
    x_axis = ax1.axes.get_xaxis()
    x_axis.set_visible(False)


    ax2.plot(la_time, la_temperature, 'b', label = 'Los Angeles, CA')
    ax2.tick_params(axis='x', labelsize=6)
    ax2.tick_params(axis='y', labelsize=6)
    x_axis = ax2.axes.get_xaxis()
    x_axis.set_visible(False)

    ax3.plot(chi_time, chi_temperature, 'r', label = 'Chicago, IL')
    ax3.tick_params(axis='x', labelsize=6)
    ax3.tick_params(axis='y', labelsize=6)
    x_axis = ax3.axes.get_xaxis()
    x_axis.set_visible(False)

    ax4.plot(det_temperature, 'g', label = 'Detroit, MI')
    ax4.tick_params(axis='x', labelsize=6)
    ax4.tick_params(axis='y', labelsize=6)
    x_axis = ax4.axes.get_xaxis()
    x_axis.set_visible(False)

    ax5.plot(nyc_time, nyc_temperature, 'k', label = 'New York City, NY')
    ax5.tick_params(axis='x', labelsize=6)
    ax5.tick_params(axis='y', labelsize=6)

    plt.legend()
    plt.grid(True)
    plt.show()



def yelp_visualization():
    with sqlite3.connect(path) as Yelpdatabase:
        cur = Yelpdatabase.cursor()
        cur.execute("SELECT * FROM YelpData")
        data = cur.fetchall()
        print(data)

        AnnArborRatings = [] 
        NewYorkRatings = [] 
        
        for items in data[:50]: 
            AnnArborRatings.append(items[2])
        for items in data[200:]: 
            NewYorkRatings.append(items[2])
        
        AA_rated_four = [] 
        NY_rated_four = [] 
        for rating in AnnArborRatings: 
            if rating == 4.0: 
                AA_rated_four.append(rating)
        for rating in NewYorkRatings: 
            if rating == 4.0: 
                NY_rated_four.append(rating)

        AA_rated_four_five = []
        NY_rated_four_five =[]
        for rating in AnnArborRatings: 
            if rating == 4.5: 
                AA_rated_four_five.append(rating)
        for rating in NewYorkRatings: 
            if rating == 4.5: 
                NY_rated_four_five.append(rating)

        AA_rated_five = []
        NY_rated_five = []
        for rating in AnnArborRatings: 
            if rating == 5.0: 
                AA_rated_five.append(rating)
        for rating in NewYorkRatings: 
            if rating == 5.0: 
                NY_rated_five.append(rating)
        

    '''Plotting the data'''
    labels = ['4.0', '4.5', '5.0']
    AARatingsCount = [12, 35, 3]
    NYRatingsCount = [0, 19, 30]

    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars
    opacity = 0.4

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, AARatingsCount, width, alpha = opacity, color = 'blue', label='Ann Arbor')
    rects2 = ax.bar(x + width/2, NYRatingsCount, width, alpha = opacity, color = 'red', label='Los Angeles')

    '''Adding labels, title and custom x-axis tick labels, etc. '''
    ax.set_ylabel('Number of Restaurants With Rating')
    ax.set_title('Restaurants in Ann Arbor and New York With Each Rating')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    fig.tight_layout()
    plt.show()



def cities_visualization(cur):
    cur.execute("SELECT * FROM CitiesData")
    data = cur.fetchall()

    cityNames = []
    income = []
    qualityOfLife = []
    population = [] 
    for tup in data: 
        cityNames.append(tup[0])
        population.append(tup[1])
        income.append(tup[2])
        qualityOfLife.append(tup[3])

    relationships = []
    for i in range(len(income)): 
        calc = income[i]/qualityOfLife[i]
        relationships.append([cityNames[i], calc])


    '''Plotting the data'''
    plt.figure(figsize=(15,10))

    labels = [] 
    for i in cityNames: 
        labels.append(i)

    x = []
    for i in cityNames: 
        x.append(i)
    
    y = [] 
    for i in relationships: 
        y.append(i[1])
    
    plt.scatter(x, y)
    plt.title("The Value of 1 point on the Quality of Life Scale for Each Each City (based on avg income/quality of life rating)")
    plt.xticks(rotation = 90)
    plt.tight_layout
    plt.subplots_adjust(bottom = 0.5) 
    plt.ylabel('Value ($) of 1 point on Quality of Life Scale')
    plt.xlabel('City Name')

    plt.show()



'''–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– JOIN –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––'''



'''–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– MAIN –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––'''
def main():
    '''The main function calls the function to set up the database, sets up the YelpData table, RestaurantCities table, WeatherData table, 
    and CitiesData Table. It calls all the visualization functions and calculation functions, as well as the JOIN statement.'''
    cur, conn = setUpDatabase('finalprojectdatabase.db')
    


    '''Calling the weather_data function for Ann Arbor, Los Angeles, Chicago, Detroit, and NYC, and setting up the WeatherData table with the information
    from those cities.'''
    AA = weather_data(WEATHER_KEY, annarbor_latitude, annarbor_longitude, start_date)
    LA = weather_data(WEATHER_KEY, la_latitude, la_longitude, start_date)
    CHI = weather_data(WEATHER_KEY, chi_latitude, chi_longitude, start_date)
    DET = weather_data(WEATHER_KEY, det_latitude, det_longitude, start_date)
    NYC = weather_data(WEATHER_KEY, nyc_latitude, nyc_longitude, start_date)
    weather_table(cur, conn, AA)
    weather_table(cur, conn, LA)
    weather_table(cur, conn, CHI)
    weather_table(cur, conn, DET)
    weather_table(cur, conn, NYC)



    '''Calling the dataFromYelp function, setUpRestaurantCitiesTable function, and CreateYelpTable function on the given list of cities 
    and setting up the YelpData table and RestaurantCities table with the information from those cities.'''
    setUpRestaurantCitiesTable(dataFromYelp(YELP_KEY, yelp_cities), cur, conn)
    CreateYelpTable(dataFromYelp(YELP_KEY, yelp_cities), cur, conn)
    


    '''Calling the getTags function and setUpCitiesTable using Beautiful Soup on Business Insider to get the data about the 50 cities and put
    them into a table.'''
    data = getTags()
    setUpCitiesTable(data, cur, conn)



    '''Calling all calculation functions.'''
    convertFromKelvinToCelsiusAndFahrenheit(cur, conn, 'TempInDiffForms.csv')
    PricesPerCityCount(cur, conn,'PricesPerCityCount.csv')
    salary_quality(cur, conn, 'CitiesInformation.csv')



    '''Calling all visualization functions.'''
    weather_visualization()
    yelp_visualization()
    cities_visualization(cur)

if __name__ == "__main__":
    main()
