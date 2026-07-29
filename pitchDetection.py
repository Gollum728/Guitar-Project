import numpy as np

def _highestPeak(frequency, magnitude):
    max = np.argmax(magnitude)
    return frequency[max]

def _harmonicProductSpectrum(frequency, magnitude):
    downsizingList = [2,3]
    hps = magnitude.copy()
    for factor in downsizingList:
        downsized = magnitude[::factor]
        hps[:len(downsized)] = hps[:len(downsized)] * downsized # Take the first part of HPS an multiply it in place
        hps = hps[:len(downsized)] # Restricts the sample size so that other harmonics that haven't been considered do not "win" over the fundamental
    max = np.argmax(hps)
    # indices = np.argsort(hps)[-15:]
    # indices = indices[::-1]

    # for i in indices:
    #     print(f"{frequency[i]:8.2f} Hz   {hps[i]:8.2f}   {i}")
    # print(hps.shape)
    return frequency[max]

def detectFrequency(recording, sample_rate, method):
    print(method)
    fft = np.fft.rfft(recording)
    magnitude = np.abs(fft)
    frequency = np.fft.rfftfreq(len(recording), d=1/sample_rate)
    
    if method == "max":
        return _highestPeak(frequency, magnitude)
    elif method == "hps":
        return _harmonicProductSpectrum(frequency, magnitude)