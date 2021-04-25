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

    salaries = []
    qualityOfLife = []
    population = [] 
    for tup in data: 
        # print(tup)
        population.append(tup[1])
        salaries.append(tup[2])
        qualityOfLife.append(tup[3])
        # for i in tup: 
        #     info.append(i)
    # print("population: " + str(population))
    # print("::::::::::::")
    # print("salaries: " + str(salaries))
    # print(":::::::::::::")
    # print("qual of life: " + str(qualityOfLife))

    MoneyPerPersonn = [] 
    for i in range(len(population)): 
        moneyperperson = population[i]/salaries[i]
        MoneyPerPersonn.append(moneyperperson)
    print(MoneyPerPersonn)


    with open('CitiesInformation.csv', 'w', newline = '', encoding= 'utf-8') as f: 
        f = csv.writer(f, delimiter = ',')
        f.writerow(['Populations', 'Salaries', 'Quality of Life', 'Money Per Person'])
        count = 0
        for i in population:
            headers = (population[count], salaries[count], qualityOfLife[count], MoneyPerPersonn[count])
            count += 1



        # headers = (population, salaries, qualityOfLife, MoneyPerPersonn)
            f.writerow(headers)


#socioeconomic status for each city to see if restaurants that are pricer have more wealthy people in that city 

salary_quality()