import numpy as np
import plot

def autocorrelation(recording, sampleRate):
    recording = recording * 10
    recording = recording - np.mean(recording)
    print("Recording samples:", len(recording))
    print("Recording mean:", np.mean(recording))
    print("Recording std:", np.std(recording))
    print("Max amplitude:", np.max(np.abs(recording)))
    print("RMS:", np.sqrt(np.mean(recording**2)))


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
            closestLag, closestValue = min(peaks, key=lambda peak: abs(peak[0]-expected)) # Finds the difference between every peak and the expected, then finds the peak that produces the smallest difference
            difference = abs(closestLag-expected) # Sees how close the values of the expected and closetLag are
            if difference < 3:
                scores[closestLag] += closestValue / (1 + difference)
                

                print(
                    f"{multiple}x -> {expected:.1f} "
                    f"-> {closestLag} "
                    f"(difference {difference:.2f}, "
                )
    
    print("\nScores:")
    for lag in sorted(scores):
        value = next(value for peak, value in peaks if peak == lag)

        print(
            f"Lag {lag}: "
            f"Frequency = {sampleRate / lag:.2f} Hz, "
            f"NSDF = {value:.3f}, "
            f"Score = {scores[lag]:.3f}"
        )
    
    print("\nHarmonic support:")


    for candidateLag in scores:

        print(f"\nLag {candidateLag}:")

        for harmonic in range(2, 6):

            expectedLag = candidateLag / harmonic

            closestLag, closestValue = min(
                peaks,
                key=lambda peak: abs(peak[0] - expectedLag)
            )

            difference = abs(closestLag - expectedLag)

            if difference < 3:
                print(
                    f"  {harmonic}x: "
                    f"expected {expectedLag:.2f}, "
                    f"found {closestLag}, "
                    f"difference {difference:.2f}, "
                    f"NSDF {closestValue:.3f}"
                )
            else:
                print(
                    f"  {harmonic}x: "
                    f"expected {expectedLag:.2f}, "
                    f"no match"
                )
    
    for lag in [67, 134]:
        value = next((value for peak, value in peaks if peak == lag), None)

        if value is not None:
            print(f"Lag {lag}: NSDF = {value:.6f}, Score = {scores[lag]:.6f}")
        else:
            print(f"Lag {lag}: not detected as a peak")


 
    

    
    bestLag = max(
        scores.keys(),
        key=lambda lag: scores[lag]
    )

    frequency = sampleRate / bestLag

    print(f"Detected lag: {bestLag}")
    print(f"Frequency: {frequency:.2f} Hz")

    
    plot.plot_autocorrelation(results)
    return frequency
