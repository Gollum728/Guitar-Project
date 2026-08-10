import numpy as np
import plot

def autocorrelation(recording, sampleRate):
    print("Recording samples:", len(recording))
    print("Recording mean:", np.mean(recording))
    print("Recording std:", np.std(recording))


    print(sampleRate)
    results = []
    for lag in range(1,750):
        nsdf = 0
        numerator = np.sum(recording[lag:] * recording[:-lag]) # Original x shifted (see notes on this!!)
        denominator = np.sum(recording[:-lag]**2) + np.sum(recording[lag:]**2)
        nsdf = (2 * numerator) / denominator
        results.append(nsdf)
    print("NSDF range:", min(results), max(results))
    print(results[:20])

    maxFrequency = 1500
    minLag = int(sampleRate / maxFrequency)

    sampleShift = 0
    threshold = 0.90 * max(results)
    print(f"Maximum NSDF: {max(results):.3f}")
    print(f"Threshold: {threshold:.3f}")


    peaks = []

    for i in range(minLag, len(results) - 1):
        if (results[i] > results[i-1] and
            results[i] > results[i+1] and
            results[i] > threshold):

            peaks.append((i + 1, results[i]))
    

    scores = {lag: 0 for lag, value in peaks}
    if not peaks:
        return None

    
    for lag, value in peaks:
        print(f"\nCandidate: {lag}")

        for multiple in range(2, 6):
            expected = lag / multiple
            closestLag = min(scores.keys(), key=lambda peak: abs(peak-expected)) # Finds the difference between every peak and the expected, then finds the peak that produces the smallest difference
            difference = abs(closestLag-expected) # Sees how close the values of the expected and closetLag are
            if difference < 3:
                scores[closestLag] += value / (1 + difference)
                

                print(
                    f"{multiple}x -> {expected:.1f} "
                    f"-> {closestLag} "
                    f"(difference {difference:.2f}, "
                )
    
    print("\nScores:")
    for lag, score in scores.items():
        print(f"Lag: {lag}, Score: {score}")

    

    
    bestLag = max(scores, key=scores.get)

    frequency = sampleRate / bestLag

    print(f"Detected lag: {bestLag}")
    print(f"Frequency: {frequency:.2f} Hz")

    
    plot.plot_autocorrelation(results)
    return frequency
