import matplotlib.pyplot as plt
import numpy as np

def plot_sound(recording):
    plt.plot(recording[75000:76000])
    plt.title("Audio graph")
    plt.xlabel("Time")
    plt.ylabel("Height")
    plt.show()

def plot_frequencies(frequency, magnitude):
    plt.figure(figsize=(12,5))
    plt.plot(frequency, magnitude)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.grid(True)
    plt.show()

def plot_autocorrelation(results):
    lags = range(1, len(results)+1)
    plt.plot(lags, results)
    plt.title("Autocorrelation")
    plt.xlabel("Lags (sample)")
    plt.ylabel("Peaks")
    plt.show()