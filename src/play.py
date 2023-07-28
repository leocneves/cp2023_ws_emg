from datetime import datetime
import pandas as pd
import numpy as np
import serial
import time
import os
import matplotlib.pyplot as plt


data = pd.DataFrame()
signals = []
sensor = serial.Serial('COM9',115200)


targets = {
    0: 'pedra',
    1: 'papel',
    2: 'tesoura',
    3: 'relaxado'
    }

window_size = 3000

while True:
    c = 0
    sensor.flush()
    sensor.flushInput()
    sensor.read_all()
    data = []
    while True:
        try:
            data.append(sensor.readline().decode().strip().split(';'))
            c+1
        except:
            pass
        if c == window_size:
            # Data prep. methods

            # Prediction method

            break