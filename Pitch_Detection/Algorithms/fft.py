import numpy as np

def detectFrequency(recording, sample_rate, method):
    
    recording = recording.flatten()
    window = np.hanning(len(recording))
    recording = recording * window

    fft = np.fft.rfft(recording)
    magnitude = np.abs(fft)
    frequency = np.fft.rfftfreq(len(recording), d=1/sample_rate)
    
    # if method == "max":
    #     return _highestPeak(frequency, magnitude)
    # elif method == "hps":
    #     return _harmonicProductSpectrum(frequency, magnitude)