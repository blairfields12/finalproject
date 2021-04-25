import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import json
import os
import sqlite3
import csv

base_dir = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(base_dir, '/Users/blairfields/Desktop/SI206/finalprojectfolder/finalproject/finalprojectdatabase.db')

def salary_quality():
    conn = sqlite3.connect(path)
    cur = conn.cursor()
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
        # for i in tup: 
        #     info.append(i)
    # print("population: " + str(population))
    # print("::::::::::::")
    # print("income: " + str(income))
    # print(":::::::::::::")
    # print("qual of life: " + str(qualityOfLife))

    """Trying to calculate if there is a relationship between each cities income and their quality of life rating"""
    relationships = []
    for i in range(len(income)): 
        calc = income[i]/qualityOfLife[i]
        relationships.append([cityNames[i], calc])
    # print(relationships)



    with open('CitiesInformation.csv', 'w', newline = '', encoding= 'utf-8') as f: 
        f = csv.writer(f, delimiter = ',')
        f.writerow(['City Name', 'Populations', 'Avg Income', 'Quality of Life', 'Avg Income / Quality of Life'])
        count = 0
        for i in population:
            headers = (cityNames[count], population[count], income[count], qualityOfLife[count], relationships[count][1])
            count += 1
            f.writerow(headers)
    

#socioeconomic status for each city to see if restaurants that are pricer have more wealthy people in that city 
salary_quality()

