#Yelp API Visualizations

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import json
import os
import sqlite3

base_dir = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(base_dir, '/Users/blairfields/finalprojectfolder/finalproject/finalproject.db')

with sqlite3.connect(path) as Yelpdatabase:
    cur = Yelpdatabase.cursor()
    cur.execute("SELECT * FROM YelpData")
    data = cur.fetchall()

    

