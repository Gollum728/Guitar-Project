import numpy as np

def _highestPeak(frequency, magnitude):
    max = np.argmax(magnitude)
    return frequency[max]

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

    print(f"HPS    : {frequency[max]:.2f} Hz")
    return parabolicInterpolation(max, frequency, magnitude)

    
"""

def _harmonicProductSpectrum(frequency, magnitude):
    hps = magnitude.copy()

    idx = np.argmin(np.abs(frequency - 330))

    print(f"Testing index: {idx}")
    print(f"Frequency: {frequency[idx]} Hz")
    print()

    print("===== BEFORE MULTIPLICATION =====")
    print(f"Original HPS value: {hps[idx]}")
    print()

    for factor in [2, 3, 4]:
        downsized = magnitude[::factor]

        print(f"----- Factor {factor} -----")
        print(f"Current HPS value: {hps[idx]}")

        if idx * factor < len(magnitude):
            print(f"Magnitude at harmonic ({frequency[idx * factor]} Hz): {magnitude[idx * factor]}")
            print(f"Expected after multiplication: {hps[idx] * magnitude[idx * factor]}")

        hps[:len(downsized)] *= downsized

        print(f"Actual after multiplication: {hps[idx]}")
        print()

        hps = hps[:len(downsized)]

    print("===== FINAL =====")
    print(f"Final HPS value: {hps[idx]}")
    print()

    # Print top peaks
    indices = np.argsort(hps)[-15:][::-1]

    idx330 = np.argmin(np.abs(frequency - 330))
    idx658 = np.argmin(np.abs(frequency - 658))

    print("\nManual check:")
    print(f"HPS[330] = {hps[idx330]}")
    print(f"HPS[658] = {hps[idx658]}")

    
    for i in indices:
        print(f"{frequency[i]:8.2f} Hz   {hps[i]:12.2f}   {i}")

    maximum = np.argmax(hps)

    print()
    print(f"Raw FFT: {frequency[np.argmax(magnitude)]:.2f} Hz")
    print(f"HPS    : {frequency[maximum]:.2f} Hz")

    return frequency[maximum]

"""


def detectFrequency(recording, sample_rate, method):
    print(f"Recording shape: {recording.shape}")
    print(f"Recording dtype: {recording.dtype}")
    print(f"Min: {recording.min()}")
    print(f"Max: {recording.max()}")
    print(f"Mean abs: {np.mean(np.abs(recording))}")
    
    recording = recording.flatten()
    window = np.hanning(len(recording))
    recording = recording * window

    fft = np.fft.rfft(recording)
    magnitude = np.abs(fft)
    frequency = np.fft.rfftfreq(len(recording), d=1/sample_rate)
    
    if method == "max":
        return _highestPeak(frequency, magnitude)
    elif method == "hps":
        return _harmonicProductSpectrum(frequency, magnitude)
    

def parabolicInterpolation(k, frequency, magnitude):
    #Formula derived by me, check notes!!

    print(f"k = {k}")
    print(f"Frequency = {frequency[k]}")
    
    left = magnitude[k-1]
    centre = magnitude[k]
    right = magnitude[k+1]

    print(f"Left   : {left}")
    print(f"Centre : {centre}")
    print(f"Right  : {right}")

    denominator = left - (2 * centre) + right
    print(f"Denominator: {denominator}")

    

    binSize = frequency[k] - frequency[k-1]

    offset = (left-right) / (2*(left-(2*centre)+right))
    newFrequency = frequency[k] + (offset * binSize)
    print(f"HPS Freq. {frequency[k]}   PI Freq {newFrequency}")
    return newFrequency


def autocorrelation(recording, sampleRate):
    print(sampleRate)
    results = []
    for lag in range(1,750):
        nsdf = 0
        numerator = np.sum(recording[lag:] * recording[:-lag]) # Original x shifted (see notes on this!!)
        denominator = np.sum(recording[:-lag]**2) + np.sum(recording[lag:]**2)
        nsdf = (2 * numerator) / denominator
        results.append(nsdf)


    minLag = sampleRate // 1000

    sampleShift = 0
    threshold = 0.86 * max(results)
    for i in range(minLag, len(results)-1):
        if (results[i] > results[i-1] and results[i] > results[i+1] and results[i] > threshold):
            sampleShift = i + 1 # Add 1 to account for indexing from 0 - WE START LOOPING FROM 1 NOT 0!!
            break

    
    period = sampleShift/sampleRate
    frequency = 1/period
    for i in range(35, 110):
        print(i+1, results[i])
    threshold = 0.3 * max(results)


    for i in range(minLag, len(results)-1):
        if (results[i] > results[i-1] and
            results[i] > results[i+1] and
            results[i] > threshold):
            print(i + 1, results[i])
    print(f"Detected lag: {sampleShift}")
    print(f"Frequency: {frequency:.2f} Hz")
    return frequency, results

