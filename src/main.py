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

os.system('cls')
print('##  PREPARE-SE  ##')
time.sleep(2)

targets = {
    0: 'pedra',
    1: 'papel',
    2: 'tesoura',
    3: 'relaxado'
    }
c = 0
stim = 0
target = 0
timeStim = 3 # in seconds
totalExp = 120

while True:
    os.system('cls')
    print(f'#### FAÇA {targets[target]} ####')
    # print(f'#### PRÓXIMO {targets[target + 1 if target < 3 else 0]} ####')
    time.sleep(2)
    sensor.flush()
    sensor.flushInput()
    sensor.read_all()
    startTime = time.time()
    while (time.time() - startTime) <= timeStim:
        try:
            signal = sensor.readline().decode().strip().split(';')
            signals.append([
                datetime.now().strftime('%y-%m-%d %H:%M:%S.%f'),
                signal[0],
                signal[1],
                stim,
                target,
                targets[target]
                ])
        except:
            pass
    stim += 1
    target = target + 1 if target < 3 else 0

    if ((stim - 1) * timeStim) == totalExp: break

print("##### FIM DO EXPERIMENTO #####")

df = pd.DataFrame(signals,
                  columns=['time', 'data1', 'data2', 'stim', 'target_id', 'target'])

df['data1_decoded'] = df.data1.apply(lambda x: ((float(x) * 0.6) / 1023) if x != '' else np.nan)
df['data2_decoded'] = df.data2.apply(lambda x: ((float(x) * 0.6) / 1023) if x != '' else np.nan)


df.to_csv(f'exp_{datetime.now().strftime("%y%m%d_%H_%M")}.csv', index=False)