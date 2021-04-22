#Yelp API Visualizations

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import json
import os
import sqlite3

base_dir = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(base_dir, '/Users/blairfields/Desktop/SI206/finalprojectfolder/finalproject/finalprojectdatabase.db')

with sqlite3.connect(path) as Yelpdatabase:
    cur = Yelpdatabase.cursor()
    cur.execute("SELECT * FROM YelpData")
    data = cur.fetchall()
    # print(data)

    AnnArborRatings = [] 
    NewYorkRatings = [] 
    
    for items in data[:50]: 
        AnnArborRatings.append(items[2])
    for items in data[200:]: 
        NewYorkRatings.append(items[2])
    # print(AnnArborRatings)
    # print(LosAngelesRatings)

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
    
    print("AA 4.0 ratings: " + str(len(AA_rated_four)))
    print("NY 4.0 ratings: " + str(len(NY_rated_four)))

    print("AA 4.5 ratings: " + str(len(AA_rated_four_five)))
    print("NY 4.5 ratings: " + str(len(NY_rated_four_five)))

    print("AA 5.0 ratings: " + str(len(AA_rated_five)))
    print("NY 5.0 ratings: " + str(len(NY_rated_five)))

'''Plotting the data'''
labels = ['4.0', '4.5', '5.0']
AARatingsCount = [12, 35, 3]
NYRatingsCount = [0, 19, 30]

x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars
# opacity = 0.8

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, AARatingsCount, width, label='Ann Arbor')
rects2 = ax.bar(x + width/2, NYRatingsCount, width, label='Los Angeles')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Number of Restaurants With Rating')
ax.set_title('Restaurants in Ann Arbor and New York With Each Rating')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()


fig.tight_layout()

plt.show()