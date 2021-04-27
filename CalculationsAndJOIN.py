#Calculations and JOIN

import sqlite3
import os
import csv


'''––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– DB: Function to set up a database –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––'''
def setUpDatabase(db_name):
    '''This function will create a database named after the string input into the function.'''

    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn



'''–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– CALCULATIONS ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––'''
def convertFromKelvinToCelsiusAndFahrenheit(cur, conn, filepath):
    '''Converting the Kelvin input temperature to Celsius and Fahrenheit and ouputting the results into a CSV file.'''
    cur.execute('SELECT WeatherData.Temperature, WeatherData.City, WeatherData.Time FROM WeatherData')
    data = cur.fetchall()
    conn.commit()

    kelvinTemp = []
    for tup in data: 
        kelvinTemp.append(tup[0])

    celsiusTemp = []
    for i in kelvinTemp:
        c = i - 273.15
        celsiusTemp.append((c))

    cityname = []
    for tup in data:
        cityname.append(tup[1])

    times = []
    for tup in data:
        times.append(tup[2])

    '''Converting temperatures in degrees Celsius to Fahrenheit, multiply by 1.8 (or 9/5) and add 32.'''
    FahrenheitTemp = [] 
    for i in celsiusTemp:
        F = (1.8 * i) + 32
        FahrenheitTemp.append((F))

    with open(filepath, 'w', newline = '', encoding= 'utf-8') as f: 
        f = csv.writer(f, delimiter = ',')
        f.writerow(['City Name', 'Time in Unix', 'Temp in Kelvin', 'Temp in Celsius', 'Temp in Fahrenheit'])
        count = 0
        
        for i in kelvinTemp:
            temps = (cityname[count], times[count], kelvinTemp[count], celsiusTemp[count], FahrenheitTemp[count])
            count += 1
            f.writerow(temps)


def PricesPerCityCount(cur, conn, filepath): 
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
                if tup[1] == 41: 
                    NewYorkprice1 += 1 
            if tup[0] == '$$':
                if tup[1] == 2:
                    annArborprice2 += 1 
                if tup[1] == 41: 
                    NewYorkprice2 += 1 

            if tup[0] == '$$$':
                if tup[1] == 2:
                    annArborprice3 += 1 
                if tup[1] == 41: 
                    NewYorkprice3 += 1 
            
            if tup[0] == '$$$$':
                if tup[1] == 2:
                    annArborprice4 += 1 
                if tup[1] == 41:
                    NewYorkprice4 += 1
        

        priceCityData = (annArborprice1, NewYorkprice1, annArborprice2, NewYorkprice2, annArborprice3, NewYorkprice3, annArborprice4, NewYorkprice4)
        f.writerow(['Ann Arbor $', 'New York $', 'Ann Arbor $$', 'New York $$', 'Ann Arbor $$$', 'New York $$$', 'Ann Arbor $$$$', 'New York $$$$'])
        f.writerow(priceCityData)


def salary_quality(cur, conn, filepath):
    '''Dividing the average annual salary by the quality of life (for the respective city) to get the dollar value of a quality of life point
    for each individual city.'''
    cur.execute('SELECT * FROM CitiesData')
    data = cur.fetchall()
    conn.commit()

    cityNames = []
    income = []
    qualityOfLife = []
    population = [] 
    stateNames = []
    for tup in data: 
        cityNames.append(tup[0])
        stateNames.append(tup[1])
        population.append(tup[2])
        income.append(tup[3])
        qualityOfLife.append(tup[4])


    """Trying to calculate if there is a relationship between each cities income and their quality of life rating."""
    relationships = []
    for i in range(len(income)): 
        calc = income[i]/qualityOfLife[i]
        relationships.append([cityNames[i], calc])


    with open(filepath, 'w', newline = '', encoding= 'utf-8') as f: 
        f = csv.writer(f, delimiter = ',')
        f.writerow(['City Name', 'State Name', 'Populations', 'Avg Income', 'Quality of Life', 'Avg Income / Quality of Life'])
        count = 0
        for i in population:
            headers = (cityNames[count], stateNames[count], population[count], income[count], qualityOfLife[count], relationships[count][1])
            count += 1
            f.writerow(headers)




'''–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– JOIN –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––'''
def joinCitiesData(cur, conn):
    cur.execute("SELECT Quality_of_Life, Average_Annual_Salary, Population FROM CitiesData JOIN RestaurantCities ON trim(CitiesData.City_Name) = trim(RestaurantCities.Cities)")
    joined = cur.fetchall()
    for x in joined: 
        print(x)
    conn.commit()




'''–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– MAIN –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––'''
def main():
    '''The main function calls the function to set up the database and calls all the calculation functions, as well as the JOIN statement.'''
    cur, conn = setUpDatabase('finalprojectdatabase.db')


    '''Calling all calculation functions.'''
    convertFromKelvinToCelsiusAndFahrenheit(cur, conn, 'TempInDiffForms.csv')
    PricesPerCityCount(cur, conn, 'PricesPerCityCount.csv')
    salary_quality(cur, conn, 'CitiesInformation.csv')



    '''Calling the JOIN statement function.'''
    joinCitiesData(cur, conn)


    cur.close()


if __name__ == "__main__":
    main()
