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
    time_count = []

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
        time_count.append(i[1])

fig, ax = plt.subplots()


ax.plot(time_count, aa_temperature, 'y', label = 'Ann Arbor, MI')
ax.plot(time_count, la_temperature, 'b', label = 'Los Angeles, CA')
ax.plot(time_count, chi_temperature, 'r', label = 'Chicago, IL')
ax.plot(time_count, det_temperature, 'g', label = 'Detroit, MI')
ax.plot(time_count, nyc_temperature, 'k', label = 'New York City, NY')

ax.legend()
ax.set_xlabel('Unix Tie')
ax.set_ylabel('Temperature (Kelvin)')
ax.set_title('Temperature Values for Ann Arbor vs. Los Angeles vs. Chicago vs. Detroit vs. NYC Over a 25 Hour Period')

ax.grid()
plt.show()