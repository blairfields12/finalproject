#cities visualization 

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import json
import os
import sqlite3
import csv



base_dir = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(base_dir, '/Users/blairfields/Desktop/SI206/finalprojectfolder/finalproject/finalprojectdatabase.db')

with sqlite3.connect(path) as Yelpdatabase:
    cur = Yelpdatabase.cursor()
    cur.execute("SELECT * FROM CitiesData")
    data = cur.fetchall()
    print(data)

    


