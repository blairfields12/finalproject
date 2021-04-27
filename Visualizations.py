#Visualizations

import sqlite3
import os
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
from numpy import genfromtxt
import pandas as pd 


'''––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– DB: Function to set up a database –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––'''
def setUpDatabase(db_name):
    '''This function will create a database named after the string input into the function.'''

    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn



'''–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– VISUALIZATION ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––'''
def weather_visualization(cur):
    data = cur.execute("SELECT * FROM WeatherData").fetchall()

    times = []
    for item in data:
        if item[1] not in times:
            times.append(item[1])
    
    AA_data = []
    LA_data = []
    Chi_data = []
    Det_data = []
    NYC_data = []
    for item in data: 
        if 'Ann Arbor' in item: 
            AA_data.append(item) 
        if "Los Angeles" in item: 
            LA_data.append(item)
        if "Chicago" in item: 
            Chi_data.append(item)
        if "Detroit" in item: 
            Det_data.append(item)
        if "New York City" in item: 
            NYC_data.append(item)
    
    aa_temperature = []
    la_temperature = []
    chi_temperature = []
    det_temperature = []
    nyc_temperature = []


    for i in AA_data: 
        aa_temperature.append(i[3])

    for i in LA_data: 
        la_temperature.append(i[3])

    for i in Chi_data: 
        chi_temperature.append(i[3])

    for i in Det_data: 
        det_temperature.append(i[3])
    
    for i in NYC_data: 
        nyc_temperature.append(i[3])


    '''Plotting the data'''
    fig, ax = plt.subplots()

    ax.plot(times, aa_temperature, 'y', label = 'Ann Arbor')
    ax.plot(times, la_temperature, 'r', label = 'Los Angeles')
    ax.plot(times, chi_temperature, 'g', label = 'Chicago')
    ax.plot(times, det_temperature, 'b', label = 'Detroit')
    ax.plot(times, nyc_temperature, 'k', label = 'NYC')
    ax.legend()
    ax.set_ylabel('Temperature (in Kelvin)')
    ax.set_xlabel('Time (in Unix - shorted to last 5 digits)')
    ax.set_title('Temperature Values for Ann Arbor vs. Los Angeles vs. Chicago \n vs. Detroit vs. NYC Over a 25 Hour Period', fontsize= 10)
    ax.grid()
    plt.show()





def yelp_visualization(cur):
    cur.execute("SELECT * FROM YelpData")
    data = cur.fetchall()

    AnnArborRatings = [] 
    NewYorkRatings = [] 
    
    for items in data: 
        if 'Ann Arbor' in items:
            AnnArborRatings.append(items[2])
        if 'New York' in items:
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
    rects2 = ax.bar(x + width/2, NYRatingsCount, width, alpha = opacity, color = 'red', label='New York')

    '''Adding labels, title and custom x-axis tick labels, etc. '''
    ax.set_ylabel('Number of Restaurants With Rating')
    ax.set_xlabel('Rating')
    ax.set_title('Restaurants in Ann Arbor and New York With Each Rating')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    fig.tight_layout()
    plt.show()



def yelp_visualization2(cur):
    CitiesData = cur.execute("SELECT * FROM CitiesData").fetchall()
    data = cur.execute("SELECT * FROM YelpData").fetchall()

    GrandRapidsPrices = [] 
    NashPrices = [] 
    IndiPrices = []
    LancasterPrices = []

    for items in data: 
        if 59 in items:
            GrandRapidsPrices.append(items[1])
        if 53 in items:
            NashPrices.append(items[1])
        if 51 in items:
            IndiPrices.append(items[1])
        if 65 in items:
            LancasterPrices.append(items[1])

    GR_S = [] 
    Nash_S = [] 
    Indi_S = [] 
    Lancaster_S = [] 
    GR_SS = [] 
    Nash_SS = [] 
    Indi_SS = [] 
    Lancaster_SS = [] 
    GR_SSS = [] 
    Nash_SSS = [] 
    Indi_SSS = [] 
    Lancaster_SSS = [] 
    GR_SSSS = [] 
    Nash_SSSS = [] 
    Indi_SSSS = [] 
    Lancaster_SSSS = [] 

    for price in GrandRapidsPrices: 
        if price == '$': 
            GR_S.append(price)
        if price == '$$': 
            GR_SS.append(price)
        if price == '$$$': 
            GR_SSS.append(price)
        if price == '$$$$': 
            GR_SSSS.append(price)

    for price in NashPrices: 
        if price == '$': 
            Nash_S.append(price)
        if price == '$$': 
            Nash_SS.append(price)
        if price == '$$$': 
            Nash_SSS.append(price)
        if price == '$$$$': 
            Nash_SSSS.append(price)

    for price in IndiPrices: 
        if price == '$': 
            Indi_S.append(price)
        if price == '$$': 
            Indi_SS.append(price)
        if price == '$$$': 
            Indi_SSS.append(price)
        if price == '$$$$': 
            Indi_SSSS.append(price)
    
    for price in LancasterPrices: 
        if price == '$': 
            Lancaster_S.append(price)
        if price == '$$': 
            Lancaster_SS.append(price)
        if price == '$$$': 
            Lancaster_SSS.append(price)
        if price == '$$$$': 
            Lancaster_SSSS.append(price)

    '''Plotting the data''' 
    '''Creating pie chart for Distribution of Indiana Prices'''
    IndianaLow = len(Indi_S) #doing this to create the percentages of each price within the total amount 
    IndianaMidLow = len(Indi_SS)
    IndianaMidHigh = len(Indi_SSS)
    IndianaHigh = len(Indi_SSSS)

    y = np.array([IndianaLow, IndianaMidLow, IndianaMidHigh, IndianaHigh])
    mylabels = "Range 1: 0-10", "Range 2: 11-30", 'Range 3: 31-60', 'Range 4: 61+'
    myexplode = [0.1, 0.1, 0.1, 0.1]
    colors = ["magenta", "blue", "pink", "yellow"]

    plt.pie(y, labels = mylabels, colors = colors, explode = myexplode, shadow = True, autopct='%1.1f%%')
    plt.title('Indianapolis Price Distribution Across 50 Restaurants')
    plt.legend(loc="lower right", title = "Indiana Prices:")
    plt.show() 

    '''Creating pie chart for Distribution of Lancaster Prices'''
    LancasterLow = len(Lancaster_S) #doing this to create the percentages of each price within the total amount 
    LancasterMidLow = len(Lancaster_SS)
    LancasterMidHigh = len(Lancaster_SSS)
    LancasterHigh = len(Lancaster_SSSS)

    y = np.array([LancasterLow, LancasterMidLow, LancasterMidHigh, LancasterHigh])
    mylabels = "Range 1: 0-10", "Range 2: 11-30", 'Range 3: 31-60', 'Range 4: 61+'
    myexplode = [0.1, 0.1, 0, 0.1]
    colors = ["magenta", "blue", "pink", "yellow"]


    plt.pie(y, labels = mylabels, colors = colors, explode = myexplode, shadow = True, autopct='%1.1f%%')
    plt.title('Lancaster Price Distribution Across 50 Restaurants')
    plt.legend(loc="lower right", title = "Lancaster Prices:")
    plt.show() 

    '''Creating pie chart for Distribution of Grand Rapids Prices'''
    GrandRapidsLow = len(GR_S) #doing this to create the percentages of each price within the total amount 
    GrandRapidsMidLow = len(GR_SS)
    GrandRapidsMidHigh = len(GR_SSS)
    GrandRapidsHigh = len(GR_SSSS)

    y = np.array([GrandRapidsLow, GrandRapidsMidLow, GrandRapidsMidHigh, GrandRapidsHigh])
    mylabels = "Range 1: 0-10", "Range 2: 11-30", 'Range 3: 31-60', 'Range 4: 61+'
    myexplode = [0.1, 0.1, 0.1, 0]
    colors = ["magenta", "blue", "pink", "yellow"]

    plt.tight_layout()

    plt.pie(y, labels = mylabels, colors = colors, explode = myexplode, shadow = True, autopct='%1.1f%%', pctdistance=0.9)
    plt.title('Grand Rapids Price Distribution Across 50 Restaurants')
    plt.legend(loc="lower right", title = "Grand Rapids Prices:")
    plt.show() 

    '''Creating pie chart for Distribution of Nashville Prices'''
    NashvilleLow = len(Lancaster_S) #doing this to create the percentages of each price within the total amount 
    NashvilleMidLow = len(Lancaster_SS)
    NashvilleMidHigh = len(Nash_SSS)
    NashvilleHigh = len(Nash_SSSS)

    y = np.array([NashvilleLow, NashvilleMidLow, NashvilleMidHigh, NashvilleHigh])
    mylabels = "Range 1: 0-10", "Range 2: 11-30", 'Range 3: 31-60', 'Range 4: 61+'
    myexplode = [0.1, 0.1, 0.1, 0.1]
    colors = ["magenta", "blue", "pink", "yellow"]

    plt.pie(y, labels = mylabels, colors = colors, explode = myexplode, shadow = True, autopct='%1.1f%%')
    plt.title('Nashville Price Distribution Across 50 Restaurants')
    plt.legend(loc="lower right", title = "Nashville Prices:")
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
    plt.grid(True)
    plt.show()




'''–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– MAIN –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––'''
def main():
    '''The main function calls the function to set up the database and calls all the visualizations functions.'''
    cur, conn = setUpDatabase('finalprojectdatabase.db')
    

    '''Calling all visualization functions.'''
    weather_visualization(cur)
    yelp_visualization(cur)
    yelp_visualization2(cur)
    cities_visualization(cur)


    cur.close()


if __name__ == "__main__":
    main()