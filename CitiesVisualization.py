#cities visualization 
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd #import pandas
import matplotlib
import sqlite3
import numpy as np
import os
import csv
from matplotlib import style
from numpy import genfromtxt

base_dir = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(base_dir, '/Users/blairfields/Desktop/SI206/finalprojectfolder/finalproject/finalprojectdatabase.db')

with sqlite3.connect(path) as finalprojectdatabase:
    cur = finalprojectdatabase.cursor()
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
    # print(labels)
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



    # for i, txt in enumerate(labels): 
    #     plt.annotate(labels, (x[i], y[i]))
    plt.show()





# def citiesVisualization():
#     # data = genfromtxt('CitiesInformation.csv',delimiter=' ')
#     # plt.plot(data)

#     # plt.title('Epic Info')
#     # plt.ylabel('Y axis')
#     # plt.xlabel('X axis')
#     x = [] 
#     y = [] 
#     with open('CitiesInformation.txt','r') as csvfile:
#         plots = csv.reader(csvfile, delimiter=',')
#         for row in plots:
#             x.append(row[0])
#             y.append(int(row[4]))

#     plt.plot(x,y, label='Loaded from file!')
#     plt.xlabel('x')
#     plt.ylabel('y')
#     plt.title('Interesting Graph\nCheck it out')
#     plt.legend()
#     plt.show()
#     plt.show()






# py.iplot(fig, filename='apple-stock-prices')


