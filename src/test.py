from datetime import datetime
import pandas as pd
import numpy as np
import serial
import time
import os
import matplotlib.pyplot as plt
import matplotlib.animation as animation


data = pd.DataFrame()
signals = []
sensor = serial.Serial('COM9',115200)


targets = {
    0: 'pedra',
    1: 'papel',
    2: 'tesoura',
    3: 'relaxado'
    }


# Create figure for plotting
# fig = plt.figure()
# ax = fig.add_subplot(1, 1, 1)

fig, ax = plt.subplots(nrows=2, figsize=(14, 6))
# ax = fig.add_subplot(1, 1, 1)

xs1 = []
ys1 = []
xs2 = []
ys2 = []


# This function is called periodically from FuncAnimation
def animate(i, xs1, ys1, xs2, ys2):

    try: 
        sensor.flush()
        sensor.flushInput()
        sensor.read_all()
        data = sensor.readline().decode().strip().split(';')
        data1 = data[0]
        data2 = data[1]
    except:
        return None

    # Add x and y to lists
    time = datetime.now().strftime('%H:%M:%S.%f')
    xs1.append(time)
    ys1.append(data1)
    xs2.append(time)
    ys2.append(data2)


    # Limit x and y lists to 20 items
    xs1 = xs1[-20:]
    ys1 = ys1[-20:]
    xs2 = xs2[-20:]
    ys2 = ys2[-20:]

    # Draw x and y lists
    ax[0].clear()
    ax[0].plot(xs1, ys1)
    ax[1].clear()
    ax[1].plot(xs2, ys2)

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('Sensor data')
    plt.ylabel('Analog sensor output')
    # ax[0].set_ylim([0, 1023])
    # ax[1].set_ylim([0, 1023])
    print(data1, data2)

ani = animation.FuncAnimation(fig, animate, fargs=(xs1, ys1, xs2, ys2), interval=200)
plt.show()