import numpy as np

def detectFrequency(recording, sample_rate):
    
    recording = recording.flatten()
    window = np.hanning(len(recording))
    recording = recording * window

    fft = np.fft.rfft(recording)
    magnitude = np.abs(fft)
    frequency = np.fft.rfftfreq(len(recording), d=1/sample_rate)
    return magnitude, frequency

    # if method == "max":
    #     return _highestPeak(frequency, magnitude)
    # elif method == "hps":
    #     return _harmonicProductSpectrum(frequency, magnitude)