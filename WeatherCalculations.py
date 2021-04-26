#weather API calculations and visualizations 

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import json
import os
import sqlite3
import csv

base_dir = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(base_dir, '/Users/blairfields/Desktop/SI206/finalprojectfolder/finalproject/finalprojectdatabase.db')

def convertFromKelvinToCelciusAndFahrenheit():
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.execute('SELECT WeatherData.Temperature FROM WeatherData')
    data = cur.fetchall()
    # for i in data: 
    #     data = data.strip(',')
    # print(data)
    # print(type(data))
    conn.commit()

    kelvinTemp = []
    for tup in data: 
        for i in tup: 
            kelvinTemp.append(i)
    # print(kelvinTemp)
    # print(data2)
    
     # C = K - 273.15
    celciusTemp = []
    for i in kelvinTemp:
        c = i - 273.15
        celciusTemp.append((c))
    # print(celciusTemp)

    #convert temperatures in degrees Celsius to Fahrenheit, multiply by 1.8 (or 9/5) and add 32.
    FahrenheitTemp = [] 
    for i in celciusTemp:
        F = (1.8 * i) + 32
        FahrenheitTemp.append((F))
    # print(FahrenheitTemp)

    with open('TempInDiffForms.csv', 'w', newline = '', encoding= 'utf-8') as f: 
        f = csv.writer(f, delimiter = ',')
        f.writerow(['Temp in Kelvin', 'Temp in Celcius', 'Temp in Fahrenheit'])
        count = 0
        for i in kelvinTemp:
            temps = (kelvinTemp[count], celciusTemp[count], FahrenheitTemp[count])
            count += 1
        
            # temps = (kelvinTemp, celciusTemp, FahrenheitTemp)
            
            f.writerow(temps)  

def weatherVisualization(): 
    with sqlite3.connect(path) as weather_data:
        cur = weather_data.cursor()
        data = cur.execute("SELECT * FROM WeatherData").fetchall()
    print(data)
    

convertFromKelvinToCelciusAndFahrenheit()
weatherVisualization()


