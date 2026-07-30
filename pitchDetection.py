import numpy as np

def _highestPeak(frequency, magnitude):
    max = np.argmax(magnitude)
    return frequency[max]

def _harmonicProductSpectrum(frequency, magnitude):
    raw_peak = np.argmax(magnitude)
    downsizingList = [2,3,4]
    idx330 = np.argmin(np.abs(frequency - 330))

    print("\n330 Hz components:")
    print("Original:", magnitude[idx330])

    for factor in [2, 3, 4]:
        print(f"{factor}x:", magnitude[idx330 * factor])

    print()

    downsizingList = [2, 3, 4]



    idx658 = np.argmin(np.abs(frequency - 658))

    print("\n658 Hz components:")
    print("Original:", magnitude[idx658])

    for factor in [2, 3, 4]:
        if idx658 * factor < len(magnitude):
            print(f"{factor}x:", magnitude[idx658 * factor])


    idx330 = np.argmin(np.abs(frequency - 330))

    for i in range(idx330-3, idx330+4):
        print(frequency[i], magnitude[i])

    idx658 = np.argmin(np.abs(frequency - 658))

    for i in range(idx658-3, idx658+4):
        print(frequency[i], magnitude[i])

    hps = magnitude.copy()
    for factor in downsizingList:
        downsized = magnitude[::factor]
        hps[:len(downsized)] = hps[:len(downsized)] * downsized # Take the first part of HPS an multiply it in place
        hps = hps[:len(downsized)] # Restricts the sample size so that other harmonics that haven't been considered do not "win" over the fundamental
    max = np.argmax(hps)
    indices = np.argsort(hps)[-15:]
    indices = indices[::-1]

    for i in indices:
        print(f"{frequency[i]:8.2f} Hz   {hps[i]:8.2f}   {i}")
    print(hps.shape)
    

    print(f"Raw FFT: {frequency[raw_peak]:.2f} Hz")
    print(f"HPS    : {frequency[max]:.2f} Hz")
    return frequency[max]

def detectFrequency(recording, sample_rate, method):
    print(f"Recording shape: {recording.shape}")
    print(f"Recording dtype: {recording.dtype}")
    print(f"Min: {recording.min()}")
    print(f"Max: {recording.max()}")
    print(f"Mean abs: {np.mean(np.abs(recording))}")
    
    fft = np.fft.rfft(recording)
    magnitude = np.abs(fft)
    frequency = np.fft.rfftfreq(len(recording), d=1/sample_rate)
    
    if method == "max":
        return _highestPeak(frequency, magnitude)
    elif method == "hps":
        return _harmonicProductSpectrum(frequency, magnitude)