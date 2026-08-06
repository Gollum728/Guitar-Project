import numpy as np

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