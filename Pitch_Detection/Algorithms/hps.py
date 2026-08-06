import numpy as np

def _harmonicProductSpectrum(frequency, magnitude):


    downsizingList = [2, 3, 4]
    
    hps = magnitude.copy()
    for factor in downsizingList:
        downsized = magnitude[::factor]
        hps[:len(downsized)] = hps[:len(downsized)] * downsized # Take the first part of HPS an multiply it in place
        hps = hps[:len(downsized)] # Restricts the sample size so that other harmonics that haven't been considered do not "win" over the fundamental
    max = np.argmax(hps)
    indices = np.argsort(hps)[-15:]
    indices = indices[::-1]

    return frequency[max]
