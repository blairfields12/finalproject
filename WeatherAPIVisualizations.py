#Weather API Visualizations

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import json
import os
import sqlite3

base_dir = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(base_dir, '/Users/blairfields/Desktop/SI206/finalprojectfolder/finalproject/finalprojectdatabase.db')

with sqlite3.connect(path) as weather_data:
    cur = weather_data.cursor()
    data = cur.execute("SELECT * FROM WeatherData").fetchall()

    AA_data = []
    for item in data: 
        if 'Ann Arbor' in item: 
            AA_data.append(item)

    LA_data = []
    for item in data: 
        if "Los Angeles" in item: 
            LA_data.append(item)
    
    Chi_data = []
    for item in data: 
        if "Chicago" in item: 
            Chi_data.append(item)

    Det_data = []
    for item in data: 
        if "Detroit" in item: 
            Det_data.append(item)

    NYC_data = []
    for item in data: 
        if "New York City" in item: 
            NYC_data.append(item)
    
    aa_temperature = []
    la_temperature = []
    chi_temperature = []
    det_temperature = []
    nyc_temperature = []
    # time_count = []
    aa_time = []
    la_time = [] 
    chi_time = [] 
    det_time = [] 
    nyc_time = [] 


    for i in AA_data: 
        aa_temperature.append(i[3])
        aa_time.append(i[1])

    for i in LA_data: 
        la_temperature.append(i[3])
        la_time.append(i[1])

    for i in Chi_data: 
        chi_temperature.append(i[3])
        chi_time.append(i[1])

    for i in Det_data: 
        det_temperature.append(i[3])
        det_time.append(i[1])
    
    for i in NYC_data: 
        nyc_temperature.append(i[3])
        nyc_time.append(i[1])


'''Plotting the data'''

time2 = aa_time[1]
time3 = aa_time[2]
time4 = aa_time[3]
time5 = aa_time[4]
time6 = aa_time[5]

# fig,a =  plt.subplots(4)
f, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5)
f.suptitle('Temperature Values for Ann Arbor vs. Los Angeles vs. Chicago \n vs. Detroit vs. NYC Over a 25 Hour Period', fontsize= 10)

x = np.arange(1,5)
# a[0][0].plot(aa_time, aa_temperature, 'y', label = 'Ann Arbor, MI')
# a[0][0].set_title('Temp Value for AA Over 25 Hour Period',  fontsize = 8)
ax1.plot(aa_time, aa_temperature, 'y', label = 'Ann Arbor, MI')
# ax1.set_title('Temp Value for AA Over 25 Hour Period',  fontsize = 8)
ax1.tick_params(axis='x', labelsize=6)
ax1.tick_params(axis='y', labelsize=6)
x_axis = ax1.axes.get_xaxis()
x_axis.set_visible(False)




# a[0][1].plot(la_time, la_temperature, 'b', label = 'Los Angeles, CA')
# a[0][1].set_title('Temp Value for LA Over 25 Hour Period',  fontsize = 8)
ax2.plot(la_time, la_temperature, 'b', label = 'Los Angeles, CA')
# ax2.set_title('Temp Value for LA Over 25 Hour Period',  fontsize = 8)
ax2.tick_params(axis='x', labelsize=6)
ax2.tick_params(axis='y', labelsize=6)
x_axis = ax2.axes.get_xaxis()
x_axis.set_visible(False)





# a[1][0].plot(chi_time, chi_temperature, 'r', label = 'Chicago, IL')
# a[1][0].set_title('Temp Value for Chicago Over 25 Hour Period',  fontsize = 8)
ax3.plot(chi_time, chi_temperature, 'r', label = 'Chicago, IL')
ax3.tick_params(axis='x', labelsize=6)
ax3.tick_params(axis='y', labelsize=6)
x_axis = ax3.axes.get_xaxis()
x_axis.set_visible(False)



# ax3.set_title('Temp Value for Chicago Over 25 Hour Period',  fontsize = 8)

# a[1][1].plot(det_temperature, 'g', label = 'Detroit, MI')
# a[1][1].set_title('Temp Value for Detroit Over 25 Hour Period',  fontsize = 8)
ax4.plot(det_temperature, 'g', label = 'Detroit, MI')
ax4.tick_params(axis='x', labelsize=6)
ax4.tick_params(axis='y', labelsize=6)
x_axis = ax4.axes.get_xaxis()
x_axis.set_visible(False)



# ax4.set_title('Temp Value for Detroit Over 25 Hour Period',  fontsize = 8)

# a[1][1].plot(nyc_time, nyc_temperature, 'k', label = 'New York City, NY')
# a[1][1].set_title('Temp Value for NYC Over 25 Hour Period', fontsize = 8)
ax5.plot(nyc_time, nyc_temperature, 'k', label = 'New York City, NY')
# ax5.set_title('Temp Value for NYC Over 25 Hour Period', fontsize = 8)
ax5.tick_params(axis='x', labelsize=6)
ax5.tick_params(axis='y', labelsize=6)

# plt.legend(["Ann Arbor", "Los Angeles", "Chicago", "Detroit", "New York City"], loc ="lower right")
plt.legend()

plt.grid(True)
plt.show()


# fig, ax = plt.subplots()

# ax.plot(aa_time, aa_temperature, 'y', label = 'Ann Arbor, MI')
# ax.plot(la_time, la_temperature, 'b', label = 'Los Angeles, CA')
# ax.plot(chi_time, chi_temperature, 'r', label = 'Chicago, IL')
# ax.plot(det_time, det_temperature, 'g', label = 'Detroit, MI')
# ax.plot(nyc_time, nyc_temperature, 'k', label = 'New York City, NY')

# ax.legend()
# ax.set_xlabel('Unix Time')
# ax.set_ylabel('Temperature (Kelvin)')
# ax.set_title('Temperature Values for Ann Arbor vs. Los Angeles vs. Chicago vs. Detroit vs. NYC Over a 25 Hour Period', fontsize = 8)

# ax.grid()



plt.show()