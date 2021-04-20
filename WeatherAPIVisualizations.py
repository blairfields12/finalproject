#Weather API Visualizations
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import json
import os
import sqlite3

base_dir = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(base_dir, '/Users/miaschaftel/finalproject/WeatherData.db')

with sqlite3.connect(path) as weather_data:
    cur = weather_data.cursor()
    cur.execute("SELECT * FROM WeatherData")
    data = cur.fetchall()
    
    aa_temperature = []
    la_temperature = []
    chi_temperature = []
    det_temperature = []
    nyc_temperature = []

    for i in data:
        if i == 'Ann Arbor':
            aa_temperature.append(i[3])
        if i == 'Los Angeles':
            la_temperature.append(i[3])
        if i == 'Chicago':
            chi_temperature.append(i[3])
        if i == 'Detroit':
            det_temperature.append(i[3])
        if i == 'New York City':
            nyc_temperature.append(i[3])

fig, ax = plt.subplots()

y_count = 25

ax.plot(y_count, aa_temperature, 'y', label = 'Ann Arbor, MI')
ax.plot(y_count, la_temperature, 'b', label = 'Los Angeles, CA')
ax.plot(y_count, chi_temperature, 'r', label = 'Chicago, IL')
ax.plot(y_count, det_temperature, 'g', label = 'Detroit, MI')
ax.plot(y_count, nyc_temperature, 'k', label = 'New York City, NY')
ax.legend()
ax.set_xlabel('Unix Time')
ax.set_ylabel('Temperature (Kelvin)')