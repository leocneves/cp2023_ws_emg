import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sn

from scipy.fft import fft
from scipy.stats import skew, kurtosis
from scipy import signal

from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, plot_confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA


def extract_mean_frequency(window, sample_rate=2341):
    # Aplica a Transformada de Fourier nos sinais na janela
    fft_values = fft(window.values)
    
    # Calcula as frequências correspondentes
    frequencies = np.fft.fftfreq(len(window), d=1/sample_rate)
    
    # Calcula a média ponderada das frequências
    mean_frequency = np.average(frequencies, weights=np.abs(fft_values))
    
    return mean_frequency

def extract_zero_crossing_rate(window):
    zero_crossings = np.where(np.diff(np.sign(window)))[0]
    zero_crossing_rate = len(zero_crossings) / len(window)
    return zero_crossing_rate

def extract_higher_order_moments(window):
    skewness = skew(window)
    kurt = kurtosis(window)
    return skewness

def featureExtraction(window, suf):
    thrsWindow = 0
    s = window.shape[0]
    # window = window[int(s*0.01):]
    if (not window.empty)and(window.shape[0] >= thrsWindow):
        window = window - window.mean()
        features = {
#             'mean':window.mean(),
            'sum_square_'+suf: window.apply(np.square).sum(),
            'max_'+suf: window.max(),
            'min_'+suf: window.min(),
            'amplitude_'+suf: np.max(window) - np.min(window),
            'var_'+suf: np.var(window),
            'rms_'+suf: np.sqrt(np.mean(np.square(window))),
            # 'mean_frequency_'+suf: extract_mean_frequency(window),
            'zero_crossing_rate_'+suf: extract_zero_crossing_rate(window),
            'higher_order_moments_'+suf: extract_higher_order_moments(window)
        }
        return pd.DataFrame.from_dict([features])
    
def rms(a):
    return np.sqrt(np.mean(np.square(a)))


def filter_band(x, lowcut, highcut, btype='bandpass', sampling_rate=512, order=4):
    nyq = 0.5 * sampling_rate
    low = lowcut / nyq
    high = highcut / nyq
    b, a = signal.butter(order, [low, high], analog=1, btype=btype)
#     print(b, a)
    return signal.filtfilt(b, a, x)