#2nd Yelp API Visualizations

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import json
import os
import sqlite3

base_dir = os.path.dirname(os.path.realpath(__file__))
path = (base_dir + '/finalprojectdatabase.db') #PUT THIS IN ALL OTHER FILES

with sqlite3.connect(path) as finalprojectdatabase:
    cur = finalprojectdatabase.cursor()
    CitiesData = cur.execute("SELECT * FROM CitiesData").fetchall()
    data = cur.execute("SELECT * FROM YelpData").fetchall()
    # print(CitiesData)
    # print(yelpData)

    GrandRapidsPrices = [] 
    NashPrices = [] 
    IndiPrices = []
    LancasterPrices = []

    for items in data[350:399]: 
        GrandRapidsPrices.append(items[1])
    # print(GrandRapidsPrices)
    for items in data[300:349]: 
        NashPrices.append(items[1])
    for items in data[250:299]: 
        IndiPrices.append(items[1])
    for items in data[400:]:
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
    # print("$: " + str(AA_S))
    # print("$$: " + str(AA_SS))
    # print('$$$: ' + str(AA_SSS))
    # print('$$$$: ' + str(AA_SSSS))
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

#creating pie chart for Distribution of Indiana Prices
IndianaLow = len(Indi_S) #doing this to create the percentages of each price within the total amount 
IndianaMidLow = len(Indi_SS)
IndianaMidHigh = len(Indi_SSS)
IndianaHigh = len(Indi_SSSS)
# print(IndianaLow)
# print(IndianaMidLow)
# print(IndianaMidHigh)
# print(IndianaHigh)

y = np.array([IndianaLow, IndianaMidLow, IndianaMidHigh, IndianaHigh])
mylabels = "1", "2", '3', '4'
myexplode = [0.1, 0.1, 0.1, 0.1]
colors = ["magenta", "blue", "pink", "yellow"]


plt.pie(y, labels = mylabels, colors = colors, explode = myexplode, shadow = True, autopct='%1.1f%%')
plt.title('Indiana Price Distribution Across 50 Restaurants')
plt.legend(loc="lower right", title = "Indiana Prices:")
plt.show() 

#creating pie chart for Distribution of Lancaster Prices
LancasterLow = len(Lancaster_S) #doing this to create the percentages of each price within the total amount 
LancasterMidLow = len(Lancaster_SS)
LancasterMidHigh = len(Lancaster_SSS)
LancasterHigh = len(Lancaster_SSSS)
# print(LancasterLow)
# print(LancasterMidLow)
# print(LancasterMidHigh)
# print(LancasterHigh)

y = np.array([LancasterLow, LancasterMidLow, LancasterMidHigh, LancasterHigh])
mylabels = "1", "2", '3', '4'
myexplode = [0.1, 0.1, 0, 0.1]
colors = ["magenta", "blue", "pink", "yellow"]


plt.pie(y, labels = mylabels, colors = colors, explode = myexplode, shadow = True, autopct='%1.1f%%')
plt.title('Lancaster Price Distribution Across 50 Restaurants')
plt.legend(loc="lower right", title = "Lancaster Prices:")
plt.show() 

#creating pie chart for Distribution of Grand Rapids Prices
GrandRapidsLow = len(GR_S) #doing this to create the percentages of each price within the total amount 
GrandRapidsMidLow = len(GR_SS)
GrandRapidsMidHigh = len(GR_SSS)
GrandRapidsHigh = len(GR_SSSS)
# print(GrandRapidsLow)
# print(GrandRapidsMidLow)
# print(GrandRapidsMidHigh)
# print(GrandRapidsHigh)
# print(":::::::::::::::::::")
y = np.array([GrandRapidsLow, GrandRapidsMidLow, GrandRapidsMidHigh, GrandRapidsHigh])
mylabels = "1", "2", '3', '4'
myexplode = [0.1, 0.1, 0.1, 0]
colors = ["magenta", "blue", "pink", "yellow"]

plt.tight_layout()



plt.pie(y, labels = mylabels, colors = colors, explode = myexplode, shadow = True, autopct='%1.1f%%', pctdistance=0.9)
plt.title('Grand Rapids Price Distribution Across 50 Restaurants')
plt.legend(loc="lower right", title = "Grand Rapids Prices:")
plt.show() 

#creating pie chart for Distribution of Nashville Prices
NashvilleLow = len(Lancaster_S) #doing this to create the percentages of each price within the total amount 
NashvilleMidLow = len(Lancaster_SS)
NashvilleMidHigh = len(Nash_SSS)
NashvilleHigh = len(Nash_SSSS)
# print(NashvilleLow)
# print(NashvilleMidLow)
# print(NashvilleMidHigh)
# print(NashvilleHigh)

y = np.array([NashvilleLow, NashvilleMidLow, NashvilleMidHigh, NashvilleHigh])
mylabels = "1", "2", '3', '4'
myexplode = [0.1, 0.1, 0.1, 0.1]
colors = ["magenta", "blue", "pink", "yellow"]


plt.pie(y, labels = mylabels, colors = colors, explode = myexplode, shadow = True, autopct='%1.1f%%')
plt.title('Nashville Price Distribution Across 50 Restaurants')
plt.legend(loc="lower right", title = "Nashville Prices:")
plt.show() 