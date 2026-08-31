import numpy as np
from Pitch_Detection.Algorithms import parabolic_interpolation as p_i


OPEN_STRINGS = {
    "E2": 82.41,
    "A2": 110.00,
    "D3": 146.83,
    "G3": 196.00,
    "B3": 246.94,
    "E4": 329.63,
}

def autocorrelation(recording, sampleRate):
    recording = recording * 10
    recording = recording - np.mean(recording)
    print("Recording samples:", len(recording))
    print("Recording mean:", np.mean(recording))
    print("Recording std:", np.std(recording))
    print("Max amplitude:", np.max(np.abs(recording)))
    print("RMS:", np.sqrt(np.mean(recording**2)))
    # clipLevel = 0.3 * np.max(np.abs(recording))
    # recording = np.where(np.abs(recording) > clipLevel, recording, 0)


    print(sampleRate)
    results = []
    for lag in range(1,750):
        nsdf = 0
        numerator = np.sum(recording[lag:] * recording[:-lag]) # Original x shifted (see notes on this!!)
        denominator = np.sum(recording[:-lag]**2) + np.sum(recording[lag:]**2)
        nsdf = (2 * numerator) / denominator
        results.append(nsdf)
    print("NSDF range:", min(results), max(results))
    
    maxFrequency = 1500
    minLag = int(sampleRate / maxFrequency)
    results = results[minLag:]

    tolerancePercent = 0.07
    bestName, bestIndex, bestValue = None, None, -1.0

    for name, targetFreq in OPEN_STRINGS.items():
        expectedLag = sampleRate / targetFreq
        expectedIndex = int(expectedLag) - minLag
        windowSize = int(expectedIndex * tolerancePercent)
        lowIndex = max(0, expectedIndex - windowSize)
        highIndex = min(len(results), expectedIndex + windowSize)

        window = results[lowIndex:highIndex]

        localBestOffset = np.argmax(window)
        localBestIndex = lowIndex + localBestOffset
        localBestValue = window[localBestOffset]

        if localBestValue > bestValue:
            bestValue = localBestValue
            bestIndex = localBestIndex
            bestName = name
    #     print(f"{name}: best index {localBestIndex}, NSDF {localBestValue:.3f}")

    # print(f"\nWinner: {bestName}, index {bestIndex}, NSDF {bestValue:.3f}")

    if bestName is None or bestValue < 0.3:
        return None
    
    print("Selected string:", bestName)
    print("Selected NSDF:", bestValue)
    
    bestLag = bestIndex+minLag+1
    bestLag+=p_i.parabolicInterpolationAuto(bestIndex, results)
    frequency = sampleRate/bestLag
    print("Selected frequency:", frequency)

    return frequency

    

    # sampleShift = 0
    # threshold = 0.6 * max(results)
    # print(f"Maximum NSDF: {max(results):.3f}")
    # print(f"Threshold: {threshold:.3f}")


    # peaks = []

    # for i in range(minLag, len(results) - 1):
    #     if (results[i] >= results[i-1] and
    #         results[i] > results[i+1] and
    #         results[i] > threshold):

    #         peaks.append((i + 1, results[i]))
    

    # scores = {lag: 0 for lag, value in peaks}
    # if not peaks:
    #     return None

    
    # for lag, value in peaks:
    #     print(f"\nCandidate: {lag}")

    #     for multiple in range(2, 6):
    #         expected = lag / multiple
    #         closestLag, closestValue = min(peaks, key=lambda peak: abs(peak[0]-expected)) # Finds the difference between every peak and the expected, then finds the peak that produces the smallest difference
    #         difference = abs(closestLag-expected) # Sees how close the values of the expected and closetLag are
    #         if difference < 3:
    #             scores[closestLag] += closestValue / (1 + difference)
                

    #             print(
    #                 f"{multiple}x -> {expected:.1f} "
    #                 f"-> {closestLag} "
    #                 f"(difference {difference:.2f}, "
    #             )
    
    # print("\nScores:")
    # for lag in sorted(scores):
    #     value = next(value for peak, value in peaks if peak == lag)

    #     print(
    #         f"Lag {lag}: "
    #         f"Frequency = {sampleRate / lag:.2f} Hz, "
    #         f"NSDF = {value:.3f}, "
    #         f"Score = {scores[lag]:.3f}"
    #     )
    
    # print("\nHarmonic support:")


    # for candidateLag in scores:

    #     print(f"\nLag {candidateLag}:")

    #     for harmonic in range(2, 6):

    #         expectedLag = candidateLag / harmonic

    #         closestLag, closestValue = min(
    #             peaks,
    #             key=lambda peak: abs(peak[0] - expectedLag)
    #         )

    #         difference = abs(closestLag - expectedLag)

    #         if difference < 3:
    #             print(
    #                 f"  {harmonic}x: "
    #                 f"expected {expectedLag:.2f}, "
    #                 f"found {closestLag}, "
    #                 f"difference {difference:.2f}, "
    #                 f"NSDF {closestValue:.3f}"
    #             )
    #         else:
    #             print(
    #                 f"  {harmonic}x: "
    #                 f"expected {expectedLag:.2f}, "
    #                 f"no match"
    #             )
    
    # for lag in [67, 134]:
    #     value = next((value for peak, value in peaks if peak == lag), None)

    #     if value is not None:
    #         print(f"Lag {lag}: NSDF = {value:.6f}, Score = {scores[lag]:.6f}")
    #     else:
    #         print(f"Lag {lag}: not detected as a peak")


 
    

    
    # bestLag = max(
    #     scores.keys(),
    #     key=lambda lag: (scores[lag], next(v for l, v in peaks if l == lag))
    # )

    bestLag = max(peaks, key=lambda peak: peak[1])[0]
    frequency = sampleRate / bestLag

    print(f"Detected lag: {bestLag}")
    print(f"Frequency: {frequency:.2f} Hz")

    
    #plot.plot_autocorrelation(results)
    return frequency
